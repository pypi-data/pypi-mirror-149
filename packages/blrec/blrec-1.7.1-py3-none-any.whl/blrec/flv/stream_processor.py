from __future__ import annotations
import io
import math
from abc import ABC, abstractmethod
import json
import logging
from typing import (
    Any, BinaryIO, Dict, List, Final, Iterable, Iterator, Optional, Tuple,
    Protocol, TypedDict, Union, cast, TYPE_CHECKING
)

import attr
from rx.subject import Subject
from rx.core import Observable

from .models import FlvHeader, FlvTag, ScriptTag, VideoTag, AudioTag
from .data_analyser import DataAnalyser, MetaData
from .stream_cutter import StreamCutter
from .limit_checker import LimitChecker
from .parameters_checker import ParametersChecker
from .io import FlvReader, FlvWriter
from .io_protocols import RandomIO
from .utils import format_offest, format_timestamp
from .exceptions import (
    FlvTagError,
    FlvStreamCorruptedError,
    AudioParametersChanged,
    VideoParametersChanged,
    FileSizeOverLimit,
    DurationOverLimit,
    CutStream,
)
from .common import (
    is_metadata_tag, parse_metadata, is_audio_tag, is_video_tag,
    is_video_sequence_header, is_audio_sequence_header,
    enrich_metadata, update_metadata, is_data_tag, read_tags_in_duration,
)
from ..path import extra_metadata_path
if TYPE_CHECKING:
    from ..core.stream_analyzer import StreamProfile


__all__ = 'StreamProcessor', 'BaseOutputFileManager', 'JoinPoint'


logger = logging.getLogger(__name__)


class StreamProcessor:
    # Number of tags for determining whether or not tags are duplicated
    _TAG_SEQUENCE_COUNT: Final[int] = 3
    # Max duration in milliseconds the duplicated tags might last
    _MAX_DURATION: Final[int] = 20000

    def __init__(
        self,
        file_manager: OutputFileManager,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        filesize_limit: int = 0,
        duration_limit: int = 0,
        disable_limit: bool = False,
        analyse_data: bool = False,
        dedup_join: bool = False,
        save_extra_metadata: bool = False,
        backup_timestamp: bool = False,
        restore_timestamp: bool = False,
    ) -> None:
        self._file_manager = file_manager
        self._parameters_checker = ParametersChecker()
        self._stream_cutter = StreamCutter()
        if not disable_limit:
            self._limit_checker = LimitChecker(filesize_limit, duration_limit)
        if analyse_data:
            self._data_analyser = DataAnalyser()

        self._metadata = metadata.copy() if metadata else {}
        self._metadata_tag: ScriptTag

        self._disable_limit = disable_limit
        self._analyse_data = analyse_data
        self._dedup_join = dedup_join
        self._save_x_metadata = save_extra_metadata
        self._backup_timestamp = backup_timestamp
        self._restore_timestamp = restore_timestamp

        self._cancelled: bool = False
        self._finalized: bool = False
        self._stream_count: int = 0
        self._size_updates = Subject()
        self._time_updates = Subject()
        self._stream_profile_updates = Subject()

        self._delta: int = 0
        self._has_audio: bool = False
        self._last_tags: List[FlvTag] = []
        self._join_points: List[JoinPoint] = []
        self._resetting_file: bool = False

    @property
    def filesize_limit(self) -> int:
        if self._disable_limit:
            return 0
        return self._limit_checker.filesize_limit

    @filesize_limit.setter
    def filesize_limit(self, value: int) -> None:
        if not self._disable_limit:
            self._limit_checker.filesize_limit = value

    @property
    def duration_limit(self) -> int:
        if self._disable_limit:
            return 0
        return self._limit_checker.duration_limit

    @duration_limit.setter
    def duration_limit(self, value: int) -> None:
        if not self._disable_limit:
            self._limit_checker.duration_limit = value

    @property
    def join_points(self) -> Iterator[JoinPoint]:
        for point in self._join_points:
            yield point

    @property
    def metadata(self) -> Optional[MetaData]:
        if not self._analyse_data:
            return None
        try:
            return self._data_analyser.make_metadata()
        except AssertionError:
            return None
        except Exception as e:
            logger.debug(f'Failed to make metadata data, due to: {repr(e)}')
            return None

    @property
    def size_updates(self) -> Observable:
        return self._size_updates

    @property
    def time_updates(self) -> Observable:
        return self._time_updates

    @property
    def stream_profile_updates(self) -> Observable:
        return self._stream_profile_updates

    @property
    def cancelled(self) -> bool:
        return self._cancelled

    @property
    def finalized(self) -> bool:
        return self._finalized

    def cancel(self) -> None:
        self._cancelled = True

    def set_metadata(self, metadata: Dict[str, Any]) -> None:
        self._metadata = metadata.copy()

    def process_stream(self, stream: RandomIO) -> None:
        assert not self._cancelled and not self._finalized, \
            'should not be called after the processing cancelled or finalized'
        self._stream_count += 1
        self._process_stream(stream)

    def can_cut_stream(self) -> bool:
        return self._stream_cutter.can_cut_stream()

    def cut_stream(self) -> bool:
        return self._stream_cutter.cut_stream()

    def finalize(self) -> None:
        assert not self._finalized, \
            'should not be called after the processing finalized'
        self._finalized = True

        if not self._need_to_finalize():
            logger.debug('No need to finalize stream processing')
            return

        self._complete_file()
        logger.debug('Finalized stream processing')

    def _need_to_finalize(self) -> bool:
        return self._stream_count > 0 and len(self._last_tags) > 0

    def _reset_params(self) -> None:
        self._delta = 0
        self._has_audio = False
        self._last_tags = []
        self._join_points = []
        self._resetting_file = False

        self._stream_cutter.reset()
        if not self._disable_limit:
            self._limit_checker.reset()
        if self._analyse_data:
            self._data_analyser.reset()

    def _new_file(self) -> None:
        self._reset_params()
        self._out_file = self._file_manager.create_file()
        self._out_writer = FlvWriter(self._out_file)
        logger.debug(f'New file: {self._file_manager.curr_path}')

    def _reset_file(self) -> None:
        self._reset_params()
        self._out_file.truncate(0)
        logger.debug(f'Reset file: {self._file_manager.curr_path}')

    def _complete_file(self) -> None:
        curr_path = self._file_manager.curr_path

        if self._save_x_metadata:
            self._save_extra_metadata()

        self._update_metadata_tag()
        self._file_manager.close_file()

        logger.debug(f'Complete file: {curr_path}')

    def _process_stream(self, stream: RandomIO) -> None:
        logger.debug(f'Processing the {self._stream_count}th stream...')

        self._in_reader = FlvReaderWithTimestampFix(
            stream,
            backup_timestamp=self._backup_timestamp,
            restore_timestamp=self._restore_timestamp,
        )

        flv_header = self._read_header()
        self._has_audio = flv_header.has_audio()

        try:
            first_data_tag = self._read_first_data_tag()
            if not self._last_tags:
                self._process_initial_stream(flv_header, first_data_tag)
            else:
                self._process_subsequent_stream(first_data_tag)
        except (
            AudioParametersChanged, VideoParametersChanged,
            FileSizeOverLimit, DurationOverLimit, CutStream,
        ):
            self._process_split_stream(flv_header)

        logger.debug(f'Completed processing the {self._stream_count}th stream')

    def _process_initial_stream(
        self, flv_header: FlvHeader, first_data_tag: FlvTag
    ) -> None:
        if self._resetting_file:
            self._reset_file()
        else:
            self._new_file()

        try:
            self._write_header(self._ensure_header_correct(flv_header))
            self._transfer_meta_tags()
            self._transfer_first_data_tag(first_data_tag)
            self._update_stream_profile(flv_header, first_data_tag)
        except Exception:
            self._last_tags = []
            self._resetting_file = True
            raise
        else:
            del flv_header, first_data_tag

        self._transfer_tags_until_complete()

    def _process_subsequent_stream(self, first_data_tag: FlvTag) -> None:
        tags: List[FlvTag] = []

        if self._dedup_join:
            tags, exc = self._read_tags_for_deduplication()

            if (index := self._find_last_duplicated_tag(tags)) >= 0:
                seamless = True
                self._delta = self._calc_delta_duplicated(tags[index])
                tags = tags[index + 1:]
                if not tags:
                    tags = [self._read_first_data_tag()]

        if not self._dedup_join or index == -1:
            seamless = False
            self._delta = self._calc_delta_no_duplicated(first_data_tag)
            tags.insert(0, first_data_tag)

        offset = self._out_file.tell()
        timestamp = tags[0].timestamp + self._delta
        self._add_join_point(offset, timestamp, seamless)

        self._transfer_tags(tags)
        del first_data_tag, tags

        if self._dedup_join and exc:
            raise exc

        self._transfer_tags_until_complete()

    def _process_split_stream(self, flv_header: FlvHeader) -> None:
        self._complete_file()

        first_data_tag: FlvTag

        if self._stream_cutter.is_cutting():
            assert self._stream_cutter.last_keyframe_tag is not None
            last_keyframe_tag = self._stream_cutter.last_keyframe_tag
            original_ts = last_keyframe_tag.timestamp - self._delta
            first_data_tag = last_keyframe_tag.evolve(timestamp=original_ts)
        elif (
            not self._disable_limit and (
                self._limit_checker.is_filesize_over_limit() or
                self._limit_checker.is_duration_over_limit()
            )
        ):
            assert self._limit_checker.last_keyframe_tag is not None
            last_keyframe_tag = self._limit_checker.last_keyframe_tag
            original_ts = last_keyframe_tag.timestamp - self._delta
            first_data_tag = last_keyframe_tag.evolve(timestamp=original_ts)
        else:
            first_data_tag = self._read_first_data_tag()

        try:
            self._process_initial_stream(flv_header, first_data_tag)
        except (
            AudioParametersChanged, VideoParametersChanged,
            FileSizeOverLimit, DurationOverLimit, CutStream,
        ):
            self._process_split_stream(flv_header)

    def _transfer_meta_tags(self) -> None:
        logger.debug('Transfering meta tags...')

        if self._parameters_checker.last_metadata_tag is None:
            raise FlvStreamCorruptedError('No metadata tag in the stream')
        if self._parameters_checker.last_video_header_tag is None:
            raise FlvStreamCorruptedError('No video header tag in the stream')
        if self._has_audio:
            if self._parameters_checker.last_audio_header_tag is None:
                raise FlvStreamCorruptedError(
                    'No audio header tag in the stream'
                )
        metadata_tag = self._parameters_checker.last_metadata_tag
        video_header_tag = self._parameters_checker.last_video_header_tag
        audio_header_tag = self._parameters_checker.last_audio_header_tag

        offset = self._out_file.tell()
        self._metadata_tag = self._enrich_metadata(metadata_tag, offset)

        offset_delta = self._metadata_tag.tag_size - metadata_tag.tag_size
        self._update_injected_metadata(offset_delta)

        self._write_tag(
            self._correct_ts(self._metadata_tag, -self._metadata_tag.timestamp)
        )
        self._write_tag(
            self._correct_ts(video_header_tag, -video_header_tag.timestamp)
        )
        if audio_header_tag is not None:
            self._write_tag(
                self._correct_ts(audio_header_tag, -audio_header_tag.timestamp)
            )

        logger.debug('Meta tags have been transfered')

    def _update_stream_profile(
        self, flv_header: FlvHeader, first_data_tag: FlvTag
    ) -> None:
        from ..core.stream_analyzer import ffprobe

        if self._parameters_checker.last_metadata_tag is None:
            return
        if self._parameters_checker.last_video_header_tag is None:
            return

        bytes_io = io.BytesIO()
        writer = FlvWriter(bytes_io)
        writer.write_header(flv_header)
        writer.write_tag(
            self._correct_ts(
                self._parameters_checker.last_metadata_tag,
                -self._parameters_checker.last_metadata_tag.timestamp,
            )
        )
        writer.write_tag(
            self._correct_ts(
                self._parameters_checker.last_video_header_tag,
                -self._parameters_checker.last_video_header_tag.timestamp,
            )
        )
        if self._parameters_checker.last_audio_header_tag is not None:
            writer.write_tag(
                self._correct_ts(
                    self._parameters_checker.last_audio_header_tag,
                    -self._parameters_checker.last_audio_header_tag.timestamp,
                )
            )
        writer.write_tag(self._correct_ts(first_data_tag, -first_data_tag.timestamp))

        def on_next(profile: StreamProfile) -> None:
            self._stream_profile_updates.on_next(profile)

        def on_error(e: Exception) -> None:
            logger.warning(f'Failed to analyse stream: {repr(e)}')

        ffprobe(bytes_io.getvalue()).subscribe(on_next, on_error)

    def _transfer_first_data_tag(self, tag: FlvTag) -> None:
        logger.debug(f'Transfer the first data tag: {tag}')
        self._delta = -tag.timestamp
        self._transfer_tags([tag])
        logger.debug('The first data tag has been transfered')

    def _read_tags_for_deduplication(
        self
    ) -> Tuple[List[FlvTag], Optional[Exception]]:
        logger.debug('Reading tags for tag deduplication...')
        tags: List[FlvTag] = []
        try:
            for tag in read_tags_in_duration(
                self._in_reader, self._MAX_DURATION
            ):
                tags.append(tag)
        except Exception as exc:
            logger.debug(f'Failed to read data, due to: {repr(exc)}')
            return tags, exc
        else:
            return tags, None
        finally:
            logger.debug('Read {} tags, total size: {}'.format(
                len(tags), sum(t.tag_size for t in tags)
            ))

    def _transfer_tags_until_complete(self) -> None:
        logger.debug('Transfering tags until complete...')
        self._transfer_tags(self._read_tags_from_in_stream())

    def _read_tags_from_in_stream(self) -> Iterator[FlvTag]:
        while not self._cancelled:
            try:
                tag = self._in_reader.read_tag()
                self._parameters_checker.check_tag(tag)
                yield tag
            except EOFError:
                logger.debug('The input stream exhausted')
                break
            except AudioParametersChanged:
                if self._analyse_data:
                    logger.warning('Audio parameters changed at {}'.format(
                        format_timestamp(self._data_analyser.last_timestamp),
                    ))
                yield tag
            except VideoParametersChanged:
                if self._analyse_data:
                    logger.warning('Video parameters changed at {}'.format(
                        format_timestamp(self._data_analyser.last_timestamp),
                    ))
                raise
            except Exception as e:
                logger.debug(f'Failed to read data, due to: {repr(e)}')
                raise
        else:
            logger.debug('Cancelled reading tags from the input stream')

    def _transfer_tags(self, tags: Iterable[FlvTag]) -> None:
        logger.debug(f'Transfering tags... timestamp delta: {self._delta}')

        try:
            count: int = 0
            for tag in tags:
                self._ensure_ts_correct(tag)
                self._write_tag(self._correct_ts(tag, self._delta))
                count += 1
        finally:
            logger.debug(f'{count} tags have been transfered')

    def _add_join_point(
        self, offset: int, timestamp: int, seamless: bool
    ) -> None:
        join_point = JoinPoint(offset, timestamp, seamless)
        self._join_points.append(join_point)
        logger.debug(f'{repr(join_point)}; {join_point}')

    def _find_last_duplicated_tag(self, tags: List[FlvTag]) -> int:
        logger.debug('Finding duplicated tags...')

        last_out_tag = self._last_tags[0]
        logger.debug(f'The last output tag is {last_out_tag}')

        for idx, tag in enumerate(tags):
            if not tag.is_the_same_as(last_out_tag):
                continue

            if not all(
                map(
                    lambda t: t[0].is_the_same_as(t[1]),
                    zip(reversed(tags[:idx]), self._last_tags[1:])
                )
            ):
                continue

            logger.debug(f'The last duplicated tag found at {idx} is {tag}')
            return idx

        logger.debug('No duplicated tags found')
        return -1

    def _read_header(self) -> FlvHeader:
        try:
            return self._in_reader.read_header()
        except Exception as exc:
            raise FlvStreamCorruptedError(repr(exc))

    def _read_first_data_tag(self) -> Union[AudioTag, VideoTag]:
        for tag in self._read_tags_from_in_stream():
            if is_data_tag(tag):
                return tag
        raise FlvStreamCorruptedError('No data tag found in the stream!')

    def _read_tags(self, count: int) -> Iterator[FlvTag]:
        assert count > 0, 'count must greater than 0'
        for c, tag in enumerate(self._read_tags_from_in_stream(), start=1):
            yield tag
            if c >= count:
                break

    def _write_header(self, header: FlvHeader) -> None:
        try:
            size = self._out_writer.write_header(header)
            logger.debug('The flv header has been copied')
        except Exception as exc:
            logger.debug(f'Failed to write data, due to: {repr(exc)}')
            raise

        if not self._disable_limit:
            self._limit_checker.check_header(header)
        if self._analyse_data:
            self._data_analyser.analyse_header(header)
        self._size_updates.on_next(size)

    def _write_tag(self, tag: FlvTag) -> None:
        offset = self._out_file.tell()
        tag = tag.evolve(offset=offset)

        try:
            size = self._out_writer.write_tag(tag)
        except Exception as exc:
            logger.debug(f'Failed to write data, due to: {repr(exc)}')
            raise
        else:
            self._last_tags.insert(0, tag)
            if len(self._last_tags) > self._TAG_SEQUENCE_COUNT:
                self._last_tags.pop()

        self._stream_cutter.check_tag(tag)
        if not self._disable_limit:
            self._limit_checker.check_tag(tag)
        if self._analyse_data:
            self._data_analyser.analyse_tag(tag)

        self._size_updates.on_next(size)
        self._time_updates.on_next(tag.timestamp)

    def _ensure_header_correct(self, header: FlvHeader) -> FlvHeader:
        header.set_video_flag(
            self._parameters_checker.last_video_header_tag is not None
        )
        header.set_audio_flag(
            self._parameters_checker.last_audio_header_tag is not None
        )
        return header

    def _ensure_ts_correct(self, tag: FlvTag) -> None:
        if not tag.timestamp + self._delta < 0:
            return
        logger.warning(
            f'Incorrect timestamp: {tag.timestamp + self._delta}\n'
            f'last output tag: {self._last_tags[0]}\n'
            f'current tag: {tag}'
        )
        if tag.is_audio_tag() or tag.is_video_tag():
            self._delta = (
                self._last_tags[0].timestamp +
                self._in_reader.calc_interval(tag) - tag.timestamp
            )
            logger.debug(f'Updated delta: {self._delta}')
        elif tag.is_script_tag():
            self._delta = (
                self._last_tags[0].timestamp - tag.timestamp
            )
            logger.debug(f'Updated delta: {self._delta}')
        else:
            pass

    def _correct_ts(self, tag: FlvTag, delta: int) -> FlvTag:
        if delta == 0 and tag.timestamp >= 0:
            return tag
        return tag.evolve(timestamp=tag.timestamp + delta)

    def _calc_delta_duplicated(self, last_duplicated_tag: FlvTag) -> int:
        return self._last_tags[0].timestamp - last_duplicated_tag.timestamp

    def _calc_delta_no_duplicated(self, first_data_tag: FlvTag) -> int:
        return (
            self._last_tags[0].timestamp - first_data_tag.timestamp +
            self._in_reader.calc_interval(first_data_tag)
        )

    def _enrich_metadata(
        self, old_metadata_tag: ScriptTag, offset: int
    ) -> ScriptTag:
        # ensure nesessary properties exists in the metadata and init them.
        metadata = parse_metadata(old_metadata_tag)
        self._metadata.update({
            'duration': 0.0,
            'filesize': 0.0,
            'framerate': metadata.get('framerate', metadata.get('fps', 0.0)),
        })
        # merge the metadata into the metadata tag
        return enrich_metadata(old_metadata_tag, self._metadata, offset)

    def _update_injected_metadata(self, offset_delta: int) -> None:
        updated = False

        if (keyframes := self._metadata.get('keyframes')):
            keyframes['filepositions'] = list(
                map(lambda p: p + offset_delta, keyframes['filepositions'])
            )
            if 'lastkeyframelocation' in self._metadata:
                self._metadata['lastkeyframelocation'] = \
                    keyframes['filepositions'][-1]
            updated = True

        if (join_points := self._metadata.get('joinpoints')):
            join_points = cast(List[JoinPointData], join_points)
            self._metadata['joinpoints'] = list(
                {**p, 'offset': p['offset'] + offset_delta}
                for p in join_points
            )
            updated = True

        if updated:
            self._metadata_tag = \
                update_metadata(self._metadata_tag, self._metadata)

    def _update_metadata_tag(self) -> None:
        last_tag = self._last_tags[0]
        duration = last_tag.timestamp / 1000
        filesize = float(last_tag.next_tag_offset)
        updates = {
            'duration': duration,
            'filesize': filesize,
        }
        if self._analyse_data:
            updates.update({
                'framerate': self._data_analyser.calc_frame_rate(),
            })
        self._metadata_tag = update_metadata(self._metadata_tag, updates)
        self._out_file.seek(self._metadata_tag.offset)
        self._out_writer.write_tag(self._metadata_tag)
        logger.debug('The metadata tag has been updated')

    def _save_extra_metadata(self) -> None:
        if self._analyse_data:
            metadata = attr.asdict(
                self._data_analyser.make_metadata(),
                filter=lambda a, v: v is not None,
            )
        else:
            metadata = {}

        metadata['joinpoints'] = list(
            map(lambda p: p.to_metadata_value(), self._join_points)
        )

        assert self._file_manager.curr_path is not None
        path = extra_metadata_path(self._file_manager.curr_path)
        with open(path, 'wt', encoding='utf8') as file:
            json.dump(metadata, file)

        logger.debug('The extra metadata has been saved')


@attr.s(auto_attribs=True, slots=True, frozen=True)
class JoinPoint:
    offset: int
    timestamp: int  # milliseconds
    seamless: bool

    @classmethod
    def from_metadata_value(cls, value: JoinPointData) -> JoinPoint:
        return cls(
            offset=int(value['offset']),
            timestamp=int(value['timestamp']),
            seamless=value['seamless'],
        )

    def to_metadata_value(self) -> JoinPointData:
        return dict(
            offset=float(self.offset),
            timestamp=float(self.timestamp),
            seamless=self.seamless,
        )

    def __str__(self) -> str:
        return 'offset: {}, timestamp: {}, seamless: {}'.format(
            format_offest(self.offset),
            format_timestamp(self.timestamp),
            'yes' if self.seamless else 'no',
        )


class JoinPointData(TypedDict):
    offset: float
    timestamp: float
    seamless: bool


class OutputFileManager(Protocol):
    @property
    def curr_path(self) -> Optional[str]:
        ...

    @property
    def curr_file(self) -> Optional[BinaryIO]:
        ...

    def create_file(self) -> BinaryIO:
        ...

    def close_file(self) -> None:
        ...


class BaseOutputFileManager(ABC):
    def __init__(self, buffer_size: Optional[int] = None) -> None:
        super().__init__()
        self.buffer_size = buffer_size or io.DEFAULT_BUFFER_SIZE  # bytes
        self._paths: List[str] = []
        self._curr_path: Optional[str] = None
        self._curr_file: Optional[BinaryIO] = None

    @property
    def curr_path(self) -> Optional[str]:
        return self._curr_path

    @property
    def curr_file(self) -> Optional[BinaryIO]:
        return self._curr_file

    def has_file(self) -> bool:
        return len(self._paths) > 1

    def get_files(self) -> Iterator[str]:
        for file in self._paths:
            yield file

    def clear_files(self) -> None:
        self._paths.clear()

    def create_file(self) -> BinaryIO:
        assert self._curr_file is None
        path = self._make_path()
        file = open(path, mode='w+b', buffering=self.buffer_size)
        self._paths.append(path)
        self._curr_path = path
        self._curr_file = file
        return file

    def close_file(self) -> None:
        assert self._curr_file is not None
        self._curr_file.close()
        self._curr_path = None
        self._curr_file = None

    @abstractmethod
    def _make_path(self) -> str:
        ...


class RobustFlvReader(FlvReader):
    def read_tag(self, *, no_body: bool = False) -> FlvTag:
        count = 0
        while True:
            try:
                tag = super().read_tag(no_body=no_body)
            except FlvTagError as e:
                logger.warning(f'Invalid tag: {repr(e)}')
                self._parser.parse_previous_tag_size()
                count += 1
                if count > 3:
                    raise
            else:
                count = 0
                return tag


class FlvReaderWithTimestampFix(RobustFlvReader):
    def __init__(
        self,
        stream: RandomIO,
        backup_timestamp: bool = False,
        restore_timestamp: bool = False,
    ) -> None:
        super().__init__(
            stream,
            backup_timestamp=backup_timestamp,
            restore_timestamp=restore_timestamp,
        )
        self._last_tag: Optional[FlvTag] = None
        self._last_video_tag: Optional[VideoTag] = None
        self._last_audio_tag: Optional[AudioTag] = None
        self._delta = 0
        # 15 is probably the minimal frame rate
        self._frame_rate = 15.0
        self._video_frame_interval = math.ceil(1000 / self._frame_rate)
        # AAC SoundRate always is 44 KHz
        self._sound_sample_interval = math.ceil(1000 / 44)

    @property
    def frame_rate(self) -> float:
        return self._frame_rate

    @property
    def sound_sample_interval(self) -> int:
        return self._sound_sample_interval

    @property
    def video_frame_interval(self) -> int:
        return self._video_frame_interval

    def read_tag(self, *, no_body: bool = False) -> FlvTag:
        while True:
            tag = super().read_tag(no_body=no_body)

            if self._last_tag is None:
                if is_video_tag(tag) or is_audio_tag(tag):
                    self._update_last_tags(tag)
                elif is_metadata_tag(tag):
                    self._update_parameters(tag)
                return tag

            if not is_video_tag(tag) and not is_audio_tag(tag):
                return tag

            if self._is_ts_rebounded(tag):
                self._update_delta(tag)
                logger.warning(
                    f'Timestamp rebounded, updated delta: {self._delta}\n'
                    f'last video tag: {self._last_video_tag}\n'
                    f'last audio tag: {self._last_audio_tag}\n'
                    f'current tag: {tag}'
                )

            if self._is_ts_jumped(tag):
                self._update_delta(tag)
                logger.warning(
                    f'Timestamp jumped, updated delta: {self._delta}\n'
                    f'last tag: {self._last_tag}\n'
                    f'current tag: {tag}'
                )

            self._update_last_tags(tag)

            return self._correct_ts(tag)

    def rread_tag(self, *, no_body: bool = False) -> FlvTag:
        raise NotImplementedError()

    def read_body(self, tag: FlvTag) -> bytes:
        raise NotImplementedError()

    def calc_interval(self, tag: FlvTag) -> int:
        if is_audio_tag(tag):
            return self._sound_sample_interval
        elif is_video_tag(tag):
            return self._video_frame_interval
        else:
            logger.warning(f'Unexpected tag type: {tag}')
            return min(self._sound_sample_interval, self._video_frame_interval)

    def _is_ts_rebounded(self, tag: FlvTag) -> bool:
        if is_video_tag(tag):
            if self._last_video_tag is None:
                return False
            if is_video_sequence_header(self._last_video_tag):
                return tag.timestamp < self._last_video_tag.timestamp
            else:
                return tag.timestamp <= self._last_video_tag.timestamp
        elif is_audio_tag(tag):
            if self._last_audio_tag is None:
                return False
            if is_audio_sequence_header(self._last_audio_tag):
                return tag.timestamp < self._last_audio_tag.timestamp
            else:
                return tag.timestamp <= self._last_audio_tag.timestamp
        else:
            return False

    def _is_ts_jumped(self, tag: FlvTag) -> bool:
        assert self._last_tag is not None
        return (
            tag.timestamp - self._last_tag.timestamp >
            max(self._sound_sample_interval, self._video_frame_interval)
        )

    def _update_last_tags(self, tag: FlvTag) -> None:
        self._last_tag = tag
        if is_video_tag(tag):
            self._last_video_tag = tag
        elif is_audio_tag(tag):
            self._last_audio_tag = tag

    def _update_parameters(self, tag: ScriptTag) -> None:
        metadata = parse_metadata(tag)
        frame_rate = metadata.get('fps') or metadata.get('framerate')

        if not frame_rate:
            return

        self._frame_rate = frame_rate
        self._video_frame_interval = math.ceil(1000 / frame_rate)

        logger.debug('frame rate: {}, video frame interval: {}'.format(
            frame_rate, self._video_frame_interval
        ))

    def _update_delta(self, tag: FlvTag) -> None:
        assert self._last_tag is not None
        self._delta = (
            self._last_tag.timestamp + self._delta - tag.timestamp +
            self.calc_interval(tag)
        )

    def _correct_ts(self, tag: FlvTag) -> FlvTag:
        if self._delta == 0:
            return tag
        return tag.evolve(timestamp=tag.timestamp + self._delta)

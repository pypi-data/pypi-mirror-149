import os
import pickle
from datetime import datetime
from typing import Any, Iterable, Mapping, Union

import pandas as pd

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.file_io.time_series_format import (
    TimeSeriesFormat,
    TimeSeriesReader,
    TimeSeriesWriter,
)


class PickleFormat(TimeSeriesFormat):
    """
    Pickle formatter class

    Example:
        .. code-block:: python

            from kisters.water.time_series.file_io import FileStore, PickleFormat
            fs = FileStore('tests/data', PickleFormat())
    """

    def __init__(self):
        super().__init__()
        self._reader = None
        self._writer = None

    @property
    def extensions(self) -> Iterable[str]:
        return ["pkl"]

    @property
    def reader(self) -> TimeSeriesReader:
        if self._reader is None:
            self._reader = PickleReader(self)
        return self._reader

    @property
    def writer(self) -> TimeSeriesWriter:
        if self._writer is None:
            self._writer = PickleWriter(self)
        return self._writer


class PickleReader(TimeSeriesReader):
    def __init__(self, fmt: TimeSeriesFormat = None):
        if fmt is None:
            fmt = PickleFormat()
        super().__init__(fmt)

    def _extract_metadata(self, file) -> Iterable[Mapping[str, Any]]:
        with open(file, "rb") as f:
            ts_meta = pickle.load(f)[0]
        ts_meta.update(self._meta_from_file(file))
        self.format.writer.write_metadata(file, [ts_meta])
        return [ts_meta]

    def load_data_frame(self, file, columns):
        with open(file, "rb") as f:
            return pickle.load(f)[1]


class PickleWriter(TimeSeriesWriter):
    def __init__(self, fmt: TimeSeriesFormat = None):
        if fmt is None:
            fmt = PickleFormat()
        super().__init__(fmt)

    def write(
        self,
        file: str,
        data_list: Union[Iterable[pd.DataFrame], Iterable[TimeSeries]],
        start: datetime = None,
        end: datetime = None,
        meta_list: Iterable[Mapping[str, Any]] = None,
    ):
        data = list(data_list)[0]
        dirname = os.path.dirname(file)
        if not os.path.exists(dirname) and dirname != "":
            os.makedirs(dirname)
        with open(file, "wb") as f:
            if isinstance(data, TimeSeries):
                pickle.dump([data.metadata, data.read_data_frame(start, end)], f)
            else:
                meta = meta_list[0] if meta_list[0] is not None else {}
                pickle.dump([meta, data], file)
        if os.path.isfile(file + ".metadata"):
            os.unlink(file + ".metadata")
        self.write_metadata(file, self.format.reader._extract_metadata(file))

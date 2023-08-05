import csv
import os
from csv import DictWriter
from datetime import datetime
from typing import Any, Callable, Iterable, List, Mapping, TextIO, Union

import pandas as pd

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.file_io.time_series_format import (
    TimeSeriesFormat,
    TimeSeriesReader,
    TimeSeriesWriter,
)


def writer(file: TextIO, delimiter: str, quotechar: str) -> DictWriter:
    w = csv.writer(
        file,
        delimiter=delimiter,
        quotechar=quotechar,
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
    )
    return w


class CSVFormat(TimeSeriesFormat):
    """
    CSV formatter class

    Example:
        .. code-block:: python

            from kisters.water.time_series.file_io import FileStore, CSVFormat
            fs = FileStore('tests/data', CSVFormat())
    """

    def __init__(self, delimiter: str = ",", quotechar: str = '"', header_lines: int = 1):
        super().__init__()
        self._delimiter = delimiter
        self._quotechar = quotechar
        self._header_lines = header_lines
        self._writer = None
        self._reader = None

    @property
    def extensions(self) -> Iterable[str]:
        return ["csv"]

    @property
    def reader(self) -> TimeSeriesReader:
        if self._reader is None:
            self._reader = CSVReader(self, self._header_lines, self._delimiter, self._quotechar)
        return self._reader

    @property
    def writer(self) -> TimeSeriesWriter:
        if self._writer is None:
            self._writer = CSVWriter(self, writer, self._delimiter, self._quotechar)
        return self._writer


class CSVReader(TimeSeriesReader):
    def __init__(
        self,
        fmt: TimeSeriesFormat = None,
        header_lines: int = 1,
        delimiter: str = ",",
        quotechar: str = '"',
    ):
        if fmt is None:
            fmt = CSVFormat()
        super().__init__(fmt)
        self._header_lines = header_lines
        self._delimiter = delimiter
        self._quotechar = quotechar

    def _extract_metadata(self, file) -> Iterable[Mapping[str, Any]]:
        ts_meta = self._meta_from_file(file)
        with open(file, encoding="utf-8") as f:
            for _i in range(self._header_lines):
                ts_meta.update(self.__process_metadata_line(f.readline().rstrip()))
        self.format.writer.write_metadata(file, [ts_meta])
        return [ts_meta]

    def load_data_frame(self, file: str, columns: List[str]):
        df = pd.read_csv(
            file,
            engine="c",
            skiprows=self._header_lines,  # skiprows is 0-indexed
            sep=self._delimiter,
            quotechar=self._quotechar,
            names=columns,
        )
        df.columns = columns
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.set_index("timestamp")
        return df

    # TODO: improve persistence of metadata inside CSV
    @classmethod
    def __process_metadata_line(cls, line: str) -> Mapping[str, Any]:
        cols = []
        tz = "UTC"
        for e in line.split(","):
            if e.startswith("|"):
                tz = e[1:]
            else:
                cols.append(e)
        return {"columns": cols, "timezone": tz}


class CSVWriter(TimeSeriesWriter):
    def __init__(
        self,
        fmt: TimeSeriesFormat = None,
        writer: Callable = writer,
        delimiter: str = None,
        quotechar: str = None,
    ):
        if fmt is None:
            fmt = CSVFormat()
        super().__init__(fmt)
        self._writer = writer
        self._delimiter = delimiter
        self._quotechar = quotechar

    def write(
        self,
        file: str,
        data_list: Union[Iterable[pd.DataFrame], Iterable[TimeSeries]],
        start: datetime = None,
        end: datetime = None,
        meta_list: Iterable[Mapping[str, Any]] = None,
    ):
        dirname = os.path.dirname(file)
        if not os.path.exists(dirname) and dirname != "":
            os.makedirs(dirname)
        with open(file, "w") as fh:
            for i, ts in enumerate(data_list):
                if isinstance(ts, TimeSeries):
                    metadata = ts.metadata
                    ts = ts.read_data_frame(start, end)
                else:
                    metadata = meta_list[i]
                self._write_block(fh, ts, metadata)
        self.write_metadata(file, self.format.reader._get_metadata(file))

    def _write_block(self, fh: TextIO, df: pd.DataFrame, metadata: Mapping):
        writer = self._writer(fh, delimiter=self._delimiter, quotechar=self._quotechar)
        # TODO: improve metadata writings in CSV
        self._write_header(writer, ["timestamp"] + sorted(df.columns), metadata.get("timezone", "UTC"))
        df[sorted(df.columns)].reset_index().to_csv(
            fh,
            sep=self._delimiter,
            quotechar=self._quotechar,
            index=False,
            header=False,
        )

    @classmethod
    def _write_header(cls, writer: DictWriter, columns: List[str], tz: str = "UTC"):
        writer.writerow(columns + ["|" + tz])

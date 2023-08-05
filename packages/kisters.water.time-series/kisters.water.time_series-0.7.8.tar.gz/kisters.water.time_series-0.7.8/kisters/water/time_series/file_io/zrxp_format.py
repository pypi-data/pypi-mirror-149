import datetime
import os
import re
from typing import Any, Iterable, List, Mapping, TextIO, Tuple, Union

import numpy as np
import pandas as pd
from pytz import UnknownTimeZoneError

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.file_io.time_series_format import (
    TimeSeriesFormat,
    TimeSeriesReader,
    TimeSeriesWriter,
)

READ_SIZE = 10 * 1024 * 1024
ZRXP_ENCODING = "iso-8859-1"
HEADER_KEYS = {
    "SNAME": "stationName",
    "SANR": "stationNumber",
    "SWATER": "water",
    "CDASA": "dataLogger",
    "CDASANAME": "dataLoggerName",
    "CCHANNEL": "channelName",
    "CCHANNELNO": "channel",
    "CMW": "valuesPerDay",
    "CNAME": "parameterName",
    "CNR": "parameterNumber",
    "CUNIT": "unit",
    "REXCHANGE": "exchangeNumber",
    "RINVAL": "invalidValue",
    "RTIMELVL": "timeLevel",
    "XVLID": "id",
    "TSPATH": "tsPath",
    "CTAG": None,
    "CTAGKEY": None,
    "XTRUNCATE": None,
    "METCODE": None,
    "METERNUMBER": None,
    "EDIS": None,
    "TZ": "timezone",
    "ZDATE": None,
    "ZRXPVERSION": None,
    "ZRXPCREATOR": None,
    "LAYOUT": None,
    "TASKID": None,
    "SOURCESYSTEM": "sourceSystem",
    "SOURCEID": "sourceId",
}


class ZRXPLayoutError(Exception):
    def __init__(self, layout_diff):
        self.layout_diff = layout_diff

    def __str__(self):
        return repr(self.layout_diff)


class ZRXPFormat(TimeSeriesFormat):
    """
    ZRXP formatter class

    Example:
        .. code-block:: python

            from kisters.water.time_series.file_io import FileStore, ZRXPFormat
            fs = FileStore('tests/data', ZRXPFormat())
    """

    def __init__(self):
        super().__init__()
        self._reader = None
        self._writer = None

    @property
    def extensions(self) -> Iterable[str]:
        return ["zrx", "zrxp"]

    @property
    def reader(self) -> TimeSeriesReader:
        if self._reader is None:
            self._reader = ZRXPReader(self)
        return self._reader

    @property
    def writer(self) -> TimeSeriesWriter:
        if self._writer is None:
            self._writer = ZRXPWriter(self)
        return self._writer


class ZRXPReader(TimeSeriesReader):
    def __init__(
        self,
        fmt: TimeSeriesFormat = None,
        default_quality: int = 200,
        default_interpolation: int = 2,
    ):
        if fmt is None:
            fmt = ZRXPFormat()
        super().__init__(fmt)
        self._default_quality = default_quality
        self._default_interpolation = default_interpolation

    def _read_metadata(self, file: str, lines: Iterable[str]):
        ts_meta = self._meta_from_file(file)
        for line in lines:
            for part in line[1:].strip().replace(";*;", "|*|").split("|*|"):
                part = part.strip()
                for key, value in HEADER_KEYS.items():
                    if part.startswith(key):
                        ts_meta[key] = part[len(key) :]
                        if value is not None:
                            ts_meta[value] = ts_meta[key]
        ts_meta["columns"] = self.__extract_columns(ts_meta.get("LAYOUT", None))
        return ts_meta

    def _extract_metadata(self, file: str) -> List:
        meta_line_offsets, newline_offsets = self.__get_meta_line_and_newline_offsets(file)
        meta_start_offsets, data_start_offsets, n_rows = self.__get_offsets_and_rows(
            meta_line_offsets, newline_offsets
        )
        ts_metas = self.__process_metadata(file, meta_start_offsets, data_start_offsets, n_rows)
        self.format.writer.write_metadata(file, ts_metas)
        return ts_metas

    @classmethod
    def __get_meta_line_and_newline_offsets(cls, file: str) -> Tuple[np.ndarray, np.ndarray]:
        read_count = 0
        meta_offsets = []
        newline_offsets = [[0]]
        f = open(file, "rb")
        while True:
            buffer = f.read(READ_SIZE)
            if buffer == b"":
                break
            aux = np.frombuffer(buffer, dtype=np.uint8, count=len(buffer))
            meta_offsets.append(np.where(aux == 35)[0] + READ_SIZE * read_count)
            newline_offsets.append(np.where(aux == 10)[0] + 1 + READ_SIZE * read_count)
            read_count += 1

        return np.concatenate(meta_offsets), np.concatenate(newline_offsets)

    @classmethod
    def __get_offsets_and_rows(
        cls, meta_line_offsets: np.ndarray, newline_offsets: np.ndarray
    ) -> Tuple[List[int], List[int], List[int]]:
        n_rows = []
        meta_start_offsets = []
        data_start_offsets = []
        i = 0
        data_offset_index = None
        move = 0
        while i < len(meta_line_offsets):
            if data_offset_index is not None:
                new = np.where(newline_offsets == meta_line_offsets[i])[0][0]
                n_rows.append(new - data_offset_index)
                ix = new
            else:
                ix = np.where(newline_offsets == meta_line_offsets[i])[0][0]
            meta_start_offsets.append(meta_line_offsets[i])
            # If we cannot move, the next one is a data_start_offset
            if i + 1 >= len(meta_line_offsets):
                data_offset_index = ix + 1
                data_start_offsets.append(newline_offsets[data_offset_index])
                move += 1
            # Move until finding newline offset not being a metadata line
            for j in range(i + 1, len(meta_line_offsets)):
                move += 1
                # Add always next newline offset after last metadata line
                if j == len(meta_line_offsets) - 1:
                    data_offset_index = ix + j - i + 1
                    data_start_offsets.append(newline_offsets[data_offset_index])
                    move += 1
                    break
                if meta_line_offsets[j] != newline_offsets[ix + j - i]:
                    data_offset_index = ix + j - i
                    data_start_offsets.append(newline_offsets[data_offset_index])
                    break
            i += move
            move = 0
        if len(n_rows) < len(meta_start_offsets):
            n_rows.append(len(newline_offsets[data_offset_index:]))
        return meta_start_offsets, data_start_offsets, n_rows

    def __process_metadata(
        self,
        file: str,
        meta_start_offsets: List[int],
        data_start_offsets: List[int],
        n_rows: List[int],
    ) -> List[Mapping]:

        ts_metas = []
        zrxp_meta_key = list(self._format.extensions)[0].upper()
        with open(file, "rb") as f:
            for i in range(len(meta_start_offsets)):
                f.seek(meta_start_offsets[i])
                ts_meta = self._read_metadata(
                    file,
                    f.read(data_start_offsets[i] - meta_start_offsets[i])
                    .decode(ZRXP_ENCODING)
                    .splitlines(),
                )
                ts_meta[zrxp_meta_key]["data_offset"] = data_start_offsets[i]
                ts_meta[zrxp_meta_key]["invalid"] = float(ts_meta.get("RINVAL", -777.0))
                ts_meta[zrxp_meta_key]["timezone"] = ts_meta.get("TZ", "UTC")
                ts_meta[zrxp_meta_key]["nrows"] = n_rows[i]
                ts_metas.append(ts_meta)
        paths = [m.get("tsPath") for m in ts_metas]
        unique_paths = set(paths)
        if len(unique_paths) < len(paths):
            for unique_path in set(paths):
                indices = [i for i, path in enumerate(paths) if path == unique_path]
                for i in indices:
                    ts_metas[i]["_SEQUENCE_ID"] = i
        return ts_metas

    @classmethod
    def __check_layout_consistency(cls, df_columns: List[str], columns: List[str]) -> List[str]:
        diff = len(df_columns) - len(columns)
        if diff < 0 or diff > 2:
            raise ZRXPLayoutError(diff)
        else:
            if diff == 1:
                if "value.quality" in columns:
                    columns.append("value.interpolation")
                else:
                    columns.append("value.quality")
            elif diff == 2:
                columns.append("value.quality")
                columns.append("value.interpolation")
        return columns

    @classmethod
    def __localize_timestamps(cls, df_index: pd.DatetimeIndex, timezone: str) -> pd.DatetimeIndex:
        if "UTC+" in timezone or "GMT+" in timezone:
            timezone = "Etc/GMT-" + timezone.split("+")[-1].split(")")[0].split(":")[0]
        elif "UTC-" in timezone or "GMT-" in timezone:
            timezone = "Etc/GMT+" + timezone.split("-")[-1].split(")")[0].split(":")[0]
        try:
            return df_index.tz_localize(timezone)
        except UnknownTimeZoneError:
            return df_index.tz_localize("UTC")

    def load_data_frame(
        self,
        file: str,
        data_offset: int,
        columns: List[str],
        nrows: int = None,
        invalid: float = -777.0,
        timezone: str = "UTC",
    ) -> pd.DataFrame:
        if "status" in columns:
            columns[columns.index("status")] = "value.quality"
        if "interpolation_type" in columns:
            columns[columns.index("interpolation_type")] = "value.interpolation"
        with open(file, "rb") as f:
            f.seek(int(data_offset))
            df = pd.read_csv(f, engine="c", header=None, nrows=int(nrows), sep=r"\s+")
            df.columns = self.__check_layout_consistency(df.columns, columns)
            df = df.set_index("timestamp")
            df.index = pd.to_datetime(df.index, format="%Y%m%d%H%M%S")
            df.index = self.__localize_timestamps(df.index, timezone)
            df.loc[df["value"] == invalid, ["value"]] = np.nan
            if "value.quality" in columns:
                quality_col = "value.quality"
                df.loc[df[quality_col] < 0, ["value"]] = np.nan
            return df

    @classmethod
    def __extract_columns(cls, config: str) -> List[str]:
        if config is None:
            return ["timestamp", "value"]
        columns = []
        found = re.search("\\(([^)]+)\\)", config)

        if not found or not found.group(1):
            raise Exception("Invalid layout '{}'".format(config))
        for i in found.group(1).split(","):
            columns.append(i.strip())
        if "timestamp" not in columns:
            raise Exception("Missing timestamp in layout '{}'".format(config))
        if "value" not in columns:
            raise Exception("Missing value in layout '{}'".format(config))
        return columns


class ZRXPWriter(TimeSeriesWriter):
    def __init__(self, fmt: TimeSeriesFormat = None):
        if fmt is None:
            fmt = ZRXPFormat()
        super().__init__(fmt)

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
                    self._write_block(fh, ts, start, end)
                else:
                    self._write_block(fh, ts, start, end, meta_list[i])
        if os.path.isfile(file + ".metadata"):
            os.unlink(file + ".metadata")
        self.write_metadata(file, self.format.reader._extract_metadata(file))

    def _write_block(
        self,
        fh: TextIO,
        ts: Union[pd.DataFrame, TimeSeries],
        start: datetime,
        end: datetime,
        metadata: Mapping[str, Any] = None,
    ):
        if isinstance(ts, TimeSeries):
            data = ts.read_data_frame(start, end)
            metadata = ts.metadata
        else:
            data = ts
        self._write_header(fh, metadata, data)
        self._write_data(fh, data)

    def _write_header(self, fh: TextIO, metadata: Mapping[str, Any], data: pd.DataFrame):
        fh.write("#" + "|*|".join(self._header_values(metadata)) + "|*|\n")

        columns = data.columns.values.tolist()
        for i in range(len(columns)):
            if columns[i] == "value.status" or columns[i] == "value.quality":
                columns[i] = "status"
            if columns[i] == "value.interpolation":
                columns[i] = "interpolation_type"
        if len(columns) == 0:
            columns = ["value"]

        layout = "#LAYOUT(timestamp," + ",".join(columns) + ")|*|\n"
        fh.write(layout)

    @classmethod
    def _header_values(cls, metadata: Mapping[str, Any]):
        values = ["RINVAL-777"]
        for k, v in HEADER_KEYS.items():
            if metadata.get(v) is not None:
                values.append(k + str(metadata[v]))
        return values

    @classmethod
    def _write_data(cls, fh: TextIO, data: pd.DataFrame):
        for col in data.columns.values:
            if "quality" in col or "status" in col or "interpolation" in col:
                data[col] = data[col].astype(int)
        fh.write(
            data.to_csv(
                header=None,
                sep=" ",
                line_terminator="\n",
                date_format="%Y%m%d%H%M%S",
            )
        )

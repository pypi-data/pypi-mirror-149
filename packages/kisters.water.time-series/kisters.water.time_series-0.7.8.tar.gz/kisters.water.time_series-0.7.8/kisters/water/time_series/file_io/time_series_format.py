import json
import os
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any, Iterable, Mapping, MutableMapping, Union

from pandas import DataFrame

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.file_io.file_time_series import FileTimeSeries


def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        iso = obj.isoformat()
        if obj.utcoffset() is None:
            iso += "Z"
        return iso
    return str(obj)


class TimeSeriesReader(ABC):
    def __init__(self, fmt: "TimeSeriesFormat"):
        self._format = fmt

    def __extract_path(self, file):
        path = file
        for ext in list(self.format.extensions):
            if file.lower().endswith("." + ext.lower()):
                path = file[: -(len(ext) + 1)]
        if path.startswith(self.format.root_dir + "/") and self.format.root_dir != "":
            path = path[(len(self.format.root_dir) + 1) :]
        return path

    def _meta_from_file(self, file: str) -> MutableMapping[str, Any]:
        path = self.__extract_path(file)
        name = path.split("/")[-1:][0]
        meta = {
            "tsPath": path,
            "name": name,
            "shortName": name,
            list(self.format.extensions)[0].upper(): {"file": os.path.abspath(file)},
        }
        return meta

    @abstractmethod
    def _extract_metadata(self, file) -> Iterable[Mapping[str, Any]]:
        """Extracts the metadata from the corresponding format"""

    def _get_metadata(self, file: str) -> Iterable[Mapping[str, Any]]:
        meta_file = file + ".metadata"
        if os.path.isfile(meta_file):
            with open(file + ".metadata", "r") as r:
                json_list = json.load(r)
            if list(self.format.extensions)[0].upper() in json_list[0] and json_list[0][
                "tsPath"
            ] == self.__extract_path(file):
                return json_list
        return self._extract_metadata(file)

    def read(self, file: str) -> Iterable[FileTimeSeries]:
        for meta in self._get_metadata(file):
            yield FileTimeSeries(meta=meta, fmt=self.format)

    @abstractmethod
    def load_data_frame(self, *args, **kwargs) -> DataFrame:
        """Reads the DataFrame from the file format."""

    @property
    def format(self) -> "TimeSeriesFormat":
        return self._format


class TimeSeriesWriter(ABC):
    def __init__(self, fmt: "TimeSeriesFormat"):
        self._format = fmt

    @abstractmethod
    def write(
        self,
        file: str,
        data_list: Union[Iterable[DataFrame], Iterable[TimeSeries]],
        start: datetime = None,
        end: datetime = None,
        meta_list: Iterable[Mapping[str, Any]] = None,
    ):
        """
        Write the data_list (a list of TimeSeries or DataFrames) in the TimeSeries format,
        if it is a list of DataFrames then a list of metadata is required.
        """

    @classmethod
    def write_metadata(cls, file: str, meta_list: Iterable[Mapping[str, Any]]):
        with open(file + ".metadata", "w") as o:
            json.dump(meta_list, o, default=_json_serial, indent=4, sort_keys=True)

    def update_metadata(self, ts_path: str, file: str, meta: Mapping[str, Any]):
        with open(file + ".metadata", "r") as f:
            j_meta = json.load(f)
        for j in j_meta:
            if j.get("tsPath", "") == ts_path:
                j.update(meta)
        self.write_metadata(file, j_meta)

    @property
    def format(self) -> "TimeSeriesFormat":
        return self._format


class TimeSeriesFormat(ABC):
    def __init__(self):
        self.__root_dir = ""

    @property
    def root_dir(self):
        return self.__root_dir

    @property
    @abstractmethod
    def extensions(self) -> Iterable[str]:
        """Returns the list with the possible extensions for this format."""

    @property
    @abstractmethod
    def reader(self) -> TimeSeriesReader:
        """Returns the TimeSeriesReader for this format."""

    @property
    @abstractmethod
    def writer(self) -> TimeSeriesWriter:
        """Returns the TimeSeriesWriter for this format."""

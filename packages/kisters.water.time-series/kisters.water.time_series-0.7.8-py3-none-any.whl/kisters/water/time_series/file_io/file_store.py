import logging
import os
import re
from typing import Any, Iterable, List, Mapping, Union

import pandas as pd

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_store import TimeSeriesStore
from kisters.water.time_series.file_io.file_time_series import FileEnsembleTimeSeries
from kisters.water.time_series.file_io.time_series_format import TimeSeriesFormat

logger = logging.getLogger(__name__)


class FileStore(TimeSeriesStore):
    """FileStore provides a TimeSeriesStore for your local time series data files

    Args:
        root_dir: The path to your time series data folder.
        file_format: The format used by your time series data files.

    Examples:
        .. code-block:: python

            from kisters.water.time_series.file_io import FileStore, ZRXPFormat
            fs = FileStore('tests/data', ZRXPFormat())
            ts = fs.get_by_path('validation/inner_consistency1/station1/H')
    """

    def __init__(self, root_dir: str, file_format: TimeSeriesFormat):
        file_format._TimeSeriesFormat__root_dir = root_dir
        self.__file_format = file_format
        self.__root_dir = root_dir
        if not os.path.isdir(self.__root_dir):
            raise FileNotFoundError("Path " + os.path.abspath(self.__root_dir) + " does not exist")

    def create_time_series(
        self,
        path: str,
        display_name: str,
        attributes: Mapping[str, Any] = None,
        params: Mapping[str, Any] = None,
    ) -> TimeSeries:
        if attributes is None:
            attributes = {}
        self.__file_format.writer.write(
            file=os.path.join(self.__root_dir, path + "." + list(self.__file_format.extensions)[0]),
            data_list=[pd.DataFrame()],
            meta_list=[{"name": display_name, **attributes}],
        )
        return self.get_by_path(path)

    def create_time_series_from(self, copy_from: TimeSeries, new_path: str = None) -> TimeSeries:
        meta = copy_from.metadata
        if new_path is None:
            folder, file = copy_from.path.rsplit("/", 1)
            new_path = folder + "/Copy-{}".format(file)
            logger.warning(
                "To avoid overwriting original file the new Time Series file will be {},"
                " if you want to overwrite it please specify the new_path explicitly".format(new_path)
            )
        meta["tsPath"] = new_path
        return self.create_time_series(path=new_path, display_name=copy_from.name, attributes=meta)

    @staticmethod
    def is_ensemble(ts) -> bool:
        return any(
            x in ts.metadata["columns"] for x in ["member", "forecast", "dispatchinfo", "dispatch_info"]
        )

    @classmethod
    def are_ensemble(cls, ts_list) -> bool:
        return all(cls.is_ensemble(ts) for ts in ts_list)

    def _get_time_series_list(
        self,
        ts_filter: str = None,
        id_list: List[int] = None,
        params: Mapping[str, Any] = None,
    ) -> Iterable[TimeSeries]:
        ts_list = []
        for f in self._file_list(self.__root_dir):
            tss = self.__file_format.reader.read(f)

            tss = list(tss)
            if len(tss) > 1:
                stations_to_ids = self._group_indices_by_station(tss)
                for _station, ids in stations_to_ids.items():
                    ts_children = [tss[i] for i in ids]
                    if self.are_ensemble(ts_children):
                        ts_list.append(FileEnsembleTimeSeries.from_timeseries_list(ts_children))
                    else:
                        ts_list.extend(ts_children)
            else:
                ts_list.extend(tss)
        ts_list = self._filter(ts_list, ts_filter)
        ts_list = self._filter_id_list(ts_list, id_list)
        return ts_list

    @staticmethod
    def _group_indices_by_station(
        ts_list: List[TimeSeries],
    ) -> Mapping[str, Iterable[int]]:
        station_to_indices = {}
        for i in range(len(ts_list)):
            station = ts_list[i].metadata.get("REXCHANGE")
            if station not in station_to_indices:
                station_to_indices[station] = []
            station_to_indices[station].append(i)
        return station_to_indices

    @classmethod
    def _filter(cls, ts_list: Iterable[TimeSeries], ts_filter: str) -> Iterable[TimeSeries]:
        if ts_filter is None:
            return ts_list
        result = []
        exp = re.compile(
            "^"
            + ts_filter.replace(".", "\\.").replace("/", "\\/").replace("?", "\\?").replace("*", ".*")
            + "$"
        )
        for ts in ts_list:
            path = ts.path
            if exp.match(path):
                result.append(ts)
        return result

    @classmethod
    def _filter_id_list(cls, ts_list: Iterable[TimeSeries], id_list: Iterable[int]) -> Iterable[TimeSeries]:
        if id_list is None:
            return ts_list
        result = []
        for ts in ts_list:
            ts_id = ts.id
            if (ts_id is not None) and (ts_id in id_list):
                result.append(ts)
        return result

    def _get_time_series(
        self, ts_id: int = None, path: str = None, params: Mapping[str, Any] = None
    ) -> Union[TimeSeries, None]:
        if params is None:
            params = {"includeDataCoverage": True}
        ts_list = list(
            self._get_time_series_list(ts_filter=path, id_list=[ts_id] if ts_id else None, params=params)
        )
        if len(ts_list) == 0:
            raise KeyError("Requested TimeSeries does not exist.")
        else:
            return ts_list[0]

    def _file_list(self, path: str) -> List[str]:
        file_list = []
        try:
            extensions = self.__file_format.extensions
            for f in sorted(os.listdir(path)):
                if os.path.isfile(path + "/" + f):
                    for e in extensions:
                        if f.lower().endswith("." + e.lower()):
                            file_list.append(path + "/" + f)
                elif os.path.isdir(path + "/" + f):
                    for ff in self._file_list(path + "/" + f):
                        file_list.append(ff)
        except FileNotFoundError:
            return file_list
        return file_list

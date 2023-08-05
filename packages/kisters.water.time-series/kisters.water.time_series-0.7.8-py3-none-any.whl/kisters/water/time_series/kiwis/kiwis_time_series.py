import pprint
import re
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, MutableMapping, Optional

import dateutil
import pandas as pd
from pandas import DataFrame
from requests import Response

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_attributes_mixin import TimeSeriesAttributesMixin
from kisters.water.time_series.core.time_series_cut_range_mixin import TimeSeriesCutRangeMixin
from kisters.water.time_series.core.time_series_item_mixin import TimeSeriesItemMixin
from kisters.water.time_series.kiwis.helpers import prepare_params

if TYPE_CHECKING:
    from kisters.water.time_series.kiwis import KiWISStore

pp = pprint.PrettyPrinter(indent=4)


class _KiWISTimeSeries(TimeSeriesItemMixin, TimeSeriesAttributesMixin, TimeSeriesCutRangeMixin, TimeSeries):
    """KiWIS REST specific time series implementation"""

    def __init__(self, kiwis_store: "KiWISStore", j: Dict[str, Any], init_coverage: bool = True):
        j["tsPath"] = j.pop("ts_path", None)
        j["shortName"] = j.pop("ts_shortname", None)
        self.__dict__ = j.copy()
        super().__init__()
        self._kiwis_store = kiwis_store
        self._metadata = j.copy()

        if "from" in j and j["from"] != "":
            self._metadata["from"] = dateutil.parser.parse(j["from"])
        if "to" in j and j["to"] != "":
            self._metadata["to"] = dateutil.parser.parse(j["to"])

        self.__init_coverage = init_coverage

    def _raw_metadata(self) -> MutableMapping[str, Any]:
        return self._metadata

    def _data(
        self,
        start: datetime = None,
        end: datetime = None,
        params: Mapping[str, Any] = None,
    ) -> Response:
        if params is None:
            params = {}

        if start is not None:
            params["from"] = start.isoformat()

        if end is not None:
            params["to"] = end.isoformat()

        if self.path is not None:
            params["ts_path"] = self.path
        else:
            params["ts_id"] = self._metadata["id"]

        params = prepare_params(params)

        if self.__is_ensemble():
            j = self._kiwis_store._kiwis.getTimeseriesEnsembleValues(**params)
        else:
            j = self._kiwis_store._kiwis.getTimeseriesValues(**params)
        return j

    def __is_ensemble(self):
        # I have no better solution...
        ts_shortname = self._metadata["shortName"]
        return "ensemble" in ts_shortname.lower()

    def _load_data_frame(
        self,
        start: datetime = None,
        end: datetime = None,
        params: Mapping[str, Any] = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
    ) -> pd.DataFrame:
        # NOTE: KiWIS ensemble time series behavior is that it (1) returns the latest t0
        # when no query params are are used, or (2) return the t0s between from and to.

        # To get *all* t0s we could just use from=1, to=9999, but this places a heavy
        # burden on the server
        if self.__is_ensemble():
            resp = self._data(start, end, params)
            ts_id = self._metadata["id"]
            json_data = resp.json()
            ens_ts_list = json_data[str(ts_id)]
            for ens_ts in ens_ts_list:
                t0_data = pd.to_datetime(ens_ts["ensembledate"])
                dispatch_info_data = ens_ts["ensembledispatchinfo"]
                if t0 != t0_data or dispatch_info != dispatch_info_data:
                    continue
                j = ens_ts["timeseries"]
                cols = j["columns"].split(",")
                col_member_ts = 2 * (cols.index(member) - 1)
                col_member_data = col_member_ts + 1
                member_ts_data = []
                for row in j["data"]:
                    ts_member = row[col_member_ts]
                    data_member = row[col_member_data]
                    member_ts_data.append([t0_data, dispatch_info_data, member, ts_member, data_member])
                df = DataFrame(
                    member_ts_data,
                    columns=["t0", "dispatch_info", "member", "timestamp", "value"],
                )
                ts_col = "timestamp"
                df[ts_col] = pd.to_datetime(df[ts_col], utc=True)
                df.set_index(ts_col, inplace=True)
                return df
            raise ValueError("No ensemble timeseries found.")
        else:
            data = self._data(start, end, params)
            j = data.json()[0]
        c = j["columns"].split(",")
        d = j["data"]
        ts_col = "timestamp"
        c[0] = ts_col
        raw_data = DataFrame(d, columns=c)
        raw_data[ts_col] = pd.to_datetime(raw_data[ts_col], utc=True)
        raw_data.set_index(ts_col)
        raw_data.index = raw_data[ts_col]
        return raw_data[c[1:]]

    @property
    def coverage_from(self) -> Optional[datetime]:
        if "from" not in self._metadata:
            self._init_coverage()
            if "from" not in self._metadata:
                return None
        return self._metadata["from"]

    @property
    def coverage_until(self) -> Optional[datetime]:
        if "to" not in self._metadata:
            self._init_coverage()
            if "to" not in self._metadata:
                return None
        return self._metadata["to"]

    def _init_coverage(self):
        if self.__init_coverage:
            self.__init_coverage = False
            ts = self._kiwis_store._get_time_series(self._metadata["id"])
            self._metadata["from"] = ts.coverage_from
            self._metadata["to"] = ts.coverage_until

    def transform(self, transformation: str) -> TimeSeries:
        if re.match(".*\\(.*\\)", self.path):
            return self._kiwis_store._get_time_series(path=self.path + ";" + transformation)
        else:
            return self._kiwis_store._get_time_series(path="tsm(" + self.path + ");" + transformation)

    def get_comments(self, start: datetime = None, end: datetime = None) -> DataFrame:
        """Read comments from a time series and returns it as data frame

        :param start: optional start time stamp
        :param end: optional end time stamp
        """
        return self.read_data_frame(
            start=start,
            end=end,
            params={
                "returnfields": [
                    "Timestamp",
                    "Timeseries Comment",
                    "Agent Comment",
                    "Station Comment",
                    "Parameter Comment",
                    "Data Comment",
                ]
            },
        )

    def write_data_frame(
        self,
        data_frame,
        start: datetime = None,
        end: datetime = None,
        default_quality=200,
        default_interpolation=1,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
    ):
        self._to_data(data_frame)

    def _to_data(self, data_frame, default_quality=200, default_interpolation=1):
        raise NotImplementedError

    def read_ensemble_members(self, t0_start: datetime = None, t0_end: datetime = None) -> List[Mapping]:
        params = {}
        # NOTE: KiWIS can only return either the latest t0 when no query params are
        # are used, or the t0s between from and to.
        #
        # To get all t0s we could just use from=0001, to=9999, but this places a heavy
        # burden on the server
        if t0_start is not None:
            params["from"] = t0_start.isoformat()
        # else:
        #     params['from'] = '0001'

        if t0_end is not None:
            params["to"] = t0_end.isoformat()
        # else:
        #     params['to'] = '9999'

        ts_id = self._metadata["id"]
        if self.path is not None:
            params["ts_path"] = self.path
        else:
            params["ts_id"] = ts_id

        data = self._kiwis_store._kiwis.getTimeseriesEnsembleValues(**params).json()
        ens_ts_list = data[str(ts_id)]

        all_ens_members = []

        for ens_ts in ens_ts_list:
            # get t0 and dispatchinfo
            t0 = pd.to_datetime(ens_ts["ensembledate"])
            dispatch_info = ens_ts["ensembledispatchinfo"]
            # members are encoded in the timeseries columns
            ts = ens_ts["timeseries"]
            columns = ts["columns"].lower().split(",")
            if len(columns) < 2 or columns[0] != "timestamp":
                raise ValueError(
                    "Cannot determine the ensemble members for time series "
                    f"{ts_id} using this column information: {columns}."
                )
            members = columns[1:]

            ens_members = [
                {
                    "t0": t0,
                    "dispatch_info": dispatch_info,
                    "member": member,
                }
                for member in members
            ]

            all_ens_members += ens_members
        return all_ens_members

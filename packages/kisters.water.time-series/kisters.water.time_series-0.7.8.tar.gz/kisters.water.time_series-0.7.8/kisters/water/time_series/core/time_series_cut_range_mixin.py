from abc import abstractmethod
from datetime import datetime
from typing import Mapping, Union

import pytz
from pandas import DataFrame, to_datetime

from kisters.water.time_series.core import TimeSeries


class TimeSeriesCutRangeMixin(TimeSeries):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self._tz = pytz.utc

    @abstractmethod
    def _load_data_frame(
        self,
        start: datetime = None,
        end: datetime = None,
        params: Mapping = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
        **kwargs,
    ) -> DataFrame:
        """
        Return the DataFrame containing the TimeSeries data for the interval start:end
        """

    def _get_timezone(self) -> pytz.timezone:
        return self._tz

    def _to_zoned_datetime(self, dt: Union[str, datetime]) -> Union[datetime, None]:
        if dt is None:
            return None
        else:
            dt = to_datetime(dt)
            if dt.tz is None:
                return dt.tz_localize(self._get_timezone())
            return dt

    def read_data_frame(
        self,
        start: datetime = None,
        end: datetime = None,
        params: Mapping = None,
        t0=None,
        dispatch_info=None,
        member=None,
        **kwargs,
    ) -> DataFrame:
        start = start if start is not None else self.coverage_from
        end = end if end is not None else self.coverage_until
        start = self._to_zoned_datetime(start)
        end = self._to_zoned_datetime(end)
        if start is not None and end is not None and start > end:
            return DataFrame()

        df = self._load_data_frame(
            start=start,
            end=end,
            params=params,
            t0=t0,
            dispatch_info=dispatch_info,
            member=member,
        )
        df.index = df.index.tz_convert(self._get_timezone())
        return df

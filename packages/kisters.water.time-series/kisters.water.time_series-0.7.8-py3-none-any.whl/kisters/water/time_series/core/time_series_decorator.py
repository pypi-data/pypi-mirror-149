from datetime import datetime
from typing import Mapping, Union

from pandas import DataFrame

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_attributes_mixin import TimeSeriesAttributesMixin
from kisters.water.time_series.core.time_series_cut_range_mixin import TimeSeriesCutRangeMixin
from kisters.water.time_series.core.time_series_item_mixin import TimeSeriesItemMixin


class TimeSeriesDecorator(
    TimeSeriesItemMixin, TimeSeriesAttributesMixin, TimeSeriesCutRangeMixin, TimeSeries
):
    def __init__(self, forward: Union[TimeSeries, TimeSeriesCutRangeMixin]):
        super().__init__()
        self._forward = forward
        self._tz = forward._tz

    def _raw_metadata(self) -> Mapping:
        return self._forward.metadata

    def _load_data_frame(
        self,
        start: datetime = None,
        end: datetime = None,
        params: Mapping[str, str] = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
    ) -> DataFrame:
        return self._forward._load_data_frame(start, end, params)

    @property
    def coverage_from(self) -> datetime:
        return self._forward.coverage_from

    @property
    def coverage_until(self) -> datetime:
        return self._forward.coverage_until

    def write_data_frame(
        self, data_frame: DataFrame, start: datetime = None, end: datetime = None, **kwargs
    ):
        return self._forward.write_data_frame(data_frame, start, end, **kwargs)

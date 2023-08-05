from datetime import datetime
from typing import Any, Mapping, MutableMapping

import numpy as np
import pandas as pd

from kisters.water.time_series.core.time_series_attributes_mixin import TimeSeriesAttributesMixin
from kisters.water.time_series.core.time_series_cut_range_mixin import TimeSeriesCutRangeMixin
from kisters.water.time_series.core.time_series_item_mixin import TimeSeriesItemMixin


class MemoryTimeSeries(TimeSeriesCutRangeMixin, TimeSeriesAttributesMixin, TimeSeriesItemMixin):
    def __init__(
        self,
        metadata: MutableMapping[str, Any],
        data: pd.DataFrame,
        comments: pd.DataFrame = None,
    ):
        """
        Create a TimeSeries object directly with the metadata, data and comments given.

        Args:
            metadata: Mapping with all the metadata of the TimeSeries.
             At least it must contain the following: "tsPath", "id", "name" and "shortName".
            data: DataFrame object containing TimeSeries data.
             Expects as minimum a DataFrame with DatetimeIndex and one column.
            comments: DataFrame object containing comments with the form 'from', 'until', 'comment'.
        """
        super().__init__()
        validation_message = self.__validate_instance(metadata, data, comments)
        if len(validation_message) == 0:
            try:
                data.index = data.index.tz_localize("utc")
            except TypeError:
                pass
            self.__data = data
            self.__metadata = metadata
            self.__comments = comments
        else:
            raise ValueError(validation_message)

    @classmethod
    def __validate_instance(
        cls, metadata: Mapping[str, Any], data: pd.DataFrame, comments: pd.DataFrame
    ) -> str:
        if data is not None and (not isinstance(data.index, pd.DatetimeIndex) or len(data.columns) == 0):
            return "Data provided as data doesn't have a DatetimeIndex and/or doesn't have columns"
        if comments is not None and not np.all(comments.columns == ["from", "until", "comments"]):
            return "Comments provided don't have the columns: 'from', 'until', 'comments'"
        return ""

    def _raw_metadata(self) -> MutableMapping[str, Any]:
        return self.__metadata

    @property
    def coverage_from(self) -> datetime:
        return self.__data.index[0]

    @property
    def coverage_until(self) -> datetime:
        return self.__data.index[self.__data.shape[0] - 1]

    def _load_data_frame(
        self,
        start: datetime = None,
        end: datetime = None,
        params: Mapping = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
    ) -> pd.DataFrame:
        if start is None and end is None:
            return self.__data.copy()
        if start is None:
            return self.__data.loc[self.__data.index <= end].copy()
        elif end is None:
            return self.__data.loc[self.__data.index >= start].copy()
        else:
            return self.__data.loc[(self.__data.index >= start) & (self.__data.index <= end)].copy()

    def write_data_frame(self, data_frame: pd.DataFrame, start: datetime = None, end: datetime = None):
        mask = None
        try:
            data_frame.index = data_frame.index.tz_localize("utc")
        except TypeError:
            pass
        if start is not None:
            mask = data_frame.index >= start
        if end is not None:
            mask = data_frame.index <= end if mask is None else mask & (data_frame.index <= end)
        if mask is not None:
            data_frame = data_frame.loc[mask]
        if self.__data is None:
            self.__data = data_frame
        else:
            self.__data = pd.concat(
                [self.__data, data_frame[~data_frame.index.isin(self.__data.index)]],
                sort=True,
            )
            self.__data.update(data_frame)
            self.__data = self.__data.reindex(self.__data.index.sort_values())

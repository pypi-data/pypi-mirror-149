from datetime import datetime
from typing import Union

from pandas import DataFrame

from kisters.water.time_series.core.time_series import TimeSeries


class TimeSeriesItemMixin(object):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        super(TimeSeriesItemMixin, self).__init__()

    def __getitem__(self: TimeSeries, key: Union[slice, datetime, str]) -> DataFrame:
        if isinstance(key, slice):
            start = key.start
            end = key.stop
            if key.step is not None:
                raise Exception("Step not supported")
        elif isinstance(key, datetime) or isinstance(key, str):
            start = key
            end = key
        else:
            raise ValueError("Type of " + str(key) + " not supported")

        return self.read_data_frame(start, end)

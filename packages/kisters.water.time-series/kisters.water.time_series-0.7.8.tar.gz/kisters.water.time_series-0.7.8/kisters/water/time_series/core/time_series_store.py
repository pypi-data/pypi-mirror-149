import warnings
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Iterable, Mapping, Union

import pandas as pd

from kisters.water.time_series.core.entity import Entity
from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.utils import make_iterable


def deprecated(message=""):
    def wrap(f):
        def wraped_f(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)
            warnings.warn(
                "Deprecated call to function {}, {}".format(f.__name__, message),
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter("default", DeprecationWarning)
            return f(*args, **kwargs)

        return wraped_f

    return wrap


class TimeSeriesStore(ABC):
    def get_by_id(
        self,
        ts_id: Union[int, str, Iterable[int], Iterable[str]],
        params: Mapping[str, Any] = None,
    ) -> Union[TimeSeries, Iterable[TimeSeries]]:
        """Get the time series by id.

        Args:
            ts_id: List of ids or single id.
            params: The additional parameters, which are passed to the backend.

        Returns:
            The time series or a list of time series if ts_id is a list.

        Examples:
            .. code-block:: python

                store.get_by_id(4711)
                store.get_by_id([4711, 4712])

        """
        if isinstance(ts_id, (int, str)):
            return self._get_time_series(ts_id=ts_id, params=params)
        else:
            return self._get_time_series_list(id_list=ts_id, params=params)

    def get_by_path(self, path: str, params: Mapping[str, Any] = None) -> TimeSeries:
        """Get the time series by path.

        Args:
            path: The full qualified time series path.
            params: The additional parameters, which are passed to the backend.

        Returns:
            The TimeSeries object.

        Examples:
            .. code-block:: python

                store.get_by_path("W7AgentTest/20003/S/cmd")

        """
        if path[0] == "/":
            raise ValueError("Unexpected leading slash in path, use {}".format(path[1:]))
        return self._get_time_series(path=path, params=params)

    def get_by_filter(self, ts_filter: str, params: Mapping[str, Any] = None) -> Iterable[TimeSeries]:
        """Get the time series list by filter.

        Args:
            ts_filter: time series path or filter.
            params: the additional parameters, which are passed to the backend.

        Returns:
            The list of the found TimeSeries objects.

        Examples:
            .. code-block:: python

                store.get_by_filter("W7AgentTest/20004/S/*")
        """
        if ts_filter[0] == "/":
            raise ValueError("Unexpected leading slash in path, use {}".format(ts_filter[1:]))
        return self._get_time_series_list(ts_filter=ts_filter, params=params)

    @deprecated(message="use get_by_filter or get_by_id instead")
    def get_time_series_list(
        self,
        ts_filter: str = None,
        id_list: Iterable[int] = None,
        params: Mapping[str, Any] = None,
    ) -> Iterable[TimeSeries]:
        """
        Deprecated: 0.3.0
            Use :func:`get_by_filter` or :func:`get_by_id`.

        Get the time series list and return a list of TimeSeries objects.

        Args:
            ts_filter: The ts filter.
            id_list: The id list.
            params: The additional parameters, which are passed to the backend.

        Returns:
             The list of TimeSeries objects.

        """
        return self._get_time_series_list(ts_filter, id_list, params)

    @abstractmethod
    def _get_time_series_list(
        self,
        ts_filter: str = None,
        id_list: Iterable[int] = None,
        params: Mapping[str, Any] = None,
    ) -> Iterable[TimeSeries]:
        """
        Deprecated: 0.3.0
            Use :func:`get_by_filter` or :func:`get_by_id`.

        Get the time series list and return a list of TimeSeries objects.

        Args:
            ts_filter: The ts filter.
            id_list: The id list.
            params: The additional parameters, which are passed to the backend.

        Returns:
             The list of TimeSeries objects.

        """

    @deprecated(message="use get_by_path or get_by_id instead")
    def get_time_series(
        self, ts_id: int = None, path: str = None, params: Mapping[str, Any] = None
    ) -> TimeSeries:
        """
        Deprecated: 0.3.0
            Use :func:`get_by_path` or :func:`get_by_id`.

        Get a time series identified by id or by path and return a TimeSeries.

        Args:
            ts_id: The time series id.
            path: The time series path.
            params: The additional parameters, which are passed to the backend.

        Returns:
             The TimeSeries objects.
        """
        return self._get_time_series(ts_id, path, params)

    @abstractmethod
    def _get_time_series(
        self, ts_id: int = None, path: str = None, params: Mapping[str, Any] = None
    ) -> TimeSeries:
        """
        Deprecated: 0.3.0
            Use :func:`get_by_path` or :func:`get_by_id`.

        Get a time series identified by id or by path and return a TimeSeries.

        Args:
            ts_id: The time series id.
            path: The time series path.
            params: The additional parameters, which are passed to the backend.

        Returns:
             The TimeSeries objects.
        """

    def write_time_series_list(
        self,
        ts_list: Iterable[TimeSeries],
        start: datetime = None,
        end: datetime = None,
        auto_create: bool = False,
    ):
        """Write a time series list to the back end for the given time range.

        Args:
            ts_list: The time series list.
            start: The starting date from which data will be written.
            end: The ending date until which data will be written.
            auto_create: Create the time series if not exists in the back end.

        Examples:
            .. code-block:: python

                ts_list = store1.get_by_filter('W7AgentTest/2000*')
                store2.write_time_series_list(ts_list, datetime(2001, 1, 1), datetime(2002, 1, 1))

        """
        for ts in ts_list:
            self.write_time_series(ts, start, end, auto_create)

    def write_time_series(
        self,
        ts: TimeSeries,
        start: datetime = None,
        end: datetime = None,
        auto_create: bool = False,
    ) -> TimeSeries:
        """Write a single time series to the time series back end for the given time range.

        Args:
            ts: The time series to write.
            start: The starting date from which data will be written.
            end: The ending date until which data will be written.
            auto_create: Create the time series if not exists in the back end.

        Examples:
            .. code-block:: python

                ts = store1.get_by_id(47122)
                store2.write_time_series(ts)

        """
        try:
            found = self.get_by_path(ts.path)
        except KeyError:
            try:
                found = self.get_by_id(ts.path)
            except KeyError:
                if auto_create:
                    found = self.create_time_series_from(ts)
                else:
                    raise
        found.write_data_frame(ts.read_data_frame(start, end))
        return found

    def create_time_series_from(self, copy_from: TimeSeries, **kwargs) -> TimeSeries:
        """
        Create a time series as a copy from another existing time series e.g. from another system.
        This function only copies meta data and only if the underlaying backend supports it.

        Args:
            copy_from: The time series object to be copied.
        """
        return self.create_time_series(copy_from.path, copy_from.name, copy_from.metadata)

    @abstractmethod
    def create_time_series(
        self,
        path: str,
        display_name: str,
        attributes: Mapping = None,
        params: Mapping[str, Any] = None,
    ) -> TimeSeries:
        """Create an empty time series.

        Args:
            path: The time series path.
            display_name: The time series name to display.
            attributes: The metadata of the time series.
            params: The additional parameters, which are passed to the backend.
        """

    def __getitem__(self, item: Union[int, str]) -> TimeSeries:
        if isinstance(item, int):
            return self.get_by_id(item)
        else:
            return self.get_by_path(item)

    def get_entity_list(
        self, entity_filter: str = None, entities_id: Iterable[int] = None, **kwargs
    ) -> Iterable[Entity]:
        """
        Retrieve a list of entities from the backend.

        The behaviour depends totally on the backend implementation, this should decide
        if both entity_filter and entities_id arguments can be given and how they behave
        if both are given. As a rule of thumb if both arguments are given a double filter
        should be applied.
        Args:
            entity_filter: The entity filter.
            entities_id: A list of entities id.
            **kwargs: Additional arguments dependent on the backend.

        Returns:
            The list of Entity objects.
        """
        raise NotImplementedError

    def get_entity(self, entity_path: str = None, entity_id: int = None, **kwargs) -> Entity:
        """
        Retrieve a single Entity from the backend.

        Basic implementation is given based on get_entity_list, but it is recommended
        to overwrite this method based on the backend specifications.
        Args:
            entity_path: The entity path.
            entity_id: The entity id.
            **kwargs: Additional arguments dependent on the backend.

        Returns:
            The matching Entity.
        """
        return list(self.get_entity_list(entity_path, [entity_id], **kwargs))[0]

    def read_data_frames(
        self,
        ts_list: Iterable[TimeSeries],
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
        params: Mapping = None,
        # TODO: t0, dispatch_info & member are only applicable per time series, so
        #  using a single value for these parameters doesn't make sense they will be
        #  applied to all time series. To fix this one could for instance make these
        #  parameters a list of values, eg:
        #  t0: Iterable[datetime], dispatch_info: Iterable[str], member: Iterable[str]
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
    ) -> Mapping[TimeSeries, pd.DataFrame]:
        """Read multiple time series as data frames.

        Note: TimeSeriesStore provides a default unoptimized implementation. Override
        this method if your store can provide a more efficient bulk read method.
        """
        return {
            ts: ts.read_data_frame(
                start=start,
                end=end,
                params=params,
                t0=t0,
                dispatch_info=dispatch_info,
                member=member,
            )
            for ts in ts_list
        }

    def write_data_frames(
        self,
        ts_list: Iterable[TimeSeries],
        data_frames: Iterable[pd.DataFrame],
        start: Union[str, datetime, Iterable] = None,
        end: Union[str, datetime, Iterable] = None,
        t0: Union[datetime, Iterable] = None,
        dispatch_info: Union[str, Iterable] = None,
        member: Union[str, Iterable] = None,
    ):
        """Write multiple data frames to time series

        Note: Override this method if your store can provide a better implementation
        to bulk write data frames.
        """
        for ts_i, df_i, start_i, end_i, t0_i, dispatch_info_i, member_i, in zip(
            ts_list,
            data_frames,
            make_iterable(start),
            make_iterable(end),
            make_iterable(t0),
            make_iterable(dispatch_info),
            make_iterable(member),
        ):
            ts_i.write_data_frame(
                df_i,
                start=start_i,
                end=end_i,
                t0=t0_i,
                dispatch_info=dispatch_info_i,
                member=member_i,
            )

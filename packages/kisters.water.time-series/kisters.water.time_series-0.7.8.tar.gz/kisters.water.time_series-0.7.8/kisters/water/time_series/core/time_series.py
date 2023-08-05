from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Mapping, MutableMapping, Union

from pandas import DataFrame


class TimeSeries(ABC):
    """This class provides the interface of TimeSeries."""

    def __init__(self, *args, **kwargs):
        """Constructor for the TimeSeries class."""

    def __str__(self) -> str:
        """Return the string representations for the TimeSeries"""

    @property
    @abstractmethod
    def coverage_from(self) -> datetime:
        """
        The date from which the TimeSeries data starts.

        Returns:
            The start date
        """

    @property
    @abstractmethod
    def coverage_until(self) -> datetime:
        """
        The date until which the TimeSeries data covers.

        Returns:
            The end date
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The full name of the TimeSeries.

        Returns:
            The full name
        """

    @property
    @abstractmethod
    def id(self) -> int:
        """
        The id number which fully identifies the TimeSeries.

        Returns:
            The id number
        """

    @property
    @abstractmethod
    def short_name(self) -> str:
        """
        The short name of the TimeSeries.

        Returns:
            The short name
        """

    @property
    @abstractmethod
    def path(self) -> str:
        """
        The full path to this TimeSeries.

        Returns:
             The path string
        """

    @property
    @abstractmethod
    def metadata(self) -> MutableMapping[str, Any]:
        """
        The map containing all the metadata related to this TimeSeries.

        Returns:
             The metadata map
        """

    def read_ensemble_members(self, t0_start: datetime = None, t0_end: datetime = None):
        """Returns a list of dictionaries with the corresponding t0, member and dispatch_infos as key.

        Args:
            t0_start: The starting date from which the data will be returned.
            t0_end: The ending date until which the data will be covered (end date included).
        """
        raise NotImplementedError

    @abstractmethod
    def read_data_frame(
        self,
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
        params: Mapping = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
        **kwargs,
    ) -> DataFrame:
        """
        This method returns the TimeSeries data between the start and end dates (both dates included)
        structured as a pandas DataFrame.

        Args:
            start: The starting date from which the data will be returned, expressed either
            as an ISO Datetime string or as a datetime object. If TimeZone is not included,
            it assumes the TimeZone of the TimeSeries.
            end: The ending date until which the data will be covered (end date included),
            expressed either as an ISO Datetime string or as a datetime object. If TimeZone
            is not included, it assumes the TimeZone of the TimeSeries.
            params: The parameters passed to the backend call.

            For ensemble time series only:
                To retrieve all data points of all dispatch_infos and members
                    set t0, dispatch_info, member to None including t0, dispatch_info, member as additional columns
                To retrieve a single ensemble member
                    t0: the t0 time stamp of the ensemble member
                    dispatch_info: ensemble dispatch_info identifier
                    member: ensemble member identifier

        Returns:
            The DataFrame containing the TimeSeries data
        """

    @abstractmethod
    def write_data_frame(
        self,
        data_frame: DataFrame,
        start: datetime = None,
        end: datetime = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
        **kwargs,
    ):
        """
        This methods writes the TimeSeries data from the data_frame into this TimeSeries.
        If either start or end, cover data missing in the data_frame these date ranges will be deleted.
        So if you specify an empty DataFrame, you can remove all data between start and end.

        Args:
            data_frame: The TimeSeries data to be written in the form of a pandas DataFrame.
            start: The date from which data will be writen.
            end: The date until which data will be writen (end date included).

            For ensemble time series only:
                To write a single ensemble member at once
                    t0: the t0 time stamp of the ensemble member
                    dispatch_info: ensemble dispatch_info identifier
                    member: ensemble member identifier
                    start, end will be ignored
        """

from abc import ABC, abstractmethod
from typing import Any, Generic, MutableMapping, TypeVar, Union

from kisters.water.time_series.core.time_series import TimeSeries

T = TypeVar("T")


class CopyableMutableMapping(ABC, Generic[T], MutableMapping):
    @abstractmethod
    def copy(self: MutableMapping) -> MutableMapping:
        """Return a copy of self."""


class TimeSeriesAttributesMixin(TimeSeries):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        super(TimeSeriesAttributesMixin, self).__init__()

    def __str__(self) -> str:
        return "{}({})".format(self.path, str(self.id))

    def __repr__(self, *args, **kwargs) -> str:
        return "<{} {}({})>".format(self.__class__.__name__, self.path, str(self.id))

    @abstractmethod
    def _raw_metadata(self) -> CopyableMutableMapping:
        """Return the TimeSeries metadata as it originally is."""

    def _safe_meta(self, key: str) -> Union[int, str, None]:
        m = self._raw_metadata()
        if key not in m:
            return None
        return m[key]

    @property
    def name(self) -> str:
        return self._safe_meta("name")

    @property
    def id(self) -> int:
        return self._safe_meta("id")

    @property
    def short_name(self) -> str:
        return self._safe_meta("shortName")

    @property
    def path(self) -> str:
        return self._safe_meta("tsPath")

    @property
    def metadata(self) -> MutableMapping[str, Any]:
        m = self._raw_metadata().copy()
        m["tsPath"] = self.path
        m["id"] = self.id
        m["name"] = self.name
        m["shortName"] = self.short_name
        m["dataCoverageFrom"] = self.coverage_from
        m["dataCoverageUntil"] = self.coverage_until
        return m

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Mapping, Union

import pandas as pd
import pytz
from pandas.errors import EmptyDataError
from pytz import UnknownTimeZoneError

from kisters.water.time_series.core import (
    TimeSeries,
    TimeSeriesAttributesMixin,
    TimeSeriesCutRangeMixin,
    TimeSeriesItemMixin,
)
from kisters.water.time_series.core.utils import valid_ensemble_args

if TYPE_CHECKING:
    from kisters.water.time_series.file_io.time_series_format import TimeSeriesFormat

logger = logging.getLogger(__name__)


class FileTimeSeries(
    TimeSeriesItemMixin,
    TimeSeriesAttributesMixin,
    TimeSeriesCutRangeMixin,
    TimeSeries,
):
    def __init__(self, fmt: "TimeSeriesFormat", meta: Mapping[str, Any] = None):
        super().__init__()
        self.__meta = meta
        self.__fmt = fmt
        self.__meta.setdefault("dataCoverageFrom", None)
        self.__meta.setdefault("dataCoverageUntil", None)
        timezone = self.metadata.get("timezone", None)
        if timezone is None:
            timezone = self.__format_metadata().get("timezone", "UTC")
        if "UTC+" in timezone or "GMT+" in timezone:
            timezone = "Etc/GMT-" + timezone.split("+")[-1].split(")")[0].split(":")[0]
        elif "UTC-" in timezone or "GMT-" in timezone:
            timezone = "Etc/GMT+" + timezone.split("-")[-1].split(")")[0].split(":")[0]
        try:
            self._tz = pytz.timezone(timezone)
        except UnknownTimeZoneError:
            self._tz = pytz.timezone("UTC")

    def __refresh_coverage(self):
        try:
            df = self._load_data_frame()
            self.__meta["dataCoverageFrom"] = df.index[0]
            self.__meta["dataCoverageUntil"] = df.index[-1]
            self.__fmt.writer.update_metadata(self.path, self.__format_metadata()["file"], self.metadata)
        except (EmptyDataError, IndexError):
            self.__meta["dataCoverageFrom"] = None
            self.__meta["dataCoverageUntil"] = None

    @property
    def coverage_from(self) -> Union[datetime, None]:
        if self.__meta["dataCoverageFrom"] is None:
            self.__refresh_coverage()
            if self.__meta["dataCoverageFrom"] is None:
                return None
        return pd.to_datetime(self.__meta["dataCoverageFrom"], utc=True).tz_convert(self._tz)

    @property
    def coverage_until(self) -> Union[datetime, None]:
        if self.__meta["dataCoverageUntil"] is None:
            self.__refresh_coverage()
            if self.__meta["dataCoverageUntil"] is None:
                return None
        return pd.to_datetime(self.__meta["dataCoverageUntil"], utc=True).tz_convert(self._tz)

    def _raw_metadata(self) -> Mapping[str, str]:
        return self.__meta

    def __format_metadata(self) -> Mapping[str, Any]:
        return self.__meta.get(list(self.__fmt.extensions)[0].upper(), {})

    def __file_path(self) -> str:
        pre_path = ""
        if self.__fmt.root_dir != "":
            pre_path = self.__fmt.root_dir + "/"
        return pre_path + self.path + "." + self.__format_metadata()["file"].rsplit(".", 1)[-1]

    def _load_data_frame(
        self,
        start: datetime = None,
        end: datetime = None,
        params: Mapping[str, str] = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
        _nrows: int = None,
    ) -> pd.DataFrame:

        format_metadata = self.__format_metadata()
        if _nrows is not None:
            format_metadata = format_metadata.copy()
            format_metadata["nrows"] = _nrows

        try:
            df = self.__fmt.reader.load_data_frame(
                columns=self.__meta.get("columns"),
                **format_metadata,
            )
        except (EmptyDataError, ValueError, FileNotFoundError):
            for meta in self.__fmt.reader._extract_metadata(self.__file_path()):
                if meta.get("tsPath", "") == self.path:
                    self.__meta = meta
                    self.__meta.setdefault("dataCoverageFrom", None)
                    self.__meta.setdefault("dataCoverageUntil", None)
            df = self.__fmt.reader.load_data_frame(columns=self.__meta.get("columns"), **format_metadata)

        if start is None and end is None:
            return df
        if start is None:
            mask = df.index <= end
        elif end is None:
            mask = df.index >= start
        else:
            mask = (df.index >= start) & (df.index <= end)
        return df.loc[mask]

    @classmethod
    def write_comments(cls, comments):
        logger.warning("write_comments not implemented. Ignoring {} comments".format(len(comments)))

    @classmethod
    def update_qualities(cls, qualities):
        logger.warning("update_qualities not implemented. Ignoring {} qualities".format(len(qualities)))

    def write_data_frame(
        self,
        data_frame: pd.DataFrame,
        start: datetime = None,
        end: datetime = None,
        **kwargs,
    ):
        data = self._aggregate_internal_data(data_frame, start, end)
        self.__fmt.writer.write(self.__file_path(), [data], start, end, [self.metadata])
        for meta in self.__fmt.reader._get_metadata(self.__file_path()):
            if meta.get("tsPath", "") == self.path:
                self.__meta = meta
                self.__meta.setdefault("dataCoverageFrom", None)
                self.__meta.setdefault("dataCoverageUntil", None)

    def _aggregate_internal_data(
        self,
        data_frame: pd.DataFrame,
        start: datetime = None,
        end: datetime = None,
        read_args: Mapping = None,
    ) -> pd.DataFrame:
        start = start if start is not None else data_frame.index[0]
        end = end if end is not None else data_frame.index[-1]
        read_args = {} if read_args is None else read_args
        try:
            data_inside = self.read_data_frame(**read_args)
        except EmptyDataError:
            data_inside = pd.DataFrame()
        except ValueError:
            # branch not found, just create a new time series branch
            data_inside = None
            data = data_frame

        if data_inside is not None:
            data = pd.concat(
                [
                    data_inside,
                    data_frame[~data_frame.index.isin(data_inside.index)],
                ],
                sort=False,
            )
            data.update(data_frame)
            data = data.reindex(data.index.sort_values())
            if data_frame.shape[0] == 0:
                mask = (start <= data.index) | (data.index <= end)
            else:
                mask = ((start <= data.index) & (data.index < data_frame.index[0])) | (
                    (data_frame.index[-1] < data.index) & (data.index <= end)
                )
            if data.index[mask].shape[0] > 0:
                data = data.drop(data.index[mask])
        return data

    @property
    def fmt(self) -> "TimeSeriesFormat":
        return self.__fmt

    @property
    def path(self) -> str:
        p = self._safe_meta("tsPath")
        sequence_id = self._safe_meta("_SEQUENCE_ID")
        if sequence_id is not None:
            p = f"{p}-{sequence_id}"
        return p


class FileEnsembleTimeSeries(FileTimeSeries):
    @property
    def _children(self) -> List[FileTimeSeries]:
        return self.__children

    @_children.setter
    def _children(self, values: List[FileTimeSeries]):
        self.__children = values

    @property
    def _file_path(self):
        # TODO: fix this weird file path determination
        pre_path = ""
        if self.fmt.root_dir != "":
            pre_path = self.fmt.root_dir + "/"
        return (
            pre_path
            + self.path.rsplit("-", maxsplit=1)[0]
            + "."
            + self.metadata[self.fmt.extensions[0].upper()]["file"].rsplit(".", 1)[-1]
        )

    @classmethod
    def from_timeseries_list(cls, ts_list: List[FileTimeSeries], ts_path=None):
        fmt = ts_list[0].fmt
        metadata = ts_list[0].metadata.copy()
        if ts_path is None:
            ts_path = metadata["tsPath"].rsplit("-", maxsplit=1)[0]
        metadata["tsPath"] = ts_path
        ts_ens = cls(meta=metadata, fmt=fmt)
        ts_ens._children = ts_list
        return ts_ens

    @staticmethod
    def __get_member_info(df):
        member = df["member"][0]
        try:
            t0 = df["timestamp"][0]
        except KeyError:
            t0 = df.index[0]
        try:
            dispatch_info = df["dispatchinfo"][0]
        except KeyError:
            try:
                dispatch_info = df["dispatch_info"][0]
            except KeyError:
                dispatch_info = None
        return member, t0, dispatch_info

    def read_ensemble_members(self, t0_start: datetime = None, t0_end: datetime = None) -> List[Mapping]:
        members = []
        for ts in self._children:
            member_df, t0_df, dispatch_info_df = self.__get_member_info(
                # Performance tweak: reading just one row instead of the
                # whole data frame is enough to get all the ensemble member
                # information.
                ts._load_data_frame(_nrows=1)
            )
            if t0_end is not None and t0_df >= t0_end or t0_start is not None and t0_df <= t0_start:
                continue
            branch_member = (member_df, t0_df, dispatch_info_df)
            members.append(branch_member)

            assert len(set(members)) == len(members), "This ensemble contains non-unique member branches."
        return [{"member": m, "t0": t, "dispatch_info": d} for m, t, d in members]

    def __find_branch(self, t0, dispatch_info, member):
        for ts in self._children:
            df = ts.read_data_frame()
            member_df, t0_df, dispatch_info_df = self.__get_member_info(df)
            if all([member_df == member, t0_df == t0, dispatch_info_df == dispatch_info]):
                return df, ts
        raise ValueError("Ensemble branch not found.")

    def _load_data_frame(
        self,
        start: datetime = None,
        end: datetime = None,
        params: Mapping[str, str] = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
        **kwargs,
    ):
        if valid_ensemble_args(t0, member, dispatch_info=dispatch_info):
            df, _ = self.__find_branch(t0, dispatch_info, member)
            if df.index.name == "timestamp":
                df[df.index.name] = df.index
                tz = df.index.tz
                df["forecast"] = pd.to_datetime(df["forecast"], format="%Y%m%d%H%M%S")
                df.set_index("forecast", inplace=True)
                df.index = df.index.tz_localize(tz)
            if start is None and end is None:
                return df
            if start is None:
                mask = df.index <= end
            elif end is None:
                mask = df.index >= start
            else:
                mask = (df.index >= start) & (df.index <= end)
            return df.loc[mask]
        else:
            return super()._load_data_frame(start, end, params, t0, dispatch_info, member)

    def write_data_frame(
        self,
        data_frame: pd.DataFrame,
        start: datetime = None,
        end: datetime = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
        **kwargs,
    ):
        if valid_ensemble_args(t0, member, dispatch_info=dispatch_info):
            self._write_ensemble_data_frame(data_frame, start, end, t0, dispatch_info, member)
        else:
            super().write_data_frame(data_frame, start, end)

    def _write_ensemble_data_frame(
        self,
        data_frame: pd.DataFrame,
        start: datetime = None,
        end: datetime = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
        **kwargs,
    ):
        member_branch = self.__get_member_info(data_frame)
        if member_branch != (member, t0, dispatch_info):
            raise ValueError(
                "The branch member defined by the input data frame must "
                "match t0, member, and dispatch_info."
            )
        data = self._aggregate_internal_data(
            data_frame,
            start,
            end,
            read_args={"t0": t0, "dispatch_info": dispatch_info, "member": member},
        )

        if data.index.name == "forecast":
            data = data.copy()
            data[data.index.name] = data.index
            data["forecast"] = data["forecast"].dt.strftime("%Y%m%d%H%M%S")
            data.set_index("timestamp", inplace=True)

        ts_all = list(self.fmt.reader.read(self._file_path))
        try:
            _, ts_child_branch = self.__find_branch(t0, dispatch_info, member)
        except ValueError:
            data_list = [ts.read_data_frame() for ts in ts_all] + [data]
            meta_list = [ts.metadata for ts in ts_all] + [self.metadata]
        else:
            ts_filtered = [ts for ts in ts_all if ts.path == ts_child_branch.path]
            assert len(ts_filtered) == 1
            data_list = [ts.read_data_frame() if ts.path != ts_child_branch.path else data for ts in ts_all]
            meta_list = [ts.metadata for ts in ts_all]

        for meta in meta_list:
            # NOTE: tsPath could've been created/or modified (i.e.
            # getting replaced by self.path) by the reader if the
            # the original data didn't have one or had a TSPATH that
            # was the same for all time series. Therefore we must revert
            # it back if needed by using the original raw metadata.
            meta["tsPath"] = self._safe_meta("tsPath")
        self.fmt.writer.write(self._file_path, data_list=data_list, meta_list=meta_list)

        ts_all = list(self.fmt.reader.read(self._file_path))
        new_children = [ts for ts in ts_all if ts.metadata["REXCHANGE"] == self.metadata["REXCHANGE"]]
        self._children = new_children

    def _raw_metadata(self) -> Mapping[str, str]:
        try:
            return self.__meta
        except AttributeError:
            return super()._raw_metadata()

    @property
    def path(self) -> str:
        p = self._safe_meta("tsPath")
        station = self._safe_meta("REXCHANGE")
        if station is not None:
            p = f"{p}-{station}"
        return p

    @property
    def coverage_from(self) -> Union[datetime, None]:
        return None

    @property
    def coverage_until(self) -> Union[datetime, None]:
        return None

import json
import logging
from collections import namedtuple
from datetime import datetime
from typing import Any, Iterable, List, Mapping, Tuple

import numpy as np
import pandas as pd
from requests import HTTPError

from kisters.water.time_series.core.entity import Entity
from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_decorator import TimeSeriesDecorator
from kisters.water.time_series.core.time_series_store import TimeSeriesStore

CommitData = namedtuple("CommitData", ["df", "start", "end", "quality"])
CommitComments = namedtuple("CommitComments", ["df", "category"])
LOG = logging.getLogger(__name__)


class _CacheTimeSeries(TimeSeriesDecorator):
    def __init__(self, forward: TimeSeries):
        super().__init__(forward)
        self._data = None
        self._comments = None
        self._commit_cache_data: List[CommitData] = []
        self._commit_cache_comments: List[CommitComments] = []
        self._commit_cache_drop_comments: List[int] = []

    def _load_data_frame(
        self,
        start: datetime = None,
        end: datetime = None,
        params: Mapping = None,
        **kwargs,
    ) -> pd.DataFrame:
        if self._data is None or self._data.shape[0] == 0:
            self._data = self._forward.read_data_frame(start, end, params=params, **kwargs)
            return self._data.copy()

        dates = self._data.index
        if start < dates[0]:
            df = self._forward.read_data_frame(start, dates[0], params=params, **kwargs)
            self._data = pd.concat([df[~df.index.isin(self._data.index)], self._data])
        if end > dates[-1]:
            df = self._forward.read_data_frame(dates[-1], end, params=params, **kwargs)
            self._data = pd.concat([self._data, df[~df.index.isin(self._data.index)]])

        if start is None and end is None:
            return self._data.copy()
        if start is None:
            return self._data.loc[self._data.index <= end].copy()
        elif end is None:
            return self._data.loc[self._data.index >= start].copy()
        else:
            return self._data.loc[(self._data.index >= start) & (self._data.index <= end)].copy()

    def __remove_gaps(self, data_frame: pd.DataFrame, start: datetime, end: datetime):
        if start is not None and start < data_frame.index[0]:
            if start <= self._data.index[0]:
                self._data.drop(self._data.index[self._data.index < data_frame.index[0]])
            else:
                self._data.loc[
                    (start <= self._data.index) & (self._data.index < data_frame.index[0]),
                    :,
                ] = np.nan
        if end is not None and end > data_frame.index[-1]:
            if end >= self._data.index[-1]:
                self._data.drop(self._data.index[self._data.index > data_frame.index[-1]])
            else:
                self._data.loc[
                    (data_frame.index[-1] < self._data.index) & (self._data.index <= end),
                    :,
                ] = np.nan

    @classmethod
    def __aggregate_commit_data(cls, commit_data, df_aux, aux_start, aux_end):
        remove_index = False
        if df_aux.index[0] <= commit_data.df.index[0] and df_aux.index[-1] >= commit_data.df.index[-1]:
            return True, df_aux
        if (
            df_aux.index[0] <= commit_data.df.index[0] <= df_aux.index[-1]
            or df_aux.index[0] <= commit_data.df.index[-1] <= df_aux.index[-1]
            or (df_aux.index[0] > commit_data.df.index[0] and df_aux.index[-1] < commit_data.df.index[-1])
        ):
            df_aux = pd.concat(
                [df_aux, commit_data.df[~commit_data.df.index.isin(df_aux.index)]],
                sort=False,
            )
            df_aux = df_aux.reindex(df_aux.index.sort_values())
        return remove_index, df_aux

    def __update_commit_data(self, data_frame: pd.DataFrame, start: datetime, end: datetime):
        aux_start = start if start is not None else data_frame.index[0]
        aux_end = end if end is not None else data_frame.index[-1]
        df_aux = data_frame
        indices_to_remove = []
        for i, commit_data in enumerate(c for c in self._commit_cache_data if not c.quality):
            remove_index, df_aux = self.__aggregate_commit_data(commit_data, df_aux, aux_start, aux_end)
            if remove_index:
                indices_to_remove.append(i)
                aux_start = aux_start if aux_start <= commit_data.start else commit_data.start
                aux_end = aux_end if aux_end >= commit_data.end else commit_data.end

        for i in indices_to_remove:
            del self._commit_cache_data[i]
        self._commit_cache_data.append(CommitData(df_aux, aux_start, aux_end, False))

    def write_data_frame(self, data_frame: pd.DataFrame, start: datetime = None, end: datetime = None):
        mask = None
        if start is not None:
            mask = data_frame.index >= start
        if end is not None:
            mask = data_frame.index <= end if mask is None else mask & (data_frame.index <= end)
        if mask is not None:
            data_frame = data_frame.loc[mask]

        if data_frame.index.tz is None:
            data_frame.index = data_frame.index.tz_localize(self._tz)
        else:
            data_frame.index = data_frame.index.tz_convert(self._tz)
        self._load_data_frame(data_frame.index[0], data_frame.index[-1])
        self._data = pd.concat(
            [self._data, data_frame[~data_frame.index.isin(self._data.index)]],
            sort=False,
        )
        self._data.update(data_frame)
        self._data = self._data.reindex(self._data.index.sort_values())
        if start is not None or end is not None:
            self.__remove_gaps(data_frame, start, end)
        self.__update_commit_data(data_frame, start, end)

    def __first_comment(self) -> datetime:
        date = None
        for _i, row in self._comments.iterrows():
            if date is None:
                date = row.loc["from"]
            date = row.loc["from"] if row.loc["from"] < date else date
        return date

    def __last_comment(self) -> datetime:
        date = None
        for _i, row in self._comments.iterrows():
            if date is None:
                date = row.loc["until"]
            date = row.loc["until"] if row.loc["until"] > date else date
        return date

    def __initialize_comments(self, start: datetime, end: datetime):
        if hasattr(self._forward, "get_comments"):
            self._comments = self._forward.get_comments(start, end)
            self._comments["from"] = pd.to_datetime(self._comments["from"], utc=True)
            self._comments["until"] = pd.to_datetime(self._comments["until"], utc=True)
        else:
            self._comments = pd.DataFrame(columns=["from", "until", "comment"])

    def __retrieve_and_update_comments(self, start: datetime, end: datetime):
        first_comment = self.__first_comment()
        last_comment = self.__last_comment()
        if start < first_comment and hasattr(self._forward, "get_comments"):
            self.write_comments(self._forward.get_comments(start, first_comment))
        if end > last_comment and hasattr(self._forward, "get_comments"):
            self.write_comments(self._forward.get_comments(end, last_comment))

    def __filter_comments(self, start: datetime, end: datetime) -> pd.DataFrame:
        comments = self._comments.copy()
        for i, row in comments.iterrows():
            if end < row.loc["from"] or row.loc["until"] < start:
                comments = comments.drop(i)
            else:
                if row.loc["from"] < start:
                    comments.loc[i, "from"] = start
                if row.loc["until"] > end:
                    comments.loc[i, "until"] = end
        return comments

    def get_comments(self, start: datetime = None, end: datetime = None) -> pd.DataFrame:
        start = self._to_zoned_datetime(start)
        end = self._to_zoned_datetime(end)
        if self._comments is None:
            self.__initialize_comments(start, end)
            return self._comments.copy()
        if self._comments.shape[0] == 0:
            return self._comments.copy()

        if start is None:
            start = self.coverage_from
        if end is None:
            end = self.coverage_until
        self.__retrieve_and_update_comments(start, end)
        return self.__filter_comments(start, end)

    def __merge_comments_helper(self, comments: pd.DataFrame, i: int, row: pd.Series, row_: pd.Series):
        merge_status = "noop"
        if row.loc["comment"] == row_.loc["comment"]:
            if row.loc["from"] > row_.loc["from"] and row.loc["until"] < row_.loc["until"]:
                merge_status = "drop"
                row.loc["from"] = row_.loc["from"]
                row.loc["until"] = row_.loc["until"]
            else:
                if row.loc["from"] <= row_.loc["from"] <= row.loc["until"]:
                    merge_status = "aggregated"
                    comments, row = self._aggregate_comment(comments, i, row, row_, True)
                    self._add_cache_comment_drop(row_)
                if row.loc["until"] >= row_.loc["until"] >= row.loc["from"]:
                    merge_status = "aggregated"
                    comments, row = self._aggregate_comment(comments, i, row, row_, False)
                    self._add_cache_comment_drop(row_)
        return merge_status, comments, row

    @staticmethod
    def _aggregate_comment(comments: pd.DataFrame, i: int, row: pd.Series, row_: pd.Series, is_until: bool):
        if is_until and row_.loc["until"] > row.loc["until"]:
            comments.loc[i, "until"] = row_["until"]
            row.loc["until"] = row_["until"]
        elif row_.loc["from"] < row.loc["from"]:
            comments.loc[i, "from"] = row_["from"]
            row.loc["from"] = row_["from"]
        return comments, row

    def _add_cache_comment_drop(self, row: pd.Series):
        try:
            self._commit_cache_drop_comments.append(row.loc["id"])
        except KeyError:
            LOG.warning("Cannot drop comment without id")

    def write_comments(self, comments: pd.DataFrame, category: int = None):
        if self._comments is None or self._comments.shape[0] == 0:
            self._comments = comments
        else:
            comments, drop_list, drop_aggregated_list = self._process_comment_merging(comments)
            comments = comments.drop(drop_list)
            self._comments = self._comments.drop(drop_aggregated_list)
            self._comments = pd.concat([self._comments, comments], ignore_index=True, sort=False)
        if comments.shape[0] > 0:
            self._commit_cache_comments.append(CommitComments(comments, category))

    def _process_comment_merging(self, comments: pd.DataFrame):
        drop_list = []
        drop_aggregated_list = []
        for i, row in comments.iterrows():
            included_index = False
            for i_, row_ in self._comments.iterrows():
                merge_status, comments, row = self.__merge_comments_helper(comments, i, row, row_)
                if merge_status == "drop":
                    included_index = True
                elif merge_status == "aggregated":
                    drop_aggregated_list.append(i_)
            if included_index:
                drop_list.append(i)
        return comments, drop_list, drop_aggregated_list

    def update_qualities(self, qualities: pd.DataFrame):
        self.read_data_frame(qualities.index[0], qualities.index[-1])
        q_col = list(qualities.columns)[0]
        column_list = list(self._data.columns)
        if q_col not in column_list:
            q_col_name = "quality"
            for col in column_list:
                if "qualit" in col:
                    q_col_name = col
            qualities = qualities.rename(index=str, columns={q_col: q_col_name})
        self._data.update(qualities)
        self._commit_cache_data.append(CommitData(qualities, None, None, True))

    def read_data_frame_with_comments(self, start: datetime = None, end: datetime = None):
        df = self.read_data_frame(start, end)
        comments = self.get_comments(start, end)
        df["comment"] = pd.Series([""] * df.shape[0], index=df.index)
        for _i, row in comments.iterrows():
            df.loc[(row.loc["from"] <= df.index) & (df.index <= row.loc["until"]), ["comment"]] = df[
                "comment"
            ].map(lambda x: row.loc["comment"] if x == "" else x + ", " + row.loc["comment"])
        return df

    # TODO consider keep failed commits
    def commit_changes(self):
        self._commit_data()
        self._commit_comments()

    def _commit_data(self):
        for commit in self._commit_cache_data:
            if commit.quality:
                try:
                    self._forward.update_qualities(commit.df)
                except (AttributeError, NotImplementedError, HTTPError):
                    LOG.exception(
                        "Commit wasn't totally completed, "
                        "failed to write the qualities for {}".format(self._forward)
                    )
            else:
                try:
                    super().write_data_frame(commit.df, commit.start, commit.end)
                except (HTTPError, RuntimeError):
                    LOG.exception(
                        "Commit wasn't totally completed, "
                        "failed to write data for {}".format(self._forward)
                    )
        self._commit_cache_data: List[CommitData] = []

    def _commit_comments(self):
        for drop in self._commit_cache_drop_comments:
            try:
                self._forward.remove_comment(drop)
            except (AttributeError, NotImplementedError, HTTPError):
                LOG.exception(
                    "Commit wasn't totally completed, "
                    f"failed to drop remarkId {drop} for {self._forward}"
                )
        for comments in self._commit_cache_comments:
            if comments.category is not None:
                params = {"comments": comments.df, "category": comments.category}
            else:
                params = {"comments": comments.df}
            try:
                self._forward.write_comments(**params)
            except (AttributeError, NotImplementedError, HTTPError):
                LOG.exception(
                    "Commit wasn't totally completed, "
                    "failed to write the comments for {}".format(self._forward)
                )
        self._commit_cache_comments: List[CommitComments] = []
        self._commit_cache_drop_comments: List[int] = []


class CacheStore(TimeSeriesStore):
    """
    CacheStore is a TimeSeriesStore decorator which allows to cache the retrieval of
    TimeSeries inside the original TimeSeriesStore. Also TimeSeries retrieved this way
    cache the data they contain in memory.

    Args:
        forward: The TimeSeriesStore to be decorated.

    Example:
        .. code-block:: python

            from kisters.water.file_io import FileStore, ZRXPFormat
            from kisters.water.store_decorators import CacheStore
            store = CacheStore(FileStore('tests/data', ZRXPFormat()))
            ts = store.get_by_path('validation/threshold/05BJ004.HG.datum.O')
    """

    def __init__(self, forward: TimeSeriesStore):
        self._forward = forward

    def _get_time_series_list(
        self,
        ts_filter: str = None,
        id_list: Iterable[int] = None,
        params: Mapping[str, Any] = None,
    ) -> Iterable[TimeSeries]:
        if ts_filter is None:
            ts_filter = False
        if id_list is None:
            id_list = False
        else:
            id_list = tuple(id_list)
        if params is None:
            params = {}
        json_params = json.dumps(params)
        return [
            _CacheTimeSeries(ts)
            for ts in self.__get_cacheable_time_series_list(ts_filter, id_list, json_params)
        ]

    def __get_cacheable_time_series_list(
        self, ts_filter: str, id_list: Tuple[int], json_params: str
    ) -> Iterable[TimeSeries]:
        if not ts_filter:
            ts_filter = None
        if not id_list:
            id_list = None
        params = json.loads(json_params)
        return self._forward._get_time_series_list(ts_filter, id_list, params)

    def _get_time_series(
        self, ts_id: int = None, path: str = None, params: Mapping[str, Any] = None
    ) -> TimeSeries:
        if ts_id is None:
            ts_id = False
        if path is None:
            path = False
        if params is None:
            params = {}
        json_params = json.dumps(params)
        return _CacheTimeSeries(self.__get_cacheable_time_series(ts_id, path, json_params))

    def __get_cacheable_time_series(self, ts_id: int, path: str, json_params: str) -> TimeSeries:
        params = json.loads(json_params)
        if not ts_id:
            ts_id = None
        if not path:
            path = None
        return self._forward._get_time_series(ts_id, path, params)

    def create_time_series(
        self,
        path: str,
        display_name: str,
        attributes: Mapping = None,
        params: Mapping[str, Any] = None,
    ) -> TimeSeries:
        return self._forward.create_time_series(path, display_name, attributes, params)

    def get_entity_list(
        self, entity_filter: str = None, entities_id: Iterable[int] = None, **kwargs
    ) -> Iterable[Entity]:
        return self._forward.get_entity_list(entity_filter, entities_id, **kwargs)

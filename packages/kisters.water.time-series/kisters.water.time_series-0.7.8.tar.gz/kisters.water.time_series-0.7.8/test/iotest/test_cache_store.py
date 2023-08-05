import os
import unittest
from datetime import datetime
from typing import TYPE_CHECKING

import pandas as pd

from kisters.water.time_series.file_io import FileStore, ZRXPFormat
from kisters.water.time_series.store_decorators import CacheStore

if TYPE_CHECKING:
    from kisters.water.time_series.store_decorators.cache_store import _CacheTimeSeries


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.store = CacheStore(
            FileStore(os.path.join(os.path.dirname(__file__), "..", "data"), ZRXPFormat())
        )

    def test_cache_store(self):
        fb = self.store

        ts_list = list(fb.get_by_filter(ts_filter="*"))
        self.assertGreater(len(ts_list), 0)
        pd.DataFrame([ts.metadata for ts in ts_list])
        self.assertIsNotNone(ts_list[0])
        ts = ts_list[1]
        self.assertIsNotNone(ts.name)

        ts_list = list(fb.get_by_filter(ts_filter="*05*"))
        self.assertGreater(len(ts_list), 0)
        pd.DataFrame([ts.metadata for ts in ts_list])

        ts_list2 = fb.get_by_id(ts_id=[ts_list[0].id, ts_list[1].id])
        pd.DataFrame([ts.metadata for ts in ts_list2])

        ts_list = list(fb.get_by_filter(ts_filter="in*/05*"))
        self.assertGreater(len(list(ts_list)), 0)
        pd.DataFrame([ts.metadata for ts in ts_list])
        ts = ts_list[0]

        start = datetime(2001, 1, 1)
        end = datetime(2001, 2, 1)

        df = ts.read_data_frame(start=start, end=end)
        self.assertIsNotNone(df)

    def test_ts_get_item(self):
        _iter = iter(self.store.get_by_filter("inside/05BJ004.HG.nrt.O"))
        self.assertIsNotNone(_iter)
        ts = next(_iter)
        df = ts["2001-02-03":"2003-04-05"]
        self.assertIsNotNone(df)

    def test_storage_get_item(self):
        ts = self.store["inside/05BJ004.HG.nrt.O"]
        self.assertTrue(ts)

    def test_get_item(self):
        df = self.store["inside/05BJ004.HG.nrt.O"]["2001-02-03":"2003-04-05"]
        self.assertIsNotNone(df)

    def test_multiple_reads(self):
        ts: "_CacheTimeSeries" = self.store.get_by_path("inside/05BJ004.HG.nrt.O")
        ts.read_data_frame(datetime(1999, 11, 1), datetime(1999, 11, 2))
        ts.read_data_frame(datetime(1999, 10, 31), datetime(1999, 11, 3))
        self.assertEqual(len(ts._data), 36)

    def test_write(self):
        ts: "_CacheTimeSeries" = self.store.get_by_path("inside/05BJ004.HG.nrt.O")
        df = pd.DataFrame(
            {
                "value": [0.666, 0.666, 0.666],
                "value.interpolation": [9, 9, 9],
                "value.quality": [300, 300, 300],
            }
        )

        index = pd.to_datetime(["1980-01-01", "1999-11-02T22:00+00:00", "2005-03-01"], utc=True)
        df = df.set_index(index)
        size = ts.read_data_frame(datetime(1980, 1, 1), datetime(2005, 3, 1)).shape[0]
        ts.write_data_frame(df)
        self.assertEqual(len(ts._data), size + 2)

    def test_update_qualities(self):
        ts: "_CacheTimeSeries" = self.store.get_by_path("inside/05BJ004.HG.nrt.O")
        df = pd.DataFrame({"value.quality": [300, 300, 300]})

        index = pd.to_datetime(
            [
                "1999-11-02T21:00+00:00",
                "1999-11-02T22:00+00:00",
                "1999-11-02T23:00+00:00",
            ],
            utc=True,
        )
        df = df.set_index(index)
        ts.update_qualities(df)
        qualities = ts._data.loc[index, "value.quality"].values
        self.assertTrue(qualities[qualities == 300].all())

    def test_write_comments(self):
        ts: "_CacheTimeSeries" = self.store.get_by_path("inside/05BJ004.HG.nrt.O")
        comments1 = pd.DataFrame(
            {
                "from": pd.to_datetime(["1999-11-01T00:00", "1999-10-31T00:00", "1999-11-02T00:00"]),
                "until": pd.to_datetime(["1999-11-01T22:00", "1999-11-01T00:00", "1999-11-03T00:00"]),
                "comment": ["a", "b", "c"],
            }
        )
        ts.write_comments(comments1)
        comments2 = pd.DataFrame(
            {
                "from": pd.to_datetime(["1999-11-01T00:00", "1999-11-01T00:00", "1999-10-31T00:00"]),
                "until": pd.to_datetime(["1999-11-01T22:00", "1999-11-02T00:00", "1999-11-02T00:00"]),
                "comment": ["d", "b", "c"],
            }
        )
        ts.write_comments(comments2)

        self.assertEqual(ts._comments.shape[0], 4)
        comment_b = ts._comments.loc[ts._comments.comment == "b", ["from", "until"]]
        comment_c = ts._comments.loc[ts._comments.comment == "c", ["from", "until"]]
        self.assertEqual(
            comment_b["from"].values[0],
            comments1.loc[comments1.comment == "b", "from"].values,
        )
        self.assertEqual(
            comment_b["until"].values[0],
            comments2.loc[comments2.comment == "b", "until"].values[0],
        )
        self.assertEqual(
            comment_c["from"].values[0],
            comments2.loc[comments2.comment == "c", "from"].values[0],
        )
        self.assertEqual(
            comment_c["until"].values[0],
            comments1.loc[comments1.comment == "c", "until"].values[0],
        )

    def test_commit_changes(self):
        ts: "_CacheTimeSeries" = self.store.get_by_path("inside/CacheCommitTest.HG.nrt.O")
        df = pd.DataFrame(
            {
                "value": [0.666, 0.666, 0.666],
                "value.interpolation": [9, 9, 9],
                "value.quality": [300, 300, 300],
            }
        )

        index = pd.to_datetime(["1980-01-01", "1999-11-02T22:00", "2005-03-01"])
        df = df.set_index(index)
        ts.write_data_frame(df)
        qualities = pd.DataFrame({"value.quality": [100, 100, 100]})

        index = pd.to_datetime(["1999-11-02T21:00", "1999-11-02T22:00", "1999-11-02T23:00"])
        qualities = qualities.set_index(index)
        ts.update_qualities(qualities)
        comments1 = pd.DataFrame(
            {
                "from": pd.to_datetime(["1999-11-01T00:00", "1999-10-31T00:00", "1999-11-02T00:00"]),
                "until": pd.to_datetime(["1999-11-01T22:00", "1999-11-01T00:00", "1999-11-03T00:00"]),
                "comment": ["a", "b", "c"],
            }
        )
        ts.write_comments(comments1)
        ts.commit_changes()

    def test_write_from_store(self):
        ts = self.store.get_by_path("inside/CacheCommitTest.HG.nrt.O")
        df = pd.DataFrame(
            {
                "value": [0.666, 0.666, 0.666],
                "value.interpolation": [9, 9, 9],
                "value.quality": [300, 300, 300],
            }
        )

        index = pd.to_datetime(["1980-01-01", "1980-01-01T05:00", "1980-01-01T10:00"])
        df = df.set_index(index)
        ts.write_data_frame(df)
        start = datetime(1980, 1, 1)
        end = datetime(1980, 1, 1, 10)
        ts2 = self.store.write_time_series(ts, start, end)
        self.assertTrue(ts.read_data_frame(start, end).equals(ts2.read_data_frame(start, end)))

    def test_read_data_frames(self):
        ts_list = list(self.store.get_by_filter(ts_filter="*"))
        self.assertGreater(len(ts_list), 0)
        ts_dfs = self.store.read_data_frames(ts_list)
        self.assertGreater(len(ts_dfs), 0)
        self.assertEqual(len(ts_dfs), len(ts_list))


if __name__ == "__main__":
    unittest.main()

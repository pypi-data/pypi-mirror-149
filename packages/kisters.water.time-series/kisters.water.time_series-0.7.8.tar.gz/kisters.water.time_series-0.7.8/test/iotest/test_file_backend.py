import os
import unittest
from datetime import datetime

from pandas import DataFrame

from kisters.water.time_series.file_io import FileStore, ZRXPFormat


class Test(unittest.TestCase):
    def setUp(self):
        self.fb = FileStore(os.path.join(os.path.dirname(__file__), "..", "data"), ZRXPFormat())

    def testFileStore(self):
        fb = self.fb
        fl = fb._file_list("data")
        self.assertIsNotNone(fl)

        ts_list = list(fb.get_by_filter(ts_filter="*"))
        self.assertGreater(len(ts_list), 0)
        DataFrame([ts.metadata for ts in ts_list])
        self.assertIsNotNone(ts_list[0])
        ts = ts_list[1]
        self.assertIsNotNone(ts.name)

        ts_list = list(fb.get_by_filter(ts_filter="*05*"))
        self.assertGreater(len(ts_list), 0)
        DataFrame([ts.metadata for ts in ts_list])

        ts_list2 = fb.get_by_id(ts_id=[ts_list[0].id, ts_list[1].id])
        DataFrame([ts.metadata for ts in ts_list2])

        ts_list = list(fb.get_by_filter(ts_filter="in*/05*"))
        self.assertGreater(len(list(ts_list)), 0)
        DataFrame([ts.metadata for ts in ts_list])
        ts = ts_list[0]

        start = datetime(2001, 1, 1)
        end = datetime(2001, 2, 1)

        df = ts.read_data_frame(start=start, end=end)
        self.assertIsNotNone(df)

    def test_ts_get_item(self):
        _iter = iter(self.fb.get_by_filter("inside/05BJ004.HG.nrt.O"))
        self.assertIsNotNone(_iter)
        ts = next(_iter)
        df = ts["2001-02-03":"2003-04-05"]
        self.assertIsNotNone(df)

    def test_storage_get_item(self):
        ts = self.fb["inside/05BJ004.HG.nrt.O"]
        self.assertTrue(ts)

    def test_get_item_slice(self):
        df = self.fb["inside/05BJ004.HG.nrt.O"]["2001-02-03":"2003-04-05"]
        self.assertIsNotNone(df)

    def test_get_item(self):
        df = self.fb["inside/05BJ004.HG.nrt.O"]["2001-02-03"]
        self.assertIsNotNone(df)

    def test_get_item_not_supported(self):
        with self.assertRaises(ValueError):
            self.fb["inside/05BJ004.HG.nrt.O"][5]

    def test_value_error_path_leading_slash(self):
        with self.assertRaises(ValueError):
            self.fb.get_by_path("/inside/05BJ004.HG.nrt.O")

    def test_value_error_filter_leading_slash(self):
        with self.assertRaises(ValueError):
            self.fb.get_by_filter("/inside/05BJ004.HG.nrt.O")

    def test_create_empty_ts(self):
        self.fb.create_time_series("my/new/ts", "My new TimeSeries")
        path = os.path.join(os.path.dirname(__file__), "../data/my/new/ts.zrx")
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.exists(path + ".metadata"))
        os.remove(path)
        os.remove(path + ".metadata")

    def test_create_and_copy_ts(self):
        ts = self.fb.get_by_path("inside/05BJ004.HG.nrt.O")
        self.fb.create_time_series_from(copy_from=ts, new_path="my_copy")
        my_copy = self.fb.get_by_path("my_copy")
        my_copy.write_data_frame(ts.read_data_frame())
        self.assertEqual(ts.read_data_frame().shape[0], my_copy.read_data_frame().shape[0])

    def test_read_data_frames(self):
        ts_list = list(self.fb.get_by_filter(ts_filter="*"))
        self.assertGreater(len(ts_list), 0)
        ts_dfs = self.fb.read_data_frames(ts_list)
        self.assertGreater(len(ts_dfs), 0)
        self.assertEqual(len(ts_dfs), len(ts_list))


if __name__ == "__main__":
    unittest.main()

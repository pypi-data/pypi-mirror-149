import os
import unittest
from datetime import datetime

from kisters.water.time_series.file_io import CSVFormat, FileStore, ZRXPFormat


class Test(unittest.TestCase):
    def setUp(self):
        self.csv = CSVFormat()
        self.zrxp = ZRXPFormat()
        self.zrxpreader = self.zrxp.reader
        self.csvreader = self.csv.reader
        self.csvwriter = self.csv.writer
        self.testdatadir = os.path.dirname(__file__)

    def testWrite(self):
        ts_list = self.zrxpreader.read(
            os.path.join(self.testdatadir, "../data/inside/05BJ004.HG.nrt.O.zrx")
        )
        self.csvwriter.write(os.path.join(self.testdatadir, "../data/testoutput.csv"), ts_list)
        ts = list(self.csvreader.read(os.path.join(self.testdatadir, "../data/testoutput.csv")))[0]
        df = ts.read_data_frame()
        df["value"] = 2
        ts.write_data_frame(df)
        df2 = ts.read_data_frame()
        self.assertTrue(df["value.quality"].equals(df2["value.quality"]))

    def testRead(self):
        ts_list = list(
            self.zrxpreader.read(os.path.join(self.testdatadir, "../data/inside/05BJ004.HG.nrt.O.zrx"))
        )
        l = len(ts_list[0].read_data_frame())
        self.csvwriter.write(os.path.join(self.testdatadir, "../data/testoutput.csv"), ts_list)
        ts_list = list(self.csvreader.read(os.path.join(self.testdatadir, "../data/testoutput.csv")))
        self.assertEqual(len(list(ts_list)), 1)
        df = ts_list[0].read_data_frame()
        self.assertEqual(l, len(df))

        date = df.index[0]
        f = df["value"][0]
        self.assertIsInstance(date, datetime)
        self.assertIsInstance(f, float)

    def test_file_store_create(self):
        fs = FileStore(os.path.join(os.path.dirname(__file__), "../data"), CSVFormat())
        fs.create_time_series("my/new/ts", "My new TimeSeries")
        path = os.path.join(os.path.dirname(__file__), "../data/my/new/ts.csv")
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.exists(path + ".metadata"))
        os.remove(path)
        os.remove(path + ".metadata")


if __name__ == "__main__":
    unittest.main()

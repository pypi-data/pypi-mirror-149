import os
import unittest
from datetime import datetime

from kisters.water.time_series.file_io import PickleFormat, ZRXPFormat


class Test(unittest.TestCase):
    def setUp(self):
        self.pickle = PickleFormat()
        self.zrxp = ZRXPFormat()
        self.zrxpreader = self.zrxp.reader
        self.picklereader = self.pickle.reader
        self.picklewriter = self.pickle.writer
        self.testdatadir = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def testWrite(self):
        tslist = self.zrxpreader.read(os.path.join(self.testdatadir, "../data/inside/05BJ004.HG.nrt.O.zrx"))
        self.picklewriter.write(os.path.join(self.testdatadir, "../data/testoutput.pkl"), tslist)

    def testRead(self):
        ts_list = list(
            self.zrxpreader.read(os.path.join(self.testdatadir, "../data/inside/05BJ004.HG.nrt.O.zrx"))
        )
        ts_df = ts_list[0].read_data_frame()
        self.picklewriter.write(os.path.join(self.testdatadir, "../data/testoutput.pkl"), ts_list)
        ts_list = list(self.picklereader.read(os.path.join(self.testdatadir, "../data/testoutput.pkl")))
        self.assertEqual(len(ts_list), 1)
        df = ts_list[0].read_data_frame()
        self.assertEqual(len(ts_df), len(df))

        date = df.index[0]
        f = df["value"][0]
        self.assertIsInstance(date, datetime)
        self.assertIsInstance(f, float)


if __name__ == "__main__":
    unittest.main()

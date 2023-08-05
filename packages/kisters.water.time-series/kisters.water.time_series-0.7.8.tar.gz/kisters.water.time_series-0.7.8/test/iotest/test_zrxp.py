import os
import shutil
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from kisters.water.time_series.file_io import FileStore
from kisters.water.time_series.file_io.file_time_series import FileEnsembleTimeSeries
from kisters.water.time_series.file_io.zrxp_format import ZRXPFormat


class Test(unittest.TestCase):
    def setUp(self):
        self.zrxp = ZRXPFormat()
        self.reader = self.zrxp.reader
        self.writer = self.zrxp.writer
        self.testdatadir = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def testName(self):
        tslist = list(
            self.reader.read(os.path.join(os.path.dirname(__file__), "../data/inside/05BJ004.HG.nrt.O.zrx"))
        )
        self.assertGreater(len(DataFrame([ts.metadata for ts in tslist])), 0)

        self.assertGreater(len(tslist[0].metadata), 0)

        ts = tslist[0]

        self.assertEqual(ts.name, "05BJ004.HG.nrt.O")

        start = datetime(2001, 1, 1)
        end = datetime(2001, 2, 1)

        df = ts.read_data_frame(start=start, end=end)
        self.assertIsNotNone(df)

    def testlayout(self):
        tslist = list(self.reader.read(os.path.join(os.path.dirname(__file__), "../data/testlayout.zrx")))
        df = tslist[0].read_data_frame()
        cols = df.columns.values
        self.assertEqual(len(cols), 2)
        self.assertEqual("value", cols[0])
        self.assertEqual("value.quality", cols[1])

    def testnolayout(self):
        tslist = list(self.reader.read(os.path.join(os.path.dirname(__file__), "../data/testnolayout.zrx")))
        df = tslist[0].read_data_frame()
        cols = df.columns.values
        self.assertEqual(len(cols), 1)
        self.assertEqual("value", cols[0])

    def testWrite(self):
        tslist = self.reader.read(os.path.join(self.testdatadir, "../data/inside/05BJ004.HG.nrt.O.zrx"))
        self.writer.write(os.path.join(self.testdatadir, "../data/testoutput.zrxp"), tslist)

    def test_read_zrxp_multiple_spaces(self):
        list(self.reader.read(os.path.join(self.testdatadir, "../data/testwhitespaces.zrxp")))[
            0
        ].read_data_frame()


class TestEnsembleRead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # setup temp dir
        testdatadir_src = Path(__file__).parent / "../data"
        cls.testdatadir = tempfile.TemporaryDirectory()
        cls.testdatadirpath = cls.testdatadir.name
        shutil.copy(testdatadir_src / "multi_ensemble_ts.zrx", cls.testdatadirpath)
        # setup zrxp machinery
        cls.fs = FileStore(cls.testdatadirpath, ZRXPFormat())

    @classmethod
    def tearDownClass(cls):
        cls.testdatadir.cleanup()

    def test_read_zrxp_multiple_ts(self):
        """Test reading all time series in a multi ensemble file, with no
        grouping by ensemble branches"""
        zrxp = ZRXPFormat()
        reader = zrxp.reader
        ts_list = list(reader.read(os.path.join(self.testdatadirpath, "multi_ensemble_ts.zrx")))
        self.assertEqual(len(ts_list), 150)
        for ts in ts_list:
            self.assertIsNotNone(ts)
            df = ts.read_data_frame()
            self.assertIsNotNone(df)
            self.assertGreater(df.shape[0], 0)
            self.assertEqual(len(df), 15)

    def test_read_ensemble_ts(self):
        """
        Test retrieving an ensemble branch by its generated tsPath, which
        in this case consists of a file path and a station identifier.
        """
        ts = self.fs.get_by_path("multi_ensemble_ts-6290_ENSRRR24")
        self.assertIsInstance(ts, FileEnsembleTimeSeries)

    def test_read_ensemble_members(self):
        """Test reading branch member information."""
        ts = self.fs.get_by_path("multi_ensemble_ts-6290_ENSRRR24")
        branch_members = ts.read_ensemble_members()
        self.assertEqual(3, len(branch_members))
        members = {d["member"] for d in branch_members}
        self.assertEqual({"AVG", "P90", "P10"}, members)
        t0 = {d["t0"] for d in branch_members}
        self.assertEqual({pd.Timestamp("2019-04-29", tz="UTC")}, t0)
        dispatch_info = {d["dispatch_info"] for d in branch_members}
        self.assertEqual({None}, dispatch_info)

    def test_read_ensemble_ts_data_frame(self):
        ts = self.fs.get_by_path("multi_ensemble_ts-6290_ENSRRR24")
        branch_members = ts.read_ensemble_members()
        for branch in branch_members:
            member = branch["member"]
            t0 = branch["t0"]
            dispatch_info = branch["dispatch_info"]
            df = ts.read_data_frame(member=member, t0=t0, dispatch_info=dispatch_info)
            self.assertEqual(15, len(df))
            self.assertEqual(member, df["member"][0])
            self.assertEqual(t0, df["timestamp"][0])
            self.assertEqual("forecast", df.index.name)

    def test_read_ensemble_ts_data_frame_failures(self):
        ts = self.fs.get_by_path("multi_ensemble_ts-6290_ENSRRR24")
        self.assertIsNotNone(
            ts.read_data_frame(
                member="AVG",
                t0=pd.Timestamp("2019-04-29", tz="UTC"),
                dispatch_info=None,
            )
        )
        with self.assertRaises(ValueError):
            ts.read_data_frame(
                member="AVGAAA",
                t0=pd.Timestamp("2019-04-29", tz="UTC"),
                dispatch_info=None,
            )
        with self.assertRaises(ValueError):
            ts.read_data_frame(
                member="AVG",
                t0=pd.Timestamp("2019-06-29", tz="UTC"),
                dispatch_info=None,
            )
        with self.assertRaises(ValueError):
            ts.read_data_frame(
                member="AVG",
                t0=pd.Timestamp("2019-04-29", tz="UTC"),
                dispatch_info="hallo",
            )


class TestEnsembleWrite(unittest.TestCase):
    def setUp(self):
        # setup temp dir
        testdatadir_src = Path(__file__).parent / "../data"
        self.testdatadir = tempfile.TemporaryDirectory()
        self.testdatadirpath = self.testdatadir.name
        shutil.copy(testdatadir_src / "multi_ensemble_ts.zrx", self.testdatadirpath)
        # setup zrxp machinery
        self.fs = FileStore(self.testdatadirpath, ZRXPFormat())

    def tearDown(self):
        self.testdatadir.cleanup()

    def test_write_same_ensemble(self):
        """Test that data can be rewritten to an existing ensemble branch."""
        ts = self.fs.get_by_path("multi_ensemble_ts-6290_ENSRRR24")
        member = "AVG"
        t0 = pd.Timestamp("2019-04-29", tz="UTC")
        df_old = ts.read_data_frame(member=member, t0=t0, dispatch_info=None)
        df_input = df_old.copy()
        df_input["value"] = 2
        df_input_sum = df_input["value"].sum()
        ts.write_data_frame(df_input, member=member, t0=t0, dispatch_info=None)
        self.assertEqual(3, len(ts.read_ensemble_members()))
        df_new = ts.read_data_frame(member=member, t0=t0, dispatch_info=None)
        self.assertEqual(15, len(df_new))
        self.assertNotEqual(df_old["value"].sum(), df_new["value"].sum())
        self.assertTrue(df_input_sum == df_new["value"].sum() == 15 * 2)

    def test_write_new_ensemble_branch(self):
        """Test that a new ensemble member can be created"""
        ts = self.fs.get_by_path("multi_ensemble_ts-6290_ENSRRR24")
        member = "AVG"
        t0 = pd.Timestamp("2019-04-29", tz="UTC")
        dispatch_info = None

        # test 1: different member
        df_input = ts.read_data_frame(member=member, t0=t0, dispatch_info=dispatch_info)
        member_new = "aNewMember"
        df_input["member"] = member_new
        ts.write_data_frame(df_input, member=member_new, t0=t0, dispatch_info=dispatch_info)
        self.assertEqual(4, len(ts.read_ensemble_members()))

        # test 2: different t0
        df_input = ts.read_data_frame(member=member, t0=t0, dispatch_info=dispatch_info)
        t0_new = pd.Timestamp("2019-04-30", tz="UTC")
        df_input["timestamp"] = t0_new
        ts.write_data_frame(df_input, member=member, t0=t0_new, dispatch_info=dispatch_info)
        self.assertEqual(5, len(ts.read_ensemble_members()))

        # test 3: different dispatch_info
        df_input = ts.read_data_frame(member=member, t0=t0, dispatch_info=dispatch_info)
        dispatch_info_new = "bla"
        df_input["dispatch_info"] = dispatch_info_new
        ts.write_data_frame(df_input, member=member, t0=t0, dispatch_info=dispatch_info_new)
        self.assertEqual(6, len(ts.read_ensemble_members()))

    def test_write_new_ensemble_member_different_length(self):
        """
        Test writing a new ensemble member with with a different length data frame.
        """
        ts = self.fs.get_by_path("multi_ensemble_ts-6290_ENSRRR24")
        member = "AVG"
        member_new = "aNewMember"
        t0 = pd.Timestamp("2019-04-29", tz="UTC")
        df_old = ts.read_data_frame(member=member, t0=t0, dispatch_info=None)
        new_length = 10
        df_input = df_old.copy()[:new_length]
        df_input["member"] = member_new
        ts.write_data_frame(df_input, member=member_new, t0=t0, dispatch_info=None)
        self.assertEqual(4, len(ts.read_ensemble_members()))
        # newly written df has a new length
        df_new = ts.read_data_frame(member=member_new, t0=t0, dispatch_info=None)
        self.assertEqual(new_length, len(df_new))
        # sanity check: old df stays unchanged
        self.assertEqual(15, len(ts.read_data_frame(member=member, t0=t0, dispatch_info=None)))

    def test_write_new_ensemble_branch_input_error(self):
        """
        Test write_data_frame must have input parameters that must match the data frame.
        """
        ts = self.fs.get_by_path("multi_ensemble_ts-6290_ENSRRR24")
        member = "AVG"
        member_new = "aNewMember"
        t0 = pd.Timestamp("2019-04-29", tz="UTC")
        df_input = ts.read_data_frame(member=member, t0=t0, dispatch_info=None)
        df_input["member"] = member_new
        with self.assertRaises(ValueError):
            ts.write_data_frame(df_input, member=member, t0=t0, dispatch_info=None)
        self.assertEqual(3, len(ts.read_ensemble_members()))


if __name__ == "__main__":
    unittest.main()

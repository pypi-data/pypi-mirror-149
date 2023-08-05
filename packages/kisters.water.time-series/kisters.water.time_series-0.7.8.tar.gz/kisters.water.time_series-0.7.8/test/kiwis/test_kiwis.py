import os
import unittest
from datetime import datetime
from pathlib import Path
from unittest import skipIf

from kisters.water.time_series.kiwis import KiWISStore

NOT_AVAILABLE = os.system("ping -c 1 kiwis.kisters.de")


@skipIf(NOT_AVAILABLE, "Public KiWIS is not available")
class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_url = "http://kiwis.kisters.de/KiWIS2/KiWIS"

        cls.start = datetime.strptime("2018-01-01", "%Y-%m-%d")
        cls.end = datetime.strptime("2018-01-02", "%Y-%m-%d")

        cls.kiwis = KiWISStore(base_url, user="Test", password="Test")
        cls.tsid = 7411042
        cls.tspath = "123/*/Precip/MMonth.Total"
        cls.ts_name = "0 Stundenwerte"
        cls.ts_default = cls.kiwis.get_by_id(ts_id=cls.tsid)
        cls.ts_meta = cls.kiwis.get_by_id(ts_id=cls.tsid, params={"metadata": ["type_id"]})
        cls.ts_meta_all = cls.kiwis.get_by_id(ts_id=cls.tsid, params={"metadata": ["type_id", "site.all"]})

        cls.tsl = cls.kiwis.get_by_filter(ts_filter=cls.tspath)

        cls.default_meta = [
            "id",
            "tsPath",
            "name",
            "shortName",
            "dataCoverageFrom",
            "dataCoverageUntil",
        ]

    def test_get_time_series(self):
        """"""
        # Getting ID
        self.assertEqual(self.ts_default.id, self.tsid)
        self.assertEqual(self.kiwis.get_by_path(self.ts_default.path).id, self.tsid)

    def test_get_item_by_id(self):
        """"""
        # Getting ID
        self.assertEqual(self.kiwis[self.tsid].id, self.tsid)

    def test_get_time_series_rows(self):
        # Testing rows in time series
        self.assertEqual(
            len(self.ts_default.read_data_frame(start=self.start, end=self.end).values),
            25,
        )
        self.assertEqual(
            len(self.ts_meta_all.read_data_frame(start=self.start, end=self.end).values),
            25,
        )

    def test_get_time_series_metadata(self):
        # Testing metadata in time series
        for key in self.default_meta:
            self.assertIsNotNone(self.ts_default.metadata[key])
            self.assertIsNotNone(self.ts_meta.metadata[key])
            self.assertIsNotNone(self.ts_meta_all.metadata[key])
        self.assertIsNotNone(self.ts_meta.metadata["type_id"])
        self.assertGreater(len(self.ts_meta_all.metadata["site"]), 0)

    def test_get_time_series_list(self):
        self.assertGreaterEqual(len(list(self.tsl)), 9)

    def test_read_data_frames(self):
        ts_list = self.tsl
        self.assertGreater(len(ts_list), 0)
        ts_dfs = self.kiwis.read_data_frames(ts_list, start=self.start, end=self.end)
        self.assertGreater(len(ts_dfs), 0)
        self.assertEqual(len(ts_dfs), len(ts_list))


NOT_IN_KISTERS_NETWORK = os.system("ping -c 1 vm-gis-rasdaman.kisters.de")


@skipIf(NOT_IN_KISTERS_NETWORK, "Only works in internal KISTERS network")
class TestEnsemble(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_url = "https://vm-gis-rasdaman.kisters.de/KiWIS/KiWIS"
        os.environ["REQUESTS_CA_BUNDLE"] = (Path(__file__).parent / "vm-gis-rasdaman.ca-bundle").as_posix()
        cls.kiwis = KiWISStore(base_url)
        cls.tsid = 24212010
        cls.ts = cls.kiwis.get_by_id(cls.tsid)
        cls.t0_start = datetime(2019, 1, 1)
        cls.t0_end = datetime(2019, 12, 31)

    def test_ensemble_members(self):
        members_last_t0 = self.ts.read_ensemble_members()
        members_all = self.ts.read_ensemble_members(t0_start=self.t0_start, t0_end=self.t0_end)
        self.assertTrue(len(members_last_t0) > 0)
        self.assertTrue(len(members_last_t0) < len(members_all))
        self.assertTrue(32, len(members_all))

    def test_read_data_frame(self):
        members_all = self.ts.read_ensemble_members(t0_start=self.t0_start, t0_end=self.t0_end)
        for branch in members_all:
            df = self.ts.read_data_frame(**branch)
            self.assertEqual(branch["member"], df["member"][0])
            self.assertEqual(branch["t0"], df["t0"][0])


if __name__ == "__main__":
    unittest.main()

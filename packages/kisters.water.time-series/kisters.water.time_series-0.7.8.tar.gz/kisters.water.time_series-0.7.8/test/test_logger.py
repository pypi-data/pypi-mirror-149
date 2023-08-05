import logging
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        self._logger = logging.getLogger(__name__)

    def testLogger(self):
        self._logger.info("Log test with info {}".format("hi there"))
        self._logger.error("Log test with error {}".format("hi there"))
        self._logger.warning("Log test with warning {}".format("hi there"))
        self._logger.debug("Log test with debug {}".format("hi there"))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

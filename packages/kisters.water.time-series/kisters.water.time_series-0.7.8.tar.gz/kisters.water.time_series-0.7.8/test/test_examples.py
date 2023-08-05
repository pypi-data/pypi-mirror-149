import os
import unittest
from unittest import skip

import nbformat
from nbconvert import NotebookExporter
from nbconvert.preprocessors import ExecutePreprocessor


def _notebook_run(path):
    """Execute a notebook via nbconvert and collect output.
    :returns (parsed nb object, execution errors)
    """
    nb_dir, nb_name = os.path.split(path)
    nb = nbformat.read(path, as_version=4)
    ep = ExecutePreprocessor(timeout=600)
    ep.preprocess(nb, {"metadata": {"path": nb_dir}})
    body, __ = NotebookExporter().from_notebook_node(nb)

    nb = nbformat.reads(body, nbformat.current_nbformat)
    errors = [
        output
        for cell in nb.cells
        if "outputs" in cell
        for output in cell["outputs"]
        if output.output_type == "error"
    ]

    return nb, errors


def _test_ipynb(filename):
    nb, errors = _notebook_run(filename)
    return errors


@skip("Examples not up to date, remove after reviewing them")
class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.examples_dir = os.path.join(os.path.dirname(__file__), "../examples/")

    def test_file_store_example(self):
        self.assertEqual(
            len(_test_ipynb(os.path.abspath(self.examples_dir + "file_store_example.ipynb"))),
            0,
        )

    def test_memory_ts_example(self):
        self.assertEqual(
            len(_test_ipynb(os.path.abspath(self.examples_dir + "memory_time_series_example.ipynb"))),
            0,
        )

    def test_arima_example(self):
        self.assertEqual(
            len(_test_ipynb(os.path.abspath(self.examples_dir + "statistics/arima.ipynb"))),
            0,
        )

    def test_autocorrelation_example(self):
        self.assertEqual(
            len(_test_ipynb(os.path.abspath(self.examples_dir + "statistics/autocorrelation.ipynb"))),
            0,
        )

    def test_sarimax_example(self):
        self.assertEqual(
            len(_test_ipynb(os.path.abspath(self.examples_dir + "statistics/sarimax_interpolate.ipynb"))),
            0,
        )

    def test_kiwis_adapter(self):
        self.assertEqual(
            len(_test_ipynb(os.path.abspath(self.examples_dir + "kiwis_adapter/basic_example.ipynb"))),
            0,
        )

    def test_overview_example(self):
        self.assertEqual(len(_test_ipynb(os.path.abspath(self.examples_dir + "overview.ipynb"))), 0)


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import tempfile
import unittest

from labanotation.data.laban_suite_data import get_laban_suite_sample_data
from labanotation.process import get_labanotation_results


class TestProcess(unittest.TestCase):

    def test_get_labanotation_results(self):
        output_dir = tempfile.TemporaryDirectory()
        filenames = get_laban_suite_sample_data()
        for fn in filenames:
            get_labanotation_results(
                fn,
                Path(output_dir.name) / fn.stem)
        output_dir.cleanup()

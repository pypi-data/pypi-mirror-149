import unittest

import numpy as np

from labanotation.visualization import labanotation_to_image


class TestLabanToImage(unittest.TestCase):

    def test_labanotation_to_image(self):
        timestamps = np.array(
            [1, 67, 364, 694, 760, 1123, 1222, 1816, 2608, 2971,
             3697, 4225, 4654, 4918, 5314,
             6238, 6667, 7096, 7492, 7822], dtype=np.float32) * 0.001
        all_laban = [[['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Right Forward', 'Low']],  # NOQA
                     [['Right Forward', 'Low'], ['Right Forward', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Right Forward', 'Low'], ['Right Forward', 'Middle'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Right', 'Low'], ['Forward', 'Middle'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Right Forward', 'Middle'], ['Forward', 'Middle'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Right Forward', 'Middle'], ['Right Forward', 'Middle'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Right Forward', 'Middle'], ['Right Forward', 'Middle'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Right Forward', 'Middle'], ['Right Forward', 'Middle'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']],  # NOQA
                     [['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low'], ['Place', 'Low']]]  # NOQA
        labanotation_to_image(timestamps, all_laban)

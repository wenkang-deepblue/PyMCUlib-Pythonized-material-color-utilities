# contrast/contrast_test.py

import unittest
from PyMCUlib.contrast.contrast import Contrast

class ContrastTest(unittest.TestCase):
    def test_ratio_of_tones_out_of_bounds_input(self):
        """Test that out-of-bounds input is handled correctly in ratio_of_tones"""
        self.assertAlmostEqual(21.0, Contrast.ratio_of_tones(-10.0, 110.0), delta=0.001)

    def test_lighter_impossible_ratio_errors(self):
        """Test that impossible ratios return -1 in lighter"""
        self.assertAlmostEqual(-1.0, Contrast.lighter(90.0, 10.0), delta=0.001)

    def test_lighter_out_of_bounds_input_above_errors(self):
        """Test that out-of-bounds input returns -1 in lighter"""
        self.assertAlmostEqual(-1.0, Contrast.lighter(110.0, 2.0), delta=0.001)

    def test_lighter_out_of_bounds_input_below_errors(self):
        """Test that out-of-bounds input returns -1 in lighter"""
        self.assertAlmostEqual(-1.0, Contrast.lighter(-10.0, 2.0), delta=0.001)

    def test_lighter_unsafe_returns_max_tone(self):
        """Test that lighter_unsafe returns 100 when ratio is not achievable"""
        self.assertAlmostEqual(100.0, Contrast.lighter_unsafe(100.0, 2.0), delta=0.001)

    def test_darker_impossible_ratio_errors(self):
        """Test that impossible ratios return -1 in darker"""
        self.assertAlmostEqual(-1.0, Contrast.darker(10.0, 20.0), delta=0.001)

    def test_darker_out_of_bounds_input_above_errors(self):
        """Test that out-of-bounds input returns -1 in darker"""
        self.assertAlmostEqual(-1.0, Contrast.darker(110.0, 2.0), delta=0.001)

    def test_darker_out_of_bounds_input_below_errors(self):
        """Test that out-of-bounds input returns -1 in darker"""
        self.assertAlmostEqual(-1.0, Contrast.darker(-10.0, 2.0), delta=0.001)

    def test_darker_unsafe_returns_min_tone(self):
        """Test that darker_unsafe returns 0 when ratio is not achievable"""
        self.assertAlmostEqual(0.0, Contrast.darker_unsafe(0.0, 2.0), delta=0.001)


if __name__ == '__main__':
    unittest.main()
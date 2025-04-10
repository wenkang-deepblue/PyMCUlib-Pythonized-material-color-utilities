# contrast_test.py

import unittest
from PyMCUlib.contrast.contrast import (
    ratio_of_tones,
    lighter,
    darker,
    lighter_unsafe,
    darker_unsafe
)

class ContrastTest(unittest.TestCase):
    def test_ratio_of_tones_out_of_bounds_input(self):
        self.assertAlmostEqual(ratio_of_tones(-10.0, 110.0), 21.0, delta=0.001)
    
    def test_lighter_impossible_ratio_errors(self):
        self.assertAlmostEqual(lighter(90.0, 10.0), -1.0, delta=0.001)
    
    def test_lighter_out_of_bounds_input_above_errors(self):
        self.assertAlmostEqual(lighter(110.0, 2.0), -1.0, delta=0.001)
    
    def test_lighter_out_of_bounds_input_below_errors(self):
        self.assertAlmostEqual(lighter(-10.0, 2.0), -1.0, delta=0.001)
    
    def test_lighter_unsafe_returns_max_tone(self):
        self.assertAlmostEqual(lighter_unsafe(100.0, 2.0), 100.0, delta=0.001)
    
    def test_darker_impossible_ratio_errors(self):
        self.assertAlmostEqual(darker(10.0, 20.0), -1.0, delta=0.001)
    
    def test_darker_out_of_bounds_input_above_errors(self):
        self.assertAlmostEqual(darker(110.0, 2.0), -1.0, delta=0.001)
    
    def test_darker_out_of_bounds_input_below_errors(self):
        self.assertAlmostEqual(darker(-10.0, 2.0), -1.0, delta=0.001)
    
    def test_darker_unsafe_returns_min_tone(self):
        self.assertAlmostEqual(darker_unsafe(0.0, 2.0), 0.0, delta=0.001)

if __name__ == '__main__':
    unittest.main()
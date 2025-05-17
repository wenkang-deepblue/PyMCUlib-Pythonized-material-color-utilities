# blend/blend_test.py

import unittest
from PyMCUlib.blend.blend import Blend

# Define color constants
RED = 0xffff0000
BLUE = 0xff0000ff
GREEN = 0xff00ff00
YELLOW = 0xffffff00

class BlendTest(unittest.TestCase):
    def _assert_colors_equal(self, actual, expected, msg=None):
        if actual != expected:
            self.fail(f"Colors don't match. Expected: {hex(expected)}, Got: {hex(actual)}")
    
    def test_harmonize_red_to_blue(self):
        answer = Blend.harmonize(RED, BLUE)
        self._assert_colors_equal(answer, 0xffFB0057)
    
    def test_harmonize_red_to_green(self):
        answer = Blend.harmonize(RED, GREEN)
        self._assert_colors_equal(answer, 0xffD85600)
    
    def test_harmonize_red_to_yellow(self):
        answer = Blend.harmonize(RED, YELLOW)
        self._assert_colors_equal(answer, 0xffD85600)
    
    def test_harmonize_blue_to_green(self):
        answer = Blend.harmonize(BLUE, GREEN)
        self._assert_colors_equal(answer, 0xff0047A3)
    
    def test_harmonize_blue_to_red(self):
        answer = Blend.harmonize(BLUE, RED)
        self._assert_colors_equal(answer, 0xff5700DC)
    
    def test_harmonize_blue_to_yellow(self):
        answer = Blend.harmonize(BLUE, YELLOW)
        self._assert_colors_equal(answer, 0xff0047A3)
    
    def test_harmonize_green_to_blue(self):
        answer = Blend.harmonize(GREEN, BLUE)
        self._assert_colors_equal(answer, 0xff00FC94)
    
    def test_harmonize_green_to_red(self):
        answer = Blend.harmonize(GREEN, RED)
        self._assert_colors_equal(answer, 0xffB1F000)
    
    def test_harmonize_green_to_yellow(self):
        answer = Blend.harmonize(GREEN, YELLOW)
        self._assert_colors_equal(answer, 0xffB1F000)
    
    def test_harmonize_yellow_to_blue(self):
        answer = Blend.harmonize(YELLOW, BLUE)
        self._assert_colors_equal(answer, 0xffEBFFBA)
    
    def test_harmonize_yellow_to_green(self):
        answer = Blend.harmonize(YELLOW, GREEN)
        self._assert_colors_equal(answer, 0xffEBFFBA)
    
    def test_harmonize_yellow_to_red(self):
        answer = Blend.harmonize(YELLOW, RED)
        self._assert_colors_equal(answer, 0xffFFF6E3)

if __name__ == '__main__':
    unittest.main()
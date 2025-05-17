# utils/utils_test.py

import unittest
from PyMCUlib.utils import color_utils
from PyMCUlib.utils import math_utils
from PyMCUlib.utils.test_utils import ColorTestCase


class ColorUtilsTest(ColorTestCase):
    """Tests for color_utils module."""
    
    def test_argb_from_rgb(self):
        """Tests for argb_from_rgb function."""
        self.assertEqual(color_utils.argb_from_rgb(255, 255, 255), 0xffffffff)
        self.assertEqual(color_utils.argb_from_rgb(255, 255, 255), 4294967295)
        
        self.assertEqual(color_utils.argb_from_rgb(0, 0, 0), 0xff000000)
        self.assertEqual(color_utils.argb_from_rgb(0, 0, 0), 4278190080)
        
        self.assertEqual(color_utils.argb_from_rgb(50, 150, 250), 0xff3296fa)
        self.assertEqual(color_utils.argb_from_rgb(50, 150, 250), 4281505530)


class MathUtilsTest(unittest.TestCase):
    """Tests for math_utils module."""
    
    def original_rotation_direction(self, from_val: float, to_val: float) -> float:
        """Reference implementation of rotation direction for testing."""
        a = to_val - from_val
        b = to_val - from_val + 360.0
        c = to_val - from_val - 360.0
        a_abs = abs(a)
        b_abs = abs(b)
        c_abs = abs(c)
        if a_abs <= b_abs and a_abs <= c_abs:
            return 1.0 if a >= 0.0 else -1.0
        elif b_abs <= a_abs and b_abs <= c_abs:
            return 1.0 if b >= 0.0 else -1.0
        else:
            return 1.0 if c >= 0.0 else -1.0
    
    def test_rotation_direction(self):
        """Tests for rotation_direction function."""
        for from_val in range(0, 360, 15):
            for to_val in range(8, 360, 15):
                expected = self.original_rotation_direction(from_val, to_val)
                actual = math_utils.rotation_direction(from_val, to_val)
                self.assertEqual(actual, expected)
                self.assertEqual(abs(actual), 1.0)


class LuminanceTest(unittest.TestCase):
    """Tests for luminance conversion functions."""

    def test_y_from_lstar(self):
        """Tests for y_from_lstar function."""
        test_values = [
            (0.0, 0.0),
            (0.1, 0.0110705),
            (0.2, 0.0221411),
            (0.3, 0.0332116),
            (0.4, 0.0442822),
            (0.5, 0.0553528),
            (1.0, 0.1107056),
            (2.0, 0.2214112),
            (3.0, 0.3321169),
            (4.0, 0.4428225),
            (5.0, 0.5535282),
            (8.0, 0.8856451),
            (10.0, 1.1260199),
            (15.0, 1.9085832),
            (20.0, 2.9890524),
            (25.0, 4.4154767),
            (30.0, 6.2359055),
            (40.0, 11.2509737),
            (50.0, 18.4186518),
            (60.0, 28.1233342),
            (70.0, 40.7494157),
            (80.0, 56.6812907),
            (90.0, 76.3033539),
            (95.0, 87.6183294),
            (99.0, 97.4360239),
            (100.0, 100.0)
        ]
        
        for lstar, expected_y in test_values:
            actual_y = color_utils.y_from_lstar(lstar)
            self.assertAlmostEqual(actual_y, expected_y, places=5)

    def test_lstar_from_y(self):
        """Tests for lstar_from_y function."""
        test_values = [
            (0.0, 0.0),
            (0.1, 0.9032962),
            (0.2, 1.8065925),
            (0.3, 2.7098888),
            (0.4, 3.6131851),
            (0.5, 4.5164814),
            (0.8856451, 8.0),
            (1.0, 8.9914424),
            (2.0, 15.4872443),
            (3.0, 20.0438970),
            (4.0, 23.6714419),
            (5.0, 26.7347653),
            (10.0, 37.8424304),
            (15.0, 45.6341970),
            (20.0, 51.8372115),
            (25.0, 57.0754208),
            (30.0, 61.6542222),
            (40.0, 69.4695307),
            (50.0, 76.0692610),
            (60.0, 81.8381891),
            (70.0, 86.9968642),
            (80.0, 91.6848609),
            (90.0, 95.9967686),
            (95.0, 98.0335184),
            (99.0, 99.6120372),
            (100.0, 100.0)
        ]
        
        for y, expected_lstar in test_values:
            actual_lstar = color_utils.lstar_from_y(y)
            self.assertAlmostEqual(actual_lstar, expected_lstar, places=5)
    
    def test_lstar_y_roundtrip(self):
        """Tests that y_from_lstar and lstar_from_y are inverses."""
        for y in [x / 10.0 for x in range(0, 1001)]:
            lstar = color_utils.lstar_from_y(y)
            reconstructed_y = color_utils.y_from_lstar(lstar)
            self.assertAlmostEqual(reconstructed_y, y, places=8)


if __name__ == "__main__":
    unittest.main()
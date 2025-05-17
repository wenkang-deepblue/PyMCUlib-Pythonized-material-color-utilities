# scheme/dynamic_scheme_test.py

"""
Tests for the dynamic_scheme module.
"""

import unittest

from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib.hct.hct import Hct


class DynamicSchemeTest(unittest.TestCase):
    """Tests for the DynamicScheme class."""

    def test_zero_length_input(self):
        """Test with 0 length input."""
        hue = DynamicScheme.get_rotated_hue(Hct.from_hct(43, 16, 16), [], [])
        self.assertAlmostEqual(43, hue, delta=0.4)

    def test_one_length_input_no_rotation(self):
        """Test with 1 length input and no rotation."""
        hue = DynamicScheme.get_rotated_hue(Hct.from_hct(43, 16, 16), [0], [0])
        self.assertAlmostEqual(43, hue, delta=0.4)

    def test_input_length_mismatch_asserts(self):
        """Test with input length mismatch."""
        hue = DynamicScheme.get_rotated_hue(Hct.from_hct(43, 16, 16), [0], [0, 1])
        self.assertAlmostEqual(43, hue, delta=0.4)

    def test_on_boundary_rotation_correct(self):
        """Test that rotation on boundary is correct."""
        hue = DynamicScheme.get_rotated_hue(
            Hct.from_hct(43, 16, 16),
            [0, 42, 360],
            [0, 15, 0],
        )
        self.assertAlmostEqual(43 + 15, hue, delta=0.4)

    def test_rotation_result_larger_than_360_degrees_wraps(self):
        """Test that rotation result larger than 360 degrees wraps."""
        hue = DynamicScheme.get_rotated_hue(
            Hct.from_hct(43, 16, 16),
            [0, 42, 360],
            [0, 480, 0],
        )
        self.assertAlmostEqual(163, hue, delta=0.4)


if __name__ == '__main__':
    unittest.main()
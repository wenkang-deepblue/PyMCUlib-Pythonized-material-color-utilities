# scheme/scheme_test.py

"""
Tests for the scheme module.
"""

import unittest

from PyMCUlib.scheme.scheme_android import SchemeAndroid


class SchemeAndroidTest(unittest.TestCase):
    """Tests for the SchemeAndroid class."""

    def assert_matches_color(self, actual_color, expected_color):
        """
        Assert that the actual color matches the expected color.
        
        Args:
            actual_color: The actual color value.
            expected_color: The expected color value.
        """
        self.assertEqual(actual_color, expected_color, 
                         f"Expected color 0x{expected_color:08x}, but got 0x{actual_color:08x}")

    def test_blue_light_scheme(self):
        """Test blue light scheme."""
        scheme = SchemeAndroid.light(0xff0000ff)
        self.assert_matches_color(scheme.color_accent_primary, 0xffe0e0ff)

    def test_blue_dark_scheme(self):
        """Test blue dark scheme."""
        scheme = SchemeAndroid.dark(0xff0000ff)
        self.assert_matches_color(scheme.color_accent_primary, 0xffe0e0ff)

    def test_third_party_light_scheme(self):
        """Test 3rd party light scheme."""
        scheme = SchemeAndroid.light(0xff6750a4)
        self.assert_matches_color(scheme.color_accent_primary, 0xffe9ddff)
        self.assert_matches_color(scheme.color_accent_secondary, 0xffe8def8)
        self.assert_matches_color(scheme.color_accent_tertiary, 0xffffd9e3)
        self.assert_matches_color(scheme.color_surface, 0xfffdf8fd)
        self.assert_matches_color(scheme.text_color_primary, 0xff1c1b1e)

    def test_third_party_dark_scheme(self):
        """Test 3rd party dark scheme."""
        scheme = SchemeAndroid.dark(0xff6750a4)
        self.assert_matches_color(scheme.color_accent_primary, 0xffe9ddff)
        self.assert_matches_color(scheme.color_accent_secondary, 0xffe8def8)
        self.assert_matches_color(scheme.color_accent_tertiary, 0xffffd9e3)
        self.assert_matches_color(scheme.color_surface, 0xff313033)
        self.assert_matches_color(scheme.text_color_primary, 0xfff4eff4)


if __name__ == '__main__':
    unittest.main()
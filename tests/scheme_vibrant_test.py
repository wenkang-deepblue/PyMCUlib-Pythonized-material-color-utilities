# scheme_vibrant_test.py

import unittest
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.vibrant import SchemeVibrant, HUES, SECONDARY_ROTATIONS, TERTIARY_ROTATIONS
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme

class TestSchemeVibrant(unittest.TestCase):
    def test_vibrant_scheme_dark_theme(self):
        """Test SchemeVibrant with dark theme"""
        # Create a scheme with blue color (0xff0000ff) in dark mode
        scheme = SchemeVibrant(Hct.from_int(0xff0000ff), True, 0.0)
        
        # Test some key colors to ensure they match expected values
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.VIBRANT)
        self.assertTrue(scheme.is_dark)
        
        # Test core palettes
        self.assertEqual(scheme.primary_palette.get_hue(), 
                         scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.primary_palette.get_chroma(), 200.0)
        
        # Test secondary palette which uses hue rotation
        secondary_hue = DynamicScheme.get_rotated_hue(
            scheme.source_color_hct, HUES, SECONDARY_ROTATIONS)
        self.assertEqual(scheme.secondary_palette.get_hue(), secondary_hue)
        self.assertEqual(scheme.secondary_palette.get_chroma(), 24.0)
        
        # Test tertiary palette which uses hue rotation
        tertiary_hue = DynamicScheme.get_rotated_hue(
            scheme.source_color_hct, HUES, TERTIARY_ROTATIONS)
        self.assertEqual(scheme.tertiary_palette.get_hue(), tertiary_hue)
        self.assertEqual(scheme.tertiary_palette.get_chroma(), 32.0)
        
        # Test neutral palettes
        self.assertEqual(scheme.neutral_palette.get_hue(),
                        scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.neutral_palette.get_chroma(), 10.0)
        
        self.assertEqual(scheme.neutral_variant_palette.get_hue(),
                        scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.neutral_variant_palette.get_chroma(), 12.0)
        
    def test_vibrant_scheme_light_theme(self):
        """Test SchemeVibrant with light theme"""
        # Create a scheme with blue color (0xff0000ff) in light mode
        scheme = SchemeVibrant(Hct.from_int(0xff0000ff), False, 0.0)
        
        # Test some key colors to ensure they match expected values
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.VIBRANT)
        self.assertFalse(scheme.is_dark)
        
    def test_default_constructor(self):
        """Test the default constructor without contrast_level parameter"""
        # Create a scheme using the simplified constructor
        scheme = SchemeVibrant(Hct.from_int(0xff0000ff), True)
        
        # Verify the default contrast level is 0.0
        self.assertEqual(scheme.contrast_level, 0.0)
        
    def test_hue_rotation_constants(self):
        """Test that the hue rotation constants are correctly defined"""
        # Verify HUES array
        self.assertEqual(len(HUES), 9)
        self.assertEqual(HUES[0], 0)
        self.assertEqual(HUES[-1], 360)
        
        # Verify SECONDARY_ROTATIONS array
        self.assertEqual(len(SECONDARY_ROTATIONS), 9)
        
        # Verify TERTIARY_ROTATIONS array
        self.assertEqual(len(TERTIARY_ROTATIONS), 9)

if __name__ == '__main__':
    unittest.main()
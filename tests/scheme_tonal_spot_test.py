# test_scheme_tonal_spot.py

import unittest
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.tonal_spot import SchemeTonalSpot
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.utils.utils import sanitize_degrees_double
from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors

class TestSchemeTonalSpot(unittest.TestCase):
    def test_dark_theme(self):
        """Test SchemeTonalSpot with dark theme"""
        # Create a scheme with blue color (0xff0000ff) in dark mode
        scheme = SchemeTonalSpot(Hct.from_int(0xff0000ff), True, 0.0)
        
        # Test some key colors to ensure they match expected values
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.TONAL_SPOT)
        self.assertTrue(scheme.is_dark)
        
        # Test core palettes
        self.assertEqual(scheme.primary_palette.get_hue(), 
                         scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.primary_palette.get_chroma(), 36.0)
        
        self.assertEqual(scheme.secondary_palette.get_hue(), 
                         scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.secondary_palette.get_chroma(), 16.0)
        
        # Test tertiary palette which uses hue rotation
        tertiary_hue = sanitize_degrees_double(scheme.source_color_hct.get_hue() + 60)
        self.assertEqual(scheme.tertiary_palette.get_hue(), tertiary_hue)
        self.assertEqual(scheme.tertiary_palette.get_chroma(), 24.0)
        
        # Test neutral palettes
        self.assertEqual(scheme.neutral_palette.get_hue(),
                        scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.neutral_palette.get_chroma(), 6.0)
        
        self.assertEqual(scheme.neutral_variant_palette.get_hue(),
                        scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.neutral_variant_palette.get_chroma(), 8.0)
        
    def test_light_theme(self):
        """Test SchemeTonalSpot with light theme"""
        # Create a scheme with blue color (0xff0000ff) in light mode
        scheme = SchemeTonalSpot(Hct.from_int(0xff0000ff), False, 0.0)
        
        # Test some key colors to ensure they match expected values
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.TONAL_SPOT)
        self.assertFalse(scheme.is_dark)
        
    def test_default_constructor(self):
        """Test the default constructor without contrast_level parameter"""
        # Create a scheme using the simplified constructor
        scheme = SchemeTonalSpot(Hct.from_int(0xff0000ff), True)
        
        # Verify the default contrast level is 0.0
        self.assertEqual(scheme.contrast_level, 0.0)

if __name__ == '__main__':
    unittest.main()
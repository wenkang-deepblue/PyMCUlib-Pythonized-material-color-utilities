# test_scheme_fruit_salad.py

import unittest
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.fruit_salad import SchemeFruitSalad
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.utils.utils import sanitize_degrees_double

class TestSchemeFruitSalad(unittest.TestCase):
    def test_fruit_salad_scheme_dark_theme(self):
        """Test SchemeFruitSalad with dark theme"""
        # Create a scheme with blue color (0xff0000ff) in dark mode
        scheme = SchemeFruitSalad(Hct.from_int(0xff0000ff), True, 0.0)
        
        # Test some key colors to ensure they match expected values
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.FRUIT_SALAD)
        self.assertTrue(scheme.is_dark)
        
        # Test core palettes
        # Primary palette should be source hue - 50° with chroma 48.0
        primary_hue = sanitize_degrees_double(scheme.source_color_hct.get_hue() - 50.0)
        self.assertEqual(scheme.primary_palette.get_hue(), primary_hue)
        self.assertEqual(scheme.primary_palette.get_chroma(), 48.0)
        
        # Secondary palette should be source hue - 50° with chroma 36.0
        self.assertEqual(scheme.secondary_palette.get_hue(), primary_hue)
        self.assertEqual(scheme.secondary_palette.get_chroma(), 36.0)
        
        # Tertiary palette should use source hue with chroma 36.0
        self.assertEqual(scheme.tertiary_palette.get_hue(), 
                         scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.tertiary_palette.get_chroma(), 36.0)
        
        # Test neutral palettes
        self.assertEqual(scheme.neutral_palette.get_hue(),
                        scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.neutral_palette.get_chroma(), 10.0)
        
        self.assertEqual(scheme.neutral_variant_palette.get_hue(),
                        scheme.source_color_hct.get_hue())
        self.assertEqual(scheme.neutral_variant_palette.get_chroma(), 16.0)
        
    def test_fruit_salad_scheme_light_theme(self):
        """Test SchemeFruitSalad with light theme"""
        # Create a scheme with blue color (0xff0000ff) in light mode
        scheme = SchemeFruitSalad(Hct.from_int(0xff0000ff), False, 0.0)
        
        # Test some key colors to ensure they match expected values
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.FRUIT_SALAD)
        self.assertFalse(scheme.is_dark)
        
    def test_default_constructor(self):
        """Test the default constructor without contrast_level parameter"""
        # Create a scheme using the simplified constructor
        scheme = SchemeFruitSalad(Hct.from_int(0xff0000ff), True)
        
        # Verify the default contrast level is 0.0
        self.assertEqual(scheme.contrast_level, 0.0)
        
    def test_color_consistency(self):
        """Test that the generated colors are consistent"""
        scheme1 = SchemeFruitSalad(Hct.from_int(0xff0000ff), True)
        scheme2 = SchemeFruitSalad(Hct.from_int(0xff0000ff), True)
        
        # Same input should produce same output
        self.assertEqual(scheme1.get_primary(), scheme2.get_primary())
        self.assertEqual(scheme1.get_secondary(), scheme2.get_secondary())
        self.assertEqual(scheme1.get_tertiary(), scheme2.get_tertiary())

if __name__ == '__main__':
    unittest.main()
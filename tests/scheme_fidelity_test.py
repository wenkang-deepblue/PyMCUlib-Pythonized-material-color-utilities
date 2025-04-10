# scheme_fidelity_test.py

import unittest
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.fidelity import SchemeFidelity
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.dislike.dislike import fix_if_disliked

class TestSchemeFidelity(unittest.TestCase):
    def test_fidelity_scheme_dark_theme(self):
        """Test SchemeFidelity with dark theme"""
        # Create a scheme with blue color (0xff0000ff) in dark mode
        blue_hct = Hct.from_int(0xff0000ff)
        scheme = SchemeFidelity(blue_hct, True, 0.0)
        
        # Test some key colors to ensure they are generated
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.FIDELITY)
        self.assertTrue(scheme.is_dark)
        
        # Test primary palette
        self.assertEqual(scheme.primary_palette.get_hue(), blue_hct.get_hue())
        self.assertEqual(scheme.primary_palette.get_chroma(), blue_hct.get_chroma())
        
        # Test secondary palette
        self.assertEqual(scheme.secondary_palette.get_hue(), blue_hct.get_hue())
        secondary_chroma = max(blue_hct.get_chroma() - 32.0, blue_hct.get_chroma() * 0.5)
        self.assertEqual(scheme.secondary_palette.get_chroma(), secondary_chroma)
        
        # Test tertiary palette
        complement_hct = fix_if_disliked(
            TemperatureCache(blue_hct).get_complement())
        self.assertEqual(scheme.tertiary_palette.get_hue(), complement_hct.get_hue())
        self.assertEqual(scheme.tertiary_palette.get_chroma(), complement_hct.get_chroma())
        
        # Test neutral palette
        self.assertEqual(scheme.neutral_palette.get_hue(), blue_hct.get_hue())
        self.assertEqual(scheme.neutral_palette.get_chroma(), blue_hct.get_chroma() / 8.0)
        
        # Test neutral variant palette
        self.assertEqual(scheme.neutral_variant_palette.get_hue(), blue_hct.get_hue())
        self.assertEqual(scheme.neutral_variant_palette.get_chroma(), 
                         blue_hct.get_chroma() / 8.0 + 4.0)
        
    def test_fidelity_scheme_light_theme(self):
        """Test SchemeFidelity with light theme"""
        # Create a scheme with blue color (0xff0000ff) in light mode
        scheme = SchemeFidelity(Hct.from_int(0xff0000ff), False, 0.0)
        
        # Test some key colors to ensure they are generated
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.FIDELITY)
        self.assertFalse(scheme.is_dark)
        
    def test_default_constructor(self):
        """Test the default constructor without contrast_level parameter"""
        # Create a scheme using the simplified constructor
        scheme = SchemeFidelity(Hct.from_int(0xff0000ff), True)
        
        # Verify the default contrast level is 0.0
        self.assertEqual(scheme.contrast_level, 0.0)
        
    def test_color_consistency(self):
        """Test that the generated colors are consistent"""
        scheme1 = SchemeFidelity(Hct.from_int(0xff0000ff), True)
        scheme2 = SchemeFidelity(Hct.from_int(0xff0000ff), True)
        
        # Same input should produce same output
        self.assertEqual(scheme1.get_primary(), scheme2.get_primary())
        self.assertEqual(scheme1.get_secondary(), scheme2.get_secondary())
        self.assertEqual(scheme1.get_tertiary(), scheme2.get_tertiary())

if __name__ == '__main__':
    unittest.main()
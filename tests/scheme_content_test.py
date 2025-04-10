# scheme_content_test.py

import unittest
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.content import SchemeContent
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.dislike.dislike import fix_if_disliked

class TestSchemeContent(unittest.TestCase):
    def test_content_scheme_dark_theme(self):
        """Test SchemeContent with dark theme"""
        # Create a scheme with blue color (0xff0000ff) in dark mode
        blue_hct = Hct.from_int(0xff0000ff)
        scheme = SchemeContent(blue_hct, True, 0.0)
        
        # Test some key colors to ensure they are generated
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.CONTENT)
        self.assertTrue(scheme.is_dark)
        
        # Test primary palette
        self.assertEqual(scheme.primary_palette.get_hue(), blue_hct.get_hue())
        self.assertEqual(scheme.primary_palette.get_chroma(), blue_hct.get_chroma())
        
        # Test secondary palette
        self.assertEqual(scheme.secondary_palette.get_hue(), blue_hct.get_hue())
        secondary_chroma = max(blue_hct.get_chroma() - 32.0, blue_hct.get_chroma() * 0.5)
        self.assertEqual(scheme.secondary_palette.get_chroma(), secondary_chroma)
        
        # Test tertiary palette
        tertiary_hct = fix_if_disliked(
            TemperatureCache(blue_hct).get_analogous_colors(3, 6)[2])
        self.assertEqual(scheme.tertiary_palette.get_hue(), tertiary_hct.get_hue())
        self.assertEqual(scheme.tertiary_palette.get_chroma(), tertiary_hct.get_chroma())
        
        # Test neutral palette
        self.assertEqual(scheme.neutral_palette.get_hue(), blue_hct.get_hue())
        self.assertEqual(scheme.neutral_palette.get_chroma(), blue_hct.get_chroma() / 8.0)
        
        # Test neutral variant palette
        self.assertEqual(scheme.neutral_variant_palette.get_hue(), blue_hct.get_hue())
        self.assertEqual(scheme.neutral_variant_palette.get_chroma(), 
                         blue_hct.get_chroma() / 8.0 + 4.0)
        
    def test_content_scheme_light_theme(self):
        """Test SchemeContent with light theme"""
        # Create a scheme with blue color (0xff0000ff) in light mode
        scheme = SchemeContent(Hct.from_int(0xff0000ff), False, 0.0)
        
        # Test some key colors to ensure they are generated
        self.assertIsNotNone(scheme.get_primary())
        self.assertIsNotNone(scheme.get_secondary())
        self.assertIsNotNone(scheme.get_tertiary())
        
        # Verify scheme properties
        self.assertEqual(scheme.variant, Variant.CONTENT)
        self.assertFalse(scheme.is_dark)
        
    def test_default_constructor(self):
        """Test the default constructor without contrast_level parameter"""
        # Create a scheme using the simplified constructor
        scheme = SchemeContent(Hct.from_int(0xff0000ff), True)
        
        # Verify the default contrast level is 0.0
        self.assertEqual(scheme.contrast_level, 0.0)
        
    def test_color_consistency(self):
        """Test that the generated colors are consistent"""
        scheme1 = SchemeContent(Hct.from_int(0xff0000ff), True)
        scheme2 = SchemeContent(Hct.from_int(0xff0000ff), True)
        
        # Same input should produce same output
        self.assertEqual(scheme1.get_primary(), scheme2.get_primary())
        self.assertEqual(scheme1.get_secondary(), scheme2.get_secondary())
        self.assertEqual(scheme1.get_tertiary(), scheme2.get_tertiary())

if __name__ == '__main__':
    unittest.main()
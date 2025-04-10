# scheme_neutral_test.py

import unittest
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.neutral import SchemeNeutral
from PyMCUlib.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from PyMCUlib.dynamiccolor.variant import Variant


class SchemeNeutralTest(unittest.TestCase):
    
    def test_neutral_scheme_properties(self):
        """Test the SchemeNeutral properties"""
        # Create a scheme from a blue color
        source_color = Hct.from_int(0xff0000ff)  # Blue color
        scheme = SchemeNeutral(source_color, False)
        
        # Test variant type
        self.assertEqual(scheme.variant, Variant.NEUTRAL)
        
        # Test palette hues and chromas
        self.assertEqual(scheme.primary_palette.get_hue(), source_color.get_hue())
        self.assertEqual(scheme.primary_palette.get_chroma(), 12.0)
        
        self.assertEqual(scheme.secondary_palette.get_hue(), source_color.get_hue())
        self.assertEqual(scheme.secondary_palette.get_chroma(), 8.0)
        
        self.assertEqual(scheme.tertiary_palette.get_hue(), source_color.get_hue())
        self.assertEqual(scheme.tertiary_palette.get_chroma(), 16.0)
        
        self.assertEqual(scheme.neutral_palette.get_hue(), source_color.get_hue())
        self.assertEqual(scheme.neutral_palette.get_chroma(), 2.0)
        
        self.assertEqual(scheme.neutral_variant_palette.get_hue(), source_color.get_hue())
        self.assertEqual(scheme.neutral_variant_palette.get_chroma(), 2.0)
    
    def test_light_and_dark_schemes(self):
        """Test light and dark mode schemes"""
        source_color = Hct.from_int(0xff0000ff)  # Blue color
        
        # Light scheme
        light_scheme = SchemeNeutral(source_color, False)
        self.assertFalse(light_scheme.is_dark)
        
        # Dark scheme
        dark_scheme = SchemeNeutral(source_color, True)
        self.assertTrue(dark_scheme.is_dark)
        
        # Verify different tone mappings between light and dark schemes
        light_primary_tone = MaterialDynamicColors.primary().get_hct(light_scheme).get_tone()
        dark_primary_tone = MaterialDynamicColors.primary().get_hct(dark_scheme).get_tone()
        self.assertNotEqual(light_primary_tone, dark_primary_tone)
    
    def test_contrast_level(self):
        """Test contrast level parameter"""
        source_color = Hct.from_int(0xff0000ff)  # Blue color
        
        # Default contrast level
        default_scheme = SchemeNeutral(source_color, False)
        self.assertEqual(default_scheme.contrast_level, 0.0)
        
        # Custom contrast level
        custom_scheme = SchemeNeutral(source_color, False, 0.5)
        self.assertEqual(custom_scheme.contrast_level, 0.5)

if __name__ == "__main__":
    unittest.main()
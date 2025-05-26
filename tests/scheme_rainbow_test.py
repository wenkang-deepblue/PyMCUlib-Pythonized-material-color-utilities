# test_scheme_rainbow.py

import unittest
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.rainbow import SchemeRainbow
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.utils.utils import sanitize_degrees_double

class TestSchemeRainbow(unittest.TestCase):
    def test_initialization(self):
        # Create a color in HCT
        hct = Hct.from_int(0xFF0000FF)  # Blue
        
        # Create a rainbow scheme
        scheme = SchemeRainbow(hct, False)
        
        # Check the variant
        self.assertEqual(scheme.variant, Variant.RAINBOW)
        
        # Check that palettes have expected properties
        self.assertEqual(scheme.primary_palette.get_hue(), hct.get_hue())
        self.assertEqual(scheme.primary_palette.get_chroma(), 48.0)
        
        self.assertEqual(scheme.secondary_palette.get_hue(), hct.get_hue())
        self.assertEqual(scheme.secondary_palette.get_chroma(), 16.0)
        
        # Check tertiary palette with 60 degree hue shift
        expected_tertiary_hue = sanitize_degrees_double(hct.get_hue() + 60.0)
        self.assertEqual(scheme.tertiary_palette.get_hue(), expected_tertiary_hue)
        self.assertEqual(scheme.tertiary_palette.get_chroma(), 24.0)
        
        self.assertEqual(scheme.neutral_palette.get_hue(), hct.get_hue())
        self.assertEqual(scheme.neutral_palette.get_chroma(), 0.0)
        
        self.assertEqual(scheme.neutral_variant_palette.get_hue(), hct.get_hue())
        self.assertEqual(scheme.neutral_variant_palette.get_chroma(), 0.0)
    
    def test_color_scheme(self):
        # Create a color in HCT
        hct = Hct.from_int(0xFF0000FF)  # Blue
        
        # Create light and dark schemes for comparison
        light_scheme = SchemeRainbow(hct, False)
        dark_scheme = SchemeRainbow(hct, True)
        
        # Verify that schemes have different colors appropriate for light/dark modes
        self.assertNotEqual(light_scheme.get_primary(), dark_scheme.get_primary())
        self.assertNotEqual(light_scheme.get_surface(), dark_scheme.get_surface())

    def test_color_values(self):
        """Test actual color values from the scheme."""
        hct = Hct.from_int(0xFF0000FF)  # Blue
        scheme = SchemeRainbow(hct, False)
        
        # Test that specific color values can be retrieved
        primary = scheme.get_primary()
        on_primary = scheme.get_on_primary()
        # Add assertions to verify the color values

if __name__ == '__main__':
    unittest.main()
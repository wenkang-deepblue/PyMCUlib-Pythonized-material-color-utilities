# test_material_dynamic_colors.py

import unittest
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib_cpp.palettes.tones import TonalPalette
from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import (
    MaterialDynamicColors, is_fidelity, is_monochrome
)

class TestMaterialDynamicColors(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.source_color = Hct.from_int(0xFF0000FF)  # Blue
        
        # Create palettes
        self.primary_palette = TonalPalette(self.source_color.get_hue(), 40.0)
        self.secondary_palette = TonalPalette(self.source_color.get_hue(), 16.0)
        self.tertiary_palette = TonalPalette(self.source_color.get_hue() + 60, 24.0)
        self.neutral_palette = TonalPalette(self.source_color.get_hue(), 4.0)
        self.neutral_variant_palette = TonalPalette(self.source_color.get_hue(), 8.0)
        
        # Create schemes
        self.light_scheme = DynamicScheme(
            self.source_color,
            Variant.TONAL_SPOT,
            0.0,  # Standard contrast
            False,  # Light mode
            self.primary_palette,
            self.secondary_palette,
            self.tertiary_palette,
            self.neutral_palette,
            self.neutral_variant_palette
        )
        
        self.dark_scheme = DynamicScheme(
            self.source_color,
            Variant.TONAL_SPOT,
            0.0,  # Standard contrast
            True,  # Dark mode
            self.primary_palette,
            self.secondary_palette,
            self.tertiary_palette,
            self.neutral_palette,
            self.neutral_variant_palette
        )
        
        # Create schemes with different variants
        self.fidelity_scheme = DynamicScheme(
            self.source_color,
            Variant.FIDELITY,
            0.0,
            False,
            self.primary_palette,
            self.secondary_palette,
            self.tertiary_palette,
            self.neutral_palette,
            self.neutral_variant_palette
        )
        
        self.monochrome_scheme = DynamicScheme(
            self.source_color,
            Variant.MONOCHROME,
            0.0,
            False,
            self.primary_palette,
            self.secondary_palette,
            self.tertiary_palette,
            self.neutral_palette,
            self.neutral_variant_palette
        )
    
    def test_helper_functions(self):
        """Test the helper functions."""
        # Test is_fidelity
        self.assertFalse(is_fidelity(self.light_scheme))
        self.assertTrue(is_fidelity(self.fidelity_scheme))
        
        # Test is_monochrome
        self.assertFalse(is_monochrome(self.light_scheme))
        self.assertTrue(is_monochrome(self.monochrome_scheme))
    
    def test_basic_dynamic_colors(self):
        """Test basic dynamic colors."""
        # Test primary color in light scheme
        primary_light = MaterialDynamicColors.primary().get_argb(self.light_scheme)
        self.assertIsNotNone(primary_light)
        
        # Test primary color in dark scheme
        primary_dark = MaterialDynamicColors.primary().get_argb(self.dark_scheme)
        self.assertIsNotNone(primary_dark)
        
        # Test on_primary color contrasts with primary
        on_primary_light = MaterialDynamicColors.on_primary().get_argb(self.light_scheme)
        self.assertIsNotNone(on_primary_light)
        self.assertNotEqual(primary_light, on_primary_light)
    
    def test_background_colors(self):
        """Test background and surface colors."""
        # Test background
        bg_light = MaterialDynamicColors.background().get_argb(self.light_scheme)
        bg_dark = MaterialDynamicColors.background().get_argb(self.dark_scheme)
        self.assertIsNotNone(bg_light)
        self.assertIsNotNone(bg_dark)
        
        # Test on_background contrasts with background
        on_bg_light = MaterialDynamicColors.on_background().get_argb(self.light_scheme)
        on_bg_dark = MaterialDynamicColors.on_background().get_argb(self.dark_scheme)
        self.assertIsNotNone(on_bg_light)
        self.assertIsNotNone(on_bg_dark)
        self.assertNotEqual(bg_light, on_bg_light)
        self.assertNotEqual(bg_dark, on_bg_dark)
    
    def test_container_colors(self):
        """Test container colors."""
        # Test primary container
        primary_container_light = MaterialDynamicColors.primary_container().get_argb(self.light_scheme)
        primary_container_dark = MaterialDynamicColors.primary_container().get_argb(self.dark_scheme)
        self.assertIsNotNone(primary_container_light)
        self.assertIsNotNone(primary_container_dark)
        
        # Test on_primary_container contrasts with primary_container
        on_primary_container_light = MaterialDynamicColors.on_primary_container().get_argb(self.light_scheme)
        on_primary_container_dark = MaterialDynamicColors.on_primary_container().get_argb(self.dark_scheme)
        self.assertIsNotNone(on_primary_container_light)
        self.assertIsNotNone(on_primary_container_dark)
        self.assertNotEqual(primary_container_light, on_primary_container_light)
        self.assertNotEqual(primary_container_dark, on_primary_container_dark)
    
    def test_variant_specific_colors(self):
        """Test colors that behave differently based on variant."""
        # Test primary in monochrome scheme
        primary_mono = MaterialDynamicColors.primary().get_argb(self.monochrome_scheme)
        self.assertIsNotNone(primary_mono)
        
        # Test primary in fidelity scheme
        primary_fidelity = MaterialDynamicColors.primary().get_argb(self.fidelity_scheme)
        self.assertIsNotNone(primary_fidelity)
        
        # Test tertiary container in different schemes
        tertiary_container_light = MaterialDynamicColors.tertiary_container().get_argb(self.light_scheme)
        tertiary_container_mono = MaterialDynamicColors.tertiary_container().get_argb(self.monochrome_scheme)
        tertiary_container_fidelity = MaterialDynamicColors.tertiary_container().get_argb(self.fidelity_scheme)
        
        self.assertIsNotNone(tertiary_container_light)
        self.assertIsNotNone(tertiary_container_mono)
        self.assertIsNotNone(tertiary_container_fidelity)
    
    def test_fixed_colors(self):
        """Test fixed colors."""
        # Test primary fixed
        primary_fixed_light = MaterialDynamicColors.primary_fixed().get_argb(self.light_scheme)
        primary_fixed_dark = MaterialDynamicColors.primary_fixed().get_argb(self.dark_scheme)
        self.assertIsNotNone(primary_fixed_light)
        self.assertIsNotNone(primary_fixed_dark)
        self.assertEqual(primary_fixed_light, primary_fixed_dark)  # Fixed colors should be the same in light and dark
        
        # Test on_primary_fixed contrasts with primary_fixed
        on_primary_fixed = MaterialDynamicColors.on_primary_fixed().get_argb(self.light_scheme)
        self.assertIsNotNone(on_primary_fixed)
        self.assertNotEqual(primary_fixed_light, on_primary_fixed)

if __name__ == "__main__":
    unittest.main()
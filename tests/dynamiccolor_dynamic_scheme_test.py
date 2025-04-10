# test_dynamic_scheme.py

import unittest
from PyMCUlib.cam.hct import Hct
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.palettes.tones import TonalPalette
from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme

class TestDynamicScheme(unittest.TestCase):
    
    def test_initialization(self):
        """Test that DynamicScheme can be properly initialized."""
        source_color = Hct.from_int(0xFF0000FF)  # Blue
        variant = Variant.TONAL_SPOT
        contrast_level = 0.0
        is_dark = False
        
        # Create tonal palettes
        primary_palette = TonalPalette(source_color.get_hue(), 40.0)
        secondary_palette = TonalPalette(source_color.get_hue(), 16.0)
        tertiary_palette = TonalPalette(source_color.get_hue() + 60, 24.0)
        neutral_palette = TonalPalette(source_color.get_hue(), 4.0)
        neutral_variant_palette = TonalPalette(source_color.get_hue(), 8.0)
        
        # Create DynamicScheme
        scheme = DynamicScheme(
            source_color,
            variant,
            contrast_level,
            is_dark,
            primary_palette,
            secondary_palette,
            tertiary_palette,
            neutral_palette,
            neutral_variant_palette
        )
        
        # Check basic properties
        self.assertEqual(scheme.source_color_hct, source_color)
        self.assertEqual(scheme.variant, variant)
        self.assertEqual(scheme.contrast_level, contrast_level)
        self.assertEqual(scheme.is_dark, is_dark)
        self.assertEqual(scheme.primary_palette, primary_palette)
        self.assertEqual(scheme.secondary_palette, secondary_palette)
        self.assertEqual(scheme.tertiary_palette, tertiary_palette)
        self.assertEqual(scheme.neutral_palette, neutral_palette)
        self.assertEqual(scheme.neutral_variant_palette, neutral_variant_palette)
        
        # Check error palette default
        self.assertIsNotNone(scheme.error_palette)
    
    def test_get_rotated_hue(self):
        """Test the hue rotation functionality."""
        source_color = Hct.from_int(0xFFFF0000)  # Red
        
        # Single rotation
        rotated_single = DynamicScheme.get_rotated_hue(source_color, [0], [15])
        expected_single = (source_color.get_hue() + 15) % 360
        self.assertAlmostEqual(rotated_single, expected_single, places=5)
        
        # Multiple hue points - not matching
        rotated_multiple = DynamicScheme.get_rotated_hue(
            source_color, 
            [30, 60, 90],  # Hues that don't include source color's hue
            [10, 20, 30]
        )
        # Should return original hue
        self.assertEqual(rotated_multiple, source_color.get_hue())
        
        # Multiple hue points - matching
        another_color = Hct.from_hct(45, 50, 50)  # Color with hue 45
        rotated_matching = DynamicScheme.get_rotated_hue(
            another_color,
            [30, 60, 90],  # Hues include 45 between 30 and 60
            [10, 20, 30]
        )
        # Should return hue + rotation[0] = 45 + 10 = 55
        self.assertTrue(54.5 <= rotated_matching <= 55.5, 
                        f"Expected value near 55, got {rotated_matching}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
# test_dynamic_color.py

import unittest
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib_cpp.dynamiccolor.dynamic_color import (
    DynamicColor, foreground_tone, enable_light_foreground,
    tone_prefers_light_foreground, tone_allows_light_foreground
)
from PyMCUlib_cpp.contrast.contrast import (
    ratio_of_tones, lighter, darker, lighter_unsafe, darker_unsafe
)
from PyMCUlib_cpp.dynamiccolor.contrast_curve import ContrastCurve
from PyMCUlib_cpp.dynamiccolor.tone_delta_pair import ToneDeltaPair, TonePolarity
from PyMCUlib_cpp.palettes.tones import TonalPalette
from PyMCUlib_cpp.dynamiccolor.variant import Variant

class TestDynamicColorFunctions(unittest.TestCase):
    def test_foreground_tone(self):
        """Test the foreground_tone function for different background tones."""
        # Test with light background (prefer dark foreground)
        light_bg = 90.0
        light_bg_result = foreground_tone(light_bg, 4.5)
        self.assertLess(light_bg_result, light_bg)
        self.assertGreaterEqual(light_bg_result, 0)
        
        # Test with dark background (prefer light foreground)
        dark_bg = 20.0
        dark_bg_result = foreground_tone(dark_bg, 4.5)
        self.assertGreater(dark_bg_result, dark_bg)
        self.assertLessEqual(dark_bg_result, 100)
    
    def test_enable_light_foreground(self):
        """Test enable_light_foreground function."""
        # Test with tone that prefers light foreground but doesn't allow it
        adjusted = enable_light_foreground(55.0)
        self.assertEqual(adjusted, 49.0)
        
        # Test with tone that prefers light foreground and allows it
        unchanged = enable_light_foreground(45.0)
        self.assertEqual(unchanged, 45.0)
        
        # Test with tone that doesn't prefer light foreground
        also_unchanged = enable_light_foreground(70.0)
        self.assertEqual(also_unchanged, 70.0)
    
    def test_tone_prefers_light_foreground(self):
        """Test tone_prefers_light_foreground function."""
        self.assertTrue(tone_prefers_light_foreground(0.0))
        self.assertTrue(tone_prefers_light_foreground(59.0))
        self.assertFalse(tone_prefers_light_foreground(60.0))
        self.assertFalse(tone_prefers_light_foreground(100.0))
    
    def test_tone_allows_light_foreground(self):
        """Test tone_allows_light_foreground function."""
        self.assertTrue(tone_allows_light_foreground(0.0))
        self.assertTrue(tone_allows_light_foreground(49.0))
        self.assertFalse(tone_allows_light_foreground(50.0))
        self.assertFalse(tone_allows_light_foreground(100.0))


class TestDynamicColor(unittest.TestCase):
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
    
    def test_from_palette(self):
        """Test the from_palette constructor."""
        dc = DynamicColor.from_palette(
            name="test_color",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 40.0 if s.is_dark else 80.0
        )
        
        self.assertEqual(dc.name, "test_color")
        self.assertFalse(dc.is_background)
        self.assertIsNone(dc.background)
        self.assertIsNone(dc.second_background)
        self.assertIsNone(dc.contrast_curve)
        self.assertIsNone(dc.tone_delta_pair)
        
        # Test that tone function works correctly
        self.assertEqual(dc.tone(self.light_scheme), 80.0)
        self.assertEqual(dc.tone(self.dark_scheme), 40.0)
    
    def test_get_argb(self):
        """Test get_argb method."""
        dc = DynamicColor.from_palette(
            name="test_color",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 40.0
        )
        
        argb = dc.get_argb(self.light_scheme)
        self.assertEqual(argb & 0xFF000000, 0xFF000000)  # Alpha should be 0xFF
    
    def test_get_hct(self):
        """Test get_hct method."""
        dc = DynamicColor.from_palette(
            name="test_color",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 40.0
        )
        
        hct = dc.get_hct(self.light_scheme)
        self.assertAlmostEqual(hct.get_hue(), self.primary_palette.get_hue(), delta=0.5)
        self.assertAlmostEqual(hct.get_tone(), 40.0, delta=0.2)
    
    def test_get_tone_with_background(self):
        """Test get_tone with background contrast requirements."""
        # Create a background color
        bg_color = DynamicColor.from_palette(
            name="background",
            palette=lambda s: self.neutral_palette,
            tone=lambda s: 90.0 if not s.is_dark else 10.0
        )
        
        # Create a foreground color with contrast requirements
        fg_color = DynamicColor(
            name="foreground",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 50.0,
            is_background=False,
            background=lambda s: bg_color,
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None
        )
        
        # In light mode, foreground should be darker to contrast with light background
        fg_tone_light = fg_color.get_tone(self.light_scheme)
        self.assertLess(fg_tone_light, 50.0)
        
        # In dark mode, foreground should be lighter to contrast with dark background
        fg_tone_dark = fg_color.get_tone(self.dark_scheme)
        self.assertGreater(fg_tone_dark, 50.0)

    def test_get_tone_with_tone_delta_pair(self):
        """Test get_tone with tone delta pair constraint."""
        # This is a more complex test that would require setting up
        # two colors with a tone delta constraint between them
        
        # First background color
        bg_color = DynamicColor.from_palette(
            name="background",
            palette=lambda s: self.neutral_palette,
            tone=lambda s: 90.0 if not s.is_dark else 10.0
        )
        
        # Primary color
        primary = DynamicColor(
            name="primary",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 40.0 if s.is_dark else 80.0,
            is_background=False,
            background=lambda s: bg_color,
            second_background=None,
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),  # 添加对比度曲线
            tone_delta_pair=None
        )

        container = None
        
        # Create a tone delta pair function
        def create_tone_delta_pair(scheme):
            return ToneDeltaPair(
                primary, container, 15.0, 
                TonePolarity.DARKER if scheme.is_dark else TonePolarity.LIGHTER,
                False
            )
        
        # Container color with tone delta constraint
        container = DynamicColor(
            name="container",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 90.0 if not s.is_dark else 30.0,
            is_background=True,
            background=lambda s: bg_color,
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=create_tone_delta_pair
        )
        
        # Primary with tone delta constraint
        primary_with_delta = DynamicColor(
            name="primary",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 40.0 if s.is_dark else 80.0,
            is_background=False,
            background=lambda s: bg_color,
            second_background=None,
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=create_tone_delta_pair
        )
        
        # Check tone delta in light mode
        primary_tone_light = primary_with_delta.get_tone(self.light_scheme)
        container_tone_light = container.get_tone(self.light_scheme)
        self.assertGreaterEqual(abs(primary_tone_light - container_tone_light), 15.0)
        
        # Check tone delta in dark mode
        primary_tone_dark = primary_with_delta.get_tone(self.dark_scheme)
        container_tone_dark = container.get_tone(self.dark_scheme)
        self.assertGreaterEqual(abs(primary_tone_dark - container_tone_dark), 15.0)

    def test_decreasing_contrast(self):
        """Test the behavior when contrast level is negative (decreasing contrast)."""
        # Create background color
        bg_color = DynamicColor.from_palette(
            name="background",
            palette=lambda s: self.neutral_palette,
            tone=lambda s: 90.0 if not s.is_dark else 10.0
        )
        
        # Create foreground color with contrast requirements
        fg_color = DynamicColor(
            name="foreground",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 50.0,
            is_background=False,
            background=lambda s: bg_color,
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None
        )
        
        # Create a scheme with negative contrast level
        decreasing_contrast_scheme = DynamicScheme(
            self.source_color,
            Variant.TONAL_SPOT,
            -0.5,  # Negative contrast level
            False,  # Light mode
            self.primary_palette,
            self.secondary_palette,
            self.tertiary_palette,
            self.neutral_palette,
            self.neutral_variant_palette
        )
        
        # Test tone in negative contrast level
        fg_tone_normal = fg_color.get_tone(self.light_scheme)
        fg_tone_decreased = fg_color.get_tone(decreasing_contrast_scheme)
        
        # Lowering contrast should result in a color closer to the background color
        bg_tone = bg_color.get_tone(self.light_scheme)
        self.assertLess(abs(bg_tone - fg_tone_decreased), abs(bg_tone - fg_tone_normal))
        
        # Verify if the contrast value meets the contrast curve requirements
        contrast_value = fg_color.contrast_curve.get(-0.5)  # Value at -0.5 contrast level
        actual_contrast = ratio_of_tones(bg_tone, fg_tone_decreased)
        self.assertAlmostEqual(actual_contrast, contrast_value, delta=0.5)

    def test_awkward_zone_handling(self):
        """Test handling of the 'awkward zone' (tones 50-59)."""
        # Create background color
        bg_color = DynamicColor.from_palette(
            name="background",
            palette=lambda s: self.neutral_palette,
            tone=lambda s: 90.0 if not s.is_dark else 10.0
        )
        
        # Create color with initial tone in awkward zone
        awkward_color = DynamicColor(
            name="awkward_color",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 55.0,  # In awkward zone (50-59)
            is_background=True,   # Set as background color, as is_background triggers awkward zone handling
            background=lambda s: bg_color,
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=None
        )
        
        # Get actual tone
        light_tone = awkward_color.get_tone(self.light_scheme)
        dark_tone = awkward_color.get_tone(self.dark_scheme)
        
        # Verify if tone is moved out of awkward zone
        self.assertFalse(50 <= light_tone < 60, "In light mode, tone should be moved out of awkward zone")
        self.assertFalse(50 <= dark_tone < 60, "In dark mode, tone should be moved out of awkward zone")
        
        # Verify moving direction: In light mode, it should move down (to 49 or below), and in dark mode, it should move up (to 60 or above)
        if light_tone < 50:
            self.assertLessEqual(light_tone, 49, "In light mode, it should move to 49 or below")
        else:
            self.assertGreaterEqual(light_tone, 60, "In light mode, it should move to 60 or above")
            
        if dark_tone < 50:
            self.assertLessEqual(dark_tone, 49, "In dark mode, it should move to 49 or below")
        else:
            self.assertGreaterEqual(dark_tone, 60, "In dark mode, it should move to 60 or above")

    def test_dual_backgrounds(self):
        """Test the behavior with dual backgrounds (Case 3)."""
        # Create two background colors
        bg_color1 = DynamicColor.from_palette(
            name="background1",
            palette=lambda s: self.neutral_palette,
            tone=lambda s: 95.0 if not s.is_dark else 5.0
        )
        
        bg_color2 = DynamicColor.from_palette(
            name="background2",
            palette=lambda s: self.neutral_palette,
            tone=lambda s: 80.0 if not s.is_dark else 30.0
        )
        
        # Create color with two backgrounds
        dual_bg_color = DynamicColor(
            name="dual_background_color",
            palette=lambda s: self.primary_palette,
            tone=lambda s: 50.0,
            is_background=False,
            background=lambda s: bg_color1,
            second_background=lambda s: bg_color2,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None
        )
        
        # Get actual tone
        light_tone = dual_bg_color.get_tone(self.light_scheme)
        dark_tone = dual_bg_color.get_tone(self.dark_scheme)
        
        # Get background tone
        bg1_light_tone = bg_color1.get_tone(self.light_scheme)
        bg2_light_tone = bg_color2.get_tone(self.light_scheme)
        bg1_dark_tone = bg_color1.get_tone(self.dark_scheme)
        bg2_dark_tone = bg_color2.get_tone(self.dark_scheme)
        
        # Calculate desired contrast
        desired_ratio = dual_bg_color.contrast_curve.get(0.0)  # Standard contrast level
        
        # Verify contrast with two backgrounds
        # Light mode
        self.assertGreaterEqual(
            ratio_of_tones(max(bg1_light_tone, bg2_light_tone), light_tone), 
            desired_ratio, 
            "In light mode, contrast should meet the requirements of the higher background"
        )
        self.assertGreaterEqual(
            ratio_of_tones(min(bg1_light_tone, bg2_light_tone), light_tone), 
            desired_ratio, 
            "In light mode, contrast should meet the requirements of the lower background"
        )
        
        # 暗模式
        self.assertGreaterEqual(
            ratio_of_tones(max(bg1_dark_tone, bg2_dark_tone), dark_tone), 
            desired_ratio, 
            "In dark mode, contrast should meet the requirements of the higher background"
        )
        self.assertGreaterEqual(
            ratio_of_tones(min(bg1_dark_tone, bg2_dark_tone), dark_tone), 
            desired_ratio, 
            "In dark mode, contrast should meet the requirements of the lower background"
        )


if __name__ == "__main__":
    unittest.main()
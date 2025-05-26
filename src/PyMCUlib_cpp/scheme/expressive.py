# expressive.py

from typing import List
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.palettes.tones import TonalPalette

# Hue points for calculating rotations
HUES = [0, 21, 51, 121, 151, 191, 271, 321, 360]

# Rotation values for secondary colors at each hue
SECONDARY_ROTATIONS = [45, 95, 45, 20, 45, 90, 45, 45, 45]

# Rotation values for tertiary colors at each hue
TERTIARY_ROTATIONS = [120, 120, 20, 45, 20, 15, 20, 120, 120]

class SchemeExpressive(DynamicScheme):
    """
    An expressive theme - a theme that uses unconventional colors.
    """
    
    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0):
        """
        Create an expressive color scheme based on the source color.
        
        Args:
            source_color_hct: Source color of the scheme in HCT
            is_dark: Whether the scheme is dark or light
            contrast_level: Level of contrast between colors
        """
        super().__init__(
            source_color_hct=source_color_hct,
            variant=Variant.EXPRESSIVE,
            contrast_level=contrast_level,
            is_dark=is_dark,
            primary_palette=TonalPalette(source_color_hct.get_hue() + 240.0, 40.0),
            secondary_palette=TonalPalette(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, HUES, SECONDARY_ROTATIONS),
                24.0),
            tertiary_palette=TonalPalette(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, HUES, TERTIARY_ROTATIONS),
                32.0),
            neutral_palette=TonalPalette(source_color_hct.get_hue() + 15.0, 8.0),
            neutral_variant_palette=TonalPalette(source_color_hct.get_hue() + 15.0, 12.0)
        )
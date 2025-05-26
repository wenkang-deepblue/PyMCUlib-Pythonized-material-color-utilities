# vibrant.py

from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.palettes.tones import TonalPalette

# Hue points for calculating rotations
HUES = [0, 41, 61, 101, 131, 181, 251, 301, 360]

# Rotation values for secondary colors at each hue
SECONDARY_ROTATIONS = [18, 15, 10, 12, 15, 18, 15, 12, 12]

# Rotation values for tertiary colors at each hue
TERTIARY_ROTATIONS = [35, 30, 20, 25, 30, 35, 30, 25, 25]

class SchemeVibrant(DynamicScheme):
    """
    A vibrant theme - a theme that uses fully saturated, vivid colors, 
    close to the source color's hue.
    """
    
    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0):
        """
        Create a vibrant color scheme based on the source color.
        
        Args:
            source_color_hct: Source color of the scheme in HCT
            is_dark: Whether the scheme is dark or light
            contrast_level: Level of contrast between colors
        """
        super().__init__(
            source_color_hct=source_color_hct,
            variant=Variant.VIBRANT,
            contrast_level=contrast_level,
            is_dark=is_dark,
            primary_palette=TonalPalette(source_color_hct.get_hue(), 200.0),
            secondary_palette=TonalPalette(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, HUES, SECONDARY_ROTATIONS),
                24.0),
            tertiary_palette=TonalPalette(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, HUES, TERTIARY_ROTATIONS),
                32.0),
            neutral_palette=TonalPalette(source_color_hct.get_hue(), 10.0),
            neutral_variant_palette=TonalPalette(source_color_hct.get_hue(), 12.0)
        )
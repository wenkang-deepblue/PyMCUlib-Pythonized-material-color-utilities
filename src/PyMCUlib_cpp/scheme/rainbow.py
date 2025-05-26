# rainbow.py

from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.palettes.tones import TonalPalette
from PyMCUlib_cpp.utils.utils import sanitize_degrees_double

class SchemeRainbow(DynamicScheme):
    """
    A rainbow theme - a playful theme with high colorfulness.
    """
    
    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0):
        """
        Create a rainbow color scheme based on the source color.
        
        Args:
            source_color_hct: Source color of the scheme in HCT
            is_dark: Whether the scheme is dark or light
            contrast_level: Level of contrast between colors
        """
        super().__init__(
            source_color_hct=source_color_hct,
            variant=Variant.RAINBOW,
            contrast_level=contrast_level,
            is_dark=is_dark,
            primary_palette=TonalPalette(source_color_hct.get_hue(), 48.0),
            secondary_palette=TonalPalette(source_color_hct.get_hue(), 16.0),
            tertiary_palette=TonalPalette(
                sanitize_degrees_double(source_color_hct.get_hue() + 60.0),
                24.0),
            neutral_palette=TonalPalette(source_color_hct.get_hue(), 0.0),
            neutral_variant_palette=TonalPalette(source_color_hct.get_hue(), 0.0)
        )
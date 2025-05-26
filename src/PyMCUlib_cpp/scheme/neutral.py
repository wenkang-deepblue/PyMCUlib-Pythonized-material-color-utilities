# neutral.py

from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.palettes.tones import TonalPalette

class SchemeNeutral(DynamicScheme):
    """
    A neutral theme - a palette with just one color (one hue) but with variations
    in tone and a very low chroma.
    """
    
    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0):
        """
        Create a neutral color scheme based on the source color.
        
        Args:
            source_color_hct: Source color of the scheme in HCT
            is_dark: Whether the scheme is dark or light
            contrast_level: Level of contrast between colors
        """
        super().__init__(
            source_color_hct=source_color_hct,
            variant=Variant.NEUTRAL,
            contrast_level=contrast_level,
            is_dark=is_dark,
            primary_palette=TonalPalette(source_color_hct.get_hue(), 12.0),
            secondary_palette=TonalPalette(source_color_hct.get_hue(), 8.0),
            tertiary_palette=TonalPalette(source_color_hct.get_hue(), 16.0),
            neutral_palette=TonalPalette(source_color_hct.get_hue(), 2.0),
            neutral_variant_palette=TonalPalette(source_color_hct.get_hue(), 2.0)
        )
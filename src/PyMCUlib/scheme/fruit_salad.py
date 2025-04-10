# fruit_salad.py

from PyMCUlib.cam.hct import Hct
from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.palettes.tones import TonalPalette
from PyMCUlib.utils.utils import sanitize_degrees_double

class SchemeFruitSalad(DynamicScheme):
    """
    A fruit salad theme - a playful theme that uses colors that are unrelated to
    the source color.
    """
    
    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0):
        """
        Create a fruit salad color scheme based on the source color.
        
        Args:
            source_color_hct: Source color of the scheme in HCT
            is_dark: Whether the scheme is dark or light
            contrast_level: Level of contrast between colors
        """
        super().__init__(
            source_color_hct=source_color_hct,
            variant=Variant.FRUIT_SALAD,
            contrast_level=contrast_level,
            is_dark=is_dark,
            primary_palette=TonalPalette(
                sanitize_degrees_double(source_color_hct.get_hue() - 50.0),
                48.0),
            secondary_palette=TonalPalette(
                sanitize_degrees_double(source_color_hct.get_hue() - 50.0),
                36.0),
            tertiary_palette=TonalPalette(source_color_hct.get_hue(), 36.0),
            neutral_palette=TonalPalette(source_color_hct.get_hue(), 10.0),
            neutral_variant_palette=TonalPalette(source_color_hct.get_hue(), 16.0)
        )
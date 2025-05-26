# fidelity.py

from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dislike.dislike import fix_if_disliked
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.palettes.tones import TonalPalette
from PyMCUlib_cpp.temperature.temperature_cache import TemperatureCache

class SchemeFidelity(DynamicScheme):
    """
    A fidelity theme - a theme that keeps the source color as close as possible.
    """
    
    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0):
        """
        Create a fidelity color scheme based on the source color.
        
        Args:
            source_color_hct: Source color of the scheme in HCT
            is_dark: Whether the scheme is dark or light
            contrast_level: Level of contrast between colors
        """
        # Get complementary color for tertiary palette
        complement_hct = fix_if_disliked(
            TemperatureCache(source_color_hct).get_complement()
        )
        
        # Calculate secondary chroma (max of source_chroma - 32.0 and source_chroma * 0.5)
        secondary_chroma = max(
            source_color_hct.get_chroma() - 32.0,
            source_color_hct.get_chroma() * 0.5
        )
        
        super().__init__(
            source_color_hct=source_color_hct,
            variant=Variant.FIDELITY,
            contrast_level=contrast_level,
            is_dark=is_dark,
            primary_palette=TonalPalette(
                source_color_hct.get_hue(),
                source_color_hct.get_chroma()
            ),
            secondary_palette=TonalPalette(
                source_color_hct.get_hue(),
                secondary_chroma
            ),
            tertiary_palette=TonalPalette(complement_hct),
            neutral_palette=TonalPalette(
                source_color_hct.get_hue(),
                source_color_hct.get_chroma() / 8.0
            ),
            neutral_variant_palette=TonalPalette(
                source_color_hct.get_hue(),
                source_color_hct.get_chroma() / 8.0 + 4.0
            )
        )
# scheme/scheme_rainbow.py

"""
A playful theme - the source color's hue does not appear in the theme.
"""

from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.hct.hct import Hct


class SchemeRainbow(DynamicScheme):
    """A playful theme - the source color's hue does not appear in the theme."""
    
    DEFAULT_SPEC_VERSION = '2021'
    DEFAULT_PLATFORM = 'phone'

    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float):
        """
        Initialize a rainbow theme with a source color.
        
        Args:
            source_color_hct: Source color in HCT color space.
            is_dark: Whether the theme is in dark mode.
            contrast_level: The contrast level of the theme.
        """
        super().__init__({
            'source_color_hct': source_color_hct,
            'variant': Variant.RAINBOW,
            'contrast_level': contrast_level,
            'is_dark': is_dark,
            'platform': SchemeRainbow.DEFAULT_PLATFORM,
            'spec_version': SchemeRainbow.DEFAULT_SPEC_VERSION,
        })
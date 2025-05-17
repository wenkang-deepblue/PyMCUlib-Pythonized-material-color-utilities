# scheme/scheme_content.py
"""
A scheme that places the source color in `Scheme.primary_container`.

Primary Container is the source color, adjusted for color relativity.
It maintains constant appearance in light mode and dark mode.
This adds ~5 tone in light mode, and subtracts ~5 tone in dark mode.
Tertiary Container is the complement to the source color, using
`TemperatureCache`. It also maintains constant appearance.
"""

from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.hct.hct import Hct

class SchemeContent(DynamicScheme):
    """
    A scheme that places the source color in `Scheme.primary_container`.

    Primary Container is the source color, adjusted for color relativity.
    It maintains constant appearance in light mode and dark mode.
    This adds ~5 tone in light mode, and subtracts ~5 tone in dark mode.
    Tertiary Container is the complement to the source color, using
    `TemperatureCache`. It also maintains constant appearance.
    """

    DEFAULT_SPEC_VERSION = '2021'
    DEFAULT_PLATFORM = 'phone'

    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float):
        """
        Construct a new SchemeContent instance.

        Args:
            source_color_hct: The source color of the theme as an HCT color.
            is_dark: Whether the scheme is in dark mode or light mode.
            contrast_level: The contrast level of the theme.
        """
        super().__init__({
            'source_color_hct': source_color_hct,
            'variant': Variant.CONTENT,
            'contrast_level': contrast_level,
            'is_dark': is_dark,
            'platform': SchemeContent.DEFAULT_PLATFORM,
            'spec_version': SchemeContent.DEFAULT_SPEC_VERSION,
        })
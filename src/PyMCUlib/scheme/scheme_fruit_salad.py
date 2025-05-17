# scheme/scheme_fruit_salad.py
"""
A playful theme - the source color's hue does not appear in the theme.
"""

from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.hct.hct import Hct


class SchemeFruitSalad(DynamicScheme):
    """
    A playful theme - the source color's hue does not appear in the theme.
    """

    DEFAULT_SPEC_VERSION = '2021'
    DEFAULT_PLATFORM = 'phone'

    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float):
        """
        Construct a new SchemeFruitSalad instance.

        Args:
            source_color_hct: The source color of the theme as an HCT color.
            is_dark: Whether the scheme is in dark mode or light mode.
            contrast_level: The contrast level of the theme.
        """
        super().__init__({
            'source_color_hct': source_color_hct,
            'variant': Variant.FRUIT_SALAD,
            'contrast_level': contrast_level,
            'is_dark': is_dark,
            'platform': SchemeFruitSalad.DEFAULT_PLATFORM,
            'spec_version': SchemeFruitSalad.DEFAULT_SPEC_VERSION,
        })
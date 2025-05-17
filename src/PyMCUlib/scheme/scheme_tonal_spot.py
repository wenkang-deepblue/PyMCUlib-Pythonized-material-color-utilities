# scheme/scheme_tonal_spot.py

"""
A Dynamic Color theme with low to medium colorfulness and a Tertiary
TonalPalette with a hue related to the source color.

The default Material You theme on Android 12 and 13.
"""

from PyMCUlib.dynamiccolor.color_spec_delegate import SpecVersion
from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme, Platform
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.hct.hct import Hct


class SchemeTonalSpot(DynamicScheme):
    """
    A Dynamic Color theme with low to medium colorfulness and a Tertiary
    TonalPalette with a hue related to the source color.

    The default Material You theme on Android 12 and 13.
    """
    
    DEFAULT_SPEC_VERSION = '2021'
    DEFAULT_PLATFORM = 'phone'

    def __init__(
            self, 
            source_color_hct: Hct, 
            is_dark: bool, 
            contrast_level: float,
            spec_version: SpecVersion = DEFAULT_SPEC_VERSION,
            platform: Platform = DEFAULT_PLATFORM
    ):
        """
        Initialize a tonal spot theme with a source color.
        
        Args:
            source_color_hct: Source color in HCT color space.
            is_dark: Whether the theme is in dark mode.
            contrast_level: The contrast level of the theme.
            spec_version: The Material specification version to use. Defaults to '2021'.
            platform: The platform to use. Defaults to 'phone'.
        """           
        super().__init__({
            'source_color_hct': source_color_hct,
            'variant': Variant.TONAL_SPOT,
            'contrast_level': contrast_level,
            'is_dark': is_dark,
            'platform': platform,
            'spec_version': spec_version,
        })
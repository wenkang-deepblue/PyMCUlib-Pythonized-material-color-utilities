# scheme/scheme_expressive.py
"""
A Dynamic Color theme that is intentionally detached from the source color.
"""

from typing import Optional

from PyMCUlib.dynamiccolor.color_spec_delegate import SpecVersion
from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme, Platform
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.hct.hct import Hct


class SchemeExpressive(DynamicScheme):
    """
    A Dynamic Color theme that is intentionally detached from the source color.
    """

    DEFAULT_SPEC_VERSION = '2021'
    DEFAULT_PLATFORM = 'phone'

    def __init__(
            self, 
            source_color_hct: Hct, 
            is_dark: bool, 
            contrast_level: float,
            spec_version: Optional[SpecVersion] = None,
            platform: Optional[Platform] = None
    ):
        """
        Construct a new SchemeExpressive instance.

        Args:
            source_color_hct: The source color of the theme as an HCT color.
            is_dark: Whether the scheme is in dark mode or light mode.
            contrast_level: The contrast level of the theme.
            spec_version: The specification version to use. Defaults to '2021'.
            platform: The platform to use. Defaults to 'phone'.
        """
        super().__init__({
            'source_color_hct': source_color_hct,
            'variant': Variant.EXPRESSIVE,
            'contrast_level': contrast_level,
            'is_dark': is_dark,
            'platform': platform or SchemeExpressive.DEFAULT_PLATFORM,
            'spec_version': spec_version or SchemeExpressive.DEFAULT_SPEC_VERSION,
        })
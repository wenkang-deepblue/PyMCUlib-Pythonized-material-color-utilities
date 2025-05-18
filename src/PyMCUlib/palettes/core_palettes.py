# palettes/core_palettes.py

"""
Comprises foundational palettes to build a color scheme. Generated from a
source color, these palettes will then be part of a DynamicScheme together
with appearance preferences.
"""

from PyMCUlib.palettes.tonal_palette import TonalPalette


class CorePalettes:
    """
    Comprises foundational palettes to build a color scheme. Generated from a
    source color, these palettes will then be part of a DynamicScheme together
    with appearance preferences.
    """

    def __init__(
            self,
            primary: TonalPalette,
            secondary: TonalPalette,
            tertiary: TonalPalette,
            neutral: TonalPalette,
            neutral_variant: TonalPalette) -> None:
        """
        Initialize a CorePalettes with tonally-consistent palettes.
        
        Args:
            primary: TonalPalette for primary color
            secondary: TonalPalette for secondary color
            tertiary: TonalPalette for tertiary color
            neutral: TonalPalette for neutral color
            neutral_variant: TonalPalette for neutral variant color
        """
        self.primary = primary
        self.secondary = secondary
        self.tertiary = tertiary
        self.neutral = neutral
        self.neutral_variant = neutral_variant
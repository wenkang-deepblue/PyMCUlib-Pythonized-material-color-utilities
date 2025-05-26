# core.py

from dataclasses import dataclass
from PyMCUlib_cpp.palettes.tones import TonalPalette
from PyMCUlib_cpp.utils.utils import Argb

@dataclass
class CorePalettes:
    """
    Comprises foundational palettes to build a color scheme. Generated from a
    source color, these palettes will then be part of a [DynamicScheme] together
    with appearance preferences.
    """
    primary: TonalPalette
    secondary: TonalPalette
    tertiary: TonalPalette
    neutral: TonalPalette
    neutral_variant: TonalPalette
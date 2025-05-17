# palettes/__init__.py

# --- tonal_palette ---
from PyMCUlib.palettes.tonal_palette import TonalPalette, KeyColor

# --- core_palette ---
from PyMCUlib.palettes.core_palette import CorePalette

# --- core_palettes ---
from PyMCUlib.palettes.core_palettes import CorePalettes

__all__ = [
    "TonalPalette",
    "KeyColor",
    "CorePalette",
    "CorePalettes",
]
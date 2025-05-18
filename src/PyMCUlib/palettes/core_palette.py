# palettes/core_palette.py

"""
An intermediate concept between the key color for a UI theme, and a full
color scheme. 5 sets of tones are generated, all except one use the same hue
as the key color, and all vary in chroma.
"""

from typing import TypedDict, Optional

from PyMCUlib.hct.hct import Hct
from PyMCUlib.palettes.tonal_palette import TonalPalette


# Primary color is required; other colors are optional.
class CorePaletteColorsBase(TypedDict):
    """
    Colors needed to create a core palette.
    
    @deprecated Use DynamicScheme for color scheme generation.
    Use CorePalettes for core palettes container class.
    """
    primary: int

class CorePaletteColors(CorePaletteColorsBase, total=False):
    secondary: Optional[int]
    tertiary: Optional[int]
    neutral: Optional[int]
    neutralVariant: Optional[int]
    error: Optional[int]


class CorePalette:
    """
    An intermediate concept between the key color for a UI theme, and a full
    color scheme. 5 sets of tones are generated, all except one use the same hue
    as the key color, and all vary in chroma.
    
    @deprecated Use DynamicScheme for color scheme generation.
    Use CorePalettes for core palettes container class.
    """

    def __init__(self, argb: int, is_content: bool) -> None:
        """
        Initialize a CorePalette with a color and content flag.
        
        Args:
            argb: ARGB representation of a color
            is_content: Whether this palette is for content
        """
        hct = Hct.from_int(argb)
        hue = hct.hue
        chroma = hct.chroma
        
        if is_content:
            self.a1 = TonalPalette.from_hue_and_chroma(hue, chroma)
            self.a2 = TonalPalette.from_hue_and_chroma(hue, chroma / 3)
            self.a3 = TonalPalette.from_hue_and_chroma(hue + 60, chroma / 2)
            self.n1 = TonalPalette.from_hue_and_chroma(hue, min(chroma / 12, 4))
            self.n2 = TonalPalette.from_hue_and_chroma(hue, min(chroma / 6, 8))
        else:
            self.a1 = TonalPalette.from_hue_and_chroma(hue, max(48, chroma))
            self.a2 = TonalPalette.from_hue_and_chroma(hue, 16)
            self.a3 = TonalPalette.from_hue_and_chroma(hue + 60, 24)
            self.n1 = TonalPalette.from_hue_and_chroma(hue, 4)
            self.n2 = TonalPalette.from_hue_and_chroma(hue, 8)
            
        self.error = TonalPalette.from_hue_and_chroma(25, 84)

    @staticmethod
    def of(argb: int) -> 'CorePalette':
        """
        Create a standard CorePalette from a color.
        
        Args:
            argb: ARGB representation of a color
            
        Returns:
            Standard CorePalette
            
        @deprecated Use DynamicScheme for color scheme generation.
        Use CorePalettes for core palettes container class.
        """
        return CorePalette(argb, False)

    @staticmethod
    def content_of(argb: int) -> 'CorePalette':
        """
        Create a content CorePalette from a color.
        
        Args:
            argb: ARGB representation of a color
            
        Returns:
            Content CorePalette
            
        @deprecated Use DynamicScheme for color scheme generation.
        Use CorePalettes for core palettes container class.
        """
        return CorePalette(argb, True)

    @staticmethod
    def from_colors(colors: CorePaletteColors) -> 'CorePalette':
        """
        Create a CorePalette from a set of colors.
        
        Args:
            colors: CorePaletteColors
            
        Returns:
            Standard CorePalette
            
        @deprecated Use DynamicScheme for color scheme generation.
        Use CorePalettes for core palettes container class.
        """
        return CorePalette._create_palette_from_colors(False, colors)

    @staticmethod
    def content_from_colors(colors: CorePaletteColors) -> 'CorePalette':
        """
        Create a content CorePalette from a set of colors.
        
        Args:
            colors: CorePaletteColors
            
        Returns:
            Content CorePalette
            
        @deprecated Use DynamicScheme for color scheme generation.
        Use CorePalettes for core palettes container class.
        """
        return CorePalette._create_palette_from_colors(True, colors)

    @staticmethod
    def _create_palette_from_colors(
            content: bool,
            colors: CorePaletteColors) -> 'CorePalette':
        """
        Internal method to create a CorePalette from colors.
        
        Args:
            content: Whether this palette is for content
            colors: CorePaletteColors
            
        Returns:
            CorePalette
        """
        palette = CorePalette(colors["primary"], content)
        
        if "secondary" in colors and colors["secondary"] is not None:
            p = CorePalette(colors["secondary"], content)
            palette.a2 = p.a1
            
        if "tertiary" in colors and colors["tertiary"] is not None:
            p = CorePalette(colors["tertiary"], content)
            palette.a3 = p.a1
            
        if "error" in colors and colors["error"] is not None:
            p = CorePalette(colors["error"], content)
            palette.error = p.a1
            
        if "neutral" in colors and colors["neutral"] is not None:
            p = CorePalette(colors["neutral"], content)
            palette.n1 = p.n1
            
        if "neutralVariant" in colors and colors["neutralVariant"] is not None:
            p = CorePalette(colors["neutralVariant"], content)
            palette.n2 = p.n2
            
        return palette
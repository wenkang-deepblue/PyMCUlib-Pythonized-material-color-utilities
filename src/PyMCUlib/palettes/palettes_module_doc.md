# Palettes Component Documentation
## Overview
The Palettes component provides tools to create and manipulate harmonious color sets for Material Design themes. This component bridges the gap between a single key color and a full color scheme by generating consistent tonal variations that maintain harmony while providing sufficient contrast for UI elements.

## Key Features
Generate tonally-consistent color palettes from key colors
Create variations with consistent hue but different chroma values
Support for both standard UI and content-focused color generation
Consistent tone mapping across different hues and chromas
Mathematical approach to finding optimal colors within sRGB gamut

## Core Classes
`TonalPalette`
A convenience class for retrieving colors that are constant in hue and chroma, but vary in tone. It provides a harmonious range of colors from light to dark.
```python
class TonalPalette:
    def __init__(self, hue: float, chroma: float, key_color: Hct)
    
    @staticmethod
    def from_int(argb: int) -> 'TonalPalette'
    
    @staticmethod
    def from_hct(hct: Hct) -> 'TonalPalette'
    
    @staticmethod
    def from_hue_and_chroma(hue: float, chroma: float) -> 'TonalPalette'
    
    def tone(self, tone: float) -> int
    
    def get_hct(self, tone: float) -> Hct
```
`KeyColor`
Represents the hue and chroma of a tonal palette. Uses binary search to find the most appropriate tone for a requested chroma.
```python
class KeyColor:
    def __init__(self, hue: float, requested_chroma: float)
    
    def create(self) -> Hct
    
    def _max_chroma(self, tone: float) -> float
```
`CorePalette` (**Deprecated**)
An intermediate concept between a key color and a full color scheme. This class is deprecated; use `CorePalettes` or `DynamicScheme` for theme generation. Generates 3 accent tonal palettes (a1, a2, a3), 2 neutral tonal palettes (n1, n2), and a fixed error palette (error, hue=25°, chroma=84).
```python
class CorePalette:
    def __init__(self, argb: int, is_content: bool)
    
    @staticmethod
    def of(argb: int) -> 'CorePalette'
    
    @staticmethod
    def content_of(argb: int) -> 'CorePalette'
    
    @staticmethod
    def from_colors(colors: CorePaletteColors) -> 'CorePalette'
    
    @staticmethod
    def content_from_colors(colors: CorePaletteColors) -> 'CorePalette'
```
`CorePalettes`
A container for the foundational palettes needed to build a color scheme. Generated from a source color, these palettes will then be part of a DynamicScheme together with appearance preferences.
```python
class CorePalettes:
    def __init__(
            self,
            primary: TonalPalette,
            secondary: TonalPalette,
            tertiary: TonalPalette,
            neutral: TonalPalette,
            neutral_variant: TonalPalette)
```
## Main Function Categories

### TonalPalette Creation
- `TonalPalette.from_int(argb)`: Creates a tonal palette from an ARGB integer.
- `TonalPalette.from_hct(hct)`: Creates a tonal palette from an HCT instance.
- `TonalPalette.from_hue_and_chroma(hue, chroma)`: Creates a palette from hue and chroma values.

### Color Retrieval
- `tone(tone)`: Gets an ARGB color from a tonal palette with the specified tone (0-100).
- `get_hct(tone)`: Gets an HCT object for a specific tone.

### CorePalette Generation
- `CorePalette.of(argb)`: Creates a standard core palette from a color.
- `CorePalette.content_of(argb)`: Creates a content-focused core palette from a color.
- `CorePalette.from_colors(colors)`: Creates a core palette from a set of colors.
- `CorePalette.content_from_colors(colors)`: Creates a content core palette from a set of colors.

## Usage Examples

### Creating a TonalPalette
```python
from PyMCUlib.palettes.tonal_palette import TonalPalette
from PyMCUlib.utils.string_utils import argb_from_hex

# Create a TonalPalette from a hex color
blue_argb = argb_from_hex("#0000FF")
blue_palette = TonalPalette.from_int(blue_argb)

# Create a TonalPalette from hue and chroma values
custom_palette = TonalPalette.from_hue_and_chroma(270, 80)  # Purple with high chroma

# Get colors at various tones
white = blue_palette.tone(100)     # Lightest tone
light_blue = blue_palette.tone(80) # Light tone
mid_blue = blue_palette.tone(50)   # Medium tone
dark_blue = blue_palette.tone(20)  # Dark tone
black = blue_palette.tone(0)       # Darkest tone
hct_obj = blue_palette.get_hct(50) # Get the HCT object for a specific tone
```
### Working with CorePalette
```python
from PyMCUlib.palettes.core_palette import CorePalette
from PyMCUlib.utils.string_utils import argb_from_hex

# Create a CorePalette from a primary color
red_argb = argb_from_hex("#FF0000")
palette = CorePalette.of(red_argb)

# Access the different tonal palettes
primary_colors = palette.a1
secondary_colors = palette.a2
tertiary_colors = palette.a3
neutral_colors = palette.n1
neutral_variant_colors = palette.n2
error_colors = palette.error

# Get colors for UI elements at appropriate tones
primary_container = primary_colors.tone(90)
on_primary_container = primary_colors.tone(10)
primary = primary_colors.tone(40)
on_primary = primary_colors.tone(100)

# Create a content-optimized palette
content_palette = CorePalette.content_of(red_argb)
```
### Creating a Custom CorePalette
```python
from PyMCUlib.palettes.core_palette import CorePalette, CorePaletteColors
from PyMCUlib.utils.string_utils import argb_from_hex

# Define a custom palette with specific colors for each role
colors: CorePaletteColors = {
    "primary": argb_from_hex("#6750A4"),      # Purple
    "secondary": argb_from_hex("#958DA5"),    # Light purple
    "tertiary": argb_from_hex("#B58392"),     # Pink
    "neutral": argb_from_hex("#939094"),      # Gray
    "neutralVariant": argb_from_hex("#929094") # Slightly different gray
}

# Create a standard palette from these colors
custom_palette = CorePalette.from_colors(colors)

# Create a content palette from these colors
content_palette = CorePalette.content_from_colors(colors)
```
### Using CorePalettes for Schemes
```python
from PyMCUlib.palettes.core_palettes import CorePalettes
from PyMCUlib.palettes.tonal_palette import TonalPalette

# Create individual tonal palettes
primary_palette = TonalPalette.from_hue_and_chroma(270, 40)
secondary_palette = TonalPalette.from_hue_and_chroma(270, 16)
tertiary_palette = TonalPalette.from_hue_and_chroma(330, 24)
neutral_palette = TonalPalette.from_hue_and_chroma(270, 4)
neutral_variant_palette = TonalPalette.from_hue_and_chroma(270, 8)

# Create a CorePalettes object
palettes = CorePalettes(
    primary=primary_palette,
    secondary=secondary_palette,
    tertiary=tertiary_palette,
    neutral=neutral_palette,
    neutral_variant=neutral_variant_palette
)

# These palettes can be used to build a dynamic scheme
# For example, retrieving colors for a light theme:
bg_color = palettes.neutral.tone(99)
primary_color = palettes.primary.tone(40)
secondary_color = palettes.secondary.tone(40)
```
## Implementation Notes

### TonalPalette
- Caches generated colors to avoid recalculating ARGB values
- Uses the `KeyColor` class to find the appropriate tone for a given hue and chroma
- Maintains consistent hue and chroma while varying tone
- Provides a consistent interface for getting colors regardless of how the palette was created

### KeyColor
- Performs binary search to find the best tone for a given hue and chroma
- Handles cases where requested chroma is higher than what's achievable
- Finds closest achievable color that maintains requested hue and chroma
- Starts search from T50 (tone 50) as it typically has the most available chroma

### CorePalette
- Generates 5 tonal palettes: 3 accent palettes (a1, a2, a3) and 2 neutral palettes (n1, n2)
- Additionally creates an error palette with a fixed hue of 25° and chroma of 84
- `of()` method creates palettes optimized for UI elements
- `content_of()` method creates palettes optimized for content (text, images, etc.)
- Allows creating custom palettes from a set of predefined colors

### CorePalettes
- Provides a cleaner, more modern API compared to CorePalette
- Designed to work with `DynamicScheme` for theme generation
- Uses more semantic naming (primary, secondary, tertiary)
- Does not include an error palette, which is handled separately

### Dependencies
- `PyMCUlib.hct.hct`: For color manipulation using the HCT color space
- `PyMCUlib.utils.string_utils`: For hex color conversion (in examples)

## Related Components
- `hct`: HCT color space implementation that combines CAM16 hue/chroma with L* tone
- `utils`: Utility functions for color manipulation
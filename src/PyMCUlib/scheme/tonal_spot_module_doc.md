# <center> Tonal Spot Module Documentation </center>

## Overview
`SchemeTonalSpot` is a class that generates a tonal spot color scheme based on a source color. This is the standard color scheme in Material Design 3, featuring a primary color, a secondary color with lower chroma, and a tertiary accent color that complements the source color.

Tonal spot schemes are designed to provide a harmonious set of colors that work well together in UI design, with complementary accent colors that create visual interest while maintaining a coherent design language.

## Usage

```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.tonal_spot import SchemeTonalSpot

# Create a tonal spot scheme from a color
# Example with blue color (0xff0000ff) in dark mode
source_color = Hct.from_int(0xff0000ff)
is_dark = True
scheme = SchemeTonalSpot(source_color, is_dark)

# Access colors from the scheme
primary_color = scheme.get_primary()  # Returns ARGB value (e.g., 0xFF6750A4)
on_primary_color = scheme.get_on_primary()  # Returns ARGB value (e.g., 0xFFFFFFFF)
primary_container = scheme.get_primary_container()  # Returns ARGB value (e.g., 0xFFEADDFF)

# For higher contrast, use the contrast_level parameter (0.0 to 1.0)
high_contrast_scheme = SchemeTonalSpot(source_color, is_dark, contrast_level=0.5)
```

## Constructor

```python
def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0):
    """
    Create a tonal spot color scheme based on the source color.
    
    Args:
        source_color_hct: Source color of the scheme in HCT
        is_dark: Whether the scheme is dark or light
        contrast_level: Level of contrast between colors (0.0 to 1.0, default is 0.0)
    """
```

## Parameters

* `source_color_hct`: A color in HCT color space that serves as the source color for the scheme.
* `is_dark`: A boolean indicating whether the scheme should be dark (True) or light (False).
* `contrast_level`: A float between 0.0 and 1.0 that adjusts the contrast of the scheme. Default is 0.0.

## Color Palettes
The `SchemeTonalSpot` class generates the following palettes:

1. **Primary Palette**: Based on the source color's hue with a chroma of 36.0.
2. **Secondary Palette**: Based on the source color's hue with a reduced chroma of 16.0.
3. **Tertiary Palette**: A complementary color palette with the source color's hue rotated by 60 degrees and a chroma of 24.0.
4. **Neutral Palette**: Based on the source color's hue with a very low chroma of 6.0.
5. **Neutral Variant Palette**: Based on the source color's hue with a low chroma of 8.0.

## Available Colors
Through inheritance from `DynamicScheme`, `SchemeTonalSpot` provides access to a wide range of Material Design 3 colors. All methods return ARGB integer values.

### Primary Colors
* `get_primary() -> int`: The primary color
* `get_on_primary() -> int`: Color for content on the primary color
* `get_primary_container() -> int`: Container color derived from primary
* `get_on_primary_container() -> int`: Color for content on primary container
* `get_inverse_primary() -> int`: Inverse of the primary color for contrast

### Secondary Colors
* `get_secondary() -> int`: The secondary color
* `get_on_secondary() -> int`: Color for content on the secondary color
* `get_secondary_container() -> int`: Container color derived from secondary
* `get_on_secondary_container() -> int`: Color for content on secondary container

### Tertiary Colors
* `get_tertiary() -> int`: The tertiary color
* `get_on_tertiary() -> int`: Color for content on the tertiary color
* `get_tertiary_container() -> int`: Container color derived from tertiary
* `get_on_tertiary_container() -> int`: Color for content on tertiary container

### Surface Colors
* `get_surface() -> int`: The main surface color
* `get_on_surface() -> int`: Color for content on the surface
* `get_surface_variant() -> int`: An alternative surface color
* `get_on_surface_variant() -> int`: Color for content on surface variant
* `get_surface_bright() -> int`: A brighter variant of the surface color
* `get_surface_dim() -> int`: A dimmer variant of the surface color
* `get_surface_container() -> int`: Main container surface color
* `get_surface_container_low() -> int`: Low container surface color
* `get_surface_container_high() -> int`: High container surface color
* `get_surface_container_lowest() -> int`: Lowest container surface color
* `get_surface_container_highest() -> int`: Highest container surface color

### Background Colors
* `get_background() -> int`: The background color
* `get_on_background() -> int`: Color for content on the background

### Other Colors
* `get_outline() -> int`: Color for UI outlines
* `get_outline_variant() -> int`: Variant color for UI outlines
* `get_shadow() -> int`: Color for shadows
* `get_scrim() -> int`: Color for scrim overlays
* `get_inverse_surface() -> int`: Opposite of the surface color
* `get_inverse_on_surface() -> int`: Opposite of the on-surface color
* `get_surface_tint() -> int`: Tint color for surfaces

### Error Colors
* `get_error() -> int`: The error color
* `get_on_error() -> int`: Color for content on the error color
* `get_error_container() -> int`: Container color derived from error
* `get_on_error_container() -> int`: Color for content on error container

### Fixed Colors
* `get_primary_fixed() -> int`: Fixed primary color (not affected by light/dark mode)
* `get_primary_fixed_dim() -> int`: Dimmer fixed primary color
* `get_on_primary_fixed() -> int`: Color for content on fixed primary
* `get_on_primary_fixed_variant() -> int`: Variant color for content on fixed primary
* `get_secondary_fixed() -> int`: Fixed secondary color
* `get_secondary_fixed_dim() -> int`: Dimmer fixed secondary color
* `get_on_secondary_fixed() -> int`: Color for content on fixed secondary
* `get_on_secondary_fixed_variant() -> int`: Variant color for content on fixed secondary
* `get_tertiary_fixed() -> int`: Fixed tertiary color
* `get_tertiary_fixed_dim() -> int`: Dimmer fixed tertiary color
* `get_on_tertiary_fixed() -> int`: Color for content on fixed tertiary
* `get_on_tertiary_fixed_variant() -> int`: Variant color for content on fixed tertiary

## Example

```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.tonal_spot import SchemeTonalSpot

# Create a tonal spot scheme from a color
source_color = Hct.from_int(0xff4285F4)  # Google Blue
is_dark = False  # Light theme
scheme = SchemeTonalSpot(source_color, is_dark)

# Access various colors for UI components
primary = scheme.get_primary()  # Main brand color
primary_container = scheme.get_primary_container()  # Container color derived from primary
secondary = scheme.get_secondary()  # Secondary color for UI elements
tertiary = scheme.get_tertiary()  # Accent color for highlighting
background = scheme.get_background()  # Background color
surface = scheme.get_surface()  # Surface color for cards, sheets, etc.
outline = scheme.get_outline()  # Color for UI element outlines

# Sample output (actual values will vary based on the source color)
# primary: 0xFF1A73E8
# primary_container: 0xFFD3E3FD
# secondary: 0xFF3C4043
# tertiary: 0xFF0B8043
# background: 0xFFFAFAFA
# surface: 0xFFFEFEFE
# outline: 0xFF747775
```

## Inheritance

`SchemeTonalSpot` inherits from `DynamicScheme`, which is the base class for all Material Design 3 color schemes. The class handles the complex logic of generating accessible and harmonious color combinations based on a source color.

## Related Classes
* `DynamicScheme`: The base class for all color schemes
* `SchemeMonochrome`: A monochromatic color scheme with a single hue
* `SchemeNeutral`: A neutral color scheme with minimal color
* `SchemeExpressive`: A vibrant, expressive color scheme with unconventional colors
* `SchemeFidelity`: A scheme that preserves the source color exactly
* `SchemeVibrant`: A scheme with fully saturated, vivid colors
* `SchemeContent`: A scheme that stays closer to the source color with analogous hues for tertiary colors
* `SchemeRainbow`: A playful scheme with high colorfulness
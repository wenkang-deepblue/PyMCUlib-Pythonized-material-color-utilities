# <center> Fidelity Module Documentation </center>

## Overview
`SchemeFidelity` is a class that generates a fidelity color scheme based on a source color. This color scheme is designed to preserve the original source color as closely as possible, maintaining high fidelity to the user's color selection while creating a harmonious palette for UI design.

The fidelity scheme uses the exact hue and chroma from the source color for the primary palette, creating a design that stays true to the user's chosen color. Secondary colors use the same hue with reduced chroma, and tertiary colors are derived from a complementary color.

## Usage

```python
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.fidelity import SchemeFidelity

# Create a fidelity scheme from a color
# Example with blue color (0xff0000ff) in dark mode
source_color = Hct.from_int(0xff0000ff)
is_dark = True
scheme = SchemeFidelity(source_color, is_dark)

# Access colors from the scheme
primary_color = scheme.get_primary()
on_primary_color = scheme.get_on_primary()
primary_container = scheme.get_primary_container()

# For higher contrast, use the contrast_level parameter (0.0 to 1.0)
high_contrast_scheme = SchemeFidelity(source_color, is_dark, contrast_level=0.5)
```

## Parameters
* `source_color_hct`: A color in HCT color space that serves as the source color for the scheme.
* `is_dark`: A boolean indicating whether the scheme should be dark (True) or light (False).
* `contrast_level`: A float between 0.0 and 1.0 that adjusts the contrast of the scheme. Default is 0.0.

## Color Generation Process
The `SchemeFidelity` class generates its color palettes using the following processes:

1. __Primary Palette__: Uses the source color's original hue and chroma without modification, preserving the exact color.

2. __Secondary Palette__: Uses the source color's hue but with reduced chroma, calculated as the maximum of (source chroma - 32.0) and (source chroma * 0.5).

3. __Tertiary Palette__: Uses a complementary color obtained from the `TemperatureCache`. The complementary color is processed through the `fix_if_disliked` function to ensure harmonious color results.

4. __Neutral Palette__: Uses the source color's hue with significantly reduced chroma (source chroma / 8.0).

5. __Neutral Variant Palette__: Uses the source color's hue with slightly higher chroma than the neutral palette (source chroma / 8.0 + 4.0).

## Key Supporting Functions
* `TemperatureCache`: Provides a system for generating complementary colors based on color temperature principles.
* `fix_if_disliked`: A utility function that adjusts colors that might be considered unpleasant or problematic in interface design.

## Available Colors
Through inheritance from `DynamicScheme`, `SchemeFidelity` provides access to a wide range of Material Design 3 colors, including:

### Primary Colors
* `get_primary()`: The primary color
* `get_on_primary()`: Color for content on the primary color
* `get_primary_container()`: Container color derived from primary
* `get_on_primary_container()`: Color for content on primary container

### Secondary Colors
* `get_secondary()`: The secondary color
* `get_on_secondary()`: Color for content on the secondary color
* `get_secondary_container()`: Container color derived from secondary
* `get_on_secondary_container()`: Color for content on secondary container

### Tertiary Colors
* `get_tertiary()`: The tertiary color
* `get_on_tertiary()`: Color for content on the tertiary color
* `get_tertiary_container()`: Container color derived from tertiary
* `get_on_tertiary_container()`: Color for content on tertiary container

### Surface Colors
* `get_surface()`: The main surface color
* `get_on_surface()`: Color for content on the surface
* `get_surface_variant()`: An alternative surface color
* `get_on_surface_variant()`: Color for content on surface variant
And many more surface variations: `get_surface_bright()`, `get_surface_dim()`, etc.

### Other Colors
* `get_outline()`: Color for UI outlines
* `get_shadow()`: Color for shadows
* `get_inverse_surface()`: Opposite of the surface color
* `get_inverse_primary()`: Opposite of the primary color
And many more, including error colors and fixed colors

## Example
```python
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.fidelity import SchemeFidelity

# Create a fidelity scheme from a color
source_color = Hct.from_int(0xff4285F4)  # Google Blue
is_dark = False  # Light theme
scheme = SchemeFidelity(source_color, is_dark)

# Access various colors for UI components
primary = scheme.get_primary()  # Main brand color (exact match to source)
primary_container = scheme.get_primary_container()  # Container color derived from primary
secondary = scheme.get_secondary()  # Secondary color (same hue, reduced chroma)
tertiary = scheme.get_tertiary()  # Accent color (complementary)
background = scheme.get_background()  # Background color
surface = scheme.get_surface()  # Surface color for cards, sheets, etc.
outline = scheme.get_outline()  # Color for UI element outlines
```

## Related Classes
* `DynamicScheme`: The base class for all color schemes.
* `SchemeMonochrome`: A monochromatic color scheme with a single hue.
* `SchemeNeutral`: A neutral color scheme with minimal color.
* `SchemeTonalSpot`: The standard Material You color scheme with complementary accent colors.
* `SchemeVibrant`: A vibrant color scheme with highly saturated colors.
* `SchemeExpressive`: A scheme with unconventional, expressive colors.
* `SchemeContent`: A variant that's closer to the source color.
* `SchemeRainbow`: A playful scheme with high colorfulness.
* `SchemeFruitSalad`: A playful scheme that uses colors unrelated to the source color.

# <center> Vibrant Module Documentation </center>

## Overview
`SchemeVibrant` is a class that generates a vibrant color scheme based on a source color. This color scheme is designed to be eye-catching and uses highly saturated colors with the primary palette having a high chroma value (200.0), creating a vivid and energetic visual identity.

The vibrant scheme uses intelligent color rotation algorithms to create harmonious secondary and tertiary colors that complement the primary color while maintaining the vibrant aesthetic.

## Usage

```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.vibrant import SchemeVibrant

# Create a vibrant scheme from a color
# Example with blue color (0xff0000ff) in dark mode
source_color = Hct.from_int(0xff0000ff)
is_dark = True
scheme = SchemeVibrant(source_color, is_dark)

# Access colors from the scheme
primary_color = scheme.get_primary()
on_primary_color = scheme.get_on_primary()
primary_container = scheme.get_primary_container()

# For higher contrast, use the contrast_level parameter (0.0 to 1.0)
high_contrast_scheme = SchemeVibrant(source_color, is_dark, contrast_level=0.5)
```

## Parameters
* `source_color_hct`: A color in HCT color space that serves as the source color for the scheme.
* `is_dark`: A boolean indicating whether the scheme should be dark (True) or light (False).
* `contrast_level`: A float between 0.0 and 1.0 that adjusts the contrast of the scheme. Default is 0.0.

## Constants
`SchemeVibrant` uses the following constants to calculate color rotations:
* `HUES`: List of hue angles in degrees (0, 41, 61, 101, 131, 181, 251, 301, 360) that define hue intervals.
* `SECONDARY_ROTATIONS`: Rotation angles for secondary colors (18, 15, 10, 12, 15, 18, 15, 12, 12) corresponding to each hue interval.
* `TERTIARY_ROTATIONS`: Rotation angles for tertiary colors (35, 30, 20, 25, 30, 35, 30, 25, 25) corresponding to each hue interval.

## Implementation Details
`SchemeVibrant` creates its vibrant color scheme through the following approach:
1. Primary palette uses the source color's hue with a very high chroma of 200.0 to create maximum vibrancy.
2. Secondary palette uses a rotated hue (computed via `get_rotated_hue` function with `HUES` and `SECONDARY_ROTATIONS`) with a lower chroma of 24.0.
3. Tertiary palette uses a different rotated hue (computed via `get_rotated_hue` function with `HUES` and `TERTIARY_ROTATIONS`) with a chroma of 32.0.
4. Neutral palette retains the source color's hue but with a much lower chroma of 10.0.
5. Neutral variant palette also retains the source color's hue with a slightly higher chroma of 12.0.

## Color Palettes
The SchemeVibrant class generates the following palettes:
1. __Primary Palette__: Based on the source color's hue with a very high chroma of 200.0 for maximum vibrancy.
2. __Secondary Palette__: Based on a rotated hue with a chroma of 24.0.
3. __Tertiary Palette__: Based on a different rotated hue with a chroma of 32.0.
4. __Neutral Palette__: Based on the source color's hue with a low chroma of 10.0.
5. __Neutral Variant Palette__: Based on the source color's hue with a slightly higher chroma of 12.0.

## Available Colors
Through inheritance from `DynamicScheme`, `SchemeVibrant` provides access to a wide range of Material Design 3 colors, including:

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
* `get_surface_bright()`: A brighter variant of the surface color
* `get_surface_dim()`: A dimmer variant of the surface color
* `get_surface_container_lowest()`: The lowest surface container color
* `get_surface_container_low()`: A low surface container color
* `get_surface_container()`: The main surface container color
* `get_surface_container_high()`: A high surface container color
* `get_surface_container_highest()`: The highest surface container color

### Other Colors
* `get_outline()`: Color for UI outlines
* `get_outline_variant()`: Alternative color for UI outlines
* `get_shadow()`: Color for shadows
* `get_scrim()`: Color for scrims (semi-transparent overlays)
* `get_inverse_surface()`: Opposite of the surface color
* `get_inverse_primary()`: Opposite of the primary color
* `get_inverse_on_surface()`: Opposite of the on-surface color

## Example
```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.vibrant import SchemeVibrant

# Create a vibrant scheme from a color
source_color = Hct.from_int(0xffFF5722)  # Deep Orange
is_dark = False  # Light theme
scheme = SchemeVibrant(source_color, is_dark)

# Access various colors for UI components
primary = scheme.get_primary()  # Main brand color (highly saturated)
primary_container = scheme.get_primary_container()  # Container color derived from primary
secondary = scheme.get_secondary()  # Secondary color (with hue rotation)
tertiary = scheme.get_tertiary()  # Accent color (with different hue rotation)
background = scheme.get_background()  # Background color
surface = scheme.get_surface()  # Surface color for cards, sheets, etc.
outline = scheme.get_outline()  # Color for UI element outlines
```

## Related Classes
* `DynamicScheme`: The base class for all color schemes.
* `SchemeMonochrome`: A monochromatic color scheme with a single hue.
* `SchemeNeutral`: A neutral color scheme with minimal color.
* `SchemeTonalSpot`: The standard Material You color scheme with complementary accent colors.
* `SchemeExpressive`: A scheme with unconventional, expressive colors.
* `SchemeFidelity`: A scheme that preserves the source color exactly.
* `SchemeContent`: A scheme that's closer to the source color with slightly reduced chroma for secondary colors.
* `SchemeRainbow`: A playful scheme with high colorfulness.
* `SchemeFruitSalad`: A playful scheme that uses colors unrelated to the source color.
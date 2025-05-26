# <center> Expressive Module Documentation </center>

## Overview
`SchemeExpressive` is a class that generates an expressive color scheme based on a source color. This color scheme is designed to be bold and unconventional, using dramatically shifted hues and specific chromatic values to create a visually striking and unique aesthetic.

The expressive scheme is characterized by a primary palette that shifts the source color's hue by 240 degrees, creating a dramatically different primary color. The secondary and tertiary colors are calculated using specialized rotation algorithms that produce harmonious yet unconventional color combinations.

## Usage

```python
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.expressive import SchemeExpressive

# Create an expressive scheme from a color
# Example with blue color (0xff0000ff) in dark mode
source_color_hct = Hct.from_int(0xff0000ff)
is_dark = True
scheme = SchemeExpressive(source_color_hct, is_dark)

# Access colors from the scheme
primary_color = scheme.get_primary()
on_primary_color = scheme.get_on_primary()
primary_container = scheme.get_primary_container()

# For higher contrast, use the contrast_level parameter (0.0 to 1.0)
high_contrast_scheme = SchemeExpressive(source_color_hct, is_dark, contrast_level=0.5)
```

## Parameters
* `source_color_hct`: A color in HCT color space that serves as the source color for the scheme.
* `is_dark`: A boolean indicating whether the scheme should be dark (True) or light (False).
* `contrast_level`: A float between 0.0 and 1.0 that adjusts the contrast of the scheme. Default is 0.0.

## Color Generation Process
The `SchemeExpressive` class generates the following palettes:

1. __Primary Palette__: Based on the source color's hue shifted by +240 degrees with a chroma of 40.0.

2. __Secondary Palette__: Based on a rotated hue calculated using the `get_rotated_hue` method with the HUES and SECONDARY_ROTATIONS arrays. The resulting color has a chroma of 24.0.

3. __Tertiary Palette__: Based on a different rotated hue calculated using the `get_rotated_hue` method with the HUES and TERTIARY_ROTATIONS arrays. The resulting color has a chroma of 32.0.

4. __Neutral Palette__: Based on the source color's hue shifted by +15 degrees with a chroma of 8.0.

5. __Neutral Variant Palette__: Based on the source color's hue shifted by +15 degrees with a chroma of 12.0.

## Key Supporting Functions
* `get_rotated_hue`: A static method inherited from `DynamicScheme` that calculates a new hue based on the source color's hue and predefined rotation patterns.
* `HUES`: An array defining key hue points at [0, 21, 51, 121, 151, 191, 271, 321, 360].
* `SECONDARY_ROTATIONS`: An array defining rotation values for secondary colors at each hue point.
* `TERTIARY_ROTATIONS`: An array defining rotation values for tertiary colors at each hue point.

## Available Colors
Through inheritance from `DynamicScheme`, `SchemeExpressive` provides access to a wide range of Material Design 3 colors, including:

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
from PyMCUlib_cpp.scheme.expressive import SchemeExpressive

# Create an expressive scheme from a color
source_color_hct = Hct.from_int(0xffFF5722)  # Deep Orange
is_dark = False  # Light theme
scheme = SchemeExpressive(source_color_hct, is_dark)

# Access various colors for UI components
primary = scheme.get_primary()  # Main brand color (dramatically shifted)
primary_container = scheme.get_primary_container()  # Container color derived from primary
secondary = scheme.get_secondary()  # Secondary color (with calculated hue rotation)
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
* `SchemeVibrant`: A vibrant color scheme with highly saturated colors.
* `SchemeFidelity`: A scheme that preserves the source color exactly.
* `SchemeContent`: A scheme that stays close to the source color.
* `SchemeRainbow`: A playful scheme with high colorfulness.
* `SchemeFruitSalad`: A playful scheme that uses colors unrelated to the source color.

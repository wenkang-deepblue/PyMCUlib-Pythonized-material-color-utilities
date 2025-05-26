# <center> Rainbow Module Documentation </center>

__SchemeRainbow__ is a module of component `Scheme` of the Material Color Utilities library. It creates a rainbow color scheme based on a source color.

## Overview

A rainbow theme is a playful theme with high colorfulness. It uses the source color as the primary color, with specific chroma values for different palettes and a tertiary color with a hue 60 degrees away from the source color. This creates a vibrant, multi-colored theme while maintaining cohesiveness.

## Usage

```python
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.rainbow import SchemeRainbow

# Create a color in HCT
hct = Hct.from_int(0xFF0000FF)  # Blue

# Create a rainbow scheme
scheme = SchemeRainbow(hct, False)  # Light theme

# Access colors
primary_color = scheme.get_primary()  # Returns an ARGB integer
secondary_color = scheme.get_secondary()  # Returns an ARGB integer
tertiary_color = scheme.get_tertiary()  # Returns an ARGB integer
```

## Constructor
`SchemeRainbow(source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0)`
Creates a rainbow color scheme.

## Parameters
* `source_color_hct`: Hct - The source color for the scheme.
* `is_dark`: `bool` - Whether the scheme is dark or light.
* `contrast_level`: `float` - The contrast level for the scheme. Default is 0.0.

## Variant
SchemeRainbow uses `Variant.RAINBOW` from the `Variant` enum. This variant is designed to create highly colorful, playful themes that work well for expressive, creative applications where a wider color range is desired.

## Palettes
The rainbow scheme includes the following palettes:

* `primary_palette`: A palette with the source color's hue and a chroma of 48.0, providing vibrant primary colors.
* `secondary_palette`: A palette with the source color's hue and a chroma of 16.0, creating more subtle secondary colors.
* `tertiary_palette`: A palette with a hue 60 degrees from the source color's hue and a chroma of 24.0, introducing complementary colors for accents.
* `neutral_palette`: A palette with the source color's hue and a chroma of 0.0, providing neutral colors for backgrounds and text containers.
* `neutral_variant_palette`: A palette with the source color's hue and a chroma of 0.0, providing alternative neutral colors.

These palettes determine the tonal values used for generating the complete color scheme, with each palette contributing to different UI elements.

## Color Access Methods
SchemeRainbow inherits all color access methods from the DynamicScheme class.
These include:

* `get_primary()`: Returns the primary color as an ARGB integer.
* `get_on_primary()`: Returns the on-primary color as an ARGB integer.
* `get_primary_container()`: Returns the primary container color as an ARGB integer.
* `get_on_primary_container()`: Returns the on-primary-container color as an ARGB integer.
* `get_secondary()`: Returns the secondary color as an ARGB integer.
* `get_on_secondary()`: Returns the on-secondary color as an ARGB integer.
* `get_secondary_container()`: Returns the secondary container color as an ARGB integer.
* `get_on_secondary_container()`: Returns the on-secondary-container color as an ARGB integer.
* `get_tertiary()`: Returns the tertiary color as an ARGB integer.
* `get_on_tertiary()`: Returns the on-tertiary color as an ARGB integer.
* `get_tertiary_container()`: Returns the tertiary container color as an ARGB integer.
* `get_on_tertiary_container()`: Returns the on-tertiary-container color as an ARGB integer.
* And additional utility color methods for elements like surface, background, outline, etc.

## Use Cases
The rainbow scheme works well for:
- Creative applications
- Kids' content
- Applications that need a playful, vibrant feel
- Situations where high colorfulness is desired
- Themes needing clear visual distinction between color categories

## Example
```python
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.rainbow import SchemeRainbow

# Create a color in HCT
hct = Hct.from_int(0xFF0000FF)  # Blue

# Create a rainbow scheme
scheme = SchemeRainbow(hct, False)  # Light theme

# Get the primary color
primary_color = scheme.get_primary()
print(f"Primary color: {hex(primary_color)}")

# Get other colors
on_primary = scheme.get_on_primary()
secondary = scheme.get_secondary()
tertiary = scheme.get_tertiary()

# Compare to see the vibrancy difference
print(f"Primary: {hex(primary_color)}")
print(f"Secondary: {hex(secondary)}")
print(f"Tertiary: {hex(tertiary)}")
```
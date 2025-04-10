# <center> Neutral Module Documentation </center>

A neutral theme - a palette with just one color (one hue) but with variations in tone and a very low chroma.

## Overview

`SchemeNeutral` is a color scheme that provides a neutral and subtle color palette based on the source color. It uses the same hue as the source color but with very low chroma values to create a neutral appearance.

This scheme is part of the Material Color Utilities package and extends the `DynamicScheme` class. Neutral schemes are useful for creating balanced and subtle UI designs where color isn't meant to be prominent.

## Usage

```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.neutral import SchemeNeutral

# Create a neutral scheme from a color
source_color = Hct.from_int(0xff0000ff)  # Blue color
is_dark = False  # Light mode
scheme = SchemeNeutral(source_color, is_dark)

# Use the scheme to get colors
primary_color = scheme.get_primary()
on_primary_color = scheme.get_on_primary()
```

## Constructor
```python
SchemeNeutral(source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0)
```
Creates a neutral color scheme based on the source color.

### Parameters

- `source_color_hct (Hct)`: Source color of the scheme in HCT
- `is_dark (bool)`: Whether the scheme is dark or light
- `contrast_level (float, optional)`: Level of contrast between colors. Defaults to 0.0.

## Color Palettes
SchemeNeutral creates the following color palettes:

1. __Primary Palette__: The source color hue with a chroma of 12.0
2. __Secondary Palette__: The source color hue with a chroma of 8.0
3. __Tertiary Palette__: The source color hue with a chroma of 16.0
4. __Neutral Palette__: The source color hue with a chroma of 2.0
5. __Neutral Variant Palette__: The source color hue with a chroma of 2.0

All palettes use the same hue as the source color, but vary in chroma to create a harmonious neutral color scheme.

## Inherited Methods
As a subclass of `DynamicScheme`, `SchemeNeutral` provides access to all the dynamic colors defined in Material Design, including:

* `get_primary()`: Returns the primary color
* `get_on_primary()`: Returns the on-primary color
* `get_primary_container()`: Returns the primary container color
* `get_on_primary_container()`: Returns the on-primary-container color
* `get_secondary()`: Returns the secondary color
* `get_tertiary()`: Returns the tertiary color
* `get_surface()`: Returns the surface color
* `get_surface_variant()`: Returns the surface variant color
* And many more...

## Example
```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.neutral import SchemeNeutral

# Create a neutral scheme from a blue color
blue = Hct.from_int(0xff0000ff)
light_scheme = SchemeNeutral(blue, False)  # Light mode
dark_scheme = SchemeNeutral(blue, True)    # Dark mode

# Access colors from the scheme
primary_light = light_scheme.get_primary()
primary_dark = dark_scheme.get_primary()

# Get surface colors
surface = light_scheme.get_surface()
surface_variant = light_scheme.get_surface_variant()
```

## Notes

* The neutral scheme creates a subtle, low-chroma design based on the source color's hue
* In light mode vs. dark mode, the tones of colors are automatically adjusted to maintain proper contrast
* The contrast_level parameter can be used to adjust the contrast between colors in the scheme
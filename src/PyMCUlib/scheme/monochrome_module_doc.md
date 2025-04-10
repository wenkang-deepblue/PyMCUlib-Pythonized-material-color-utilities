# <center> Monochrome Module Documentation </center>

## Overview

`SchemeMonochrome` is a theme scheme in the Material Color Utilities library that provides a monochromatic design system. It creates a palette with just one color (one hue) but with variations in tone, which means all colors share the same hue but vary in lightness.

## Features

- Creates a monochromatic color scheme from a source color
- All palettes have a chroma of 0.0, making them true monochromatic (grayscale with the source hue)
- Supports both light and dark themes
- Configurable contrast level

## Usage

### Basic Usage

```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.monochrome import SchemeMonochrome

# Create a source color (blue)
source_color = Hct.from_int(0xff0000ff)  # ARGB format

# Create a light theme monochrome scheme
light_scheme = SchemeMonochrome(source_color, is_dark=False)

# Create a dark theme monochrome scheme
dark_scheme = SchemeMonochrome(source_color, is_dark=True)

# Create a dark theme with higher contrast
high_contrast_dark = SchemeMonochrome(source_color, is_dark=True, contrast_level=0.5)
```

## Accessing Colors
```python
from PyMCUlib.dynamiccolor.material_dynamic_colors import MaterialDynamicColors

# Get primary color in ARGB format
primary_color = light_scheme.get_primary()

# Get on-surface color in ARGB format
on_surface_color = light_scheme.get_on_surface()

# Get color objects (HCT)
primary_hct = MaterialDynamicColors.primary().get_hct(light_scheme)
```

## Complete Example
```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.monochrome import SchemeMonochrome
from PyMCUlib.dynamiccolor.material_dynamic_colors import MaterialDynamicColors

# Create a source color (blue)
source_color = Hct.from_int(0xff0000ff)

# Create monochrome schemes
light_scheme = SchemeMonochrome(source_color, is_dark=False)
dark_scheme = SchemeMonochrome(source_color, is_dark=True)

# Access and use colors
primary_light = light_scheme.get_primary()
primary_dark = dark_scheme.get_primary()

# Print tone values
primary_light_tone = MaterialDynamicColors.primary().get_hct(light_scheme).get_tone()
primary_dark_tone = MaterialDynamicColors.primary().get_hct(dark_scheme).get_tone()

print(f"Light scheme primary tone: {primary_light_tone}")  # Should be 0.0
print(f"Dark scheme primary tone: {primary_dark_tone}")    # Should be 100.0
```

## Class Definition
```python
class SchemeMonochrome(DynamicScheme):
    def __init__(self, source_color_hct: Hct, is_dark: bool, contrast_level: float = 0.0):
        """
        Create a monochrome color scheme based on the source color.
        
        Args:
            source_color_hct: Source color of the scheme in HCT
            is_dark: Whether the scheme is dark or light
            contrast_level: Level of contrast between colors (0.0 to 1.0)
        """
```

## Characteristics
In a monochromatic scheme:

* All colors share the same hue as the source color
* All palettes have a chroma of 0.0, making them true monochromatic (grayscale with the source hue)
* Tones are set according to Material Design specifications for light or dark themes

## Tone Values
For a dark theme monochrome scheme, typical tone values include:

* Primary: 100.0
* On Primary: 10.0
* Primary Container: 85.0
* Secondary: 80.0
* On Secondary: 10.0
* Tertiary: 90.0

For a light theme monochrome scheme, typical tone values include:

* Primary: 0.0
* On Primary: 90.0
* Primary Container: 25.0
* Secondary: 40.0
* On Secondary: 100.0
* Tertiary: 25.0

## Related Classes
- `DynamicScheme`: Base class that provides the framework for all scheme types
- `TonalPalette`: Class that generates a range of tones with the same hue and chroma
- `MaterialDynamicColors`: Provides standard Material Design color components
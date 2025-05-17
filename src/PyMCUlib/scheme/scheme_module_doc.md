# Scheme Module Documentation

The Scheme module is a key component of the Material Color Utilities (MCU) library, providing functionality for generating Material Design color schemes. These schemes map color roles (like primary, secondary, background, etc.) to specific colors based on a source color.

## Overview

The scheme module offers several classes for generating color schemes:

- `Scheme`: The base class (deprecated in favor of `DynamicScheme`)
- `SchemeAndroid`: Android 12-specific color scheme
- Various dynamic scheme implementations (recommended order):
  1. `SchemeTonalSpot`
  2. `SchemeVibrant`
  3. `SchemeContent`
  4. `SchemeFidelity`
  5. `SchemeNeutral`
  6. `SchemeMonochrome`
  7. `SchemeExpressive`
  8. `SchemeRainbow`
  9. `SchemeFruitSalad`

Each scheme provides a different aesthetic approach to generating a harmonic color system from a single source color.

## Base Scheme Class

```python
from PyMCUlib.scheme.scheme import Scheme

# Create a light scheme from an ARGB color
light_scheme = Scheme.light(0xFF0000FF)  # Blue

# Create a dark scheme from an ARGB color
dark_scheme = Scheme.dark(0xFF0000FF)  # Blue

# Create a light content scheme from an ARGB color
content_light = Scheme.light_content(0xFF0000FF)

# Create a dark content scheme from an ARGB color
content_dark = Scheme.dark_content(0xFF0000FF)

# Access colors in the scheme
primary_color = light_scheme.primary
on_primary_color = light_scheme.on_primary

# Advanced: Create a scheme directly from a CorePalette
from PyMCUlib.palettes.core_palette import CorePalette
light_scheme_alt = Scheme.light_from_core_palette(CorePalette.of(0xFF0000FF))
```

The `Scheme` class is **deprecated** and should be replaced with `DynamicScheme` for new applications. It provides methods for creating light and dark color schemes from a source color.

### Key Properties

The `Scheme` class provides properties for accessing various color roles:

- **Primary colors**: `primary`, `on_primary`, `primary_container`, `on_primary_container`
- **Secondary colors**: `secondary`, `on_secondary`, `secondary_container`, `on_secondary_container`
- **Tertiary colors**: `tertiary`, `on_tertiary`, `tertiary_container`, `on_tertiary_container`
- **Error colors**: `error`, `on_error`, `error_container`, `on_error_container`
- **Surface colors**: `surface`, `on_surface`, `surface_variant`, `on_surface_variant`
- **Background colors**: `background`, `on_background`
- **Other colors**: `outline`, `outline_variant`, `shadow`, `scrim`, `inverse_surface`, `inverse_on_surface`, `inverse_primary`

## Android-Specific Scheme

```python
from PyMCUlib.scheme.scheme_android import SchemeAndroid

# Create a light Android scheme from an ARGB color
android_light = SchemeAndroid.light(0xFF0000FF)

# Create a light Android content color scheme
android_content_light = SchemeAndroid.light_content(0xFF0000FF)

# Create a dark Android content color scheme
android_content_dark = SchemeAndroid.dark_content(0xFF0000FF)

# Access Android-specific colors
accent_primary = android_light.color_accent_primary
background = android_light.color_background
```

The `SchemeAndroid` class provides Android 12-specific color roles, different from the standard Material Design color system.

## JSON Serialization

Both `Scheme` and `SchemeAndroid` provide a `to_json()` method that returns a dictionary mapping color role names to ARGB integers. For example:

```python
# Serialize a light scheme to JSON
scheme_dict = light_scheme.to_json()
print(scheme_dict['primary'])  # 4278190335 (0xFF0000FF)

# Convert ARGB integer to hex string
from PyMCUlib.utils.string_utils import hex_from_argb
print(hex_from_argb(scheme_dict['primary']))  # #0000ff
```

## Dynamic Scheme Types

All dynamic schemes extend the `DynamicScheme` class and provide different aesthetic approaches to Material Design color generation.

### Common Usage Pattern

```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.scheme.scheme_vibrant import SchemeVibrant

# Create an HCT color
source_hct = Hct.from_int(0xFF0000FF)  # Blue

# Create a scheme with the HCT color
is_dark = False  # Light mode
contrast_level = 0.0  # Standard contrast
scheme = SchemeVibrant(source_hct, is_dark, contrast_level)

# Access colors
primary = scheme.primary
on_primary = scheme.on_primary
```

### Available Dynamic Schemes

1. **Tonal Spot** (`SchemeTonalSpot`): The default Material You theme on Android 12 and 13. It has low to medium colorfulness and a Tertiary TonalPalette with a hue related to the source color.

2. **Vibrant** (`SchemeVibrant`): Maximizes colorfulness at each position in the Primary Tonal Palette.

3. **Expressive** (`SchemeExpressive`): Intentionally detached from the source color for a more creative palette.

4. **Content** (`SchemeContent`): Places the source color in the primary container, maintaining constant appearance in light and dark modes.

5. **Fidelity** (`SchemeFidelity`): Similar to Content, places the source color in the primary container.

6. **Neutral** (`SchemeNeutral`): A near-grayscale theme with minimal colorfulness.

7. **Monochrome** (`SchemeMonochrome`): A completely grayscale theme.

8. **Rainbow** (`SchemeRainbow`): A playful theme where the source color's hue does not appear in the theme.

9. **Fruit Salad** (`SchemeFruitSalad`): Another playful theme where the source color's hue does not appear in the theme.

### Scheme Parameters

All dynamic schemes accept the following parameters:

- `source_color_hct`: The source color of the theme as an HCT color.
- `is_dark`: Whether the scheme is in dark mode or light mode.
- `contrast_level`: Value from -1 to 1, where -1 represents minimum contrast, 0 standard contrast, and 1 maximum contrast.

Some schemes also accept:
- `spec_version`: The Material specification version to use (`'2021'` or `'2025'`).
- `platform`: The platform to use (`'phone'` or `'watch'`).

Note: Only `SchemeExpressive`, `SchemeNeutral`, `SchemeTonalSpot`, and `SchemeVibrant` support the optional `spec_version` and `platform` parameters in their constructors. Other dynamic schemes (`SchemeContent`, `SchemeFidelity`, `SchemeFruitSalad`, `SchemeMonochrome`, `SchemeRainbow`) only accept `source_color_hct`, `is_dark`, and `contrast_level`.

## Extended Example

```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.scheme.scheme_vibrant import SchemeVibrant
from PyMCUlib.scheme.scheme_neutral import SchemeNeutral
from PyMCUlib.scheme.scheme_tonal_spot import SchemeTonalSpot

# Create source color
source_color = Hct.from_int(0xFF4285F4)  # Google Blue

# Create different schemes
vibrant_light = SchemeVibrant(source_color, False, 0.0)
neutral_dark = SchemeNeutral(source_color, True, 0.0)
tonal_spot = SchemeTonalSpot(source_color, False, 0.0)

# Access colors
vibrant_primary = vibrant_light.primary
neutral_secondary = neutral_dark.secondary
tonal_tertiary = tonal_spot.tertiary

# Get all colors in a scheme
vibrant_all_colors = {
    'primary': vibrant_light.primary,
    'on_primary': vibrant_light.on_primary,
    'primary_container': vibrant_light.primary_container,
    'on_primary_container': vibrant_light.on_primary_container,
    'secondary': vibrant_light.secondary,
    # ... and so on
}
```

## Platform and Specification Version Differences

Some schemes allow specifying `platform` ('phone' or 'watch') and `spec_version` ('2021' or '2025'):

```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.scheme.scheme_vibrant import SchemeVibrant

source_color = Hct.from_int(0xFF4285F4)  # Google Blue

# Create scheme with specific platform and spec version
scheme = SchemeVibrant(
    source_color, 
    is_dark=False, 
    contrast_level=0.0,
    spec_version='2025',  
    platform='watch'
)
```

## Advanced DynamicScheme Properties

`DynamicScheme` (especially with `spec_version='2025'`) exposes additional properties beyond the core roles:

- Surface and tint:  
  `surface_tint`

- Tone variants:  
  `surface_dim`, `surface_bright`,  
  `surface_container_lowest`,  
  `surface_container_low`,  
  `surface_container`,  
  `surface_container_high`,  
  `surface_container_highest`

- Dimmed colors:  
  `primary_dim`, `secondary_dim`,  
  `tertiary_dim`, `error_dim`

- Fixed colors:  
  `primary_fixed`, `secondary_fixed`,  
  `tertiary_fixed`

- On-fixed colors:  
  `on_primary_fixed`, `on_secondary_fixed`,  
  `on_tertiary_fixed`

- On-fixed variants:  
  `on_primary_fixed_variant`,  
  `on_secondary_fixed_variant`,  
  `on_tertiary_fixed_variant`

For the full list of available properties, see the `DynamicScheme` class in `src/PyMCUlib/dynamiccolor/dynamic_scheme.py`.

## Related Modules

The scheme module works closely with:

- **HCT Module**: Provides the color space representation used by schemes
- **Palettes Module**: Used by schemes to generate tonal palettes
- **DynamicColor Module**: Contains the `DynamicScheme` base class and related functionality

## Implementation Details

The scheme module is implemented in Python with the following files:

- `scheme.py`: Contains the deprecated base `Scheme` class
- `scheme_android.py`: Contains the `SchemeAndroid` class for Android 12 color schemes
- `scheme_content.py`: Contains the `SchemeContent` class
- `scheme_expressive.py`: Contains the `SchemeExpressive` class
- `scheme_fidelity.py`: Contains the `SchemeFidelity` class
- `scheme_fruit_salad.py`: Contains the `SchemeFruitSalad` class
- `scheme_monochrome.py`: Contains the `SchemeMonochrome` class
- `scheme_neutral.py`: Contains the `SchemeNeutral` class
- `scheme_rainbow.py`: Contains the `SchemeRainbow` class
- `scheme_tonal_spot.py`: Contains the `SchemeTonalSpot` class
- `scheme_vibrant.py`: Contains the `SchemeVibrant` class

All dynamic scheme classes extend the `DynamicScheme` class from the `dynamiccolor` module.

## Usage Recommendations

1. For new applications, use `DynamicScheme` variants instead of the deprecated `Scheme` class.
2. The `SchemeTonalSpot` is recommended as the default scheme for most applications, as it matches the default Material You theme on Android 12 and 13.
3. For more vibrant colors, use `SchemeVibrant`.
4. For more neutral or monochrome aesthetics, use `SchemeNeutral` or `SchemeMonochrome`.
5. For special creative applications, consider `SchemeExpressive`, `SchemeRainbow`, or `SchemeFruitSalad`.

## Code Example with Output

```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.scheme.scheme_vibrant import SchemeVibrant
from PyMCUlib.utils.string_utils import hex_from_argb

# Create a vibrant scheme from blue
source_color = Hct.from_int(0xFF0000FF)  # Blue
scheme = SchemeVibrant(source_color, False, 0.0)

# Print important colors in hex format (lowercase by default)
print(f"Primary: {hex_from_argb(scheme.primary)}")
print(f"Secondary: {hex_from_argb(scheme.secondary)}")
print(f"Tertiary: {hex_from_argb(scheme.tertiary)}")
print(f"Error: {hex_from_argb(scheme.error)}")
print(f"Background: {hex_from_argb(scheme.background)}")
print(f"On Background: {hex_from_argb(scheme.on_background)}")
```

Example output (hex values may vary):
```
Primary: #0000ff
Secondary: #7a7aff
Tertiary: #b47aff
Error: #b3261e
Background: #fffbff
On Background: #1c1b1f
```

Note: The exact hex values may vary as they depend on the implementation details of the color algorithms.
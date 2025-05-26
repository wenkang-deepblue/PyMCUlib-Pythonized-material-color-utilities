# <center> DynamicColor Component Documentation </center>

## Overview

The Dynamic Color component is a crucial part of the Material Color Utilities library that enables adaptive coloring based on user preferences, themes, and accessibility requirements. This component provides functionality to create color schemes that dynamically adjust based on:

- Light/dark theme preferences
- Contrast level requirements
- Color relationships and constraints
- Different design variants (monochrome, tonal spot, vibrant, etc.)

Dynamic colors are designed to maintain appropriate contrast ratios, preserve harmony between related colors, and adapt to different UI environments while staying true to the original design intent.

## Core Concepts

### Dynamic Colors

A `DynamicColor` is a color that can adapt its properties based on context, particularly light/dark theme and contrast settings. Unlike a static color (such as "red" or "#FF0000"), a dynamic color might be darker in light theme and lighter in dark theme, ensuring proper contrast and readability.

### Schemes

A `DynamicScheme` defines a complete color system based on a source color and design preferences. It includes palettes for primary, secondary, tertiary, neutral, and error colors, which are used to generate the final set of UI colors.

### Variants

`Variant` represents different design approaches for generating color schemes, such as:
- Monochrome: A single-hue color scheme
- Tonal Spot: The standard Material You scheme
- Vibrant: A more colorful scheme
- Fidelity: A scheme that stays closer to the source color
- Content: A scheme that prioritizes maintaining the source color's exact appearance

### Contrast and Tone

Contrast relationships between colors are essential for accessibility. The `ContrastCurve` class provides different contrast levels based on user preferences.

`ToneDeltaPair` defines tone distance requirements between two colors, ensuring they maintain proper visual separation.

## Main Classes

### ContrastCurve

Defines how contrast between colors changes across different contrast level settings.

```python
curve = ContrastCurve(1.0, 3.0, 4.5, 7.0) # ContrastCurve (low, normal, medium, high)
contrast_at_level_0 = curve.get(0.0)  # Returns 3.0
contrast_at_level_0_5 = curve.get(0.5)  # Returns 4.5
```
### TonePolarity and ToneDeltaPair
`TonePolarity` describes the relationship between two tones:

* DARKER: One color should be darker than another
* LIGHTER: One color should be lighter than another
* NEARER: One color should be closer to the background tone
* FARTHER: One color should be further from the background tone

`ToneDeltaPair` defines a constraint in tone distance between two DynamicColors.
```python
# Create a constraint that color_a should be at least 15 tones darker than color_b
delta_pair = ToneDeltaPair(role_a, role_b, 15.0, TonePolarity.DARKER, False)
```
### Variant
An enumeration of different design approaches for color schemes:
```python
variant = Variant.TONAL_SPOT  # Standard Material You scheme
```
Available variants:
* MONOCHROME
* NEUTRAL
* TONAL_SPOT
* VIBRANT
* EXPRESSIVE
* FIDELITY
* CONTENT
* RAINBOW
* FRUIT_SALAD

### DynamicColor
The core class that represents a color that adjusts based on context. A DynamicColor is defined by:
* A name
* A tonal palette (providing hue and chroma)
* A tone function that determines lightness based on context
* Optional background colors and contrast requirements
* Optional tone delta constraints

Example of creating a basic dynamic color:
```python
primary_color = DynamicColor.from_palette(
    name="primary",
    palette=lambda s: s.primary_palette,
    tone=lambda s: 80.0 if s.is_dark else 40.0
)
```
Example of a more complex dynamic color with contrast requirements:
```python
on_primary_color = DynamicColor(
    name="on_primary",
    palette=lambda s: s.primary_palette,
    tone=lambda s: 20.0 if s.is_dark else 100.0,
    is_background=False,
    background=lambda s: MaterialDynamicColors.primary(),
    second_background=None,
    contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
    tone_delta_pair=None
)
```
### DynamicScheme
Represents a complete color scheme based on a source color and preferences. It contains:
* The source color
* Light/dark mode setting
* Contrast level
* Variant type
* Tonal palettes for primary, secondary, tertiary, neutral, and error colors
```python
# Create a light theme dynamic scheme with default contrast
scheme = DynamicScheme(
    source_color_hct=Hct.from_int(0xFF0000FF),  # Blue color
    variant=Variant.TONAL_SPOT,
    contrast_level=0.0,
    is_dark=False,
    primary_palette=primary_palette,
    secondary_palette=secondary_palette,
    tertiary_palette=tertiary_palette,
    neutral_palette=neutral_palette,
    neutral_variant_palette=neutral_variant_palette,
    error_palette=TonalPalette(25.0, 84.0)  # Optional, defaults to red error palette
)
```

### MaterialDynamicColors
A collection of predefined dynamic colors based on Material Design principles. This class provides static methods for all standard Material Design colors:
```python
# Get Material Design colors from a scheme
primary = MaterialDynamicColors.primary().get_argb(scheme)
on_primary = MaterialDynamicColors.on_primary().get_argb(scheme)
primary_container = MaterialDynamicColors.primary_container().get_argb(scheme)
surface = MaterialDynamicColors.surface().get_argb(scheme)
```
Available colors include:
* Background colors: background, surface, surface_dim, surface_bright
* Surface containers: surface_container_lowest, surface_container_low, etc.
* Primary colors: primary, on_primary, primary_container, on_primary_container
* Secondary colors: secondary, on_secondary, secondary_container, etc.
* Tertiary colors: tertiary, on_tertiary, tertiary_container, etc.
* Error colors: error, on_error, error_container, on_error_container
* Fixed colors: primary_fixed, on_primary_fixed, etc.
* Other utility colors: outline, shadow, scrim, etc.

## Helper Functions
### foreground_tone
```python
foreground_tone(bg_tone: float, ratio: float) -> float
```
Given a background tone, finds a foreground tone that achieves the specified contrast ratio.
### enable_light_foreground
```python
enable_light_foreground(tone: float) -> float
```
Adjusts a tone to ensure light foreground text has sufficient contrast.
### tone_prefers_light_foreground
```python
tone_prefers_light_foreground(tone: float) -> bool
```
Determines if a tone aesthetically prefers light foreground.
### tone_allows_light_foreground
```python
tone_allows_light_foreground(tone: float) -> bool
```
Determines if a tone can reach sufficient contrast with light foreground.

## Usage Examples
### Creating a Basic Dynamic Scheme
```python
from mcu_python.cam.hct import Hct
from mcu_python.palettes.tones import TonalPalette
from mcu_python.dynamiccolor.dynamic_scheme import DynamicScheme
from mcu_python.dynamiccolor.variant import Variant
from mcu_python.dynamiccolor.material_dynamic_colors import MaterialDynamicColors

# Create a source color
source_color = Hct.from_int(0xFF0000FF)  # Blue

# Create palettes
primary_palette = TonalPalette(source_color.get_hue(), 40.0)
secondary_palette = TonalPalette(source_color.get_hue(), 16.0)
tertiary_palette = TonalPalette(source_color.get_hue() + 60, 24.0)
neutral_palette = TonalPalette(source_color.get_hue(), 4.0)
neutral_variant_palette = TonalPalette(source_color.get_hue(), 8.0)

# Create light theme scheme
light_scheme = DynamicScheme(
    source_color,
    Variant.TONAL_SPOT,
    0.0,  # Standard contrast
    False,  # Light mode
    primary_palette,
    secondary_palette,
    tertiary_palette,
    neutral_palette,
    neutral_variant_palette
)

# Get colors from the scheme
primary = MaterialDynamicColors.primary().get_argb(light_scheme)
on_primary = MaterialDynamicColors.on_primary().get_argb(light_scheme)
surface = MaterialDynamicColors.surface().get_argb(light_scheme)
on_surface = MaterialDynamicColors.on_surface().get_argb(light_scheme)
```
### Creating a Custom Dynamic Color
```python
from mcu_python.dynamiccolor.dynamic_color import DynamicColor
from mcu_python.dynamiccolor.contrast_curve import ContrastCurve

# Create a custom dynamic color
custom_accent = DynamicColor(
    name="custom_accent",
    palette=lambda s: s.primary_palette,
    tone=lambda s: 70.0 if s.is_dark else 30.0,
    is_background=True,
    background=lambda s: MaterialDynamicColors.surface(),
    second_background=None,
    contrast_curve=ContrastCurve(1.0, 3.0, 4.5, 7.0),
    tone_delta_pair=None
)

# Get the color
accent_color = custom_accent.get_argb(light_scheme)
```
### Switching Between Light and Dark Themes
```python
# Create dark theme scheme with the same parameters
dark_scheme = DynamicScheme(
    source_color,
    Variant.TONAL_SPOT,
    0.0,  # Standard contrast
    True,  # Dark mode
    primary_palette,
    secondary_palette,
    tertiary_palette,
    neutral_palette,
    neutral_variant_palette
)

# Use MaterialDynamicColors to get colors for both schemes
light_primary = MaterialDynamicColors.primary().get_argb(light_scheme)
dark_primary = MaterialDynamicColors.primary().get_argb(dark_scheme)

light_surface = MaterialDynamicColors.surface().get_argb(light_scheme)
dark_surface = MaterialDynamicColors.surface().get_argb(dark_scheme)
```
### Working with Different Contrast Levels
```python
# Create a high contrast scheme
high_contrast_scheme = DynamicScheme(
    source_color,
    Variant.TONAL_SPOT,
    1.0,  # High contrast
    False,  # Light mode
    primary_palette,
    secondary_palette,
    tertiary_palette,
    neutral_palette,
    neutral_variant_palette
)

# Standard contrast primary vs. high contrast primary
standard_primary = MaterialDynamicColors.primary().get_argb(light_scheme)
high_contrast_primary = MaterialDynamicColors.primary().get_argb(high_contrast_scheme)
```

### Handling Edge Cases and Contrast Failures
```python
# Example to handle cases where contrast requirements can't be met
def get_safe_color(color, scheme):
    try:
        return color.get_argb(scheme)
    except:
        # Fallback to a safe alternative if contrast can't be achieved
        return MaterialDynamicColors.surface().get_argb(scheme)
        
# Or checking contrast before using colors
from PyMCUlib_cpp.contrast.contrast import ratio_of_tones

def is_accessible(foreground_color, background_color, scheme, min_contrast=4.5):
    fg_tone = foreground_color.get_tone(scheme)
    bg_tone = background_color.get_tone(scheme)
    ratio = ratio_of_tones(fg_tone, bg_tone)
    return ratio >= min_contrast
```
## Relationship with Other Components
The Dynamic Color component relies on several other components:
* __Utils__: Provides basic color utilities like ARGB conversions
* __CAM__: Provides the color appearance model and HCT color space
* __Contrast__: Provides contrast ratio calculations
* __Palettes__: Provides tonal palettes for generating colors
* __Dislike__: Provides adjustments for colors that might be disliked

## Best Practices
1. __Use MaterialDynamicColors when possible__ - These are well-tested and follow Material Design guidelines.
2. __Avoid hard-coded tones__ - Use the tone functions to ensure colors adapt properly to theme changes.
3. __Consider accessibility__ - Use appropriate contrast ratios for text and interactive elements.
4. __Maintain tone relationships__ - Ensure related colors (like primary and on_primary) maintain proper contrast.
5. __Test in both light and dark modes__ - Colors should be visually appealing in both themes.

6. __Performance considerations__ - Cache dynamic color results when possible, especially on UI components that don't need to respond to theme changes frequently.
   ```python
   # Inefficient (recalculates every time)
   def paint(scheme):
      primary = MaterialDynamicColors.primary().get_argb(scheme)
      use_color(primary)
      
   # Better (cache colors when scheme changes)
   cached_colors = {}
   def update_cache(scheme):
      cached_colors['primary'] = MaterialDynamicColors.primary().get_argb(scheme)
      
   def paint():
      use_color(cached_colors['primary'])
   ```

7. __Handle color preferences__ - Some users may have specific color preferences or vision impairments that require adjustments.

8. __Test with contrast settings__ - Make sure your app behaves well across all contrast levels from -1.0 to 1.0.

9. __Be aware of the "awkward zone"__ - Tones between 50-59 often have uncertain text contrast relationships. The library adjusts for this, but custom implementations should be aware of this zone.

10. __Respect system theme settings__ - Use the device's theme (light/dark) as the default for your dynamic scheme unless the user has explicitly chosen a different theme in your app.
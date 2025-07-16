

# PyMCUlib - Material Color Utilities Lib for Python (Ported from Official MCU of TypeScript version)

### Based on official MCU-TypeScript 2025 most updated version

### Python version: >=3.12.0

**_Note:_** In 2025, the official Material Color Utilities library was updated to version 2025 as TypeScript & Java & Dart implementation. This Python package has since been reimplemented based on that latest TypeScript version ([main-ts](https://github.com/wenkang-deepblue/PyMCUlib-Pythonized-material-color-utilities)) and is published on PyPI as the default `PyMCUlib` package (install via `pip install PyMCUlib`). The original C++-based Python port ([main-cpp](https://github.com/wenkang-deepblue/PyMCUlib-Pythonized-material-color-utilities/tree/main-cpp)) has been renamed `PyMCUlib-cpp` and is available via `pip install PyMCUlib-cpp`. Please choose the package that best fits your needs.

## Overview
This project is a Python port of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities) library, with this version being specifically ported from the official **TypeScript** implementation. The Material Color Utilities (MCU) library provides algorithms and utilities that power the dynamic color system introduced in Material Design 3.

## Introduction

Material Design 3 introduces a dynamic color system that generates beautiful, accessible color schemes based on dynamic inputs like a user's wallpaper. This Python port aims to faithfully mirror the components, modules, parameters, outputs, and dependencies of the TypeScript MCU library, making these powerful color tools accessible to Python developers.

## Port Information

This port maintains the spirit and functionality of the original TypeScript implementation while adapting to Python's conventions and best practices:

-   **Naming Conventions**:
    -   Function and method names follow Python's `snake_case` convention (e.g., TypeScript's `getRotatedHue()` becomes Python's `get_rotated_hue()`).
    -   Class names maintain `PascalCase` as in the original TypeScript (e.g., `DynamicScheme` remains `DynamicScheme`).

-   **TypeScript Fidelity**: The port strives to be a close mirror of the TypeScript codebase in terms of logic and algorithms.

-   **Pythonic Adaptations**: Due to inherent differences between TypeScript and Python, some adaptations were necessary to align with Python's language features and common practices:
    -   **Circular Dependency Management**:
        -   In the `PyMCUlib.utils` module, components like those from `theme_utils` are imported dynamically within the `__init__.py` using `__getattr__` to prevent circular import issues that can arise from complex interdependencies.
        -   In the `PyMCUlib.dynamiccolor` module, `ColorSpecDelegate` was extracted into its own file (`color_spec_delegate.py`) from `color_spec.py` to resolve circular dependencies between dynamic color specification and its implementations.
    -   **Properties**: Where appropriate, getter and setter methods from TypeScript have been converted to Python properties for more idiomatic access (e.g., `hct.getHue()` and `hct.setHue()` are accessed via `hct.hue` and `hct.hue = new_value`).

-   **Documentation**: Docstrings have been added for components and modules to aid understanding and usage.

While this port aims for high fidelity to the TypeScript source, it cannot be a 1:1 replication. However, it faithfully reproduces the ideas, logic, and algorithms.

## Project Structure

Following the organization of the original MCU library, this Python project is structured into several modules, each handling specific aspects of color processing:

```
PyMCUlib/
├── __init__.py                # Package entry point with public APIs
├── blend/                     # Color blending utilities
├── contrast/                  # Contrast ratio calculation and accessibility tools
├── dislike/                   # Detection and fixing of universally disliked colors
├── dynamiccolor/              # Dynamic color system for Material Design 3
├── hct/                       # HCT (Hue, Chroma, Tone) color space & CAM16 model
├── palettes/                  # Color palette generation
├── quantize/                  # Color extraction from images
├── scheme/                    # Material Design color schemes
├── score/                     # Color ranking and evaluation
├── temperature/               # Color temperature theory implementation
└── utils/                     # Common utility functions
```

*(Note: `test` files also exist but are not part of the installable package)*

### Component Descriptions

-   **`blend`**: Provides utilities for blending colors, primarily in the HCT color space, to create harmonious combinations.
-   **`contrast`**: Contains tools for calculating contrast ratios between colors and generating accessible color combinations.
-   **`dislike`**: Implements logic to identify and adjust colors that are generally perceived as unpleasant (e.g., dark yellow-greens).
-   **`dynamiccolor`**: The core of Material Design 3's adaptive color system. It generates colors that respond to UI states (like dark/light mode) and context.
-   **`hct`**: Implements the HCT (Hue, Chroma, Tone) color space and the CAM16 color appearance model, which are foundational to Material Design's color system. This module combines concepts that might be separate (e.g., CAM16 and HCT details) in other MCU ports.
-   **`palettes`**: Creates tonal palettes (variations of a color at different tones) and core palettes, which serve as building blocks for color schemes.
-   **`quantize`**: Implements algorithms (like Wu's algorithm and K-Means) to extract key colors from images, crucial for theme generation from user content.
-   **`scheme`**: Generates complete Material Design color schemes (e.g., Vibrant, Neutral, Tonal Spot) from a source color.
-   **`score`**: Evaluates and ranks colors for their suitability in theming, considering perceptual qualities and potential usage.
-   **`temperature`**: Implements color temperature theory to find complementary and analogous colors for harmonious designs.
-   **`utils`**: Provides core utility functions for color conversions, mathematical operations, image processing for color extraction, and other common tasks.

## Installation

Install via pip (recommended):
```bash
pip install PyMCUlib
```

Alternatively, install from source:
```bash
git clone https://github.com/yourname/PyMCUlib.git
cd PyMCUlib
pip install .
```

## Quick Start

The example below demonstrates the minimal workflow from import to obtaining an ARGB color value:

```python
from PyMCUlib.dynamiccolor import DynamicScheme, DynamicColor, Variant
from PyMCUlib.hct import Hct

# 1. Create an HCT source color
source = Hct.from_int(0xFF6750A4)  # Material Purple

# 2. Construct a DynamicScheme
#    spec_version defaults to '2021', platform defaults to 'phone'
scheme = DynamicScheme({
    'source_color_hct': source,
    'variant': Variant.VIBRANT,
    'is_dark': False,
    'contrast_level': 0.0,
    'spec_version': '2025',      # <-- explicit use of 2025 spec
    'platform': 'phone'          # (optional, defaults to 'phone')
})

# 3. (Standard) Access predefined theme colors
primary_color = scheme.primary
print(f"Scheme Primary Color: {hex(primary_color)}")

# 4. (Advanced) Define and use a custom DynamicColor
custom_accent = DynamicColor.from_palette({
    'name': 'custom_accent',
    'palette': lambda s: s.primary_palette, # Uses the scheme's primary palette
    'tone':   lambda s: 40.0,
})

# 5. Get the ARGB value for the custom color
custom_argb = accent.get_argb(scheme)
print(f"Custom Accent Color: {hex(custom_argb)}")
```

## Components & Usage Examples

The library consists of various components, designed to be modular. Here are some examples of how to use them:

### Blend

Utilities for blending colors.

```python
from PyMCUlib.blend import Blend

# Harmonize one color with another (colors as ARGB integers)
design_color_argb = 0xFFFF0000  # Red
key_color_argb = 0xFF0000FF    # Blue
harmonized_color = Blend.harmonize(design_color_argb, key_color_argb)
# print(f"Harmonized Color: {hex(harmonized_color)}")

# Blend hue between two colors (amount 0.0-1.0)
from_color_argb = 0xFFFF0000 # Red
to_color_argb = 0xFF00FF00   # Green
mixed_hue_color = Blend.hct_hue(from_color_argb, to_color_argb, 0.5)
# print(f"Mixed Hue Color: {hex(mixed_hue_color)}")
```

### Contrast

Tools for measuring contrast and finding colors that meet accessibility requirements.

```python
from PyMCUlib.contrast import Contrast

# Calculate contrast ratio between two tones (0-100)
tone_a = 10.0
tone_b = 90.0
contrast_ratio = Contrast.ratio_of_tones(tone_a, tone_b)
# print(f"Contrast Ratio: {contrast_ratio}")

# Find a lighter tone with a specific contrast ratio
original_tone = 20.0
desired_ratio = 4.5
lighter_tone = Contrast.lighter(original_tone, desired_ratio) # Returns -1.0 if not possible
# if lighter_tone != -1.0:
#     print(f"Lighter Tone for ratio {desired_ratio}: {lighter_tone}")
```

### Dislike

Identifies and fixes universally disliked colors.

```python
from PyMCUlib.dislike import DislikeAnalyzer
from PyMCUlib.hct import Hct

# Example disliked color (dark olive green)
disliked_argb_color = 0xFF8F7C00 
hct_color = Hct.from_int(disliked_argb_color)

# Check if a color is disliked
is_disliked = DislikeAnalyzer.is_disliked(hct_color)
# print(f"Is color disliked? {is_disliked}")

# Fix a disliked color
fixed_hct_color = DislikeAnalyzer.fix_if_disliked(hct_color)
# print(f"Original ARGB: {hex(hct_color.to_int())}, Fixed ARGB: {hex(fixed_hct_color.to_int())}")
```

### DynamicColor

Provides colors that adjust based on UI states (dark theme, contrast levels) via `DynamicScheme`.

```python
from PyMCUlib.dynamiccolor import DynamicColor, DynamicScheme, Variant
from PyMCUlib.hct import Hct
from PyMCUlib.palettes import TonalPalette # For palette lambda example

# Define a source color for the scheme
source_hct = Hct.from_int(0xFF3F51B5) # Indigo

# Create a dynamic scheme (e.g., TonalSpot variant)
scheme_options = {
    'source_color_hct': source_hct,
    'variant': Variant.TONAL_SPOT,
    'is_dark': False,
    'contrast_level': 0.0
}
my_scheme = DynamicScheme(scheme_options)

# Example of creating a custom DynamicColor (conceptual)
# In practice, you'd often use predefined MaterialDynamicColors
custom_dynamic_color = DynamicColor.from_palette({
    'name': "custom_accent",
    'palette': lambda s: s.primary_palette, # Use primary palette from scheme
    'tone': lambda s: 40.0 if not s.is_dark else 80.0
})

# Get the ARGB value of this custom color for the specific scheme
argb_value = custom_dynamic_color.get_argb(my_scheme)
# print(f"Custom Dynamic Color ARGB: {hex(argb_value)}")

# Accessing predefined Material Design colors
primary_color_argb = my_scheme.primary
# print(f"Scheme Primary Color ARGB: {hex(primary_color_argb)}")
```

### HCT

The HCT color space (Hue, Chroma, Tone) accounts for viewing conditions and provides a perceptually accurate color model.

```python
from PyMCUlib.hct import Hct

# Create HCT color from an ARGB integer
hct_color = Hct.from_int(0xFF0000FF)  # Blue

# Access HCT components using properties
hue = hct_color.hue
chroma = hct_color.chroma
tone = hct_color.tone
# print(f"HCT: H={hue:.2f}, C={chroma:.2f}, T={tone:.2f}")

# Modify HCT components using property setters
hct_color.tone = 80.0  # Make it a lighter blue
# print(f"New Tone: {hct_color.tone}, New ARGB: {hex(hct_color.to_int())}")

# Convert back to ARGB
rgb_int = hct_color.to_int()
```

### Palettes

Creates tonal palettes (colors varying only in tone) and core palettes.

`TonalPalette`:
```python
from PyMCUlib.palettes import TonalPalette

# Create a tonal palette from an ARGB integer
# TonalPalette.from_int() or TonalPalette.from_hue_and_chroma()
palette = TonalPalette.from_int(0xFF0000FF)  # Blue

# Get different tones of the same color
light_blue_argb = palette.tone(90)
mid_blue_argb   = palette.tone(50)
dark_blue_argb  = palette.tone(10)

print(hex(light_blue_argb))  # e.g. 0xffe0e0ff
print(hex(mid_blue_argb))    # e.g. 0xff5a64ff
print(hex(dark_blue_argb))   # e.g. 0xff00006e
```
`CorePalette`:
```python
from PyMCUlib.palettes import CorePalette

# Generate a core palette from an ARGB integer
core = CorePalette.of(0xFF0000FF)  # Blue

# Access its A1 tonal palette
primary_tone = core.a1.tone(50)    # mid-tone of the primary accent
on_primary   = core.a1.tone(10)    # very dark primary accent

print(hex(primary_tone))  # e.g. 0xff5a64ff
print(hex(on_primary))    # e.g. 0xff00006e
```

### Quantize

Extracts dominant colors from images. `QuantizerCelebi` is one of the available quantizers.

```python
from PyMCUlib.quantize import QuantizerCelebi

# Example image pixels (list of ARGB integers)
pixels = [0xFFFF0000, 0xFF00FF00, 0xFF0000FF, 0xFFF00008, 0xFF0AAB00] 
max_colors_to_extract = 3

# Quantize pixels to extract key colors and their population
# Returns a dict: {argb_color: population_count}
result = QuantizerCelebi.quantize(pixels, max_colors_to_extract)
# for color, count in result.items():
#     print(f"Quantized Color: {hex(color)}, Count: {count}")
```

### Scheme

Generates Material Design color schemes from a source color.

```python
from PyMCUlib.hct import Hct
from PyMCUlib.scheme import SchemeVibrant # Example scheme, others include SchemeTonalSpot, SchemeNeutral etc.

# Source color for the scheme
source_color_hct = Hct.from_int(0xFF6750A4) # Material Purple

# Create a vibrant color scheme (defaults to spec_version='2021', platform='phone')
   vibrant_scheme = SchemeVibrant(
       source_color_hct,
       is_dark=False,
       contrast_level=0.0,
       spec_version='2025',   # optional: override to the 2025 spec
       platform='phone'       # optional, defaults to 'phone'
   )

# Access colors from the scheme (as ARGB integers)
primary_color_argb = vibrant_scheme.primary
secondary_color_argb = vibrant_scheme.secondary

print(hex(primary_color_argb))
print(hex(secondary_color_argb))
```

### Score

Ranks colors for suitability in theming, often used after quantization.

```python
from PyMCUlib.score import Score

# Example: colors_with_counts from a quantizer
colors_with_counts = {
    0xff4285f4: 100,  # Google Blue
    0xff34a853: 80,   # Google Green
    0xfffbbc05: 60,   # Google Yellow
    0xffea4335: 40    # Google Red
}
# ScoreOptions can be used to customize scoring behavior
options = {'desired': 3, 'filter': True} 
ranked_colors_argb = Score.score(colors_with_counts, options=options) # Returns a list of ARGB integers
# print("Ranked Colors for Theming:")
# for color in ranked_colors_argb:
#     print(hex(color))
```

### Temperature

Provides utilities for finding analogous and complementary colors.

```python
from PyMCUlib.temperature import TemperatureCache
from PyMCUlib.hct import Hct

# Create a temperature cache for a color
source_hct = Hct.from_int(0xFF008772) # A teal color
temp_cache = TemperatureCache(source_hct)

# Get complementary color (as HCT)
complement_hct = temp_cache.complement
# print(f"Complementary Color HCT: H={complement_hct.hue:.2f}, C={complement_hct.chroma:.2f}, T={complement_hct.tone:.2f}")
# print(f"Complementary Color ARGB: {hex(complement_hct.to_int())}")

# Get analogous colors (list of HCT objects)
# count = number of analogous colors, divisions = segments in color wheel
analogous_hcts = temp_cache.analogous(count=3, divisions=12)
# print("Analogous Colors:")
# for hct in analogous_hcts:
#     print(f"  HCT: H={hct.hue:.2f}, C={hct.chroma:.2f}, T={hct.tone:.2f}, ARGB: {hex(hct.to_int())}")

```

### Utils
- **Dynamic Import**: In `PyMCUlib/utils/__init__.py`, submodules are loaded on-demand via `__getattr__` to avoid circular dependencies.  
- **Theme Generation**: `theme_from_source_color()`, `theme_from_image()`, `custom_color()`, `apply_theme()`, `set_scheme_properties()`, etc.

## License

This project follows the original Material Color Utilities project's license, which is the Apache License 2.0.

## Disclaimer

This is a personal port created for learning and usage in Python projects. While every effort has been made to faithfully reproduce the original TypeScript library's functionality, there may be errors or inconsistencies. Contributions and issue reports are welcome.

## Acknowledgments

Special thanks to the Google Material Color Utilities team for creating this powerful library, for their original C++ and TypeScript implementations, and for making it openly available.

## Very Important
I have adopted this lib in my own project and it works well. But I didn't verify all modules in my own project. Please report any issue via this [repository issues](https://github.com/wenkang-deepblue/PyMCUlib-Pythonized-material-color-utilities/issues) to let me know bugs. Thank you very much!

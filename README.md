
# PyMCUlib-cpp - Material Color Utilities Lib for Python (Ported from Official MCU of C++ version)

### Python version: >=3.12.0

**_Note:_** In 2025, the official Material Color Utilities library was updated to version 2025 as TypeScript & Java & Dart implementation. This Python package has since been reimplemented based on that latest TypeScript version ([main-ts](https://github.com/wenkang-deepblue/PyMCUlib-Pythonized-material-color-utilities)) and is published on PyPI as the default `PyMCUlib` package (install via `pip install PyMCUlib`). The original C++-based Python port ([main-cpp](https://github.com/wenkang-deepblue/PyMCUlib-Pythonized-material-color-utilities/tree/main-cpp)) has been renamed `PyMCUlib-cpp` and is available via `pip install PyMCUlib-cpp`. Please choose the package that best fits your needs.

## Overview
This project is a Python port of Google's [Material Color Utilities](https://github.com/material-foundation/material-color-utilities) library, originally implemented in **C++**. The Material Color Utilities (MCU) library provides algorithms and utilities that power the dynamic color system introduced in Material Design 3.

## Introduction

Material Design 3 introduces a dynamic color system that generates beautiful, accessible color schemes based on dynamic inputs like a user's wallpaper. This project faithfully mirrors the original MCU library's components, modules, parameters, outputs, and dependencies, making these powerful color tools accessible to Python developers.

## Port Information

This port maintains the spirit and functionality of the original C++ implementation while adapting to Python's conventions:

- Function and method names follow Python's snake_case convention while preserving the original names. <font color="#1967d2">For example:</font>
  - C++ `IsFidelity()` → Python `is_fidelity()`
  - C++ `GetRotatedHue()` → Python `get_rotated_hue()`

- Class names maintain PascalCase as in the original:
  - C++ `DynamicScheme` → Python `DynamicScheme`
  - C++ `TonalPalette` → Python `TonalPalette`

- Documentation has been added for all components and modules.

Due to fundamental differences between C++ and Python, this port cannot achieve a 1:1 replication. However, it faithfully mirrors the original C++ code's ideas, logic, and algorithms.


## Project Structure

Following the original MCU C++ lib, this Python lib project is organized into several modules (same as original MCU lib), each handling specific aspects of color processing:

```
PyMCUlib_cpp/
├── __init__.py                # Package entry point with public APIs
├── blend/                     # Color blending utilities
├── cam/                       # Color appearance model and HCT color space
│   ├── cam.py                 # CAM16 color appearance model
│   ├── hct.py                 # HCT (Hue, Chroma, Tone) color space
│   └── hct_solver.py          # HCT color solver algorithms
├── contrast/                  # Contrast ratio calculation and accessibility tools
├── dislike/                   # Detection and fixing of universally disliked colors
├── dynamiccolor/              # Dynamic color system for Material Design 3
│   ├── dynamic_color.py       # Core dynamic color implementation
│   ├── dynamic_scheme.py      # Dynamic color scheme implementation
│   └── variant.py             # Color scheme variants
├── palettes/                  # Color palette generation
│   ├── core.py                # Core palettes for Material Design
│   └── tones.py               # Tonal palette implementation
├── quantize/                  # Color extraction from images
│   ├── celebi.py              # Combined quantization algorithm
│   ├── lab.py                 # LAB color space conversion
│   ├── wu.py                  # Wu's quantization algorithm
│   └── wsmeans.py             # Weighted spherical means quantization
├── scheme/                    # Material Design color schemes
│   ├── vibrant.py             # Vibrant color scheme
│   ├── neutral.py             # Neutral color scheme
│   ├── monochrome.py          # Monochrome color scheme
│   └── [other schemes]        # Additional scheme implementations
├── score/                     # Color ranking and evaluation
│   └── score.py               # Algorithms for ranking colors
├── temperature/               # Color temperature theory implementation
│   └── temperature_cache.py   # Cache for temperature calculations
├── utils/                     # Common utility functions
│   └── utils.py               # Color conversion and math utilities
└── tests/                     # Test files to verify components/modules
```

### Component Descriptions

- **<font color="#1967d2">blend</font>**: Provides utilities for blending colors in different color spaces, enabling harmonious color combinations.

- **<font color="#1967d2">cam</font>**: Implements the CAM16 color appearance model and the HCT (Hue, Chroma, Tone) color space, which forms the foundation of material color system.

- **<font color="#1967d2">contrast</font>**: Contains tools for calculating contrast ratios between colors and generating accessible color combinations.

- **<font color="#1967d2">dislike</font>**: Identifies and fixes colors that are generally perceived as unpleasant, particularly in the yellow-green spectrum.

- **<font color="#1967d2">dynamiccolor</font>**: Powers the adaptive color system in Material Design 3, generating colors that respond to UI states and context.

- **<font color="#1967d2">palettes</font>**: Creates tonal palettes (variations of a color at different tones) used as building blocks for schemes.

- **<font color="#1967d2">quantize</font>**: Implements algorithms to extract key colors from images, essential for deriving themes from user content.

- **<font color="#1967d2">scheme</font>**: Generates complete Material Design color schemes with different aesthetic qualities (vibrant, neutral, etc.).

- **<font color="#1967d2">score</font>**: Evaluates colors for suitability in theming, considering both perceptual qualities and usage patterns.

- **<font color="#1967d2">temperature</font>**: Implements color temperature theory to find complementary and analogous colors for more harmonious designs.

- **<font color="#1967d2">utils</font>**: Provides core utility functions for color conversion, mathematical operations, and other common tasks.

## Components

The library consists of various components, each designed to be as self-contained as possible:

### Blend

Provides utilities for blending colors in the HCT color space, enabling smooth interpolation, harmonization, and gradation of colors.

```python
from PyMCUlib_cpp.blend import blend_harmonize, blend_hct_hue, blend_cam16_ucs

# Harmonize one color with another
harmonized_color = blend_harmonize(design_color, key_color)

# Blend hue between two colors (with amount 0.0-1.0)
mixed_color = blend_hct_hue(from_color, to_color, 0.5)
```

### Contrast

Offers tools for measuring contrast and obtaining contrastful colors that meet accessibility requirements.

```python
from PyMCUlib_cpp.contrast import ratio_of_tones, lighter, darker

# Calculate contrast ratio between two tones
contrast_ratio = ratio_of_tones(tone_a, tone_b)

# Find a lighter tone with specific contrast ratio
lighter_tone = lighter(tone, contrast_ratio)
```

### Dislike

Identifies and fixes universally disliked colors, based on color science research showing that dark yellow-greens are typically disliked.

```python
from PyMCUlib_cpp.dislike import is_disliked, fix_if_disliked
from PyMCUlib_cpp.cam.hct import Hct

# Check if a color is disliked
disliked = is_disliked(Hct.from_int(argb_color))

# Fix a disliked color
fixed_color = fix_if_disliked(Hct.from_int(argb_color))
```

### DynamicColor

Provides colors that adjust based on UI states like dark theme, style preferences, and contrast requirements. This component powers the adaptive capabilities of Material Design 3.

```python
from PyMCUlib_cpp.dynamiccolor import DynamicColor, DynamicScheme
from PyMCUlib_cpp.dynamiccolor.variant import Variant

# Create a dynamic color based on a scheme
dynamic_color = DynamicColor.from_palette(
    name="example_color",
    palette=lambda s: s.primary_palette,
    tone=lambda s: 40.0 if s.is_dark else 80.0
)

# Get the ARGB value of this color for a specific scheme
argb = dynamic_color.get_argb(scheme)
```

### HCT

Implements a new color space (Hue, Chroma, Tone) based on CAM16 and L*, which accounts for viewing conditions and provides a more perceptually accurate color model.

```python
from PyMCUlib_cpp.cam.hct import Hct

# Create HCT color from RGB
hct_color = Hct.from_int(0xFF0000FF)  # Blue

# Access HCT components
hue = hct_color.get_hue()
chroma = hct_color.get_chroma()
tone = hct_color.get_tone()

# Modify HCT components
hct_color.set_tone(80.0)  # Lighter blue
rgb_int = hct_color.to_int()  # Convert back to RGB
```

### Palettes

Creates tonal palettes (colors that vary only in tone) and core palettes (sets of tonal palettes needed for Material color schemes).

```python
from PyMCUlib_cpp.palettes.tones import TonalPalette

# Create a tonal palette from a color
palette = TonalPalette(0xFF0000FF)  # Blue

# Get different tones of the same color
light_blue = palette.get(90)
mid_blue = palette.get(50)
dark_blue = palette.get(10)
```

### Quantize

Extracts dominant colors from images, combining multiple algorithms (Wu quantizer and Weighted Spherical Means) for optimal results.

```python
from PyMCUlib_cpp.quantize.celebi import quantize_celebi

# Extract key colors from an image's pixels
pixels = [0xffff0000, 0xff00ff00, 0xff0000ff]  # Example pixels
result = quantize_celebi(pixels, max_colors=5)
```

### Scheme

Generates Material Design color schemes from a single color or core palette, supporting both static and dynamic variants.

```python
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.vibrant import SchemeVibrant

# Create a vibrant color scheme from a color
source_color = Hct.from_int(0xFF0000FF)  # Blue
vibrant_scheme = SchemeVibrant(source_color, is_dark=False)

# Access colors from the scheme
primary_color = vibrant_scheme.get_primary()
secondary_color = vibrant_scheme.get_secondary()
```

### Score

Ranks colors for suitability in theming, taking into account factors like usage frequency and perceptual characteristics.

```python
from PyMCUlib_cpp.score.score import ranked_suggestions, ScoreOptions

# Rank colors for theming suitability
colors_with_counts = {
    0xff4285f4: 100,  # Google Blue
    0xff34a853: 80,   # Google Green
    0xfffbbc05: 60,   # Google Yellow
    0xffea4335: 40    # Google Red
}
ranked_colors = ranked_suggestions(colors_with_counts)
```

### Temperature

Provides utilities for finding analogous and complementary colors based on color temperature theory.

```python
from PyMCUlib_cpp.temperature.temperature_cache import TemperatureCache
from PyMCUlib_cpp.cam.hct import Hct

# Create a temperature cache for a color
temp_cache = TemperatureCache(Hct.from_int(0xFF0000FF))

# Get complementary color
complement = temp_cache.get_complement()

# Get analogous colors
analogous_colors = temp_cache.get_analogous_colors()
```

## License

This project follows the original MCU project's license, which is the Apache License 2.0.

## Disclaimer

This is a personal port created for my own projects. While I've made every effort to faithfully reproduce the original library's functionality, there may be errors or inconsistencies. Contributions and issue reports are welcome.

## Acknowledgments

Special thanks to the original Google Material Color Utilities team for creating this powerful library and making it openly available.

## Very Important
I have adopted this lib in my own project and it works good. But I didn't verify all modules in my own project. Please report any issue via this [repository issues](https://github.com/wenkang-deepblue/PyMCUlib-Pythonized-material-color-utilities/issues) to let me know bugs. Thank you very much!
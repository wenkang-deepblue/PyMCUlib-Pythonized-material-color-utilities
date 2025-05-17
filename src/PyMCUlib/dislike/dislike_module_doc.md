# Dislike Analyzer Module Documentation

## Overview

The Dislike Analyzer component provides functionality to identify and fix "universally disliked" colors. Based on color science studies, certain dark yellow-green hues are consistently rated as unpleasant across different cultures and demographics. This aversion is correlated with distaste for biological waste and rotting food.

This component can be used to:
1. Check if a color is likely to be disliked by users
2. Automatically fix disliked colors by adjusting their tone

## Research Basis

The implementation is based on research by Palmer and Schloss (2010) and further elaborated in Schloss and Palmer's Chapter 21 in the Handbook of Color Psychology (2015). These studies found that dark yellow-greens with the following characteristics tend to be universally disliked:

- Hue: Between 90° and 111°
- Chroma: Greater than 16
- Tone: Less than 65

## Key Classes and Methods

### `DislikeAnalyzer`

A utility class that encapsulates the logic for identifying and fixing disliked colors.

#### Static Methods

##### `is_disliked(hct: Hct) -> bool`

Determines if a color is likely to be disliked.

**Parameters:**
- `hct`: An instance of `Hct` representing the color to be evaluated

**Returns:**
- `bool`: `True` if the color is disliked, `False` otherwise

##### `fix_if_disliked(hct: Hct) -> Hct`

If a color is disliked, adjusts its tone to make it more pleasant.

**Parameters:**
- `hct`: An instance of `Hct` representing the color to be evaluated and potentially fixed

**Returns:**
- `Hct`: Either a new modified `Hct` instance with tone set to 70.0 (if the original was disliked), or the original `Hct` instance (if it was already acceptable)

## Usage Examples

### Checking if a Color is Disliked

```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.dislike.dislike_analyzer import DislikeAnalyzer

# Create an HCT color
bile_color = Hct.from_int(0xff95884B)  # A bile-like yellow-green

# Check if the color is disliked
is_disliked = DislikeAnalyzer.is_disliked(bile_color)
print(f"Is this color disliked? {is_disliked}")  # Should print: True
```

### Fixing a Disliked Color

```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.dislike.dislike_analyzer import DislikeAnalyzer

# Create a disliked color
bile_color = Hct.from_int(0xff95884B)

# Fix the color if it's disliked
fixed_color = DislikeAnalyzer.fix_if_disliked(bile_color)

# The fixed color should be similar but with tone = 70.0
print(f"Original color: {bile_color}")
print(f"Fixed color: {fixed_color}")
print(f"Original tone: {bile_color.tone}, Fixed tone: {fixed_color.tone}")
```

### Processing a Palette of Colors

```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.dislike.dislike_analyzer import DislikeAnalyzer

# Process a palette of colors
palette = [0xff95884B, 0xffA07E56, 0xff604134, 0xff3A312A]
processed_palette = []

for color_int in palette:
    hct = Hct.from_int(color_int)
    fixed_hct = DislikeAnalyzer.fix_if_disliked(hct)
    processed_palette.append(fixed_hct.to_int())

print("Processed palette:", [hex(color) for color in processed_palette])
```

## Implementation Notes

- The component defines "disliked" as colors with:
  - Hue between 90° and 111° (yellow-green)
  - Chroma greater than 16
  - Tone less than 65
- The fixing algorithm simply adjusts the tone to 70.0 while preserving the hue and chroma
- This implementation is based on the original TypeScript version from Material Color Utilities
- Comparisons apply `round()` to each channel before thresholding.

## Dependencies

- `PyMCUlib.hct.hct`: Provides the `Hct` class for working with colors in the HCT color space

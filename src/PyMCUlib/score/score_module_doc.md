# Score Module Documentation

## Overview

The Score module provides functionality for ranking colors based on their suitability for use in a UI theme. It takes a set of colors (with their population counts, typically from an image) and ranks them according to factors such as chroma (colorfulness) and usage proportion.

This module enables the use of a high cluster count for image quantization, ensuring colors aren't muddied, while curating the high cluster count to a much smaller number of appropriate choices for UI themes.

## Key Features

- Ranks colors based on suitability for UI themes
- Filters out unsuitable colors (low chroma, low usage)
- Ensures a good distribution of hues in the selected colors
- Provides fallback colors when no suitable colors are found

## Main Components

### ScoreOptions

TypedDict for configuring color ranking behavior.

**Properties:**
- `desired`: Maximum number of colors to return (default: 4)
- `fallbackColorARGB`: Default color to use if no suitable colors are found (default: Google Blue, 0xff4285f4)
- `filter`: Whether to filter out unsuitable colors (default: True)

### Score

Static class for scoring and ranking colors.

**Constants:**
- `TARGET_CHROMA`: Target chroma value (48.0)
- `WEIGHT_PROPORTION`: Weight for proportional usage (0.7)
- `WEIGHT_CHROMA_ABOVE`: Weight for chroma above target (0.3)
- `WEIGHT_CHROMA_BELOW`: Weight for chroma below target (0.1)
- `CUTOFF_CHROMA`: Minimum chroma for a color to be considered (5.0)
- `CUTOFF_EXCITED_PROPORTION`: Minimum usage proportion for a color to be considered (0.01)

**Methods:**
- `score(colors_to_population: Mapping[int, int], options: ScoreOptions = None) -> List[int]`: Ranks colors based on suitability for UI themes

## Usage Examples

### Basic Color Ranking

```python
from PyMCUlib.score.score import Score

# Map of colors (as ARGB integers) to their population counts
colors_to_population = {
    0xffff0000: 10,  # Red
    0xff00ff00: 20,  # Green
    0xff0000ff: 5,   # Blue
    0xffffffff: 3    # White
}

# Rank the colors (default is to return up to 4 colors)
ranked_colors = Score.score(colors_to_population)
print([hex(c) for c in ranked_colors])  # [0xff00ff00, 0xffff0000, 0xff0000ff]
```
### Custom Ranking Options
```python
from PyMCUlib.score.score import Score

colors_to_population = {
    0xffff0000: 10,  # Red
    0xff00ff00: 20,  # Green
    0xff0000ff: 5,   # Blue
    0xffffffff: 3    # White
}

# Custom ranking options
options = {
    "desired": 2,                # Return at most 2 colors
    "fallbackColorARGB": 0xffFFAB40,  # Custom fallback color (amber)
    "filter": False              # Don't filter unsuitable colors
}

ranked_colors = Score.score(colors_to_population, options)
print(ranked_colors)  # [0xff00ff00, 0xffff0000]
```
### Color Theme Extraction from Image
```python
from PyMCUlib.score.score import Score
from PyMCUlib.quantize.quantizer_wsmeans import QuantizerWsmeans

# Assume we have pixel data from an image
pixel_data = [...]  # List of ARGB integers

# Quantize the image to get key colors and their populations
colors_to_population = QuantizerWsmeans.quantize(pixel_data, 128)

# Get top 5 theme colors
theme_colors = Score.score(colors_to_population, {"desired": 5})

# Use these colors in your UI
print(f"Primary: {hex(theme_colors[0])}")
print(f"Secondary: {hex(theme_colors[1])}")
print(f"Tertiary: {hex(theme_colors[2])}")
```
### ScoreOptions

TypedDict for configuring color ranking behavior.

**Properties:**
- `desired`: Maximum number of colors to return (default: 4)
- `fallbackColorARGB`: Default color to use if no suitable colors are found (default: Google Blue, 0xff4285f4)
- `filter`: Whether to filter out unsuitable colors (default: True)

**Note:** Option dictionary keys are case-sensitive and must match exactly: `desired`, `fallbackColorARGB`, and `filter`.

### Score

Static class for scoring and ranking colors.

**Note:** This class cannot be instantiated; use its static method `Score.score(...)`.

**Constants:**
- `TARGET_CHROMA`: Target chroma value (48.0)
- `WEIGHT_PROPORTION`: Weight for proportional usage (0.7)
- `WEIGHT_CHROMA_ABOVE`: Weight for chroma above target (0.3)
- `WEIGHT_CHROMA_BELOW`: Weight for chroma below target (0.1)
- `CUTOFF_CHROMA`: Minimum chroma for a color to be considered (5.0)
- `CUTOFF_EXCITED_PROPORTION`: Minimum usage proportion for a color to be considered (0.01)

## Implementation Notes
- The scoring algorithm considers both the chroma (colorfulness) and the usage proportion of each color.
- Colors with very low chroma (below `CUTOFF_CHROMA`) or very low usage (below `CUTOFF_EXCITED_PROPORTION`) can be filtered out.
- The algorithm tries to select colors with a good distribution of hues, starting with a minimum hue difference of 90° and decreasing to 15° if necessary.
- If no suitable colors are found, a fallback color (Google Blue by default) is returned.
- The HCT color space is used for color calculations, which provides perceptually accurate measures of hue, chroma, and tone.

## Dependencies
- `PyMCUlib.hct.hct`: For working with colors in the HCT color space
- `PyMCUlib.utils.math_utils`: For mathematical operations
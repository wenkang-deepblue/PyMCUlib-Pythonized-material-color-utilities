# <center> Score Component Documentation </center>

## Overview

The Score component provides functionality for ranking colors based on their suitability for use in UI themes. It analyzes colors from a source (like an image) and determines which colors would work best as theme colors.

The component takes into account factors such as:
- Color usage frequency (how often a color appears)
- Color chroma (saturation)
- Hue distribution (to ensure selected colors have sufficient hue diversity)

## Main Features

The Score component contains:

- `ScoreOptions` class for configuring the ranking process
- `ranked_suggestions` function that ranks colors by suitability for UI themes

## Algorithm Constants

The scoring algorithm uses several important constants that affect its behavior:

| Constant | Value | Description |
|----------|-------|-------------|
| `_TARGET_CHROMA` | 48.0 | Target chroma value (based on A1 color system) |
| `_WEIGHT_PROPORTION` | 0.7 | Weight given to color usage proportion in scoring |
| `_WEIGHT_CHROMA_ABOVE` | 0.3 | Weight for chroma score when above target chroma |
| `_WEIGHT_CHROMA_BELOW` | 0.1 | Weight for chroma score when below target chroma |
| `_CUTOFF_CHROMA` | 5.0 | Minimum chroma threshold for valid colors |
| `_CUTOFF_EXCITED_PROPORTION` | 0.01 | Minimum usage proportion threshold |

## Class Details

### ScoreOptions

```python
@dataclass
class ScoreOptions:
    desired: int = 4                        # Default: 4 colors
    fallback_color_argb: int = 0xff4285f4   # Default: Google Blue
    filter: bool = True                     # Default: Apply filtering
```

Configuration options for the color ranking process.

#### Attributes:
* `desired`: Maximum number of colors to return (default: 4)
* `fallback_color_argb`: Default color to use if no suitable colors are found (default: 0xff4285f4, Google Blue)
* `filter`: Whether to filter out hues that are not used often enough and colors that are effectively grayscale (default: True)

#### Example:
```python
from PyMCUlib_cpp.score import ScoreOptions

# Default options
options = ScoreOptions()

# Custom options
custom_options = ScoreOptions(
    desired=5,                          # Return up to 5 colors
    fallback_color_argb=0xff000000,     # Use black as fallback
    filter=False                        # Don't filter out any colors
)
```

## Function Details

### ranked_suggestions

```python
def ranked_suggestions(argb_to_population: Dict[int, int], options: ScoreOptions = ScoreOptions()) -> List[int]:
```
Given a map with keys of colors and values of how often the color appears, rank the colors based on suitability for being used for a UI theme.

The list returned is of length <= desired (from options). The recommended color is the first item, the least suitable is the last. There will always be at least one color returned. If all the input colors were not suitable for a theme, a default fallback color will be provided, Google Blue, or supplied fallback color. The default number of colors returned is 4, as that's the number of colors displayed in Android 12's wallpaper picker.

#### Parameters:
* `argb_to_population`: Dictionary mapping ARGB color values to their population (frequency) count
* `options`: Configuration options for the ranking process

#### Returns:
* List of ARGB colors ranked by suitability for UI themes

#### Algorithm Workflow:
1. **Color Analysis**: Convert ARGB colors to HCT (Hue, Chroma, Tone) and calculate usage distribution
2. **Hue Excitement**: Calculate "excited proportions" for each hue by considering neighboring hues (±15 degrees)
3. **Color Scoring**: Score each color based on:
   - Proportion score = proportion × 100 × `_WEIGHT_PROPORTION`
   - Chroma score = (chroma - `_TARGET_CHROMA`) × chroma_weight
   - Total score = proportion_score + chroma_score
4. **Hue Distribution**: Select colors with maximum hue diversity:
   - Start with 90° difference, decrease down to 15° minimum
   - Avoid selecting colors with similar hues
5. **Fallback**: If no suitable colors found, use fallback color

#### Example:
```python
from PyMCUlib_cpp.score import ranked_suggestions, ScoreOptions
from PyMCUlib_cpp.utils.utils import hex_from_argb

# Sample colors and their frequencies
colors = {
    0xffff0000: 50,  # Red
    0xff00ff00: 30,  # Green
    0xff0000ff: 20,  # Blue
    0xffffff00: 10   # Yellow
}

# Get top 3 colors suitable for a theme
top_colors = ranked_suggestions(colors, ScoreOptions(desired=3))

# Print the results
for color in top_colors:
    print(f"Color: {hex_from_argb(color)}")

# Example output:
# Color: #FF0000
# Color: #00FF00
# Color: #0000FF
```

## Class Details
### ScoreOptions
```python
@dataclass
class ScoreOptions:
    desired: int = 4                        # Default: 4 colors
    fallback_color_argb: int = 0xff4285f4   # Default: Google Blue
    filter: bool = True                     # Default: Apply filtering
```
Configuration options for the color ranking process.

#### Attributes:
* `desired`: Maximum number of colors to return (default: 4)
* `fallback_color_argb`: Default color to use if no suitable colors are found (default: 0xff4285f4, Google Blue)
* `filter`: Whether to filter out hues that are not used often enough and colors that are effectively grayscale (default: True)

#### Example:
```python
from score import ScoreOptions

# Default options
options = ScoreOptions()

# Custom options
custom_options = ScoreOptions(
    desired=5,                          # Return up to 5 colors
    fallback_color_argb=0xff000000,     # Use black as fallback
    filter=False                        # Don't filter out any colors
)
```
## Usage Notes
* All colors are represented in ARGB format (32-bit integers, typically represented in hexadecimal as 0xAARRGGBB)
* The component prioritizes colors with higher chroma (more saturated) when frequencies are equal
* When selecting colors, the algorithm attempts to maximize the hue distance between them
* Colors with very low chroma (< 5.0) or low usage will be filtered out by default
* The component depends on the PyMCUlib_cpp.utils and PyMCUlib_cpp.cam.hct modules

## Hue Distribution Algorithm

The algorithm uses an iterative approach to find colors with maximum hue diversity:

1. Sort candidate colors by their score (from highest to lowest)
2. Start with a desired minimum angular difference of 90° between colors
3. Try to select up to `desired` colors with hues at least that far apart
4. If not enough colors can be found, reduce the angular requirement by small increments down to 15°
5. This process ensures the selected colors have visually distinct hues while maintaining high scores

## Complete Example
```python
from PyMCUlib_cpp.score import ranked_suggestions, ScoreOptions
from PyMCUlib_cpp.utils.utils import hex_from_argb

# Sample image color analysis (mapping colors to number of pixels)
image_colors = {
    0xff5b3a29: 1200,  # Brown
    0xff2a60b0: 800,   # Blue
    0xfff7d94c: 600,   # Yellow
    0xff9d0006: 400,   # Red
    0xff0f7173: 300,   # Teal
    0xff000000: 200,   # Black
    0xffffffff: 100    # White
}

# Get color suggestions with default options
default_suggestions = ranked_suggestions(image_colors)
print("Default color suggestions:")
for color in default_suggestions:
    print(f"  {hex_from_argb(color)}")

# Expected output:
# Default color suggestions:
#   #5B3A29
#   #F7D94C
#   #2A60B0
#   #9D0006

# Get color suggestions with custom options
custom_options = ScoreOptions(
    desired=2,                          # Only want 2 colors
    fallback_color_argb=0xff00ff00,     # Use green as fallback
    filter=False                        # Don't filter colors
)

custom_suggestions = ranked_suggestions(image_colors, custom_options)
print("\nCustom color suggestions:")
for color in custom_suggestions:
    print(f"  {hex_from_argb(color)}")

# Expected output:
# Custom color suggestions:
#   #5B3A29
#   #2A60B0
```

## Import Structure

```python
# Import the score component
from PyMCUlib_cpp.score import ranked_suggestions, ScoreOptions

# For additional utilities
from PyMCUlib_cpp.utils.utils import hex_from_argb
```
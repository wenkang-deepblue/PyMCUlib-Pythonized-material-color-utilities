# <center> Wu Module Documentation </center>

The Wu quantizer is a color quantization algorithm developed by Xiaolin Wu. This implementation is part of the Material Color Utilities library and provides functionality to reduce the number of colors in an image while preserving visual appearance.

## Overview

Wu's algorithm uses statistical techniques to find optimal color clusters in RGB space by minimizing the weighted variance of colors within each cluster. The algorithm works as follows:

1. It constructs a 3D histogram of colors in RGB space.
2. It computes statistical moments for the histogram.
3. It recursively splits the color space into boxes (cubes) that minimize color variance.
4. It computes the average color for each box to represent that color cluster.

## Usage

```python
from PyMCUlib_cpp.quantize.wu import quantize_wu
from PyMCUlib_cpp.utils.utils import argb_from_rgb

# Example: Create a list with some sample colors (in ARGB format 0xFFRRGGBB)
pixels = [
    0xFF0000FF,  # Blue
    0xFF00FF00,  # Green
    0xFFFF0000,  # Red
    0xFFFFFF00,  # Yellow
    0xFFFF00FF,  # Magenta
    0xFF00FFFF,  # Cyan
    0xFFFFFFFF,  # White
    0xFF808080   # Gray
]

# Quantize to a maximum of 4 colors
max_colors = 4
result_colors = quantize_wu(pixels, max_colors)

# Print the resulting colors
print(f"Quantized from {len(pixels)} to {len(result_colors)} colors:")
for color in result_colors:
    r = (color & 0x00FF0000) >> 16
    g = (color & 0x0000FF00) >> 8
    b = (color & 0x000000FF)
    print(f"RGB({r}, {g}, {b}) - Hex: {color:08X}")

# Sample output:
# Quantized from 8 to 4 colors:
# RGB(255, 0, 0) - Hex: FFFF0000
# RGB(0, 255, 255) - Hex: FF00FFFF
# RGB(0, 0, 255) - Hex: FF0000FF
# RGB(255, 255, 0) - Hex: FFFFFF00
```
## API Reference

### `quantize_wu(pixels: List[Argb], max_colors: int) -> List[Argb]`

Quantizes a set of colors using Wu's algorithm.

#### Parameters:
* `pixels (List[Argb])`: A list of colors in ARGB format (0xFFRRGGBB). The `Argb` type is an integer representing a color with alpha, red, green, and blue channels.
* `max_colors (int)`: The maximum number of colors to return (must be between 1 and 256).

#### Returns:
* `List[Argb]`: A list of representative colors in ARGB format.

#### Constraints:
* If `max_colors` is less than or equal to 0, greater than 256, or if `pixels` is empty, an empty list is returned.

## Type Definitions

* `Argb`: An integer type representing a color in ARGB format (0xFFRRGGBB), where:
  * Alpha (A) is in bits 24-31
  * Red (R) is in bits 16-23
  * Green (G) is in bits 8-15
  * Blue (B) is in bits 0-7

## Notes

* The implementation has a maximum limit of 256 colors.
* The algorithm discards transparency information and only works with RGB components.
* The algorithm may return fewer colors than requested if the input has fewer unique colors or if optimal clustering results in fewer clusters.
* The output colors are not sorted in any particular order.
* Wu's algorithm is computationally efficient and produces high-quality results for color quantization.

## Helper Functions

The module also provides the `argb_from_rgb` utility function to create ARGB colors from RGB components:

```python
from PyMCUlib_cpp.utils.utils import argb_from_rgb

# Create an ARGB color with full opacity
red_color = argb_from_rgb(255, 0, 0)  # Results in 0xFFFF0000
```

## References

* Wu, Xiaolin, *"Color quantization by dynamic programming and principal analysis"*, ACM Transactions on Graphics, 11(4), 1992.
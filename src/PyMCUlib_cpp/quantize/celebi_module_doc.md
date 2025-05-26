# <center> Celebi Module Documentation </center>

## Overview

The Celebi Quantizer is a color quantization component in the Material Color Utilities library. It's named after the paper "Celebi quantization" and provides an efficient way to reduce the number of colors in an image while preserving visual quality.

Celebi quantization works by combining two algorithms: Wu's color quantizer and Weighted Spherical Means (WSmeans). Wu's algorithm is used to generate initial color clusters, which then serve as starting points for the more refined WSmeans algorithm.

## Main Features

The Celebi component offers a single main function:

- `quantize_celebi`: Quantizes colors using Wu's quantizer for initial clusters, then refines using WSmeans.

## Function Details

### quantize_celebi

```python
def quantize_celebi(pixels: List[Argb], max_colors: int) -> QuantizerResult:
```
This function quantizes a list of colors to a specific maximum number, using a combination of Wu's quantizer and WSmeans.

### Parameters:
* `pixels`: List of pixels in ARGB format (integers, typically represented in hexadecimal, like 0xffrrggbb)
* `max_colors`: The maximum number of colors to generate (up to 256)

### Returns:
A `QuantizerResult` object containing:
* `color_to_count`: Dictionary mapping quantized colors to their frequency count
* `input_pixel_to_cluster_pixel`: Dictionary mapping input pixels to their corresponding quantized colors

## QuantizerResult Class

```python
class QuantizerResult:
    """
    Result of color quantization.
    Contains a mapping of colors to their frequency counts
    and a mapping of input pixels to their corresponding cluster pixels.
    """
    def __init__(self):
        self.color_to_count: Dict[Argb, int] = {}
        self.input_pixel_to_cluster_pixel: Dict[Argb, Argb] = {}
```

## Example:
```python
from PyMCUlib_cpp.quantize.celebi import quantize_celebi
from PyMCUlib_cpp.utils.utils import hex_from_argb

# Sample image pixels (simplified for illustration)
pixels = [0xffff0000, 0xff00ff00, 0xff0000ff, 0xffffff00, 0xffff00ff]

# Quantize to a maximum of 3 colors
result = quantize_celebi(pixels, 3)

# Print the quantized colors and their counts
for color, count in result.color_to_count.items():
    print(f"Color: {hex_from_argb(color)}, Count: {count}")

# Print input to output color mapping
for input_color, output_color in result.input_pixel_to_cluster_pixel.items():
    print(f"Input: {hex_from_argb(input_color)} → Output: {hex_from_argb(output_color)}")
```

## Usage Notes
* The Celebi quantizer is generally more accurate than using either Wu's algorithm or WSmeans alone.
* Transparent pixels (pixels with alpha channel values less than 255) are excluded from quantization. The function automatically filters these out before processing.
* If `max_colors` is greater than 256, it is capped at 256.
* If `max_colors` is 0 or pixels is empty, an empty QuantizerResult is returned.
* The algorithm uses Wu's quantizer to generate initial clusters that are then fed into WSmeans for refinement.
* The implementation handles all error cases gracefully without throwing exceptions.

## Dependencies
This component depends on the following components within the Material Color Utilities library:
* `PyMCUlib_cpp.utils.utils`: For ARGB color manipulation and opacity checking
* `PyMCUlib_cpp.quantize.wu`: For Wu's color quantization algorithm
* `PyMCUlib_cpp.quantize.wsmeans`: For the WSmeans color quantization algorithm

## Complete Example
```python
from PyMCUlib_cpp.quantize.celebi import quantize_celebi
from PyMCUlib_cpp.utils.utils import hex_from_argb

# Create a sample image with a variety of colors
pixels = []
for i in range(100):
    # Create a gradient of colors
    r = (i * 255) // 100
    g = ((100 - i) * 255) // 100
    b = (i % 50) * 5
    pixels.append(0xff000000 | (r << 16) | (g << 8) | b)

# Quantize to 8 colors
result = quantize_celebi(pixels, 8)

print(f"Original number of colors: {len(set(pixels))}")
print(f"Quantized number of colors: {len(result.color_to_count)}")

print("\nQuantized colors and their counts:")
for color, count in result.color_to_count.items():
    print(f"Color: {hex_from_argb(color)}, Count: {count}")

print("\nMapping of some original colors to their quantized values:")
# Print just the first 5 mappings as an example
for i, (original, quantized) in enumerate(result.input_pixel_to_cluster_pixel.items()):
    if i >= 5:
        break
    print(f"Original: {hex_from_argb(original)} → Quantized: {hex_from_argb(quantized)}")
```

This example creates a gradient of 100 colors and quantizes it down to 8 colors, demonstrating how the Celebi quantizer works to reduce the color palette while preserving visual quality.

## Implementation Details

The implementation follows these steps:
1. Validate inputs and handle edge cases
2. Filter out transparent pixels
3. Apply Wu's quantization algorithm to generate initial clusters
4. Use these clusters as starting points for WSmeans quantization
5. Return the final quantization result

This two-step approach provides better quality color quantization than either algorithm alone, making it ideal for applications requiring high-quality color palette extraction.

# <center> WSMeans Module Documentation </center>

## Overview

The WSMeans component provides an implementation of a weighted spherical k-means algorithm for color quantization. This algorithm clusters colors in a perceptually uniform color space (Lab) to produce a palette of representative colors.

## Main Features

The WSMeans component contains one main function:

- `quantize_wsmeans`: Quantizes colors using a weighted spherical k-means algorithm

## Function Details

### quantize_wsmeans

```python
def quantize_wsmeans(input_pixels: List[Argb], 
                     starting_clusters: List[Argb], 
                     max_colors: int) -> QuantizerResult
```
Quantizes colors using a weighted spherical k-means algorithm, which clusters colors in the Lab color space.

### Parameters:
* `input_pixels`: List of pixels in ARGB format
* `starting_clusters`: Initial cluster centers in ARGB format (can be empty)
* `max_colors`: Maximum number of colors to generate (capped at 256)

Returns:
* `QuantizerResult`: An object containing two mappings:

    * `color_to_count`: Maps quantized colors to their frequencies
    * `input_pixel_to_cluster_pixel`: Maps input colors to their assigned cluster colors

### Example:
```python
from PyMCUlib.quantize.wsmeans import quantize_wsmeans
from PyMCUlib.utils.utils import hex_from_argb

# Define some pixels
pixels = [0xffff0000, 0xff00ff00, 0xff0000ff, 0xffff00ff, 0xff00ffff]

# Quantize to at most 3 colors
result = quantize_wsmeans(pixels, [], 3)

# Print the result
for color, count in result.color_to_count.items():
    print(f"Color: {hex_from_argb(color)}, Count: {count}")
```
## Key Classes
### QuantizerResult
```python
class QuantizerResult:
    def __init__(self):
        self.color_to_count: Dict[Argb, int] = {}
        self.input_pixel_to_cluster_pixel: Dict[Argb, Argb] = {}
```
Stores the result of color quantization, containing mappings of colors to counts and input pixels to cluster pixels.

## Implementation Details

The implementation includes several helper classes and constants:

### Constants
* `MAX_ITERATIONS = 100`: Maximum number of iterations for the clustering algorithm
* `MIN_DELTA_E = 3.0`: Minimum color difference threshold for reassigning points

### Helper Classes
* `Swatch`: Represents a color swatch with its population count
* `DistanceToIndex`: Associates a distance with an index for sorting cluster distances

## Usage Notes

* The maximum number of colors is capped at 256
* If the `starting_clusters` list is empty, random clusters will be generated
* The algorithm uses Lab color space as it is perceptually uniform
* The algorithm iteratively refines the clusters until convergence or a maximum number of iterations
* The algorithm is deterministic due to fixed random seeds (42688)

## Algorithm Details
The algorithm works as follows:
1. Process input pixels and count frequencies of unique colors
2. Initialize clusters from starting_clusters or generate random clusters
3. Assign each unique color to a random initial cluster
4. Iteratively (max 100 iterations):
   * Calculate distances between all clusters using the delta_e function in Lab space
   * Reassign points to closer clusters if the improvement is significant (greater than MIN_DELTA_E)
   * Recalculate cluster centers as the weighted mean of their assigned points
   * Stop if no points were reassigned (except for the first iteration)
5. Construct the final mappings of colors to counts and input pixels to cluster pixels

## Dependencies
* `PyMCUlib.utils.utils`: For basic color manipulation functions
   * `Argb`: Type alias for color values in ARGB format
   * `hex_from_argb`: Converts a color in ARGB format to a hexadecimal string
   * `argb_from_rgb`: Converts RGB components to ARGB format
* `PyMCUlib.quantize.lab`: For Lab color space conversions
   * `Lab`: Class representing a color in Lab color space
   * `lab_from_int`: Converts from ARGB to Lab color space
   * `int_from_lab`: Converts from Lab to ARGB color space

## Complete Example
```python
from PyMCUlib.quantize.wsmeans import quantize_wsmeans
from PyMCUlib.utils.utils import hex_from_argb, argb_from_rgb

# Generate some test colors
red = 0xffff0000
green = 0xff00ff00
blue = 0xff0000ff
yellow = 0xffffff00
cyan = 0xff00ffff
magenta = 0xffff00ff

pixels = [red, green, blue, yellow, cyan, magenta]

# Quantize to 3 colors
result = quantize_wsmeans(pixels, [], 3)

print("Quantized colors:")
for color, count in result.color_to_count.items():
    print(f"  {hex_from_argb(color)}: {count} occurrences")

print("\nColor mappings:")
for original, quantized in result.input_pixel_to_cluster_pixel.items():
    print(f"  {hex_from_argb(original)} -> {hex_from_argb(quantized)}")
```

## Integration with Other Quantizers

The WSMeans quantizer can be used with other quantization methods like Wu's algorithm. The `quantize_celebi` function in `PyMCUlib.quantize.celebi` uses Wu's quantizer to generate initial clusters, then refines them using WSMeans.

Example integration:
```python
from PyMCUlib.quantize.celebi import quantize_celebi

# Generate some test colors
pixels = [0xffff0000, 0xff00ff00, 0xff0000ff, 0xffffff00, 0xff00ffff, 0xffff00ff]

# Use Celebi's method (Wu + WSMeans)
result = quantize_celebi(pixels, 3)
```

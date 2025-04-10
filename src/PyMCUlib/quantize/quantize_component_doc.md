# <center> Quantize Component Documentation </center>

# Overview

The Quantize component provides algorithms for color quantization - the process of reducing the number of colors in an image while preserving its visual appearance. This component is particularly useful for palette generation, image compression, and theme extraction from images.

The quantization process works by grouping similar colors together and representing each group with a representative color. Different algorithms offer various trade-offs between speed, accuracy, and quality of the resulting color palette.

## Modules

The Quantize component consists of the following modules:

### 1. Lab
Provides conversion between ARGB colors and the CIE Lab color space. Lab is a perceptually uniform color space that's ideal for color comparison and manipulation.

**Key functions:**
- `lab_from_int(argb: Argb) -> Lab`: Converts ARGB color to Lab color space
- `int_from_lab(lab: Lab) -> Argb`: Converts Lab color to ARGB format
- `Lab` class with `delta_e(lab: Lab) -> float` method for color comparison

### 2. Wu
Implements Xiaolin Wu's color quantization algorithm, which uses statistical techniques to find optimal color clusters by minimizing variance.

**Key functions:**
- `quantize_wu(pixels: List[Argb], max_colors: int) -> List[Argb]`: Reduces an array of colors to at most max_colors representative colors

### 3. WSmeans
Implements a weighted spherical k-means algorithm for color quantization, operating in Lab color space.

**Key functions:**
- `quantize_wsmeans(input_pixels: List[Argb], starting_clusters: List[Argb], max_colors: int) -> QuantizerResult`: Clusters colors in Lab space to produce a palette
- `QuantizerResult` class to store quantization results with mappings of colors to counts and input pixels to cluster pixels

### 4. Celebi
Combines Wu and WSmeans algorithms for superior color quantization results.

**Key functions:**
- `quantize_celebi(pixels: List[Argb], max_colors: int) -> QuantizerResult`: Uses Wu's algorithm for initial clusters and WSmeans for refinement

## Component Architecture
The Quantize component has the following dependency structure:

```
                    Utils
                      ↑
                      |
                     Lab
                    ↗   ↖
                   ↗      ↖
                  ↗         ↖
                 Wu         WSmeans
                  ↘         ↗
                   ↘      ↗
                    ↘   ↗
                    Celebi
```

## Key Types

### `Argb`
An integer type representing a color in ARGB format (0xFFRRGGBB), where:
- Alpha (A) is in bits 24-31
- Red (R) is in bits 16-23
- Green (G) is in bits 8-15
- Blue (B) is in bits 0-7

### `Lab`
A named tuple representing a color in CIE Lab color space:
- `l`: Lightness component (0-100)
- `a`: Green-red component (typically -128 to 127)
- `b`: Blue-yellow component (typically -128 to 127)

### `QuantizerResult`
A class containing the results of color quantization:
- `color_to_count: Dict[Argb, int]`: Maps quantized colors to their frequency counts
- `input_pixel_to_cluster_pixel: Dict[Argb, Argb]`: Maps input colors to their assigned cluster colors

# Usage Examples

## Basic Usage with Celebi Quantizer
```python
from PyMCUlib.quantize.celebi import quantize_celebi
from PyMCUlib.utils.utils import hex_from_argb

# Sample image pixels
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

## Using Wu's Algorithm Directly
```python
from PyMCUlib.quantize.wu import quantize_wu
from PyMCUlib.utils.utils import hex_from_argb

# Sample colors
pixels = [0xFF0000FF, 0xFF00FF00, 0xFFFF0000, 0xFFFFFF00, 0xFFFF00FF]

# Quantize to 3 colors
result_colors = quantize_wu(pixels, 3)

# Print the resulting colors
for color in result_colors:
    r = (color & 0x00FF0000) >> 16
    g = (color & 0x0000FF00) >> 8
    b = (color & 0x000000FF)
    print(f"RGB({r}, {g}, {b}) - Hex: {hex_from_argb(color)}")
```

## Using WSmeans with Custom Starting Clusters
```python
from PyMCUlib.quantize.wsmeans import quantize_wsmeans
from PyMCUlib.utils.utils import hex_from_argb

# Sample colors
pixels = [0xffff0000, 0xff00ff00, 0xff0000ff, 0xffffff00, 0xffff00ff]

# Define starting clusters
starting_clusters = [0xffff0000, 0xff00ff00, 0xff0000ff]  # Red, Green, Blue

# Quantize using WSmeans with provided starting clusters
result = quantize_wsmeans(pixels, starting_clusters, 3)

# Print the results
for color, count in result.color_to_count.items():
    print(f"Color: {hex_from_argb(color)}, Count: {count}")
```

## Converting Between Color Spaces
```python
from PyMCUlib.quantize.lab import Lab, lab_from_int, int_from_lab
from PyMCUlib.utils.utils import hex_from_argb

# Convert from ARGB to Lab
blue_argb = 0xFF0000FF
lab_blue = lab_from_int(blue_argb)
print(f"Blue in Lab: {lab_blue}")

# Convert from Lab to ARGB
lab_red = Lab(53.2, 80.1, 67.2)  # Approximately red
argb_red = int_from_lab(lab_red)
print(f"Red in ARGB: {hex_from_argb(argb_red)}")

# Calculate color distance
lab1 = Lab(50.0, 20.0, 30.0)
lab2 = Lab(55.0, 25.0, 35.0)
distance = lab1.delta_e(lab2)
print(f"Color distance: {distance}")
```

# Advanced Features

## Theme Generation from an Image
```python
from PyMCUlib.quantize.celebi import quantize_celebi
from PyMCUlib.utils.utils import hex_from_argb
from PIL import Image
import numpy as np

# Load an image
image = Image.open("example.jpg")
pixels = np.array(image).reshape(-1, 3)

# Convert RGB pixels to ARGB format
argb_pixels = [0xFF000000 | (r << 16) | (g << 8) | b for r, g, b in pixels]

# Quantize to 5 colors for a theme
result = quantize_celebi(argb_pixels, 5)

# Extract the 5 most common colors
theme_colors = sorted(result.color_to_count.items(), 
                     key=lambda x: x[1], reverse=True)[:5]

print("Theme colors:")
for color, count in theme_colors:
    print(f"#{hex_from_argb(color)} - Used {count} times")
```

## Performance Considerations

* **Wu's algorithm** is faster but may produce less visually coherent palettes
  * Time complexity: O(n + k²), where n is the number of pixels and k is the color depth (32 for most cases)
  * Space complexity: O(k³)
  * Best for: Large datasets where speed is critical

* **WSmeans** is more computationally intensive but produces better results for visually similar colors
  * Time complexity: O(n·c·i), where n is the number of pixels, c is the number of clusters, and i is the number of iterations
  * Space complexity: O(n + c²)
  * Best for: Situations requiring perceptually accurate color clustering

* **Celebi** offers a good balance of performance and quality by combining both approaches
  * Time complexity: Combined complexity of Wu's algorithm and WSmeans
  * Best for: Most general use cases requiring quality results

For performance-critical applications, consider using Wu's algorithm directly. For applications where quality is paramount, Celebi is recommended.

## Handling of Transparent Pixels

* All quantizers operate only on opaque colors
* The `quantize_celebi` function automatically filters out non-opaque pixels (alpha < 255)
* If transparency handling is required, you should process transparent pixels separately
* When processing images with transparency, consider pre-filtering or separating transparent regions

# API Reference

## Lab Module

### `Lab` Class
```python
class Lab(NamedTuple):
    l: float = 0.0
    a: float = 0.0
    b: float = 0.0
    
    def delta_e(self, lab: 'Lab') -> float:
        """Calculates the squared color distance between two colors in Lab space."""
```

### Functions
```python
def lab_from_int(argb: Argb) -> Lab:
    """Converts a color from ARGB format to Lab color space."""
    
def int_from_lab(lab: Lab) -> Argb:
    """Converts a color from Lab color space to ARGB format."""
```

## Wu Module

### Functions
```python
def quantize_wu(pixels: List[Argb], max_colors: int) -> List[Argb]:
    """
    Quantize colors using Wu's algorithm.
    
    Args:
        pixels: A list of pixels in ARGB format.
        max_colors: The maximum number of colors to return (1-256).
        
    Returns:
        A list of quantized colors in ARGB format.
    """
```

## WSmeans Module

### `QuantizerResult` Class
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

### Functions
```python
def quantize_wsmeans(input_pixels: List[Argb], 
                     starting_clusters: List[Argb], 
                     max_colors: int) -> QuantizerResult:
    """
    Quantizes colors using a weighted spherical k-means algorithm.
    
    Args:
        input_pixels: List of pixels in ARGB format.
        starting_clusters: Initial cluster centers in ARGB format.
        max_colors: Maximum number of colors to generate (1-256).
        
    Returns:
        A QuantizerResult with mappings of colors to counts and 
        input pixels to cluster pixels.
    """
```

## Celebi Module

### Functions
```python
def quantize_celebi(pixels: List[Argb], max_colors: int) -> QuantizerResult:
    """
    Quantizes colors using Wu's quantizer to generate initial clusters, then
    uses WSmeans to expand these clusters to the requested number of colors.
    
    Args:
        pixels: List of pixels in ARGB format.
        max_colors: The maximum number of colors to generate (1-256).
        
    Returns:
        A QuantizerResult with mappings of colors to counts and 
        input pixels to cluster pixels.
    """
```

# Implementation Details

## Algorithm Optimization Techniques

* **Wu's algorithm** uses a 3D histogram with statistical moments to efficiently find optimal clustering cuts
* **WSmeans** optimizes the search for nearest clusters using pre-computed distance matrices
* **Celebi** reduces iterations in WSmeans by providing high-quality initial clusters from Wu's algorithm

## Resource Requirements

* **Memory Usage**:
  * Wu's algorithm: O(32³) = approximately 32KB for the color histogram
  * WSmeans: O(n + c²) where n is the number of unique colors and c is the cluster count
  * Celebi: Combined memory of Wu and WSmeans components
  
* **Processing Time**:
  * For typical images (1000×1000 pixels), processing times are roughly:
    * Wu: 50-100ms
    * WSmeans: 200-500ms
    * Celebi: 250-600ms

## Constraints

* Maximum number of colors is capped at 256 for all algorithms
* Transparent pixels (non-opaque) are excluded from quantization in Celebi
* Algorithms operate on in-memory pixel arrays, so large images should be downsampled first
* The WSmeans algorithm has a hard limit of 100 iterations to prevent excessive computation
* All quantization is deterministic - the same input will always produce the same output

# Dependency Tree

```
PyMCUlib.utils.utils
├── Argb (type)
├── hex_from_argb()
├── argb_from_rgb()
├── is_opaque()
├── linearized()
├── delinearized()
└── WHITE_POINT_D65 (constant)

PyMCUlib.quantize.lab
├── Lab (class)
├── lab_from_int()
└── int_from_lab()

PyMCUlib.quantize.wsmeans
├── QuantizerResult (class)
└── quantize_wsmeans()

PyMCUlib.quantize.wu
└── quantize_wu()

PyMCUlib.quantize.celebi
└── quantize_celebi()
```

# Limitations

* Maximum number of colors is capped at 256
* Transparent pixels (non-opaque) are excluded from quantization in Celebi
* Algorithms operate on in-memory pixel arrays, so large images should be downsampled first
* The WSmeans algorithm has a maximum of 100 iterations to prevent excessive computation
* Colors very close together in RGB space might be merged even if they appear visually distinct
* No support for color spaces beyond RGB and Lab
* All quantizers assume sRGB color space with no support for other color profiles
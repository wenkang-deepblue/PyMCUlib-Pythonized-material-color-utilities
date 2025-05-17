# Quantize Module Documentation

## Overview

The Quantize module provides a collection of algorithms and tools for extracting representative colors from images. These algorithms cluster the pixels of an image into a limited number of representative colors while preserving the visual characteristics of the original image. This module is a core component of the Material Color Utilities library, providing the foundation for theme generation and palette creation.

## Key Features

- Multiple color quantization algorithm implementations (including Wu, WSMeans, and Celebi algorithms)
- Support for different color spaces through the PointProvider interface
- Efficient processing of large pixel datasets
- Configurable maximum color count
- Pixel frequency mapping (colors to pixel counts)

## Core Types and Classes

### Interfaces and Abstract Classes

```python
class PointProvider(ABC):
    """An interface to allow use of different color spaces by quantizers."""
    
    @abstractmethod
    def to_int(self, point: List[float]) -> int:
        """Converts a point in a color space to an ARGB integer."""
        pass

    @abstractmethod
    def from_int(self, argb: int) -> List[float]:
        """Converts an ARGB integer to a point in a color space."""
        pass

    @abstractmethod
    def distance(self, from_point: List[float], to_point: List[float]) -> float:
        """Calculates the distance between two points in a color space."""
        pass
```

### Implementation Classes

- **LabPointProvider**: Provides conversions and distance calculations in Lab color space
- **QuantizerMap**: A simple pixel frequency-based quantizer
- **QuantizerWu**: Implementation of Wu's color quantization algorithm
- **QuantizerWsmeans**: Implementation of Weighted Square Means quantization
- **QuantizerCelebi**: A combined approach using Wu and WSMeans for optimized quantization

## Main Function Categories

### Lab Color Space Operations

- `LabPointProvider.from_int(argb: int) -> List[float]`: Converts ARGB to a point in Lab color space.
- `LabPointProvider.to_int(point: List[float]) -> int`: Converts a Lab space point to ARGB.
- `LabPointProvider.distance(from_point: List[float], to_point: List[float]) -> float`: Returns **ΔE² (squared CIE 1976 distance)** for performance; relative ordering matches true ΔE.

### Basic Quantization Operations

- `QuantizerMap.quantize(pixels: List[int]) -> Dict[int, int]`: Counts pixels and automatically filters out transparent pixels (alpha < 255).

### Advanced Quantization Algorithms

- `QuantizerWu.quantize(pixels: List[int], max_colors: int) -> List[int]`: Also automatically filters transparent pixels.
- `QuantizerWsmeans.quantize(input_pixels: List[int], starting_clusters: List[int], max_colors: int) -> Dict[int, int]`: Clusters the given `input_pixels` but **does not** filter transparent pixels internally; you must filter them yourself before calling.
- `QuantizerCelebi.quantize(pixels: List[int], max_colors: int) -> Dict[int, int]`: Runs Wu followed by Wsmeans and likewise **does not** filter transparent pixels internally.

## Usage Examples

### Basic Quantization Example

```python
from PyMCUlib.quantize.quantizer_map import QuantizerMap

# Prepare pixel data (list of integers in ARGB format)
pixels = [0xFFFF0000, 0xFF00FF00, 0xFF0000FF]  # Red, Green, Blue pixels

# Quantize using QuantizerMap (get frequency count)
result = QuantizerMap.quantize(pixels)
print(result)  # Output: {4294901760: 1, 4278255360: 1, 4278190335: 1}
```

### Advanced Quantization with Celebi Algorithm

```python
from PyMCUlib.quantize.quantizer_celebi import QuantizerCelebi

# Prepare pixel data
pixels = [0xFFFF0000, 0xFFFF0000, 0xFF00FF00, 0xFF00FF00, 0xFF0000FF]  # 2 Red, 2 Green, 1 Blue

# Quantize to at most 3 colors using Celebi algorithm
result = QuantizerCelebi.quantize(pixels, 3)
print(result)  # Output: {4294901760: 2, 4278255360: 2, 4278190335: 1}

# Limit to at most 2 colors
result = QuantizerCelebi.quantize(pixels, 2)
# Output might contain only the two most prominent colors
```

### Advanced Quantization with Wu Algorithm

```python
from PyMCUlib.quantize.quantizer_wu import QuantizerWu

# Prepare pixel data (list of ARGB integers)
pixels = [0xFFFF0000, 0xFF00FF00, 0xFF0000FF]  # Red, Green, Blue

# Instantiate Wu quantizer
wu = QuantizerWu()

# Quantize to at most 3 colors
colors = wu.quantize(pixels, 3)

# 'colors' is a list of ARGB integers representing the 3 most representative colors
print([hex(c) for c in colors])  # Output: ['0xffff0000', '0xff00ff00', '0xff0000ff']
```

### Working with Lab Color Space

```python
from PyMCUlib.quantize.lab_point_provider import LabPointProvider

# Create Lab color space provider
lab_provider = LabPointProvider()

# Convert from ARGB to Lab
red_argb = 0xFFFF0000
red_lab = lab_provider.from_int(red_argb)  # e.g., [53.23, 80.11, 67.22]

# Convert from Lab to ARGB
new_argb = lab_provider.to_int(red_lab)  # Should be close to the original ARGB

# Calculate distance between two colors
blue_lab = lab_provider.from_int(0xFF0000FF)
distance = lab_provider.distance(red_lab, blue_lab)  # Get Lab distance between colors, returns ΔE² (squared distance)
```

### Complete Quantization Workflow

```python
from PIL import Image
from PyMCUlib.quantize.quantizer_celebi import QuantizerCelebi
from PyMCUlib.utils.color_utils import argb_from_rgb
import random

# Optional: set random seed for reproducible Wsmeans initialization
random.seed(42)

# 1. Load image and filter transparent pixels
img = Image.open("example.jpg").convert("RGBA")
pixels = [
    argb_from_rgb(r, g, b)
    for r, g, b, a in img.getdata()
    if a >= 255
]

# 2. Quantize to 8 colors using Celebi
result = QuantizerCelebi.quantize(pixels, 8)

# 3. Process the results
for color, count in result.items():
    print(f"Color: {hex(color)}, Pixel count: {count}")
```

## Algorithm Descriptions

### Wu Algorithm

Wu's algorithm is a top-down color quantizer that works by:
1. Building a 3D color histogram
2. Computing moments of boxes
3. Recursively splitting boxes to maximize variance between resulting boxes
4. Computing representative colors for each final box

### WSMeans Algorithm

Weighted Square Means is an optimized implementation of the K-means algorithm with:
1. Deduplication of identical pixels
2. Triangle inequality rule to reduce the number of color comparisons
3. Iterative optimization until convergence (no more cluster changes)
4. Consideration of pixel weights (frequencies)

### Celebi Algorithm

The Celebi algorithm combines the strengths of both Wu and WSMeans:
1. First uses Wu algorithm to get high-quality initial cluster centers
2. Then uses WSMeans to further refine the results
3. Provides both improved speed and quality

## Implementation Notes

- All colors use ARGB format (`0xAARRGGBB`).
- **Transparent pixel filtering**: Only `QuantizerMap` and `QuantizerWu` automatically skip pixels with alpha < 255; `QuantizerWsmeans` and `QuantizerCelebi` do not, so filter manually if needed.
- **Lab distance**: `LabPointProvider.distance` returns ΔE² (squared distance) to avoid expensive square roots.
- **Reproducibility**: `QuantizerWsmeans` uses random initialization when `starting_clusters` is empty; to guarantee reproducible results, set a random seed (e.g., `random.seed(42)`) before calling.
- All quantization algorithms may return fewer than the requested maximum number of colors
- QuantizerWu implementation uses 3D histograms and recursive splitting
- QuantizerWsmeans implementation includes optimized K-means iterations
- Pixel frequency mappings are implemented using Python dictionaries (Dict[int, int])

## Related Components

- **utils**: Provides color operations and conversions
- **score**: Scores quantization results to select the best representative colors
- **palettes**: Creates tonal palettes from quantization results
- **scheme**: Generates color schemes based on source colors
- **theme**: Applies color schemes to user interfaces

## Performance Considerations

- Wu algorithm is suitable for quick quantization needs
- WSMeans optimizes the standard K-means algorithm for better performance
- Celebi algorithm combines benefits of both, but at a higher computational cost
- For large images, consider downsampling before applying quantization algorithms

## Dependencies

- **typing**: For type annotations
- **abc**: For abstract base classes
- **random**: For random initialization in WSMeans
- **PyMCUlib.utils.color_utils**: For color conversions
- **math**: For mathematical operations
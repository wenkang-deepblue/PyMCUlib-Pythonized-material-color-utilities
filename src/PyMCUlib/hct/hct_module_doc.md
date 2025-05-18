# HCT Module Documentation

## Overview

The HCT (Hue, Chroma, Tone) component provides a perceptually accurate color system that links the color system, contrast, and accessibility. It uses CAM16 for hue and chroma, and L* from L*a*b* for tone. Unlike traditional color systems, HCT offers better perceptual uniformity and easier color manipulation.

Using L* creates a direct link between the color system and accessibility considerations. L* is linear to human perception, allowing for the creation of accurate color tones. A difference of 40 in HCT tone guarantees a contrast ratio >= 3.0, and a difference of 50 guarantees a contrast ratio >= 4.5.

## Key Features

- Perceptually accurate color representation
- Environment-adaptive color appearance
- Accessibility-focused color design
- Simple tone-based contrast measurement
- Color viewing condition adjustments
- Precise hue and chroma manipulation

## Core Classes

### ViewingConditions

Represents the environment where a color is observed. Colors appear differently under different lighting conditions, and ViewingConditions allows quantifying these differences.

```python
class ViewingConditions:
    """
    Caches intermediate values of the CAM16 conversion process that depend
    only on viewing conditions.
    """
    
    # Standard sRGB-like viewing conditions
    DEFAULT = None  # Initialized by make() method
    
    @classmethod
    def make(
        cls,
        white_point: Optional[List[float]] = None,
        adapting_luminance: float = (200.0 / math.pi) * color_utils.y_from_lstar(50.0) / 100.0,
        background_lstar: float = 50.0,
        surround: float = 2.0,
        discounting_illuminant: bool = False,
    ) -> "ViewingConditions":
        """Create ViewingConditions from physically relevant parameters"""
```
Attributes:
- `DEFAULT`: standard sRGB-like viewing conditions.
- `n`: relative luminance adaptation factor.
- `aw`: achromatic response to white.
- `nbb`, `ncb`: chromatic adaptation factors.
- `c`: surround factor.
- `nc`: chromatic induction factor.
- `rgb_d`: per-channel discount factors.
- `fl`: luminance adaptation factor.
- `fl_root`: fourth root of `fl`.
- `z`: lightness normalization factor.

### Cam16
CAM16 (Color Appearance Model 2016) represents colors not just by their hex codes, but by how they appear under specific viewing conditions.
```python
class Cam16:
    """
    CAM16 color appearance model. Includes coordinates in CAM16-UCS space
    (J*, a*, b*) for measuring color distances.
    """
    
    def __init__(
        self,
        hue: float,
        chroma: float,
        j: float,
        q: float,
        m: float,
        s: float,
        jstar: float,
        astar: float,
        bstar: float,
    ) -> None:
        """Constructor with all CAM16 dimensions"""
    
    @classmethod
    def from_int(cls, argb: int) -> "Cam16":
        """Create CAM16 from ARGB integer"""
    
    @classmethod
    def from_jch(cls, j: float, c: float, h: float) -> "Cam16":
        """Create CAM16 from lightness, chroma, and hue"""
        
    @classmethod
    def from_ucs(cls, jstar: float, astar: float, bstar: float) -> "Cam16":
        """Create CAM16 from CAM16-UCS coordinates"""
        
    def to_int(self) -> int:
        """Convert to ARGB integer"""
```
### HctSolver
Solves the HCT equation to find precise sRGB colors with desired hue, chroma, and tone.
```python
class HctSolver:
    """
    Solves the HCT equation to find colors with specific hue, chroma, and tone.
    """
    
    @classmethod
    def solve_to_int(cls, hue_degrees: float, chroma: float, lstar: float) -> int:
        """Find an sRGB color with given hue, chroma, and L*"""
    
    @classmethod
    def solve_to_cam(cls, hue_degrees: float, chroma: float, lstar: float) -> Cam16:
        """Find a CAM16 color with given hue, chroma, and L*"""
```
### Hct
The main class representing colors in the HCT system.
```python
class Hct:
    """
    HCT (hue, chroma, tone) color system.
    """
    
    @classmethod
    def from_hct(cls, hue: float, chroma: float, tone: float) -> "Hct":
        """Create HCT color from hue, chroma, and tone values"""
        
    @classmethod
    def from_int(cls, argb: int) -> "Hct":
        """Create HCT color from ARGB integer"""
        
    def to_int(self) -> int:
        """Convert to ARGB integer"""
        
    def in_viewing_conditions(self, vc: ViewingConditions) -> "Hct":
        """Translate color into different viewing conditions"""
```
## Main Function Categories
### Viewing Condition Creation
- `ViewingConditions.make()`: Creates ViewingConditions from physical parameters like white point, adapting luminance, etc.
- `ViewingConditions.DEFAULT`: Standard sRGB-like viewing conditions

### CAM16 Color Creation & Conversion

- `Cam16.from_int()`: Creates CAM16 color from ARGB integer
- `Cam16.from_jch()`: Creates CAM16 color from J (lightness), C (chroma), H (hue)
- `Cam16.from_ucs()`: Creates CAM16 color from CAM16-UCS coordinates
- `Cam16.from_xyz_in_viewing_conditions()`: Creates CAM16 color from XYZ coordinates in specific viewing conditions
- `Cam16.to_int()`: Converts CAM16 color to ARGB integer
- `Cam16.viewed()`: Displays CAM16 color in specific viewing conditions
- `Cam16.distance()`: Calculates distance between CAM16 colors in CAM16-UCS space

### HCT Color Creation & Manipulation

- `Hct.from_hct()`: Creates HCT color from hue, chroma, and tone values
- `Hct.from_int()`: Creates HCT color from ARGB integer
- `Hct.to_int()`: Converts HCT color to ARGB integer
- `Hct.in_viewing_conditions()`: Translates HCT color into different viewing conditions

### HCT Color Properties

- `Hct.hue`: Gets/sets hue (0-360 degrees)
- `Hct.chroma`: Gets/sets chroma (colorfulness)
- `Hct.tone`: Gets/sets tone (0-100, equivalent to L*)

### Color Solving

- `HctSolver.solve_to_int()`: Finds ARGB color with specific hue, chroma, and tone
- `HctSolver.solve_to_cam()`: Finds CAM16 color with specific hue, chroma, and tone

## Usage Examples
### Creating HCT Colors
```python
from PyMCUlib.hct import Hct

# Create HCT color from hue, chroma, and tone
blue = Hct.from_hct(270, 80, 50)  # Vibrant blue with tone 50

# Create HCT color from ARGB integer
color_from_argb = Hct.from_int(0xFF4285F4)  # Google blue

# Get HCT properties
h = color_from_argb.hue        # ~220 (blue hue)
c = color_from_argb.chroma     # ~70 (moderately saturated)
t = color_from_argb.tone       # ~67 (medium-bright)

# Convert back to ARGB
argb = color_from_argb.to_int()  # 0xFF4285F4
```
### Modifying HCT Colors
```python
from PyMCUlib.hct import Hct

# Create a color
color = Hct.from_hct(270, 80, 50)  # Vibrant blue

# Modify hue (shift toward purple)
color.hue = 290

# Reduce chroma (make less colorful)
color.chroma = 40

# Increase tone (make brighter)
color.tone = 70

# Get the new ARGB value after modifications
new_argb = color.to_int()
```
### Creating Color Palettes
```python
from PyMCUlib.hct import Hct

# Create a color palette based on a single color
base_color = Hct.from_int(0xFF4285F4)  # Google blue

# Create lighter and darker variants
tones = [10, 20, 30, 40, 50, 60, 70, 80, 90]
palette = []

for tone in tones:
    variant = Hct.from_hct(base_color.hue, base_color.chroma, tone)
    palette.append(variant.to_int())
    
# palette now contains 9 colors of the same hue and chroma but different tones
```
### Using Different Viewing Conditions
```python
import math
from PyMCUlib.utils import color_utils
from PyMCUlib.hct import Hct, ViewingConditions

# Create a color
color = Hct.from_hct(270, 80, 50)  # Vibrant blue

# Create custom viewing conditions (dim light)
dim_conditions = ViewingConditions.make(
    adapting_luminance=(50.0 / math.pi) * color_utils.y_from_lstar(50.0) / 100.0,
    background_lstar=30.0,
    surround=1.0
)

# See how the color appears in dim lighting
color_in_dim = color.in_viewing_conditions(dim_conditions)

# Get the apparent color values in dim lighting
h_dim = color_in_dim.hue
c_dim = color_in_dim.chroma
t_dim = color_in_dim.tone

# The apparent color will typically have lower chroma and appear darker
```
### Creating Accessible Color Combinations
```python
from PyMCUlib.hct import Hct

# Create a base color
base_color = Hct.from_hct(270, 80, 50)  # Vibrant blue at 50% tone

# For 3:1 contrast ratio, add/subtract at least 40 tone
text_light = Hct.from_hct(base_color.hue, base_color.chroma, base_color.tone + 40)
text_dark = Hct.from_hct(base_color.hue, base_color.chroma, base_color.tone - 40)

# For 4.5:1 contrast ratio, add/subtract at least 50 tone
accessible_light = Hct.from_hct(base_color.hue, base_color.chroma, min(base_color.tone + 50, 100))
accessible_dark = Hct.from_hct(base_color.hue, base_color.chroma, max(base_color.tone - 50, 0))

# Check which has higher contrast and use that
# (In this example, accessible_dark would have tone 0, which provides better contrast)
```
### Creating CAM16 Colors Directly
```python
from PyMCUlib.hct import Cam16, ViewingConditions

# Create a CAM16 color from JCH values
cam_from_jch = Cam16.from_jch(50, 60, 270)  # J=50, C=60, H=270

# Create a CAM16 color from ARGB
cam_from_argb = Cam16.from_int(0xFF4285F4)  # Google blue

# Create a CAM16 color with specific viewing conditions
vc = ViewingConditions.make(background_lstar=70.0)  # Lighter background
cam_with_vc = Cam16.from_int_in_viewing_conditions(0xFF4285F4, vc)

# Calculate distance between two colors (in CAM16-UCS space)
color1 = Cam16.from_int(0xFF4285F4)  # Google blue
color2 = Cam16.from_int(0xFF34A853)  # Google green
distance = color1.distance(color2)  # Perceptual distance between colors
```
### Using HctSolver Directly
```python
from PyMCUlib.hct import HctSolver

# Get an ARGB integer for a color with specific HCT values
argb = HctSolver.solve_to_int(270, 80, 50)  # Hue=270, Chroma=80, Tone=50

# Note: HctSolver might return a color with lower chroma if the requested
# chroma is impossible to achieve at the specified hue and tone
```
## Implementation Notes

- HCT is designed to provide perceptually accurate colors while maintaining accessibility.
- A difference of 40 in tone (~40% difference in L*) guarantees a contrast ratio of at least 3:1.
- A difference of 50 in tone (~50% difference in L*) guarantees a contrast ratio of at least 4.5:1.
- Hue is measured in degrees (0-360), with standard positions for primary colors (0=red, 120=green, 240=blue).
- Chroma represents colorfulness and has a dynamic maximum that depends on the hue and tone.
- The maximum achievable chroma varies by hue and tone - not all combinations are possible in sRGB.
- When setting chroma higher than achievable, HCT will provide the maximum achievable chroma.
- ViewingConditions can be customized to simulate different environments, affecting color appearance.
- All HCT objects are immutable and changes to properties generate new internal state.
- CAM16-UCS is used for measuring color distances, providing better perceptual uniformity.

## Dependencies
- `math`: For mathematical operations
- `PyMCUlib.utils.color_utils`: For color conversion utilities
- `PyMCUlib.utils.math_utils`: For mathematical utilities

## Related Components
- `utils`: Provides core color utility functions used by HCT
- `blend`: Color blending and harmony
- `palettes`: Tonal palette generation based on HCT
- `scheme`: Material Design color scheme generation
- `contrast`: Contrast calculation utilities
- `temperature`: Color temperature utilities
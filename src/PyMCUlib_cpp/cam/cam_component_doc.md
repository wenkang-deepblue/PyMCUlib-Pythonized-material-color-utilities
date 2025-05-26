
# <center> CAM Component Documentation </center>

## Overview

The CAM (Color Appearance Model) component implements the CAM16 color appearance model and the HCT (Hue, Chroma, Tone) color system. This component provides tools for color transformations and manipulations that are perceptually accurate and account for human color perception factors.

## Core Modules

The CAM component consists of several modules:

1. **cam.py**: Core implementation of the CAM16 color appearance model
2. **viewing_conditions.py**: Implementation of viewing conditions that affect color perception
3. **hct.py**: Implementation of the HCT color system
4. **hct_solver.py**: Algorithms for solving specific HCT values to RGB conversion

## Key Concepts

### CAM16 Color Appearance Model

CAM16 is a color appearance model that predicts how colors appear under various viewing conditions. It accurately models human color perception, accounting for:

- Chromatic adaptation (how colors appear under different lighting)
- Surrounding field effects
- Background effects
- Display conditions

### HCT Color System

HCT (Hue, Chroma, Tone) combines:
- Hue: the identity of a color (red, green, blue, etc.)
- Chroma: the colorfulness or saturation
- Tone: derived from L* in L*a*b*, provides a perceptually accurate measure of lightness

HCT provides several benefits over other color systems:
- Perceptually accurate across different viewing conditions
- Links color with accessibility and contrast
- Provides linear measure of lightness (unlike Y in XYZ)

## Main Classes and Functions

### Cam Class

```python
@dataclass
class Cam:
    """CAM16 color appearance model data class"""
    hue: float = 0.0        # Hue in degrees [0, 360)
    chroma: float = 0.0     # Colorfulness
    j: float = 0.0          # Lightness
    q: float = 0.0          # Brightness
    m: float = 0.0          # Colorfulness
    s: float = 0.0          # Saturation
    jstar: float = 0.0      # J* in CAM16-UCS
    astar: float = 0.0      # a* in CAM16-UCS
    bstar: float = 0.0      # b* in CAM16-UCS
```

### ViewingConditions Class

```python
@dataclass
class ViewingConditions:
    """Defines viewing conditions for the CAM16 color appearance model"""
    adapting_luminance: float = 0.0
    background_lstar: float = 0.0
    surround: float = 0.0
    discounting_illuminant: bool = False
    background_y_to_white_point_y: float = 0.0
    aw: float = 0.0
    nbb: float = 0.0
    ncb: float = 0.0
    c: float = 0.0
    n_c: float = 0.0
    fl: float = 0.0
    fl_root: float = 0.0
    z: float = 0.0
    white_point: List[float] = None
    rgb_d: List[float] = None
    
    def __post_init__(self):
        if self.white_point is None:
            self.white_point = [0.0, 0.0, 0.0]
        if self.rgb_d is None:
            self.rgb_d = [0.0, 0.0, 0.0]
```

### Hct Class

```python
@dataclass
class Hct:
    """
    HCT: hue, chroma, and tone.
    
    A color system built using CAM16 hue and chroma, and L* (lightness) from
    the L*a*b* color space, providing a perceptually accurate
    color measurement system that can also accurately render what colors
    will appear as in different lighting environments.
    """
    # Private attributes
    _hue: float = 0.0
    _chroma: float = 0.0
    _tone: float = 0.0
    _argb: int = 0
    
    @staticmethod
    def from_hct(hue: float, chroma: float, tone: float) -> 'Hct':
        """Creates an HCT color from hue, chroma, and tone."""
        pass
    
    @staticmethod
    def from_int(argb: int) -> 'Hct':
        """Creates an HCT color from an ARGB integer."""
        pass
    
    def get_hue(self) -> float:
        """Returns the hue of the color."""
        pass
    
    def get_chroma(self) -> float:
        """Returns the chroma of the color."""
        pass
    
    def get_tone(self) -> float:
        """Returns the tone of the color."""
        pass
    
    def to_int(self) -> int:
        """Returns the color in ARGB format."""
        pass
    
    def set_hue(self, hue: float) -> None:
        """Sets the hue of this color."""
        pass
    
    def set_chroma(self, chroma: float) -> None:
        """Sets the chroma of this color."""
        pass
    
    def set_tone(self, tone: float) -> None:
        """Sets the tone of this color."""
        pass
    
    def _set_internal_state(self, argb: int) -> None:
        """Sets the Hct object to represent an sRGB color."""
        pass
    
    def __eq__(self, other) -> bool:
        """Compares this Hct object with another for equality."""
        pass
    
    def __hash__(self) -> int:
        """Generates a hash value for this Hct object."""
        pass
```

### Key Functions

#### Color Format Conversion

```python
def cam_from_int(argb: Argb) -> Cam:
    """Converts ARGB to CAM16 using default viewing conditions."""

def int_from_cam(cam: Cam) -> Argb:
    """Converts CAM16 to ARGB using default viewing conditions."""

def cam_from_int_and_viewing_conditions(argb: Argb, viewing_conditions: ViewingConditions) -> Cam:
    """Converts ARGB to CAM16 with specified viewing conditions."""

def int_from_cam_and_viewing_conditions(cam: Cam, viewing_conditions: ViewingConditions) -> Argb:
    """Converts CAM16 to ARGB with specified viewing conditions."""

def cam_from_xyz_and_viewing_conditions(x: float, y: float, z: float,
                                       viewing_conditions: ViewingConditions) -> Cam:
    """Converts XYZ to CAM16 with specified viewing conditions."""

def cam_from_ucs_and_viewing_conditions(jstar: float, astar: float, bstar: float,
                                      viewing_conditions: ViewingConditions) -> Cam:
    """Creates a CAM16 object from UCS coordinates and viewing conditions."""

def cam_from_jch_and_viewing_conditions(j: float, c: float, h: float,
                                      viewing_conditions: ViewingConditions) -> Cam:
    """Creates a CAM16 object from J, C, h and viewing conditions."""

def int_from_hcl(hue: float, chroma: float, lstar: float) -> Argb:
    """Creates a color from HCL (hue, chroma, lightness)."""
```

#### Viewing Conditions

```python
WHITE_POINT_D65: List[float] = [95.047, 100.0, 108.883]

def create_viewing_conditions(
    white_point: List[float],
    adapting_luminance: float,
    background_lstar: float,
    surround: float,
    discounting_illuminant: bool
) -> ViewingConditions:
    """Creates ViewingConditions, which are parameters that inform colorimetric operations."""

def default_with_background_lstar(background_lstar: float) -> ViewingConditions:
    """Creates default viewing conditions with a custom background L*."""

DEFAULT_VIEWING_CONDITIONS: ViewingConditions
```

#### HCT Operations

```python
def solve_to_int(hue_degrees: float, chroma: float, lstar: float) -> Argb:
    """Finds an sRGB color with the given hue, chroma, and L*, if possible."""

def solve_to_cam(hue_degrees: float, chroma: float, lstar: float) -> Cam:
    """Similar to solve_to_int, but returns a CAM object."""

def cam_distance(a: Cam, b: Cam) -> float:
    """Calculates the distance between two CAM16 objects."""
```

## Usage Examples

### Converting Between Color Spaces

```python
from PyMCUlib_cpp.cam.cam import cam_from_int, int_from_cam
from PyMCUlib_cpp.utils.utils import Argb

# Convert RGB to CAM16
rgb_color: Argb = 0xff4285f4  # Google Blue
cam_color = cam_from_int(rgb_color)

# Access CAM16 properties
hue = cam_color.hue
chroma = cam_color.chroma
j = cam_color.j

# Convert back to RGB
rgb_again = int_from_cam(cam_color)
```

### Working with HCT Colors

```python
from PyMCUlib_cpp.cam.hct import Hct

# Create HCT from RGB
color = Hct.from_int(0xff4285f4)  # Google Blue

# Get HCT components
hue = color.get_hue()
chroma = color.get_chroma()
tone = color.get_tone()

# Modify color while preserving other components
color.set_hue(hue + 15.0)  # Shift hue
color.set_chroma(chroma * 0.8)  # Reduce chroma
color.set_tone(70.0)  # Set specific tone

# Convert to RGB
rgb = color.to_int()
```

### Using Custom Viewing Conditions

```python
from PyMCUlib_cpp.cam.viewing_conditions import create_viewing_conditions, WHITE_POINT_D65
from PyMCUlib_cpp.cam.cam import cam_from_int_and_viewing_conditions

# Create custom viewing conditions
custom_conditions = create_viewing_conditions(
    white_point=WHITE_POINT_D65, 
    adapting_luminance=200.0,
    background_lstar=50.0,
    surround=2.0,
    discounting_illuminant=False
)

# Convert RGB to CAM16 under custom conditions
rgb_color = 0xff4285f4  # Google Blue
cam_color = cam_from_int_and_viewing_conditions(rgb_color, custom_conditions)
```

### Color Distance Calculation

```python
from PyMCUlib_cpp.cam.cam import cam_from_int, cam_distance

color1 = cam_from_int(0xff4285f4)  # Google Blue
color2 = cam_from_int(0xff34a853)  # Google Green

distance = cam_distance(color1, color2)
print(f"Perceptual distance: {distance}")
```

### Importing Multiple Components

```python
# Import all from cam module
from PyMCUlib_cpp.cam import (
    Cam, cam_from_int, int_from_cam, cam_distance,
    ViewingConditions, DEFAULT_VIEWING_CONDITIONS,
    Hct, create_viewing_conditions, solve_to_int
)

# Now you can use these components directly
color = Hct.from_int(0xff4285f4)
cam_obj = cam_from_int(0xff4285f4)
```

## Notes on Implementation

- The CAM16 model is based on the CIECAM02 model with improvements
- All angle measurements are in degrees [0, 360)
- The implementation accounts for different illuminants and viewing conditions
- The HCT solver finds the closest sRGB color to a given HCT specification
- Type `Argb` is an integer representation of a color in ARGB format
- `solve_to_int` will maximize chroma if the requested HCT color is outside the sRGB gamut
- The color distance calculation follows the CAM16-UCS formula

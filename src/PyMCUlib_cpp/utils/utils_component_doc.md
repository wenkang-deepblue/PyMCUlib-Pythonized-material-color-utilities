# <center> Utils Component Documentation </center>

## Overview

The Utils component provides foundational utilities and functions for color handling, mathematical operations, and various conversions between color spaces. It serves as the base infrastructure for the other components in the Material Color Utilities library.

## Key Features

- Color representation and format conversions
- Mathematical utilities for color manipulation
- Color space transformations (RGB, linear RGB, XYZ, L*a*b*)
- Angle handling utilities

## Core Types and Constants

### Types

```python
Argb = int  # Representing ARGB color values as a 32-bit integer

class Vec3(NamedTuple):
    """A vector with three floating-point numbers as components."""
    a: float = 0.0
    b: float = 0.0
    c: float = 0.0
```

### Constants

```python
PI = 3.141592653589793  # Value of pi

# Standard white point; white on a sunny day
# Used in color space transformations (XYZ color space)
WHITE_POINT_D65 = [95.047, 100.0, 108.883]
```

## Main Function Categories

### ARGB Color Handling

- `argb_from_rgb(red: int, green: int, blue: int) -> Argb`: Creates ARGB from RGB components
- `red_from_int(argb: Argb) -> int`: Extracts red component (0-255)
- `green_from_int(argb: Argb) -> int`: Extracts green component (0-255)
- `blue_from_int(argb: Argb) -> int`: Extracts blue component (0-255)
- `alpha_from_int(argb: Argb) -> int`: Extracts alpha component (0-255)
- `is_opaque(argb: Argb) -> bool`: Checks if color is fully opaque
- `hex_from_argb(argb: Argb) -> str`: Converts ARGB to hex string in lowercase
- `argb_from_hex(hex_color: str) -> Argb`: Converts hex string to ARGB format

### RGB/Linear RGB Conversion

- `linearized(rgb_component: int) -> float`: Converts standard RGB (0-255) to linear RGB (0-100)
- `delinearized(rgb_component: float) -> int`: Converts linear RGB (0-100) to standard RGB (0-255)
- `argb_from_linrgb(linrgb: Vec3) -> Argb`: Converts linear RGB to ARGB

### Angle Utilities

- `sanitize_degrees_int(degrees: int) -> int`: Normalizes integer angles to [0, 360)
- `sanitize_degrees_double(degrees: float) -> float`: Normalizes floating point angles to [0.0, 360.0)
- `diff_degrees(a: float, b: float) -> float`: Calculates the shortest angle between two angles
- `rotation_direction(from_angle: float, to_angle: float) -> float`: Determines shortest rotation direction (-1.0 or 1.0)

### Color Space Conversions

- `lstar_from_argb(argb: Argb) -> float`: Calculates L* from ARGB
- `y_from_lstar(lstar: float) -> float`: Converts L* to Y (L* range: 0.0-100.0, Y range: 0.0-100.0)
- `lstar_from_y(y: float) -> float`: Converts Y to L* (Y range: 0.0-100.0, L* range: 0.0-100.0)
- `int_from_lstar(lstar: float) -> Argb`: Creates grayscale ARGB from L* (L* range: 0.0-100.0)

### Mathematical Utilities

- `signum(num: float) -> int`: Returns sign of a number (-1, 0, or 1)
- `lerp(start: float, stop: float, amount: float) -> float`: Linear interpolation
- `matrix_multiply(input_vec: Vec3, matrix: list) -> Vec3`: Multiplies Vec3 by 3x3 matrix

## Usage Examples

### Basic Color Creation and Manipulation

```python
from PyMCUlib_cpp.utils import argb_from_rgb, red_from_int, green_from_int, blue_from_int, hex_from_argb, argb_from_hex

# Create a color from RGB components
blue = argb_from_rgb(66, 133, 244)  # Google Blue

# Extract components
r = red_from_int(blue)  # 66
g = green_from_int(blue)  # 133
b = blue_from_int(blue)  # 244

# Convert to hex string
hex_color = hex_from_argb(blue)  # "ff4285f4"

# Convert from hex string to ARGB
from_hex = argb_from_hex("#4285f4")  # 0xff4285f4
from_hex_short = argb_from_hex("#48f")  # 0xff4488ff
from_hex_with_alpha = argb_from_hex("#80123456")  # 0x80123456

# Check if a color is fully opaque
from PyMCUlib_cpp.utils import is_opaque
is_fully_opaque = is_opaque(blue)  # True (alpha is 0xFF)

# Create a color with partial transparency
semi_transparent_blue = 0x80123456  # Alpha = 0x80 (128)
is_semi_transparent_opaque = is_opaque(semi_transparent_blue)  # False
```

### Color Space Conversions

```python
from PyMCUlib_cpp.utils import lstar_from_argb, y_from_lstar, lstar_from_y, int_from_lstar

# Get L* value of a color (perceptual lightness)
blue = 0xff4285f4
lstar = lstar_from_argb(blue)  # L* value between 0.0 and 100.0

# Convert between L* and Y (relative luminance)
y = y_from_lstar(lstar)  # L* range: 0.0-100.0, Y range: 0.0-100.0
lstar_again = lstar_from_y(y)  # Y range: 0.0-100.0, L* range: 0.0-100.0

# Create grayscale from L*
dark_gray = int_from_lstar(20.0)    # Dark gray (20% L*)
middle_gray = int_from_lstar(50.0)  # Middle gray (50% L*)
light_gray = int_from_lstar(80.0)   # Light gray (80% L*)
```

### Working with Linear RGB

```python
from PyMCUlib_cpp.utils import Vec3, linearized, delinearized, argb_from_linrgb

# Convert RGB components to linear RGB
r_linear = linearized(255)  # 100.0
g_linear = linearized(128)  # ~22.2
b_linear = linearized(64)   # ~4.8

# Create linear RGB vector
linrgb = Vec3(r_linear, g_linear, b_linear)

# Convert back to RGB
argb = argb_from_linrgb(linrgb)  # 0xFFFF804 (approximately)

# Converting both ways
red_component = 200
red_linear = linearized(red_component)       # Convert to linear space
red_standard = delinearized(red_linear)      # Convert back to standard RGB
# red_standard should be close to 200 (may have small rounding differences)
```

### Mathematical Operations

```python
from PyMCUlib_cpp.utils import Vec3, matrix_multiply, lerp, signum

# Signum function examples
neg_sign = signum(-15.5)    # -1
zero_sign = signum(0.0)     #  0
pos_sign = signum(42.7)     #  1

# Linear interpolation examples
start = 0.0
end = 100.0
quarter = lerp(start, end, 0.25)  # 25.0
half = lerp(start, end, 0.5)      # 50.0
three_quarters = lerp(start, end, 0.75)  # 75.0

# Matrix multiplication example
# Example 3x3 matrix (must be this exact format)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Multiply vector by 3x3 matrix
vector = Vec3(10, 20, 30)
result = matrix_multiply(vector, matrix)  # Returns a new Vec3
# result: Vec3(a=140.0, b=320.0, c=500.0)
```

### Angle Handling

```python
from PyMCUlib_cpp.utils import sanitize_degrees_double, sanitize_degrees_int, diff_degrees, rotation_direction

# Normalize angles
angle1 = sanitize_degrees_int(-30)     # 330
angle2 = sanitize_degrees_int(370)     # 10
angle3 = sanitize_degrees_double(-30.0)  # 330.0
angle4 = sanitize_degrees_double(370.0)  # 10.0

# Calculate shortest angle distance
distance1 = diff_degrees(10.0, 350.0)  # 20.0
distance2 = diff_degrees(350.0, 10.0)  # 20.0 (same result, order doesn't matter)
distance3 = diff_degrees(90.0, 270.0)  # 180.0

# Determine rotation direction
dir1 = rotation_direction(10.0, 350.0)   # -1.0 (clockwise is shorter)
dir2 = rotation_direction(350.0, 10.0)   #  1.0 (counter-clockwise is shorter)
dir3 = rotation_direction(0.0, 180.0)    #  1.0 (either direction works, defaults to 1.0)
```

## Implementation Notes

- All colors use ARGB format (int value of the form 0xAARRGGBB)
- Linear RGB uses values in range [0.0, 100.0]
- Standard RGB uses values in range [0, 255]
- Angles are handled in degrees, normalized to range [0, 360)
- L* values range from 0.0 (black) to 100.0 (white)
- Y (luminance) values range from 0.0 to 100.0
- The `matrix` parameter in `matrix_multiply` must be a 3x3 matrix represented as a list of 3 lists, each containing 3 elements
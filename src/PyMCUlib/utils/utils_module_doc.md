# Utils Module Documentation
## Overview
The Utils module provides foundational utilities and functions for color handling, mathematical operations, string parsing, image processing, and theme creation/application. It serves as the base infrastructure for other components in the Material Color Utilities (MCU) library.

## Key Features
- Color representation and format conversions
- Mathematical utilities for color manipulation
- Color space transformations (RGB, linear RGB, XYZ, Lab*)
- Angle handling utilities
- Hex color string conversions
- Color extraction from images
- Theme generation and application utilities

## Core Types and Constants
### Constants
```python
# Standard white point; white on a sunny day
WHITE_POINT_D65 = [95.047, 100.0, 108.883]

# Transformation matrices for color space conversions
SRGB_TO_XYZ = [
    [0.41233895, 0.35762064, 0.18051042],
    [0.2126, 0.7152, 0.0722],
    [0.01932141, 0.11916382, 0.95034478],
]

XYZ_TO_SRGB = [
    [3.2413774792388685, -1.5376652402851851, -0.49885366846268053],
    [-0.9691452513005321, 1.8758853451067872, 0.04156585616912061],
    [0.05562093689691305, -0.20395524564742123, 1.0571799111220335],
]
```
## Main Components
### 1. Math Utilities (`math_utils.py`)
Mathematical operations used throughout the library.

#### Key Functions:
- `signum(num: float) -> int`: Returns 1 if num > 0, -1 if num < 0, and 0 if num = 0
- `lerp(start: float, stop: float, amount: float) -> float`: Linear interpolation
- `clamp_int(min_val: int, max_val: int, input_val: int) -> int`: Clamps integer between min and max
- `clamp_double(min_val: float, max_val: float, input_val: float) -> float`: Clamps float between min and max
- `sanitize_degrees_int(degrees: int) -> int`: Normalizes integer angles to [0, 360)
- `sanitize_degrees_double(degrees: float) -> float`: Normalizes float angles to [0.0, 360.0)
- `rotation_direction(from_val: float, to_val: float) -> float`: Determines shortest rotation direction
- `difference_degrees(a: float, b: float) -> float`: Calculates shortest angular distance
- `matrix_multiply(row: List[float], matrix: List[List[float]]) -> List[float]`: Multiplies 1x3 row vector with 3x3 matrix

### 2. Color Utilities (`color_utils.py`)
Core functions for color representation, conversion, and manipulation.
#### Key Functions:
- `argb_from_rgb(red: int, green: int, blue: int) -> int`: Creates ARGB from RGB components
- `argb_from_linrgb(linrgb: List[float]) -> int`: Converts linear RGB to ARGB
- `alpha_from_argb(argb: int) -> int`: Extracts alpha component
- `red_from_argb(argb: int) -> int`: Extracts red component
- `green_from_argb(argb: int) -> int`: Extracts green component
- `blue_from_argb(argb: int) -> int`: Extracts blue component
- `is_opaque(argb: int) -> bool`: Checks if color is fully opaque
- `argb_from_xyz(x: float, y: float, z: float) -> int`: Converts XYZ to ARGB
- `xyz_from_argb(argb: int) -> List[float]`: Converts ARGB to XYZ
- `argb_from_lab(l: float, a: float, b_val: float) -> int`: Converts Lab to ARGB
- `lab_from_argb(argb: int) -> List[float]`: Converts ARGB to Lab
- `argb_from_lstar(lstar: float) -> int`: Creates grayscale ARGB from L*
- `lstar_from_argb(argb: int) -> float`: Calculates L* from ARGB
- `y_from_lstar(lstar: float) -> float`: Converts L* to Y
- `lstar_from_y(y: float) -> float`: Converts Y to L*
- `linearized(rgb_component: int) -> float`: Converts RGB to linear RGB
- `delinearized(rgb_component: float) -> int`: Converts linear RGB to RGB
- `white_point_d65() -> List[float]`: Returns standard white point D65

### 3. String Utilities (`string_utils.py`)
Functions for converting between hex strings and ARGB colors.
#### Key Functions:
- `hex_from_argb(argb: int) -> str`: Converts ARGB to hex string (e.g., "#ff4285f4")
- `argb_from_hex(hex_str: str) -> int`: Converts hex string to ARGB

### 4. Image Utilities (`image_utils.py`)
Functions for extracting source colors from images.
#### Key Functions:
- `source_color_from_image(image_data: Union[str, bytes, Image.Image], area: Optional[Tuple[int, int, int, int]] = None) -> int`: Gets source color from image
source_color_from_image_bytes(image_bytes: np.ndarray) -> int: Gets source color from image bytes
- `source_color_from_file(file_path: str, area: Optional[Tuple[int, int, int, int]] = None) -> int`: Gets source color from image file

### 5. Theme Utilities (`theme_utils.py`)
Functions for creating and applying color themes.
#### Key Classes:
- `CustomColor`: TypedDict for custom colors in themes
- `ColorGroup`: TypedDict for color groups
- `CustomColorGroup`: TypedDict for custom color groups
- `Theme`: TypedDict for complete themes
- `ApplyThemeOptions`: TypeDict for apply themes

#### Key Functions:
- `theme_from_source_color(source: int, custom_colors: List[CustomColor] = None) -> Theme`: Creates theme from source color
- `theme_from_image(image: Union[str, bytes, Image.Image], custom_colors: Optional[List[CustomColor]] = None) -> Theme`: Creates theme from image
- `custom_color(source: int, color: CustomColor) -> CustomColorGroup`: Generates custom color group
- `apply_theme(theme: Theme, options: Optional[ApplyThemeOptions] = None) -> Dict[str, str]`: Applies theme to target (returns CSS variables)

## Usage Examples
### Mathematical Operations
```python
from material_color_utilities.utils.math_utils import lerp, signum, rotation_direction, difference_degrees

# Sign of a number
sign1 = signum(-5)  # -1
sign2 = signum(0)   # 0
sign3 = signum(42)  # 1

# Linear interpolation
value = lerp(0, 100, 0.25)  # 25.0

# Angle operations
angle_diff = difference_degrees(10, 350)       # 20.0
direction = rotation_direction(10, 350)        # -1.0 (clockwise is shorter)
direction2 = rotation_direction(350, 10)       # 1.0 (counter-clockwise is shorter)
```
### Color Handling
```python
from material_color_utilities.utils.color_utils import (
    argb_from_rgb, red_from_argb, green_from_argb, blue_from_argb,
    lstar_from_argb, argb_from_lstar
)

# Create a color from RGB components
blue = argb_from_rgb(66, 133, 244)  # Google Blue (0xFF4285F4)

# Extract components
r = red_from_argb(blue)    # 66
g = green_from_argb(blue)  # 133
b = blue_from_argb(blue)   # 244

# Get L* value (perceptual lightness)
lstar = lstar_from_argb(blue)  # ~54.3

# Create grayscale from L*
dark_gray = argb_from_lstar(20.0)    # Dark gray
middle_gray = argb_from_lstar(50.0)  # Middle gray
light_gray = argb_from_lstar(80.0)   # Light gray
```
### String Conversions
```python
from material_color_utilities.utils.string_utils import hex_from_argb, argb_from_hex

# ARGB to hex string
blue = 0xFF4285F4
hex_string = hex_from_argb(blue)  # "#4285f4"

# Hex string to ARGB
from_hex = argb_from_hex("#4285f4")       # 0xFF4285F4
from_hex_short = argb_from_hex("#48f")     # 0xFF4488FF
from_hex_no_hash = argb_from_hex("4285f4") # 0xFF4285F4
```
### Image Color Extraction
```python
from material_color_utilities.utils.image_utils import source_color_from_file
from PIL import Image

# Extract source color from image file
source_color = source_color_from_file("image.jpg")

# Extract with crop area (left, top, width, height)
source_color_cropped = source_color_from_file("image.jpg", area=(100, 100, 200, 200))

# Using PIL Image
image = Image.open("image.jpg")
from material_color_utilities.utils.image_utils import source_color_from_image
source_color_from_pil = source_color_from_image(image)
```
### Creating and Applying Themes
```python
from material_color_utilities.utils.theme_utils import (
    theme_from_source_color, theme_from_image, apply_theme
)
from material_color_utilities.utils.string_utils import argb_from_hex

# Create theme from a source color
blue = argb_from_hex("#4285F4")
theme = theme_from_source_color(blue)

# Create theme with custom colors
custom_colors = [
    {
        "name": "custom-1",
        "value": argb_from_hex("#FF0000"),
        "blend": True,
    }
]
theme_with_custom = theme_from_source_color(blue, custom_colors)

# Create theme from an image
theme_from_img = theme_from_image("image.jpg")

# Apply theme (returns CSS variables)
css_vars = apply_theme(theme, {"dark": True, "paletteTones": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
```
## Implementation Notes
- All colors use ARGB format (int value of the form 0xAARRGGBB)
- Linear RGB uses values in range [0.0, 100.0]
- Standard RGB uses values in range [0, 255]
- Angles are handled in degrees, normalized to range [0, 360)
- L* values range from 0.0 (black) to 100.0 (white)
- Y (luminance) values range from 0.0 to 100.0
- Image processing supports file paths, bytes, and PIL Image objects
- Theme application returns CSS variables (platform-specific implementation may vary)
- The library enforces strict typing with type hints throughout
- Internal helper functions are prefixed with underscore (_function_name)
- Implementation follows Python conventions while preserving the algorithm and function equivalence with the TypeScript version

## Dependencies
- `typing`: For type annotations
- `math`: For mathematical operations
- `numpy`: For image data handling
- `PIL` (Pillow): For image processing
- `re`: For regular expression operations (in theme_utils)

## Related Components
- `blend`: For color harmonization and blending
- `quantize`: For color quantization (used in image processing)
- `score`: For scoring and ranking quantized colors
- `palettes`: For creating tonal palettes from source colors
- `scheme`: For generating color schemes based on source colors
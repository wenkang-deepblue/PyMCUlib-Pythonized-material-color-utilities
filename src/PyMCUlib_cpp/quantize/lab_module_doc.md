# <center> Lab Module Documentation </center>

## Overview

The Lab module provides functionality for converting between ARGB color format and the CIE Lab color space. The Lab color space is a perceptually uniform color space that is useful for color processing, comparison, and analysis.

## Classes and Functions

### `Lab` Class

Represents a color in the CIE Lab color space. Implemented as a `NamedTuple` with fixed fields.

#### Attributes

- `l` (float): Lightness component, typically ranging from 0 (black) to 100 (white)
- `a` (float): Green (-) to red (+) component
- `b` (float): Blue (-) to yellow (+) component

#### Methods

##### `delta_e(lab: Lab) -> float`

Calculates the squared distance between two Lab colors.

**Parameters**:
- `lab` (Lab): Another Lab color

**Returns**:
- `float`: The squared distance between the two colors

**Example**:
```python
lab1 = Lab(50.0, 20.0, 30.0)
lab2 = Lab(55.0, 25.0, 35.0)
distance = lab1.delta_e(lab2)  # Returns 75.0
```

##### `__str__() -> str`

Returns a string representation of the Lab color.

**Returns**:
- `str`: String representation of the Lab color

**Example**:
```python
lab = Lab(50.0, 20.0, 30.0)
print(lab)  # Outputs: "Lab: L* 50.0 a* 20.0 b* 30.0"
```

### `int_from_lab(lab: Lab) -> Argb`

Converts a Lab color to ARGB integer format.

**Parameters**:
- `lab` (Lab): Color in the Lab color space

**Returns**:
- `Argb`: Color in ARGB format (32-bit integer)

**Example**:
```python
lab = Lab(50.0, 20.0, 30.0)
argb = int_from_lab(lab)
```

### `lab_from_int(argb: Argb) -> Lab`

Converts a color in ARGB integer format to a Lab color.

**Parameters**:
- `argb` (Argb): Color in ARGB format (32-bit integer)

**Returns**:
- `Lab`: Color in the Lab color space

**Example**:
```python
argb = 0xFF5544FF  # Some shade of purple
lab = lab_from_int(argb)
```

## Constants

### `WHITE_POINT_D65`

Standard D65 white point used in color space conversions, imported from `PyMCUlib_cpp.utils.utils`.

## Dependencies

The module depends on the following imports:
- `NamedTuple` from `typing`
- `Argb`, `WHITE_POINT_D65`, `delinearized`, `linearized`, `argb_from_rgb` from `PyMCUlib_cpp.utils.utils`

## Use Cases

The Lab color space is particularly useful in the following scenarios:

1. **Color Contrast Calculations**: Lab space is a perceptually uniform color space, making it useful for calculating human-perceivable color differences.

2. **Color Clustering and Quantization**: When converting an image to a limited set of colors, operating in Lab space can yield perceptually more accurate results.

3. **Gradients and Color Interpolation**: Color interpolation in Lab space can produce more natural and smooth gradient effects.

4. **Color Correction and Matching**: In printing, photography, and design, Lab space is commonly used for color correction and matching.

## Examples

```python
from PyMCUlib_cpp.quantize.lab import Lab, int_from_lab, lab_from_int

# Convert from ARGB to Lab
argb = 0xFF0000FF  # Blue
lab_blue = lab_from_int(argb)
print(lab_blue)  # Output Lab values

# Convert from Lab to ARGB
lab_red = Lab(53.2, 80.1, 67.2)  # Approximately red
argb_red = int_from_lab(lab_red)
print(hex(argb_red))  # Output ARGB value in hex

# Calculate distance between two colors
lab1 = Lab(50.0, 20.0, 30.0)
lab2 = Lab(55.0, 25.0, 35.0)
distance = lab1.delta_e(lab2)
print(f"Color distance: {distance}")
```

## Notes

- The L component of the Lab color space typically ranges from 0 to 100, while the a and b components typically range from -128 to 127, though they may extend beyond these ranges in practice.
- Slight precision loss may occur during the conversion process, especially in round-trip conversions.
- In some edge cases, colors may be clamped to the sRGB gamut, causing saturated colors to become less saturated after conversion.
- The `Argb` type is a type alias for an integer, defined in the `PyMCUlib_cpp.utils.utils` module.
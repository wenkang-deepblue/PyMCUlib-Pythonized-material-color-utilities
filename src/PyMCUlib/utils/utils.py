# utils.py

import math
from typing import NamedTuple

# Define types and constants
Argb = int  # Use int to represent uint32_t of C++

class Vec3(NamedTuple):
    """
    A vector with three floating-point numbers as components.
    """
    a: float = 0.0
    b: float = 0.0
    c: float = 0.0

# Constants
PI = 3.141592653589793

# Standard white point; white on a sunny day
WHITE_POINT_D65 = [95.047, 100.0, 108.883]

def red_from_int(argb: Argb) -> int:
    """
    Returns the red component of a color in ARGB format.
    """
    return (argb & 0x00ff0000) >> 16

def green_from_int(argb: Argb) -> int:
    """
    Returns the green component of a color in ARGB format.
    """
    return (argb & 0x0000ff00) >> 8

def blue_from_int(argb: Argb) -> int:
    """
    Returns the blue component of a color in ARGB format.
    """
    return (argb & 0x000000ff)

def alpha_from_int(argb: Argb) -> int:
    """
    Returns the alpha component of a color in ARGB format.
    """
    return (argb & 0xff000000) >> 24

def is_opaque(argb: Argb) -> bool:
    """
    Returns whether a color in ARGB format is opaque.
    """
    return alpha_from_int(argb) == 255

def argb_from_rgb(red: int, green: int, blue: int) -> Argb:
    """
    Converts a color from RGB components to ARGB format.
    """
    return 0xFF000000 | ((red & 0xff) << 16) | ((green & 0xff) << 8) | (blue & 0xff)

def argb_from_linrgb(linrgb: Vec3) -> Argb:
    """
    Converts a color from linear RGB components to ARGB format.
    """
    r = delinearized(linrgb.a)
    g = delinearized(linrgb.b)
    b = delinearized(linrgb.c)
    return 0xFF000000 | ((r & 0xff) << 16) | ((g & 0xff) << 8) | (b & 0xff)

def delinearized(rgb_component: float) -> int:
    """
    Converts a linear RGB component to standard RGB component.
    """
    normalized = rgb_component / 100.0
    if normalized <= 0.0031308:
        delinearized_value = normalized * 12.92
    else:
        delinearized_value = 1.055 * pow(normalized, 1.0 / 2.4) - 0.055
    return max(0, min(255, round(delinearized_value * 255.0)))

def linearized(rgb_component: int) -> float:
    """
    Converts a standard RGB component to linear RGB component.
    """
    normalized = rgb_component / 255.0
    if normalized <= 0.040449936:
        return (normalized / 12.92) * 100.0
    else:
        return pow((normalized + 0.055) / 1.055, 2.4) * 100.0

def lstar_from_argb(argb: Argb) -> float:
    """
    Calculate the L* value of a color in ARGB format.
    """
    red = (argb & 0x00ff0000) >> 16
    green = (argb & 0x0000ff00) >> 8
    blue = (argb & 0x000000ff)
    red_l = linearized(red)
    green_l = linearized(green)
    blue_l = linearized(blue)
    y = 0.2126 * red_l + 0.7152 * green_l + 0.0722 * blue_l
    return lstar_from_y(y)

def y_from_lstar(lstar: float) -> float:
    """
    Converts an L* value to a Y value.

    L* in L*a*b* and Y in XYZ measure the same quantity, luminance.
    L* measures perceptual luminance, a linear scale. Y in XYZ measures relative luminance, a logarithmic scale.

    Args:
        lstar: L* in L*a*b*. 0.0 <= L* <= 100.0

    Returns:
        Y in XYZ. 0.0 <= Y <= 100.0
    """
    ke = 8.0
    if lstar > ke:
        cube_root = (lstar + 16.0) / 116.0
        cube = cube_root * cube_root * cube_root
        return cube * 100.0
    else:
        return lstar / (24389.0 / 27.0) * 100.0

def lstar_from_y(y: float) -> float:
    """
    Converts a Y value to an L* value.

    L* in L*a*b* and Y in XYZ measure the same quantity, luminance.
    L* measures perceptual luminance, a linear scale. Y in XYZ measures relative luminance, a logarithmic scale.

    Args:
        y: Y in XYZ. 0.0 <= Y <= 100.0

    Returns:
        L* in L*a*b*. 0.0 <= L* <= 100.0
    """
    e = 216.0 / 24389.0
    y_normalized = y / 100.0
    if y_normalized <= e:
        return (24389.0 / 27.0) * y_normalized
    else:
        return 116.0 * pow(y_normalized, 1.0 / 3.0) - 16.0
    
def sanitize_degrees_int(degrees: int) -> int:
    """
    Sanitizes a degree measure as an integer.

    Returns a degree measure between 0 (inclusive) and 360 (exclusive).
    """
    return ((degrees % 360) + 360) % 360

def sanitize_degrees_double(degrees: float) -> float:
    """
    Sanitizes a degree measure as a floating-point number.

    Returns a degree measure between 0.0 (inclusive) and 360.0 (exclusive).
    """
    if degrees < 0.0:
        return math.fmod(degrees, 360.0) + 360.0
    elif degrees >= 360.0:
        return math.fmod(degrees, 360.0)
    else:
        return degrees

def diff_degrees(a: float, b: float) -> float:
    """
    Distance of two points on a circle, represented using degrees.
    """
    return 180.0 - abs(abs(a - b) - 180.0)

def rotation_direction(from_angle: float, to_angle: float) -> float:
    """
    Sign of direction change needed to travel from one angle to another.

    For angles that are 180 degrees apart from each other, both
    directions have the same travel distance, so either direction is
    shortest. The value 1.0 is returned in this case.

    Args:
        from_angle: The angle travel starts from, in degrees.
        to_angle: The angle travel ends at, in degrees.

    Returns:
        -1 if decreasing from leads to the shortest travel
        distance, 1 if increasing from leads to the shortest travel
        distance.
    """
    increasing_difference = sanitize_degrees_double(to_angle - from_angle)
    return 1.0 if increasing_difference <= 180.0 else -1.0

def hex_from_argb(argb: Argb) -> str:
    """
    Converts a color in ARGB format to a hexadecimal string in lowercase.

    For instance: hex_from_argb(0xff012345) == "ff012345"
    """
    return format(argb, '08x')

def argb_from_hex(hex_color: str) -> Argb:
    """
    Converts a hexadecimal color string to an ARGB integer representation.
    
    Args:
        hex_color: Hexadecimal color string (like "#RGB", "#RRGGBB", "#AARRGGBB")
                   Can include or omit the leading # symbol
    
    Returns:
        Integer representation in ARGB format
        
    Raises:
        ValueError: If the input hex string format is incorrect
    """
    # Remove # prefix
    hex_color = hex_color.replace('#', '')
    
    # Check input length
    is_three = len(hex_color) == 3
    is_six = len(hex_color) == 6
    is_eight = len(hex_color) == 8
    
    if not (is_three or is_six or is_eight):
        raise ValueError(f"Unexpected hex string format: {hex_color}")
    
    # Initialize RGB and Alpha values
    r = 0
    g = 0
    b = 0
    a = 255  # Default to fully opaque
    
    # Extract RGB values based on string length
    if is_three:
        # For 3-digit hex, each character is repeated once
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
    elif is_six:
        # For 6-digit hex, directly extract RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    elif is_eight:
        # For 8-digit hex, first 2 digits are Alpha, next 6 are RGB
        a = int(hex_color[0:2], 16)
        r = int(hex_color[2:4], 16)
        g = int(hex_color[4:6], 16)
        b = int(hex_color[6:8], 16)
    
    # Combine into ARGB integer
    return (a << 24) | ((r & 0xff) << 16) | ((g & 0xff) << 8) | (b & 0xff)

def int_from_lstar(lstar: float) -> Argb:
    """
    Converts an L* value to an ARGB representation.

    Args:
        lstar: L* in L*a*b*. 0.0 <= L* <= 100.0

    Returns:
        ARGB representation of grayscale color with lightness matching L*
    """
    y = y_from_lstar(lstar)
    component = delinearized(y)
    return argb_from_rgb(component, component, component)

def signum(num: float) -> int:
    """
    The signum function.

    Returns 1 if num > 0, -1 if num < 0, and 0 if num = 0
    """
    if num < 0:
        return -1
    elif num == 0:
        return 0
    else:
        return 1

def lerp(start: float, stop: float, amount: float) -> float:
    """
    The linear interpolation function.

    Returns start if amount = 0 and stop if amount = 1
    """
    return (1.0 - amount) * start + amount * stop

def matrix_multiply(input_vec: Vec3, matrix: list) -> Vec3:
    """
    Multiplies a 1x3 row vector with a 3x3 matrix, returning the product.
    """
    a = input_vec.a * matrix[0][0] + input_vec.b * matrix[0][1] + input_vec.c * matrix[0][2]
    b = input_vec.a * matrix[1][0] + input_vec.b * matrix[1][1] + input_vec.c * matrix[1][2]
    c = input_vec.a * matrix[2][0] + input_vec.b * matrix[2][1] + input_vec.c * matrix[2][2]
    return Vec3(a, b, c)

def clamp_int(min_value: int, max_value: int, value: int) -> int:
    """
    Clamps an integer between two integers.
    
    Args:
        min_value: The minimum value
        max_value: The maximum value
        value: The value to clamp
        
    Returns:
        The clamped value
    """
    return max(min_value, min(max_value, value))

def clamp_double(min_value: float, max_value: float, value: float) -> float:
    """
    Clamps a floating-point number between two floating-point numbers.
    
    Args:
        min_value: The minimum value
        max_value: The maximum value
        value: The value to clamp
        
    Returns:
        The clamped value
    """
    return max(min_value, min(max_value, value))
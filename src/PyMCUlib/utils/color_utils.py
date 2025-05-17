# utils/color_utils.py

from typing import List
import math
from PyMCUlib.utils import math_utils

# Constants for color space conversions
SRGB_TO_XYZ = [
    [0.41233895, 0.35762064, 0.18051042],
    [0.2126, 0.7152, 0.0722],
    [0.01932141, 0.11916382, 0.95034478],
]

XYZ_TO_SRGB = [
    [
        3.2413774792388685,
        -1.5376652402851851,
        -0.49885366846268053,
    ],
    [
        -0.9691452513005321,
        1.8758853451067872,
        0.04156585616912061,
    ],
    [
        0.05562093689691305,
        -0.20395524564742123,
        1.0571799111220335,
    ],
]

WHITE_POINT_D65 = [95.047, 100.0, 108.883]


def argb_from_rgb(red: int, green: int, blue: int) -> int:
    """
    Converts a color from RGB components to ARGB format.

    Args:
        red: The red component (0-255)
        green: The green component (0-255)
        blue: The blue component (0-255)

    Returns:
        The ARGB representation of the color
    """
    return (255 << 24 | (red & 255) << 16 | (green & 255) << 8 | blue & 255) & 0xFFFFFFFF


def argb_from_linrgb(linrgb: List[float]) -> int:
    """
    Converts a color from linear RGB components to ARGB format.

    Args:
        linrgb: The linear RGB components

    Returns:
        The ARGB representation of the color
    """
    r = delinearized(linrgb[0])
    g = delinearized(linrgb[1])
    b = delinearized(linrgb[2])
    return argb_from_rgb(r, g, b)


def alpha_from_argb(argb: int) -> int:
    """
    Returns the alpha component of a color in ARGB format.

    Args:
        argb: The ARGB color

    Returns:
        The alpha component (0-255)
    """
    return (argb >> 24) & 255


def red_from_argb(argb: int) -> int:
    """
    Returns the red component of a color in ARGB format.

    Args:
        argb: The ARGB color

    Returns:
        The red component (0-255)
    """
    return (argb >> 16) & 255


def green_from_argb(argb: int) -> int:
    """
    Returns the green component of a color in ARGB format.

    Args:
        argb: The ARGB color

    Returns:
        The green component (0-255)
    """
    return (argb >> 8) & 255


def blue_from_argb(argb: int) -> int:
    """
    Returns the blue component of a color in ARGB format.

    Args:
        argb: The ARGB color

    Returns:
        The blue component (0-255)
    """
    return argb & 255


def is_opaque(argb: int) -> bool:
    """
    Returns whether a color in ARGB format is opaque.

    Args:
        argb: The ARGB color

    Returns:
        True if the color is opaque, False otherwise
    """
    return alpha_from_argb(argb) >= 255


def argb_from_xyz(x: float, y: float, z: float) -> int:
    """
    Converts a color from XYZ to ARGB.

    Args:
        x: The X component
        y: The Y component
        z: The Z component

    Returns:
        The ARGB representation of the color
    """
    matrix = XYZ_TO_SRGB
    linear_r = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z
    linear_g = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z
    linear_b = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z
    r = delinearized(linear_r)
    g = delinearized(linear_g)
    b = delinearized(linear_b)
    return argb_from_rgb(r, g, b)


def xyz_from_argb(argb: int) -> List[float]:
    """
    Converts a color from ARGB to XYZ.

    Args:
        argb: The ARGB color

    Returns:
        The XYZ components as a list [x, y, z]
    """
    r = linearized(red_from_argb(argb))
    g = linearized(green_from_argb(argb))
    b = linearized(blue_from_argb(argb))
    return math_utils.matrix_multiply([r, g, b], SRGB_TO_XYZ)


def argb_from_lab(l: float, a: float, b_val: float) -> int:
    """
    Converts a color represented in Lab color space into an ARGB
    integer.

    Args:
        l: The L component
        a: The a component
        b_val: The b component

    Returns:
        The ARGB representation of the color
    """
    white_point = WHITE_POINT_D65
    fy = (l + 16.0) / 116.0
    fx = a / 500.0 + fy
    fz = fy - b_val / 200.0
    x_normalized = _lab_invf(fx)
    y_normalized = _lab_invf(fy)
    z_normalized = _lab_invf(fz)
    x = x_normalized * white_point[0]
    y = y_normalized * white_point[1]
    z = z_normalized * white_point[2]
    return argb_from_xyz(x, y, z)


def lab_from_argb(argb: int) -> List[float]:
    """
    Converts a color from ARGB representation to L*a*b*
    representation.

    Args:
        argb: The ARGB representation of a color

    Returns:
        A Lab object representing the color as [L, a, b]
    """
    linear_r = linearized(red_from_argb(argb))
    linear_g = linearized(green_from_argb(argb))
    linear_b = linearized(blue_from_argb(argb))
    matrix = SRGB_TO_XYZ
    x = matrix[0][0] * linear_r + matrix[0][1] * linear_g + matrix[0][2] * linear_b
    y = matrix[1][0] * linear_r + matrix[1][1] * linear_g + matrix[1][2] * linear_b
    z = matrix[2][0] * linear_r + matrix[2][1] * linear_g + matrix[2][2] * linear_b
    white_point = WHITE_POINT_D65
    x_normalized = x / white_point[0]
    y_normalized = y / white_point[1]
    z_normalized = z / white_point[2]
    fx = _lab_f(x_normalized)
    fy = _lab_f(y_normalized)
    fz = _lab_f(z_normalized)
    l = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    return [l, a, b]


def argb_from_lstar(lstar: float) -> int:
    """
    Converts an L* value to an ARGB representation.

    Args:
        lstar: L* in L*a*b*

    Returns:
        ARGB representation of grayscale color with lightness
        matching L*
    """
    y = y_from_lstar(lstar)
    component = delinearized(y)
    return argb_from_rgb(component, component, component)


def lstar_from_argb(argb: int) -> float:
    """
    Computes the L* value of a color in ARGB representation.

    Args:
        argb: ARGB representation of a color

    Returns:
        L*, from L*a*b*, coordinate of the color
    """
    y = xyz_from_argb(argb)[1]
    return 116.0 * _lab_f(y / 100.0) - 16.0


def y_from_lstar(lstar: float) -> float:
    """
    Converts an L* value to a Y value.

    L* in L*a*b* and Y in XYZ measure the same quantity, luminance.

    L* measures perceptual luminance, a linear scale. Y in XYZ
    measures relative luminance, a logarithmic scale.

    Args:
        lstar: L* in L*a*b*

    Returns:
        Y in XYZ
    """
    return 100.0 * _lab_invf((lstar + 16.0) / 116.0)


def lstar_from_y(y: float) -> float:
    """
    Converts a Y value to an L* value.

    L* in L*a*b* and Y in XYZ measure the same quantity, luminance.

    L* measures perceptual luminance, a linear scale. Y in XYZ
    measures relative luminance, a logarithmic scale.

    Args:
        y: Y in XYZ

    Returns:
        L* in L*a*b*
    """
    return _lab_f(y / 100.0) * 116.0 - 16.0


def linearized(rgb_component: int) -> float:
    """
    Linearizes an RGB component.

    Args:
        rgb_component: 0 <= rgb_component <= 255, represents R/G/B channel

    Returns:
        0.0 <= output <= 100.0, color channel converted to linear RGB space
    """
    normalized = rgb_component / 255.0
    if normalized <= 0.040449936:
        return normalized / 12.92 * 100.0
    else:
        return math.pow((normalized + 0.055) / 1.055, 2.4) * 100.0


def delinearized(rgb_component: float) -> int:
    """
    Delinearizes an RGB component.

    Args:
        rgb_component: 0.0 <= rgb_component <= 100.0, represents linear R/G/B channel

    Returns:
        0 <= output <= 255, color channel converted to regular RGB space
    """
    normalized = rgb_component / 100.0
    delinearized_val = 0.0
    if normalized <= 0.0031308:
        delinearized_val = normalized * 12.92
    else:
        delinearized_val = 1.055 * math.pow(normalized, 1.0 / 2.4) - 0.055
    return math_utils.clamp_int(0, 255, round(delinearized_val * 255.0))


def white_point_d65() -> List[float]:
    """
    Returns the standard white point; white on a sunny day.

    Returns:
        The white point
    """
    return WHITE_POINT_D65


def _lab_f(t: float) -> float:
    """
    Helper function for Lab color space conversions.

    Args:
        t: Input value

    Returns:
        Transformed value
    """
    e = 216.0 / 24389.0
    kappa = 24389.0 / 27.0
    if t > e:
        return math.pow(t, 1.0 / 3.0)
    else:
        return (kappa * t + 16.0) / 116.0


def _lab_invf(ft: float) -> float:
    """
    Inverse of _lab_f function.

    Args:
        ft: Input value

    Returns:
        Inverse transformed value
    """
    e = 216.0 / 24389.0
    kappa = 24389.0 / 27.0
    ft3 = ft * ft * ft
    if ft3 > e:
        return ft3
    else:
        return (116.0 * ft - 16.0) / kappa
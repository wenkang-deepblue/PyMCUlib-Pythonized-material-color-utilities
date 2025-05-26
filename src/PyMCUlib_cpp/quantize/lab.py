# lab.py

from typing import NamedTuple
from PyMCUlib_cpp.utils.utils import Argb, WHITE_POINT_D65, delinearized, linearized, argb_from_rgb

class Lab(NamedTuple):
    """
    A color in the CIE Lab color space.
    L* represents lightness, a* and b* represent color dimensions.
    """
    l: float = 0.0
    a: float = 0.0
    b: float = 0.0

    def delta_e(self, lab: 'Lab') -> float:
        """
        Calculates the squared color distance between two colors in Lab space.
        
        Args:
            lab: The other color in Lab space.
            
        Returns:
            The squared color distance.
        """
        d_l = self.l - lab.l
        d_a = self.a - lab.a
        d_b = self.b - lab.b
        return (d_l * d_l) + (d_a * d_a) + (d_b * d_b)
    
    def __str__(self) -> str:
        """Returns a string representation of the Lab color."""
        return f"Lab: L* {self.l} a* {self.a} b* {self.b}"

def int_from_lab(lab: Lab) -> Argb:
    """
    Converts a color from Lab color space to ARGB format.
    
    Args:
        lab: The color in Lab color space.
        
    Returns:
        The color in ARGB format.
    """
    e = 216.0 / 24389.0
    kappa = 24389.0 / 27.0
    ke = 8.0

    fy = (lab.l + 16.0) / 116.0
    fx = (lab.a / 500.0) + fy
    fz = fy - (lab.b / 200.0)
    fx3 = fx * fx * fx
    x_normalized = fx3 if fx3 > e else (116.0 * fx - 16.0) / kappa
    if lab.l > ke:
        y_normalized = fy * fy * fy
    else:
        y_normalized = lab.l / kappa
    fz3 = fz * fz * fz
    z_normalized = fz3 if fz3 > e else (116.0 * fz - 16.0) / kappa
    x = x_normalized * WHITE_POINT_D65[0]
    y = y_normalized * WHITE_POINT_D65[1]
    z = z_normalized * WHITE_POINT_D65[2]

    # int_from_xyz
    rL = 3.2406 * x - 1.5372 * y - 0.4986 * z
    gL = -0.9689 * x + 1.8758 * y + 0.0415 * z
    bL = 0.0557 * x - 0.2040 * y + 1.0570 * z

    red = delinearized(rL)
    green = delinearized(gL)
    blue = delinearized(bL)

    return argb_from_rgb(red, green, blue)

def lab_from_int(argb: Argb) -> Lab:
    """
    Converts a color from ARGB format to Lab color space.
    
    Args:
        argb: The color in ARGB format.
        
    Returns:
        The color in Lab color space.
    """
    red = (argb & 0x00ff0000) >> 16
    green = (argb & 0x0000ff00) >> 8
    blue = (argb & 0x000000ff)
    red_l = linearized(red)
    green_l = linearized(green)
    blue_l = linearized(blue)
    x = 0.41233895 * red_l + 0.35762064 * green_l + 0.18051042 * blue_l
    y = 0.2126 * red_l + 0.7152 * green_l + 0.0722 * blue_l
    z = 0.01932141 * red_l + 0.11916382 * green_l + 0.95034478 * blue_l
    y_normalized = y / WHITE_POINT_D65[1]
    e = 216.0 / 24389.0
    kappa = 24389.0 / 27.0
    
    if y_normalized > e:
        fy = pow(y_normalized, 1.0 / 3.0)
    else:
        fy = (kappa * y_normalized + 16) / 116
    
    x_normalized = x / WHITE_POINT_D65[0]
    if x_normalized > e:
        fx = pow(x_normalized, 1.0 / 3.0)
    else:
        fx = (kappa * x_normalized + 16) / 116
    
    z_normalized = z / WHITE_POINT_D65[2]
    if z_normalized > e:
        fz = pow(z_normalized, 1.0 / 3.0)
    else:
        fz = (kappa * z_normalized + 16) / 116
    
    l = 116.0 * fy - 16
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    return Lab(l, a, b)
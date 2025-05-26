# cam.py

from dataclasses import dataclass
import math
from PyMCUlib_cpp.utils.utils import Argb, PI
from PyMCUlib_cpp.utils.utils import (
    sanitize_degrees_double, signum,
    linearized, delinearized, argb_from_rgb
)
from PyMCUlib_cpp.cam.viewing_conditions import ViewingConditions, DEFAULT_VIEWING_CONDITIONS
from PyMCUlib_cpp.cam.hct_solver import solve_to_int

@dataclass
class Cam:
    """CAM16 color appearance model data class"""
    hue: float = 0.0
    chroma: float = 0.0
    j: float = 0.0
    q: float = 0.0
    m: float = 0.0
    s: float = 0.0
    jstar: float = 0.0
    astar: float = 0.0
    bstar: float = 0.0

def cam_from_int(argb: Argb) -> Cam:
    """
    Converts an ARGB color to a CAM16 object.

    Args:
        argb: ARGB representation of a color.

    Returns:
        CAM16 object representing the color in the default viewing conditions.
    """
    return cam_from_int_and_viewing_conditions(argb, DEFAULT_VIEWING_CONDITIONS)

def cam_from_int_and_viewing_conditions(argb: Argb, viewing_conditions: ViewingConditions) -> Cam:
    """
    Converts an ARGB color to a CAM16 object under specified viewing conditions.

    Args:
        argb: ARGB representation of a color.
        viewing_conditions: Viewing conditions.

    Returns:
        CAM16 object representing the color.
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

    # Convert XYZ to 'cone'/'rgb' responses
    r_c = 0.401288 * x + 0.650173 * y - 0.051461 * z
    g_c = -0.250268 * x + 1.204414 * y + 0.045854 * z
    b_c = -0.002079 * x + 0.048952 * y + 0.953127 * z

    # Discount illuminant
    r_d = viewing_conditions.rgb_d[0] * r_c
    g_d = viewing_conditions.rgb_d[1] * g_c
    b_d = viewing_conditions.rgb_d[2] * b_c

    # Chromatic adaptation
    r_af = pow(viewing_conditions.fl * abs(r_d) / 100.0, 0.42)
    g_af = pow(viewing_conditions.fl * abs(g_d) / 100.0, 0.42)
    b_af = pow(viewing_conditions.fl * abs(b_d) / 100.0, 0.42)
    r_a = signum(r_d) * 400.0 * r_af / (r_af + 27.13)
    g_a = signum(g_d) * 400.0 * g_af / (g_af + 27.13)
    b_a = signum(b_d) * 400.0 * b_af / (b_af + 27.13)

    # Redness-greenness
    a = (11.0 * r_a + -12.0 * g_a + b_a) / 11.0
    b = (r_a + g_a - 2.0 * b_a) / 9.0
    u = (20.0 * r_a + 20.0 * g_a + 21.0 * b_a) / 20.0
    p2 = (40.0 * r_a + 20.0 * g_a + b_a) / 20.0

    radians = math.atan2(b, a)
    degrees = radians * 180.0 / PI
    hue = sanitize_degrees_double(degrees)
    hue_radians = hue * PI / 180.0
    ac = p2 * viewing_conditions.nbb

    j = 100.0 * pow(ac / viewing_conditions.aw,
                     viewing_conditions.c * viewing_conditions.z)
    q = (4.0 / viewing_conditions.c) * math.sqrt(j / 100.0) * \
        (viewing_conditions.aw + 4.0) * viewing_conditions.fl_root
    hue_prime = hue if hue >= 20.14 else hue + 360
    e_hue = 0.25 * (math.cos(hue_prime * PI / 180.0 + 2.0) + 3.8)
    p1 = 50000.0 / 13.0 * e_hue * viewing_conditions.n_c * viewing_conditions.ncb
    t = p1 * math.sqrt(a * a + b * b) / (u + 0.305)
    alpha = pow(t, 0.9) * \
            pow(1.64 - pow(0.29, viewing_conditions.background_y_to_white_point_y),
                0.73)
    c = alpha * math.sqrt(j / 100.0)
    m = c * viewing_conditions.fl_root
    s = 50.0 * math.sqrt((alpha * viewing_conditions.c) /
                         (viewing_conditions.aw + 4.0))
    jstar = (1.0 + 100.0 * 0.007) * j / (1.0 + 0.007 * j)
    mstar = 1.0 / 0.0228 * math.log(1.0 + 0.0228 * m)
    astar = mstar * math.cos(hue_radians)
    bstar = mstar * math.sin(hue_radians)
    return Cam(hue, c, j, q, m, s, jstar, astar, bstar)

def cam_from_ucs_and_viewing_conditions(jstar: float, astar: float, bstar: float,
                                       viewing_conditions: ViewingConditions) -> Cam:
    """
    Creates a CAM16 object from UCS coordinates and viewing conditions.

    Args:
        jstar: J* coordinate
        astar: a* coordinate
        bstar: b* coordinate
        viewing_conditions: Viewing conditions

    Returns:
        CAM16 object
    """
    a = astar
    b = bstar
    m = math.sqrt(a * a + b * b)
    m_2 = (math.exp(m * 0.0228) - 1.0) / 0.0228
    c = m_2 / viewing_conditions.fl_root
    h = math.atan2(b, a) * (180.0 / PI)
    if h < 0.0:
        h += 360.0
    j = jstar / (1 - (jstar - 100) * 0.007)
    return cam_from_jch_and_viewing_conditions(j, c, h, viewing_conditions)

def cam_from_jch_and_viewing_conditions(j: float, c: float, h: float,
                                       viewing_conditions: ViewingConditions) -> Cam:
    """
    Creates a CAM16 object from J, C, h and viewing conditions.
    
    Args:
        j: Lightness
        c: Chroma
        h: Hue in degrees
        viewing_conditions: Viewing conditions
        
    Returns:
        CAM16 object
    """
    q = (4.0 / viewing_conditions.c) * math.sqrt(j / 100.0) * \
        (viewing_conditions.aw + 4.0) * (viewing_conditions.fl_root)
    m = c * viewing_conditions.fl_root
    alpha = c / math.sqrt(j / 100.0)
    s = 50.0 * math.sqrt((alpha * viewing_conditions.c) /
                         (viewing_conditions.aw + 4.0))
    hue_radians = h * PI / 180.0
    jstar = (1.0 + 100.0 * 0.007) * j / (1.0 + 0.007 * j)
    mstar = 1.0 / 0.0228 * math.log(1.0 + 0.0228 * m)
    astar = mstar * math.cos(hue_radians)
    bstar = mstar * math.sin(hue_radians)
    return Cam(h, c, j, q, m, s, jstar, astar, bstar)

def int_from_cam(cam: Cam) -> Argb:
    """
    Converts a CAM16 object to an ARGB color.

    Args:
        cam: CAM16 object

    Returns:
        ARGB representation of the color
    """
    return int_from_cam_and_viewing_conditions(cam, DEFAULT_VIEWING_CONDITIONS)

def int_from_cam_and_viewing_conditions(cam: Cam, viewing_conditions: ViewingConditions) -> Argb:
    """
    Converts a CAM16 object to an ARGB color under specified viewing conditions.

    Args:
        cam: CAM16 object
        viewing_conditions: Viewing conditions

    Returns:
        ARGB representation of the color
    """
    alpha = (0.0 if cam.chroma == 0.0 or cam.j == 0.0
             else cam.chroma / math.sqrt(cam.j / 100.0))
    t = pow(
        alpha / pow(1.64 - pow(0.29,
                               viewing_conditions.background_y_to_white_point_y),
                    0.73),
        1.0 / 0.9)
    h_rad = cam.hue * PI / 180.0
    e_hue = 0.25 * (math.cos(h_rad + 2.0) + 3.8)
    ac = viewing_conditions.aw * \
         pow(cam.j / 100.0, 1.0 / viewing_conditions.c / viewing_conditions.z)
    p1 = e_hue * (50000.0 / 13.0) * viewing_conditions.n_c * \
         viewing_conditions.ncb
    p2 = ac / viewing_conditions.nbb
    h_sin = math.sin(h_rad)
    h_cos = math.cos(h_rad)
    gamma = 23.0 * (p2 + 0.305) * t / \
           (23.0 * p1 + 11.0 * t * h_cos + 108.0 * t * h_sin)
    a = gamma * h_cos
    b = gamma * h_sin
    r_a = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0
    g_a = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0
    b_a = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0

    r_c_base = max(0, (27.13 * abs(r_a)) / (400.0 - abs(r_a)))
    r_c = signum(r_a) * (100.0 / viewing_conditions.fl) * pow(r_c_base, 1.0 / 0.42)
    g_c_base = max(0, (27.13 * abs(g_a)) / (400.0 - abs(g_a)))
    g_c = signum(g_a) * (100.0 / viewing_conditions.fl) * pow(g_c_base, 1.0 / 0.42)
    b_c_base = max(0, (27.13 * abs(b_a)) / (400.0 - abs(b_a)))
    b_c = signum(b_a) * (100.0 / viewing_conditions.fl) * pow(b_c_base, 1.0 / 0.42)
    r_x = r_c / viewing_conditions.rgb_d[0]
    g_x = g_c / viewing_conditions.rgb_d[1]
    b_x = b_c / viewing_conditions.rgb_d[2]
    x = 1.86206786 * r_x - 1.01125463 * g_x + 0.14918677 * b_x
    y = 0.38752654 * r_x + 0.62144744 * g_x - 0.00897398 * b_x
    z = -0.01584150 * r_x - 0.03412294 * g_x + 1.04996444 * b_x

    # XYZ to RGB
    r_l = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g_l = -0.9689 * x + 1.8758 * y + 0.0415 * z
    b_l = 0.0557 * x - 0.2040 * y + 1.0570 * z

    # Linear RGB to sRGB
    red = delinearized(r_l)
    green = delinearized(g_l)
    blue = delinearized(b_l)

    return argb_from_rgb(red, green, blue)

def int_from_hcl(hue: float, chroma: float, lstar: float) -> Argb:
    """
    Creates a color from HCL (hue, chroma, lightness).

    Args:
        hue: 0 <= hue < 360 hue value
        chroma: chroma value
        lstar: 0 <= lstar <= 100 lightness value

    Returns:
        ARGB representation of the color
    """
    return solve_to_int(hue, chroma, lstar)

def cam_from_xyz_and_viewing_conditions(x: float, y: float, z: float,
                                       viewing_conditions: ViewingConditions) -> Cam:
    """
    Converts a color expressed in the XYZ color space and viewed
    in [viewingConditions], to a CAM16 object.
    
    Args:
        x: X coordinate
        y: Y coordinate
        z: Z coordinate
        viewing_conditions: Viewing conditions
        
    Returns:
        CAM16 object
    """
    # Convert XYZ to 'cone'/'rgb' responses
    r_c = 0.401288 * x + 0.650173 * y - 0.051461 * z
    g_c = -0.250268 * x + 1.204414 * y + 0.045854 * z
    b_c = -0.002079 * x + 0.048952 * y + 0.953127 * z

    # Discount illuminant
    r_d = viewing_conditions.rgb_d[0] * r_c
    g_d = viewing_conditions.rgb_d[1] * g_c
    b_d = viewing_conditions.rgb_d[2] * b_c

    # Chromatic adaptation
    r_af = pow(viewing_conditions.fl * abs(r_d) / 100.0, 0.42)
    g_af = pow(viewing_conditions.fl * abs(g_d) / 100.0, 0.42)
    b_af = pow(viewing_conditions.fl * abs(b_d) / 100.0, 0.42)
    r_a = signum(r_d) * 400.0 * r_af / (r_af + 27.13)
    g_a = signum(g_d) * 400.0 * g_af / (g_af + 27.13)
    b_a = signum(b_d) * 400.0 * b_af / (b_af + 27.13)

    # Redness-greenness
    a = (11.0 * r_a + -12.0 * g_a + b_a) / 11.0
    b = (r_a + g_a - 2.0 * b_a) / 9.0
    u = (20.0 * r_a + 20.0 * g_a + 21.0 * b_a) / 20.0
    p2 = (40.0 * r_a + 20.0 * g_a + b_a) / 20.0

    radians = math.atan2(b, a)
    degrees = radians * 180.0 / PI
    hue = sanitize_degrees_double(degrees)
    hue_radians = hue * PI / 180.0
    ac = p2 * viewing_conditions.nbb

    j = 100.0 * pow(ac / viewing_conditions.aw,
                     viewing_conditions.c * viewing_conditions.z)
    q = (4.0 / viewing_conditions.c) * math.sqrt(j / 100.0) * \
        (viewing_conditions.aw + 4.0) * viewing_conditions.fl_root
    hue_prime = hue if hue >= 20.14 else hue + 360
    e_hue = 0.25 * (math.cos(hue_prime * PI / 180.0 + 2.0) + 3.8)
    p1 = 50000.0 / 13.0 * e_hue * viewing_conditions.n_c * viewing_conditions.ncb
    t = p1 * math.sqrt(a * a + b * b) / (u + 0.305)
    alpha = pow(t, 0.9) * \
            pow(1.64 - pow(0.29, viewing_conditions.background_y_to_white_point_y),
                0.73)
    c = alpha * math.sqrt(j / 100.0)
    m = c * viewing_conditions.fl_root
    s = 50.0 * math.sqrt((alpha * viewing_conditions.c) /
                         (viewing_conditions.aw + 4.0))
    jstar = (1.0 + 100.0 * 0.007) * j / (1.0 + 0.007 * j)
    mstar = 1.0 / 0.0228 * math.log(1.0 + 0.0228 * m)
    astar = mstar * math.cos(hue_radians)
    bstar = mstar * math.sin(hue_radians)
    return Cam(hue, c, j, q, m, s, jstar, astar, bstar)

def cam_distance(a: Cam, b: Cam) -> float:
    """
    Calculates the distance between two CAM16 objects.
    
    Args:
        a: First CAM16 object
        b: Second CAM16 object
        
    Returns:
        Color distance value
    """
    d_j = a.jstar - b.jstar
    d_a = a.astar - b.astar
    d_b = a.bstar - b.bstar
    d_e_prime = math.sqrt(d_j * d_j + d_a * d_a + d_b * d_b)
    d_e = 1.41 * pow(d_e_prime, 0.63)
    return d_e
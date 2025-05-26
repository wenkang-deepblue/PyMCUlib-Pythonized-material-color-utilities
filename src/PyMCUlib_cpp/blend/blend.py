# blend.py
from PyMCUlib_cpp.utils.utils import (
    Argb, diff_degrees, rotation_direction, sanitize_degrees_double
)
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.cam.cam import (
    DEFAULT_VIEWING_CONDITIONS,
    cam_from_int, int_from_cam, cam_from_ucs_and_viewing_conditions
)

def blend_harmonize(design_color: Argb, key_color: Argb) -> Argb:
    """
    Harmonizes one color to another.
    
    Args:
        design_color: Color to harmonize
        key_color: Color providing the direction to move
        
    Returns:
        Harmonized color
    """
    from_hct = Hct.from_int(design_color)
    to_hct = Hct.from_int(key_color)
    difference_degrees = diff_degrees(from_hct.get_hue(), to_hct.get_hue())
    rotation_degrees = min(difference_degrees * 0.5, 15.0)
    output_hue = sanitize_degrees_double(
        from_hct.get_hue() +
        rotation_degrees *
        rotation_direction(from_hct.get_hue(), to_hct.get_hue())
    )
    from_hct.set_hue(output_hue)
    return from_hct.to_int()

def blend_hct_hue(from_color: Argb, to_color: Argb, amount: float) -> Argb:
    """
    Blends hue from two colors in the HCT color space.
    
    Args:
        from_color: Source color
        to_color: Destination color
        amount: How much of the destination to blend in, 0.0 to 1.0
        
    Returns:
        Blended color
    """
    ucs = blend_cam16_ucs(from_color, to_color, amount)
    ucs_hct = Hct.from_int(ucs)
    from_hct = Hct.from_int(from_color)
    from_hct.set_hue(ucs_hct.get_hue())
    return from_hct.to_int()

def blend_cam16_ucs(from_color: Argb, to_color: Argb, amount: float) -> Argb:
    """
    Blend two colors in the CAM16-UCS color space.
    
    Args:
        from_color: Source color
        to_color: Destination color
        amount: How much of the destination to blend in, 0.0 to 1.0
        
    Returns:
        Blended color
    """
    from_cam = cam_from_int(from_color)
    to_cam = cam_from_int(to_color)
    
    a_j = from_cam.jstar
    a_a = from_cam.astar
    a_b = from_cam.bstar
    
    b_j = to_cam.jstar
    b_a = to_cam.astar
    b_b = to_cam.bstar
    
    jstar = a_j + (b_j - a_j) * amount
    astar = a_a + (b_a - a_a) * amount
    bstar = a_b + (b_b - a_b) * amount
    
    blended = cam_from_ucs_and_viewing_conditions(
        jstar, astar, bstar, DEFAULT_VIEWING_CONDITIONS
    )
    return int_from_cam(blended)
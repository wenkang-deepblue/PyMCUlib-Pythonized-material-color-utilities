# viewing_conditions.py

import math
from dataclasses import dataclass
from typing import List
from PyMCUlib_cpp.utils.utils import y_from_lstar

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

# White point D65 (standard illuminant representing daylight)
WHITE_POINT_D65 = [95.047, 100.0, 108.883]

def lerp(start: float, stop: float, amount: float) -> float:
    """
    Linear interpolation between start and stop, with amount between 0 and 1.
    """
    return (1.0 - amount) * start + amount * stop

def create_viewing_conditions(
    white_point: List[float],
    adapting_luminance: float,
    background_lstar: float,
    surround: float,
    discounting_illuminant: bool
) -> ViewingConditions:
    """
    Creates ViewingConditions, which are parameters that inform colorimetric operations.
    
    Args:
        white_point: XYZ coordinates of the white point
        adapting_luminance: Adapting luminance
        background_lstar: L* of the background
        surround: Surround factor, 0-2
        discounting_illuminant: Whether to discount the illuminant
        
    Returns:
        ViewingConditions for use in CAM16 conversions
    """
    background_lstar_corrected = max(30.0, background_lstar)
    
    # RGB coordinates of the white point
    rgb_w = [
        0.401288 * white_point[0] + 0.650173 * white_point[1] - 0.051461 * white_point[2],
        -0.250268 * white_point[0] + 1.204414 * white_point[1] + 0.045854 * white_point[2],
        -0.002079 * white_point[0] + 0.048952 * white_point[1] + 0.953127 * white_point[2]
    ]
    
    # Surround-based constants
    f = 0.8 + (surround / 10.0)
    c = lerp(0.59, 0.69, (f - 0.9) * 10.0) if f >= 0.9 else lerp(0.525, 0.59, (f - 0.8) * 10.0)
    d = 1.0 if discounting_illuminant else f * (1.0 - ((1.0 / 3.6) * math.exp((-adapting_luminance - 42.0) / 92.0)))
    d = max(0.0, min(1.0, d))
    nc = f
    
    # Calculate rgb_d
    rgb_d = [
        (d * (100.0 / rgb_w[0]) + 1.0 - d),
        (d * (100.0 / rgb_w[1]) + 1.0 - d),
        (d * (100.0 / rgb_w[2]) + 1.0 - d)
    ]
    
    # Calculate adaptation parameters
    k = 1.0 / (5.0 * adapting_luminance + 1.0)
    k4 = k * k * k * k
    k4f = 1.0 - k4
    fl = (k4 * adapting_luminance) + (0.1 * k4f * k4f * pow(5.0 * adapting_luminance, 1.0 / 3.0))
    fl_root = pow(fl, 0.25)
    
    # Calculate background effect parameters
    n = y_from_lstar(background_lstar_corrected) / white_point[1]
    z = 1.48 + math.sqrt(n)
    nbb = 0.725 / pow(n, 0.2)
    ncb = nbb
    
    # Calculate adaptation effects
    rgb_a_factors = [
        pow(fl * rgb_d[0] * rgb_w[0] / 100.0, 0.42),
        pow(fl * rgb_d[1] * rgb_w[1] / 100.0, 0.42),
        pow(fl * rgb_d[2] * rgb_w[2] / 100.0, 0.42)
    ]
    
    rgb_a = [
        400.0 * rgb_a_factors[0] / (rgb_a_factors[0] + 27.13),
        400.0 * rgb_a_factors[1] / (rgb_a_factors[1] + 27.13),
        400.0 * rgb_a_factors[2] / (rgb_a_factors[2] + 27.13)
    ]
    
    aw = (40.0 * rgb_a[0] + 20.0 * rgb_a[1] + rgb_a[2]) / 20.0 * nbb
    
    return ViewingConditions(
        adapting_luminance=adapting_luminance,
        background_lstar=background_lstar_corrected,
        surround=surround,
        discounting_illuminant=discounting_illuminant,
        background_y_to_white_point_y=n,
        aw=aw,
        nbb=nbb,
        ncb=ncb,
        c=c,
        n_c=nc,
        fl=fl,
        fl_root=fl_root,
        z=z,
        white_point=white_point.copy(),
        rgb_d=rgb_d
    )

def default_with_background_lstar(background_lstar: float) -> ViewingConditions:
    """
    Creates default viewing conditions with a custom background L*.
    
    Args:
        background_lstar: L* of the background
        
    Returns:
        ViewingConditions for use in CAM16 conversions
    """
    return create_viewing_conditions(
        WHITE_POINT_D65,
        (200.0 / math.pi * y_from_lstar(50.0) / 100.0),
        background_lstar,
        2.0,
        False
    )

# Default viewing conditions with a 50.0 L* background
DEFAULT_VIEWING_CONDITIONS = ViewingConditions(
    adapting_luminance=11.725676537,
    background_lstar=50.000000000,
    surround=2.000000000,
    discounting_illuminant=False,
    background_y_to_white_point_y=0.184186503,
    aw=29.981000900,
    nbb=1.016919255,
    ncb=1.016919255,
    c=0.689999998,
    n_c=1.000000000,
    fl=0.388481468,
    fl_root=0.789482653,
    z=1.909169555,
    white_point=[95.047, 100.0, 108.883],
    rgb_d=[1.021177769, 0.986307740, 0.933960497]
)
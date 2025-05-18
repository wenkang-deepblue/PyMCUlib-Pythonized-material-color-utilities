# hct/viewing_conditions.py

import math
from typing import List, Optional
from PyMCUlib.utils import color_utils
from PyMCUlib.utils import math_utils

class ViewingConditions:
    """
    In traditional color spaces, a color can be identified solely by the
    observer's measurement of the color. Color appearance models such as CAM16
    also use information about the environment where the color was
    observed, known as the viewing conditions.

    For example, white under the traditional assumption of a midday sun white
    point is accurately measured as a slightly chromatic blue by CAM16. (roughly,
    hue 203, chroma 3, lightness 100)

    This class caches intermediate values of the CAM16 conversion process that
    depend only on viewing conditions, enabling speed ups.
    """

    @classmethod
    def make(
        cls,
        white_point: Optional[List[float]] = None,
        adapting_luminance: float = (200.0 / math.pi) * color_utils.y_from_lstar(50.0) / 100.0,
        background_lstar: float = 50.0,
        surround: float = 2.0,
        discounting_illuminant: bool = False,
    ) -> "ViewingConditions":
        """
        Create ViewingConditions from a simple, physically relevant, set of
        parameters.

        Args:
            white_point: White point, measured in the XYZ color space.
                default = D65, or sunny day afternoon
            adapting_luminance: The luminance of the adapting field. Informally,
                how bright it is in the room where the color is viewed. Can be
                calculated from lux by multiplying lux by 0.0586. default = 11.72,
                or 200 lux.
            background_lstar: The lightness of the area surrounding the color.
                measured by L* in L*a*b*. default = 50.0
            surround: A general description of the lighting surrounding the
                color. 0 is pitch dark, like watching a movie in a theater. 1.0 is a
                dimly light room, like watching TV at home at night. 2.0 means there
                is no difference between the lighting on the color and around it.
                default = 2.0
            discounting_illuminant: Whether the eye accounts for the tint of the
                ambient lighting, such as knowing an apple is still red in green light.
                default = false, the eye does not perform this process on
                self-luminous objects like displays.

        Returns:
            ViewingConditions instance
        """
        if white_point is None:
            white_point = color_utils.white_point_d65()

        xyz = white_point
        r_w = xyz[0] * 0.401288 + xyz[1] * 0.650173 + xyz[2] * -0.051461
        g_w = xyz[0] * -0.250268 + xyz[1] * 1.204414 + xyz[2] * 0.045854
        b_w = xyz[0] * -0.002079 + xyz[1] * 0.048952 + xyz[2] * 0.953127

        f = 0.8 + surround / 10.0
        c = (math_utils.lerp(0.59, 0.69, (f - 0.9) * 10.0) if f >= 0.9 
             else math_utils.lerp(0.525, 0.59, (f - 0.8) * 10.0))

        d = (1.0 if discounting_illuminant 
             else f * (1.0 - (1.0 / 3.6) * math.exp((-adapting_luminance - 42.0) / 92.0)))
        d = 1.0 if d > 1.0 else (0.0 if d < 0.0 else d)

        nc = f
        rgb_d = [
            d * (100.0 / r_w) + 1.0 - d,
            d * (100.0 / g_w) + 1.0 - d,
            d * (100.0 / b_w) + 1.0 - d,
        ]

        k = 1.0 / (5.0 * adapting_luminance + 1.0)
        k4 = k * k * k * k
        k4F = 1.0 - k4
        fl = (k4 * adapting_luminance +
              0.1 * k4F * k4F * math.pow(5.0 * adapting_luminance, 1/3))

        n = color_utils.y_from_lstar(background_lstar) / white_point[1]
        z = 1.48 + math.sqrt(n)
        nbb = 0.725 / math.pow(n, 0.2)
        ncb = nbb

        rgb_a_factors = [
            math.pow((fl * rgb_d[0] * r_w) / 100.0, 0.42),
            math.pow((fl * rgb_d[1] * g_w) / 100.0, 0.42),
            math.pow((fl * rgb_d[2] * b_w) / 100.0, 0.42),
        ]

        rgb_a = [
            (400.0 * rgb_a_factors[0]) / (rgb_a_factors[0] + 27.13),
            (400.0 * rgb_a_factors[1]) / (rgb_a_factors[1] + 27.13),
            (400.0 * rgb_a_factors[2]) / (rgb_a_factors[2] + 27.13),
        ]

        aw = (2.0 * rgb_a[0] + rgb_a[1] + 0.05 * rgb_a[2]) * nbb

        return cls(n, aw, nbb, ncb, c, nc, rgb_d, fl, math.pow(fl, 0.25), z)

    def __init__(self, n: float, aw: float, nbb: float, ncb: float, c: float, nc: float, rgb_d: List[float], fl: float, fl_root: float, z: float) -> None:
        """
        Parameters are intermediate values of the CAM16 conversion process. Their
        names are shorthand for technical color science terminology, this class
        would not benefit from documenting them individually. A brief overview
        is available in the CAM16 specification, and a complete overview requires
        a color science textbook, such as Fairchild's Color Appearance Models.
        """
        self.n = n
        self.aw = aw
        self.nbb = nbb
        self.ncb = ncb
        self.c = c
        self.nc = nc
        self.rgb_d = rgb_d
        self.fl = fl
        self.fl_root = fl_root
        self.z = z


# Set the default viewing conditions
ViewingConditions.DEFAULT = ViewingConditions.make()
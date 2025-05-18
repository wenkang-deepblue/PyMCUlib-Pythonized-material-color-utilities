# blend/blend.py

"""
Functions for blending in HCT and CAM16.
"""

from PyMCUlib.hct.cam16 import Cam16
from PyMCUlib.hct.hct import Hct
from PyMCUlib.utils import color_utils
from PyMCUlib.utils import math_utils


class Blend:
    """
    Functions for blending in HCT and CAM16.
    """

    @staticmethod
    def harmonize(design_color: int, source_color: int) -> int:
        """
        Blend the design color's HCT hue towards the key color's HCT
        hue, in a way that leaves the original color recognizable and
        recognizably shifted towards the key color.

        Args:
            design_color: ARGB representation of an arbitrary color.
            source_color: ARGB representation of the main theme color.
        
        Returns:
            The design color with a hue shifted towards the
            system's color, a slightly warmer/cooler variant of the design
            color's hue.
        """
        from_hct = Hct.from_int(design_color)
        to_hct = Hct.from_int(source_color)
        difference_degrees = math_utils.difference_degrees(from_hct.hue, to_hct.hue)
        rotation_degrees = min(difference_degrees * 0.5, 15.0)
        output_hue = math_utils.sanitize_degrees_double(
            from_hct.hue +
            rotation_degrees * math_utils.rotation_direction(from_hct.hue, to_hct.hue))
        return Hct.from_hct(output_hue, from_hct.chroma, from_hct.tone).to_int()

    @staticmethod
    def hct_hue(from_color: int, to_color: int, amount: float) -> int:
        """
        Blends hue from one color into another. The chroma and tone of
        the original color are maintained.

        Args:
            from_color: ARGB representation of color
            to_color: ARGB representation of color
            amount: how much blending to perform; 0.0 >= and <= 1.0
        
        Returns:
            from_color, with a hue blended towards to_color. Chroma and tone
            are constant.
        """
        ucs = Blend.cam16_ucs(from_color, to_color, amount)
        ucs_cam = Cam16.from_int(ucs)
        from_cam = Cam16.from_int(from_color)
        blended = Hct.from_hct(
            ucs_cam.hue,
            from_cam.chroma,
            color_utils.lstar_from_argb(from_color),
        )
        return blended.to_int()

    @staticmethod
    def cam16_ucs(from_color: int, to_color: int, amount: float) -> int:
        """
        Blend in CAM16-UCS space.

        Args:
            from_color: ARGB representation of color
            to_color: ARGB representation of color
            amount: how much blending to perform; 0.0 >= and <= 1.0
        
        Returns:
            from_color, blended towards to_color. Hue, chroma, and tone will
            change.
        """
        from_cam = Cam16.from_int(from_color)
        to_cam = Cam16.from_int(to_color)
        from_j = from_cam.jstar
        from_a = from_cam.astar
        from_b = from_cam.bstar
        to_j = to_cam.jstar
        to_a = to_cam.astar
        to_b = to_cam.bstar
        jstar = from_j + (to_j - from_j) * amount
        astar = from_a + (to_a - from_a) * amount
        bstar = from_b + (to_b - from_b) * amount
        return Cam16.from_ucs(jstar, astar, bstar).to_int()
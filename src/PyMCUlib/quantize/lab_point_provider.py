# quantize/lab_point_provider.py

from typing import List
from PyMCUlib.utils import color_utils
from PyMCUlib.quantize.point_provider import PointProvider


class LabPointProvider(PointProvider):
    """
    Provides conversions needed for K-Means quantization. Converting input to
    points, and converting the final state of the K-Means algorithm to colors.
    """

    def from_int(self, argb: int) -> List[float]:
        """
        Convert a color represented in ARGB to a 3-element array of L*a*b*
        coordinates of the color.
        
        Args:
            argb: The ARGB color integer
            
        Returns:
            A list of L*, a*, b* coordinates
        """
        return color_utils.lab_from_argb(argb)

    def to_int(self, point: List[float]) -> int:
        """
        Convert a 3-element array to a color represented in ARGB.
        
        Args:
            point: A list containing L*, a*, b* coordinates
            
        Returns:
            The ARGB color integer
        """
        return color_utils.argb_from_lab(point[0], point[1], point[2])

    def distance(self, from_point: List[float], to_point: List[float]) -> float:
        """
        Standard CIE 1976 delta E formula also takes the square root, unneeded
        here. This method is used by quantization algorithms to compare distance,
        and the relative ordering is the same, with or without a square root.
        
        This relatively minor optimization is helpful because this method is
        called at least once for each pixel in an image.
        
        Args:
            from_point: The first point in Lab color space
            to_point: The second point in Lab color space
            
        Returns:
            The squared distance between the two points
        """
        d_l = from_point[0] - to_point[0]
        d_a = from_point[1] - to_point[1]
        d_b = from_point[2] - to_point[2]
        return d_l * d_l + d_a * d_a + d_b * d_b
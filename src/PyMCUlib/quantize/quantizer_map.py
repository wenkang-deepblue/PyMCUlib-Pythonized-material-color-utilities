# quantize/quantizer_map.py

from typing import Dict, List
from PyMCUlib.utils import color_utils

class QuantizerMap:
    """
    Quantizes an image into a map, with keys of ARGB colors, and values of the
    number of times that color appears in the image.
    """
    
    @staticmethod
    def quantize(pixels: List[int]) -> Dict[int, int]:
        """
        Args:
            pixels: Colors in ARGB format.
        
        Returns:
            A Dict with keys of ARGB colors, and values of the number of times
            the color appears in the image.
        """
        count_by_color = {}
        for pixel in pixels:
            alpha = color_utils.alpha_from_argb(pixel)
            if alpha < 255:
                continue
            
            count_by_color[pixel] = count_by_color.get(pixel, 0) + 1
                
        return count_by_color
# quantize/quantizer_celebi.py

from typing import Dict, List
from PyMCUlib.quantize.quantizer_wsmeans import QuantizerWsmeans
from PyMCUlib.quantize.quantizer_wu import QuantizerWu


class QuantizerCelebi:
    """
    An image quantizer that improves on the quality of a standard K-Means
    algorithm by setting the K-Means initial state to the output of a Wu
    quantizer, instead of random centroids. Improves on speed by several
    optimizations, as implemented in Wsmeans, or Weighted Square Means, K-Means
    with those optimizations.

    This algorithm was designed by M. Emre Celebi, and was found in their 2011
    paper, Improving the Performance of K-Means for Color Quantization.
    https://arxiv.org/abs/1101.0395
    """

    @staticmethod
    def quantize(pixels: List[int], max_colors: int) -> Dict[int, int]:
        """
        Args:
            pixels: Colors in ARGB format.
            max_colors: The number of colors to divide the image into. A lower
                number of colors may be returned.
        
        Returns:
            Dict with keys of colors in ARGB format, and values of number of
            pixels in the original image that correspond to the color in the
            quantized image.
        """
        wu = QuantizerWu()
        wu_result = wu.quantize(pixels, max_colors)
        return QuantizerWsmeans.quantize(pixels, wu_result, max_colors)
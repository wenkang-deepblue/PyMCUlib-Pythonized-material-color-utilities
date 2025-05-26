# celebi.py

from typing import List
from PyMCUlib_cpp.utils.utils import Argb, is_opaque
from PyMCUlib_cpp.quantize.wsmeans import QuantizerResult, quantize_wsmeans
from PyMCUlib_cpp.quantize.wu import quantize_wu

def quantize_celebi(pixels: List[Argb], max_colors: int) -> QuantizerResult:
    """
    Quantizes colors using Wu's quantizer to generate initial clusters, then
    uses WSmeans to expand these clusters to the requested number of colors.
    
    Args:
        pixels: List of pixels in ARGB format.
        max_colors: The maximum number of colors to generate.
        
    Returns:
        A QuantizerResult with mappings of colors to counts and input pixels to cluster pixels.
    """
    if max_colors == 0 or not pixels:
        return QuantizerResult()
    
    if max_colors > 256:
        max_colors = 256
    
    # Filter out non-opaque pixels
    opaque_pixels = []
    for pixel in pixels:
        if not is_opaque(pixel):
            continue
        opaque_pixels.append(pixel)
    
    # Run Wu's quantization algorithm
    wu_result = quantize_wu(opaque_pixels, max_colors)
    
    # Run WSmeans quantization with Wu's result as starting clusters
    result = quantize_wsmeans(opaque_pixels, wu_result, max_colors)
    
    return result
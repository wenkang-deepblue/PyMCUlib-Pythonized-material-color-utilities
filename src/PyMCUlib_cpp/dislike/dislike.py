# dislike.py

from PyMCUlib_cpp.cam.hct import Hct

def is_disliked(hct: Hct) -> bool:
    """
    Checks whether a color is disliked.
    
    Disliked is defined as a dark yellow-green that is not neutral.
    
    Args:
        hct: The color to be tested.
        
    Returns:
        Whether the color is disliked.
    """
    rounded_hue = round(hct.get_hue())
    
    hue_passes = 90.0 <= rounded_hue <= 111.0
    chroma_passes = round(hct.get_chroma()) > 16.0
    tone_passes = round(hct.get_tone()) < 65.0
    
    return hue_passes and chroma_passes and tone_passes

def fix_if_disliked(hct: Hct) -> Hct:
    """
    If a color is disliked, lightens it to make it likable.
    
    The original color is not modified.
    
    Args:
        hct: The color to be tested (and fixed, if needed).
        
    Returns:
        The original color if it is not disliked; otherwise, the fixed color.
    """
    if is_disliked(hct):
        return Hct.from_hct(hct.get_hue(), hct.get_chroma(), 70.0)
    
    return hct
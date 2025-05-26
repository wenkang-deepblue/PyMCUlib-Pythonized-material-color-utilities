# contrast.py

from PyMCUlib_cpp.utils.utils import y_from_lstar, lstar_from_y

# Given a color and a contrast ratio to reach, the luminance of a color that
# reaches that ratio with the color can be calculated. However, that luminance
# may not contrast as desired, i.e. the contrast ratio of the input color
# and the returned luminance may not reach the contrast ratio asked for.
#
# When the desired contrast ratio and the result contrast ratio differ by
# more than this amount, an error value should be returned, or the method
# should be documented as 'unsafe', meaning, it will return a valid luminance
# but that luminance may not meet the requested contrast ratio.
#
# 0.04 selected because it ensures the resulting ratio rounds to the
# same tenth.
CONTRAST_RATIO_EPSILON = 0.04

# Color spaces that measure luminance, such as Y in XYZ, L* in L*a*b*,
# or T in HCT, are known as perceptual accurate color spaces.
#
# To be displayed, they must gamut map to a "display space", one that has
# a defined limit on the number of colors. Display spaces include sRGB,
# more commonly understood as RGB/HSL/HSV/HSB.
#
# Gamut mapping is undefined and not defined by the color space. Any
# gamut mapping algorithm must choose how to sacrifice accuracy in hue,
# saturation, and/or lightness.
#
# A principled solution is to maintain lightness, thus maintaining
# contrast/a11y, maintain hue, thus maintaining aesthetic intent, and reduce
# chroma until the color is in gamut.
#
# HCT chooses this solution, but, that doesn't mean it will _exactly_ matched
# desired lightness, if only because RGB is quantized: RGB is expressed as
# a set of integers: there may be an RGB color with, for example,
# 47.892 lightness, but not 47.891.
#
# To allow for this inherent incompatibility between perceptually accurate
# color spaces and display color spaces, methods that take a contrast ratio
# and luminance, and return a luminance that reaches that contrast ratio for
# the input luminance, purposefully darken/lighten their result such that
# the desired contrast ratio will be reached even if inaccuracy is introduced.
#
# 0.4 is generous, ex. HCT requires much less delta. It was chosen because
# it provides a rough guarantee that as long as a percetual color space
# gamut maps lightness such that the resulting lightness rounds to the same
# as the requested, the desired contrast ratio will be reached.
LUMINANCE_GAMUT_MAP_TOLERANCE = 0.4

def ratio_of_ys(y1: float, y2: float) -> float:
    """
    Calculate contrast ratio of two Y values.
    
    Args:
        y1: First Y value
        y2: Second Y value
        
    Returns:
        Contrast ratio between y1 and y2
    """
    lighter = max(y1, y2)
    darker = y1 if lighter == y2 else y2
    return (lighter + 5.0) / (darker + 5.0)

def ratio_of_tones(tone_a: float, tone_b: float) -> float:
    """
    Calculate contrast ratio of two tone values.
    
    Args:
        tone_a: First tone value between 0 and 100
        tone_b: Second tone value between 0 and 100
        
    Returns:
        Contrast ratio between tone_a and tone_b
    """
    tone_a = max(0.0, min(100.0, tone_a))
    tone_b = max(0.0, min(100.0, tone_b))
    return ratio_of_ys(y_from_lstar(tone_a), y_from_lstar(tone_b))

def lighter(tone: float, ratio: float) -> float:
    """
    Return a tone >= tone that ensures ratio.
    Return value is between 0 and 100.
    Returns -1 if ratio cannot be achieved with tone.
    
    Args:
        tone: Tone return value must contrast with.
            Range is 0 to 100. Invalid values will result in -1 being returned.
        ratio: Contrast ratio of return value and tone.
            Range is 1 to 21, invalid values have undefined behavior.
            
    Returns:
        A tone value, or -1 if ratio cannot be achieved
    """
    if tone < 0.0 or tone > 100.0:
        return -1.0
    
    dark_y = y_from_lstar(tone)
    light_y = ratio * (dark_y + 5.0) - 5.0
    real_contrast = ratio_of_ys(light_y, dark_y)
    delta = abs(real_contrast - ratio)
    
    if real_contrast < ratio and delta > CONTRAST_RATIO_EPSILON:
        return -1
    
    # ensure gamut mapping, which requires a 'range' on tone, will still result
    # the correct ratio by darkening slightly.
    value = lstar_from_y(light_y) + LUMINANCE_GAMUT_MAP_TOLERANCE
    if value < 0 or value > 100:
        return -1
    
    return value

def darker(tone: float, ratio: float) -> float:
    """
    Return a tone <= tone that ensures ratio.
    Return value is between 0 and 100.
    Returns -1 if ratio cannot be achieved with tone.
    
    Args:
        tone: Tone return value must contrast with.
            Range is 0 to 100. Invalid values will result in -1 being returned.
        ratio: Contrast ratio of return value and tone.
            Range is 1 to 21, invalid values have undefined behavior.
            
    Returns:
        A tone value, or -1 if ratio cannot be achieved
    """
    if tone < 0.0 or tone > 100.0:
        return -1.0
    
    light_y = y_from_lstar(tone)
    dark_y = ((light_y + 5.0) / ratio) - 5.0
    real_contrast = ratio_of_ys(light_y, dark_y)
    
    delta = abs(real_contrast - ratio)
    if real_contrast < ratio and delta > CONTRAST_RATIO_EPSILON:
        return -1
    
    # ensure gamut mapping, which requires a 'range' on tone, will still result
    # the correct ratio by darkening slightly.
    value = lstar_from_y(dark_y) - LUMINANCE_GAMUT_MAP_TOLERANCE
    if value < 0 or value > 100:
        return -1
    
    return value

def lighter_unsafe(tone: float, ratio: float) -> float:
    """
    Return a tone >= tone that ensures ratio.
    Return value is between 0 and 100.
    Returns 100 if ratio cannot be achieved with tone.
    
    This method is unsafe because the returned value is guaranteed to be in
    bounds for tone, i.e. between 0 and 100. However, that value may not reach
    the ratio with tone. For example, there is no color lighter than T100.
    
    Args:
        tone: Tone return value must contrast with.
            Range is 0 to 100. Invalid values will result in 100 being returned.
        ratio: Desired contrast ratio of return value and tone parameter.
            Range is 1 to 21, invalid values have undefined behavior.
            
    Returns:
        A tone value between 0 and 100
    """
    lighter_safe = lighter(tone, ratio)
    return 100.0 if lighter_safe < 0.0 else lighter_safe

def darker_unsafe(tone: float, ratio: float) -> float:
    """
    Return a tone <= tone that ensures ratio.
    Return value is between 0 and 100.
    Returns 0 if ratio cannot be achieved with tone.
    
    This method is unsafe because the returned value is guaranteed to be in
    bounds for tone, i.e. between 0 and 100. However, that value may not reach
    the ratio with tone. For example, there is no color darker than T0.
    
    Args:
        tone: Tone return value must contrast with.
            Range is 0 to 100. Invalid values will result in 0 being returned.
        ratio: Desired contrast ratio of return value and tone parameter.
            Range is 1 to 21, invalid values have undefined behavior.
            
    Returns:
        A tone value between 0 and 100
    """
    darker_safe = darker(tone, ratio)
    return 0.0 if darker_safe < 0.0 else darker_safe
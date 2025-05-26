# score.py

from dataclasses import dataclass
from typing import Dict, List
import math

from PyMCUlib_cpp.utils.utils import sanitize_degrees_int, diff_degrees
from PyMCUlib_cpp.cam.hct import Hct

# Constants
_TARGET_CHROMA = 48.0  # A1 Chroma
_WEIGHT_PROPORTION = 0.7
_WEIGHT_CHROMA_ABOVE = 0.3
_WEIGHT_CHROMA_BELOW = 0.1
_CUTOFF_CHROMA = 5.0
_CUTOFF_EXCITED_PROPORTION = 0.01

@dataclass
class ScoreOptions:
    """
    Default options for ranking colors based on usage counts.
    
    Attributes:
        desired: Max count of the colors returned.
        fallback_color_argb: Default color that should be used if no other colors are suitable.
        filter: Controls if the resulting colors should be filtered to not include
               hues that are not used often enough, and colors that are effectively grayscale.
    """
    desired: int = 4  # 4 colors matches the Android wallpaper picker.
    fallback_color_argb: int = 0xff4285f4  # Google Blue.
    filter: bool = True  # Avoid unsuitable colors.


def ranked_suggestions(argb_to_population: Dict[int, int], options: ScoreOptions = ScoreOptions()) -> List[int]:
    """
    Given a map with keys of colors and values of how often the color appears,
    rank the colors based on suitability for being used for a UI theme.
    
    The list returned is of length <= [desired]. The recommended color is the
    first item, the least suitable is the last. There will always be at least
    one color returned. If all the input colors were not suitable for a theme,
    a default fallback color will be provided, Google Blue, or supplied fallback
    color. The default number of colors returned is 4, simply because that's the
    # of colors display in Android 12's wallpaper picker.
    
    Args:
        argb_to_population: Map of ARGB colors to their population count
        options: Options for ranking colors
        
    Returns:
        A list of ARGB colors ranked by suitability
    """
    # Get the HCT color for each Argb value, while finding the per hue count and
    # total count.
    colors_hct = []
    hue_population = [0] * 360
    population_sum = 0
    
    for argb, population in argb_to_population.items():
        hct = Hct.from_int(argb)
        colors_hct.append(hct)
        
        hue = math.floor(hct.get_hue())
        hue_population[hue] += population
        population_sum += population
    
    # Hues with more usage in neighboring 30 degree slice get a larger number.
    hue_excited_proportions = [0.0] * 360
    for hue in range(360):
        proportion = hue_population[hue] / population_sum if population_sum > 0 else 0
        for i in range(hue - 14, hue + 16):
            neighbor_hue = sanitize_degrees_int(i)
            hue_excited_proportions[neighbor_hue] += proportion
    
    # Scores each HCT color based on usage and chroma, while optionally
    # filtering out values that do not have enough chroma or usage.
    scored_hcts = []
    for hct in colors_hct:
        hue = sanitize_degrees_int(round(hct.get_hue()))
        proportion = hue_excited_proportions[hue]
        
        if options.filter and (hct.get_chroma() < _CUTOFF_CHROMA or
                              proportion <= _CUTOFF_EXCITED_PROPORTION):
            continue
        
        proportion_score = proportion * 100.0 * _WEIGHT_PROPORTION
        chroma_weight = _WEIGHT_CHROMA_BELOW if hct.get_chroma() < _TARGET_CHROMA else _WEIGHT_CHROMA_ABOVE
        chroma_score = (hct.get_chroma() - _TARGET_CHROMA) * chroma_weight
        score = proportion_score + chroma_score
        
        scored_hcts.append((hct, score))
    
    # Sorted so that colors with higher scores come first.
    scored_hcts.sort(key=lambda x: x[1], reverse=True)
    
    # Iterates through potential hue differences in degrees in order to select
    # the colors with the largest distribution of hues possible. Starting at
    # 90 degrees(maximum difference for 4 colors) then decreasing down to a
    # 15 degree minimum.
    chosen_colors = []
    for difference_degrees in range(90, 14, -1):
        chosen_colors = []
        for hct, _ in scored_hcts:
            # Check if this hue is too similar to already chosen hues
            duplicate_hue = False
            for chosen_hct in chosen_colors:
                if diff_degrees(hct.get_hue(), chosen_hct.get_hue()) < difference_degrees:
                    duplicate_hue = True
                    break
            
            if not duplicate_hue:
                chosen_colors.append(hct)
                if len(chosen_colors) >= options.desired:
                    break
        
        if len(chosen_colors) >= options.desired:
            break
    
    colors = []
    if not chosen_colors:
        colors.append(options.fallback_color_argb)
    else:
        for chosen_hct in chosen_colors:
            colors.append(chosen_hct.to_int())
    
    return colors
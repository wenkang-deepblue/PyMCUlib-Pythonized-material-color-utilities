# score/score.py

from typing import List, Mapping, Optional, TypedDict
from PyMCUlib.hct.hct import Hct
from PyMCUlib.utils import math_utils

class ScoreOptions(TypedDict, total=False):
    """
    Default options for ranking colors based on usage counts.
    desired: is the max count of the colors returned.
    fallbackColorARGB: Is the default color that should be used if no
                      other colors are suitable.
    filter: controls if the resulting colors should be filtered to not include
           hues that are not used often enough, and colors that are effectively
           grayscale.
    """
    desired: int
    fallbackColorARGB: int
    filter: bool

SCORE_OPTION_DEFAULTS = {
    "desired": 4,  # 4 colors matches what Android wallpaper picker.
    "fallbackColorARGB": 0xff4285f4,  # Google Blue.
    "filter": True,  # Avoid unsuitable colors.
}

class Score:
    """
    Given a large set of colors, remove colors that are unsuitable for a UI
    theme, and rank the rest based on suitability.
    
    Enables use of a high cluster count for image quantization, thus ensuring
    colors aren't muddied, while curating the high cluster count to a much
    smaller number of appropriate choices.
    """
    
    TARGET_CHROMA = 48.0  # A1 Chroma
    WEIGHT_PROPORTION = 0.7
    WEIGHT_CHROMA_ABOVE = 0.3
    WEIGHT_CHROMA_BELOW = 0.1
    CUTOFF_CHROMA = 5.0
    CUTOFF_EXCITED_PROPORTION = 0.01
    
    def __init__(self):
        """Score cannot be instantiated."""
        raise NotImplementedError("Score cannot be instantiated")
    
    @classmethod
    def score(
        cls,
        colors_to_population: Mapping[int, int],
        options: Optional[ScoreOptions] = None
    ) -> List[int]:
        """
        Given a map with keys of colors and values of how often the color appears,
        rank the colors based on suitability for being used for a UI theme.
        
        Args:
            colors_to_population: map with keys of colors and values of how often
                the color appears, usually from a source image.
            options: optional parameters.
                
        Returns:
            Colors sorted by suitability for a UI theme. The most suitable
            color is the first item, the least suitable is the last. There will
            always be at least one color returned. If all the input colors
            were not suitable for a theme, a default fallback color will be
            provided, Google Blue.
        """
        # Apply default options if not provided
        if options is None:
            options = {}
        opts = {**SCORE_OPTION_DEFAULTS, **options}
        desired = opts["desired"]
        fallback_color_argb = opts["fallbackColorARGB"]
        filter_colors = opts["filter"]
        
        # Get the HCT color for each Argb value, while finding the per hue count and
        # total count.
        colors_hct = []
        hue_population = [0] * 360
        population_sum = 0
        
        for argb, population in colors_to_population.items():
            hct = Hct.from_int(argb)
            colors_hct.append(hct)
            hue = int(hct.hue)
            hue_population[hue] += population
            population_sum += population
        
        # Hues with more usage in neighboring 30 degree slice get a larger number.
        hue_excited_proportions = [0.0] * 360
        for hue in range(360):
            proportion = hue_population[hue] / population_sum if population_sum > 0 else 0
            for i in range(hue - 14, hue + 16):
                neighbor_hue = math_utils.sanitize_degrees_int(i)
                hue_excited_proportions[neighbor_hue] += proportion
        
        # Scores each HCT color based on usage and chroma, while optionally
        # filtering out values that do not have enough chroma or usage.
        scored_hct = []
        for hct in colors_hct:
            hue = math_utils.sanitize_degrees_int(round(hct.hue))
            proportion = hue_excited_proportions[hue]
            if filter_colors and (hct.chroma < cls.CUTOFF_CHROMA or 
                                 proportion <= cls.CUTOFF_EXCITED_PROPORTION):
                continue
            
            proportion_score = proportion * 100.0 * cls.WEIGHT_PROPORTION
            chroma_weight = cls.WEIGHT_CHROMA_BELOW if hct.chroma < cls.TARGET_CHROMA else cls.WEIGHT_CHROMA_ABOVE
            chroma_score = (hct.chroma - cls.TARGET_CHROMA) * chroma_weight
            score = proportion_score + chroma_score
            scored_hct.append({"hct": hct, "score": score})
        
        # Sort so that colors with higher scores come first
        scored_hct.sort(key=lambda x: x["score"], reverse=True)
        
        # Iterates through potential hue differences in degrees in order to select
        # the colors with the largest distribution of hues possible. Starting at
        # 90 degrees(maximum difference for 4 colors) then decreasing down to a
        # 15 degree minimum.
        chosen_colors = []
        for difference_degrees in range(90, 14, -1):
            chosen_colors.clear()
            for entry in scored_hct:
                hct = entry["hct"]
                duplicate_hue = False
                for chosen_hct in chosen_colors:
                    if math_utils.difference_degrees(hct.hue, chosen_hct.hue) < difference_degrees:
                        duplicate_hue = True
                        break
                if not duplicate_hue:
                    chosen_colors.append(hct)
                if len(chosen_colors) >= desired:
                    break
            if len(chosen_colors) >= desired:
                break
        
        colors = []
        if len(chosen_colors) == 0:
            colors.append(fallback_color_argb)
        
        for chosen_hct in chosen_colors:
            colors.append(chosen_hct.to_int())
        
        return colors
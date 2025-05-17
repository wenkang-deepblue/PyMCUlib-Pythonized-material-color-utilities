# dislike/dislike_analyzer.py

"""
Check and/or fix universally disliked colors.
Color science studies of color preference indicate universal distaste for
dark yellow-greens, and also show this is correlated to distate for
biological waste and rotting food.

See Palmer and Schloss, 2010 or Schloss and Palmer's Chapter 21 in Handbook
of Color Psychology (2015).
"""

from PyMCUlib.hct.hct import Hct


class DislikeAnalyzer:
    """
    Check and/or fix universally disliked colors.
    Color science studies of color preference indicate universal distaste for
    dark yellow-greens, and also show this is correlated to distate for
    biological waste and rotting food.

    See Palmer and Schloss, 2010 or Schloss and Palmer's Chapter 21 in Handbook
    of Color Psychology (2015).
    """

    @staticmethod
    def is_disliked(hct: Hct) -> bool:
        """
        Returns true if a color is disliked.

        Args:
            hct: A color to be judged.

        Returns:
            Whether the color is disliked.

        Disliked is defined as a dark yellow-green that is not neutral.
        """
        hue_passes = round(hct.hue) >= 90.0 and round(hct.hue) <= 111.0
        chroma_passes = round(hct.chroma) > 16.0
        tone_passes = round(hct.tone) < 65.0

        return hue_passes and chroma_passes and tone_passes

    @staticmethod
    def fix_if_disliked(hct: Hct) -> Hct:
        """
        If a color is disliked, lighten it to make it likable.

        Args:
            hct: A color to be judged.

        Returns:
            A new color if the original color is disliked, or the original
            color if it is acceptable.
        """
        if DislikeAnalyzer.is_disliked(hct):
            return Hct.from_hct(
                hct.hue,
                hct.chroma,
                70.0,
            )

        return hct
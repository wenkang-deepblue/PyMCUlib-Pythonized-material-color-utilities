# contrast/contrast.py

from PyMCUlib.utils import color_utils
from PyMCUlib.utils import math_utils

class Contrast:
    """
    Utility methods for calculating contrast given two colors, or calculating a
    color given one color and a contrast ratio.

    Contrast ratio is calculated using XYZ's Y. When linearized to match human
    perception, Y becomes HCT's tone and L*a*b*'s' L*. Informally, this is the
    lightness of a color.

    Methods refer to tone, T in the the HCT color space.
    Tone is equivalent to L* in the L*a*b* color space, or L in the LCH color
    space.
    """

    @staticmethod
    def ratio_of_tones(tone_a: float, tone_b: float) -> float:
        """
        Returns a contrast ratio, which ranges from 1 to 21.

        Args:
            tone_a: Tone between 0 and 100. Values outside will be clamped.
            tone_b: Tone between 0 and 100. Values outside will be clamped.

        Returns:
            Contrast ratio between the two tones
        """
        tone_a = math_utils.clamp_double(0.0, 100.0, tone_a)
        tone_b = math_utils.clamp_double(0.0, 100.0, tone_b)
        return Contrast.ratio_of_ys(color_utils.y_from_lstar(tone_a), color_utils.y_from_lstar(tone_b))

    @staticmethod
    def ratio_of_ys(y1: float, y2: float) -> float:
        """
        Calculates the contrast ratio between two luminance values.

        Args:
            y1: First luminance value
            y2: Second luminance value

        Returns:
            Contrast ratio between the two luminance values
        """
        lighter = y1 if y1 > y2 else y2
        darker = y1 if lighter == y2 else y2
        return (lighter + 5.0) / (darker + 5.0)

    @staticmethod
    def lighter(tone: float, ratio: float) -> float:
        """
        Returns a tone >= tone parameter that ensures ratio parameter.
        Return value is between 0 and 100.
        Returns -1 if ratio cannot be achieved with tone parameter.

        Args:
            tone: Tone return value must contrast with.
                Range is 0 to 100. Invalid values will result in -1 being returned.
            ratio: Contrast ratio of return value and tone.
                Range is 1 to 21, invalid values have undefined behavior.

        Returns:
            Tone value that achieves the desired contrast ratio, or -1 if not possible
        """
        if tone < 0.0 or tone > 100.0:
            return -1.0

        dark_y = color_utils.y_from_lstar(tone)
        light_y = ratio * (dark_y + 5.0) - 5.0
        real_contrast = Contrast.ratio_of_ys(light_y, dark_y)
        delta = abs(real_contrast - ratio)
        if real_contrast < ratio and delta > 0.04:
            return -1

        # Ensure gamut mapping, which requires a 'range' on tone, will still result
        # the correct ratio by darkening slightly.
        return_value = color_utils.lstar_from_y(light_y) + 0.4
        if return_value < 0 or return_value > 100:
            return -1
        return return_value

    @staticmethod
    def darker(tone: float, ratio: float) -> float:
        """
        Returns a tone <= tone parameter that ensures ratio parameter.
        Return value is between 0 and 100.
        Returns -1 if ratio cannot be achieved with tone parameter.

        Args:
            tone: Tone return value must contrast with.
                Range is 0 to 100. Invalid values will result in -1 being returned.
            ratio: Contrast ratio of return value and tone.
                Range is 1 to 21, invalid values have undefined behavior.

        Returns:
            Tone value that achieves the desired contrast ratio, or -1 if not possible
        """
        if tone < 0.0 or tone > 100.0:
            return -1.0

        light_y = color_utils.y_from_lstar(tone)
        dark_y = ((light_y + 5.0) / ratio) - 5.0
        real_contrast = Contrast.ratio_of_ys(light_y, dark_y)

        delta = abs(real_contrast - ratio)
        if real_contrast < ratio and delta > 0.04:
            return -1

        # Ensure gamut mapping, which requires a 'range' on tone, will still result
        # the correct ratio by darkening slightly.
        return_value = color_utils.lstar_from_y(dark_y) - 0.4
        if return_value < 0 or return_value > 100:
            return -1
        return return_value

    @staticmethod
    def lighter_unsafe(tone: float, ratio: float) -> float:
        """
        Returns a tone >= tone parameter that ensures ratio parameter.
        Return value is between 0 and 100.
        Returns 100 if ratio cannot be achieved with tone parameter.

        This method is unsafe because the returned value is guaranteed to be in
        bounds for tone, i.e. between 0 and 100. However, that value may not reach
        the ratio with tone. For example, there is no color lighter than T100.

        Args:
            tone: Tone return value must contrast with.
                Range is 0 to 100. Invalid values will result in 100 being returned.
            ratio: Desired contrast ratio of return value and tone parameter.
                Range is 1 to 21, invalid values have undefined behavior.

        Returns:
            Tone value that achieves the desired contrast ratio, or 100 if not possible
        """
        lighter_safe = Contrast.lighter(tone, ratio)
        return 100.0 if lighter_safe < 0.0 else lighter_safe

    @staticmethod
    def darker_unsafe(tone: float, ratio: float) -> float:
        """
        Returns a tone <= tone parameter that ensures ratio parameter.
        Return value is between 0 and 100.
        Returns 0 if ratio cannot be achieved with tone parameter.

        This method is unsafe because the returned value is guaranteed to be in
        bounds for tone, i.e. between 0 and 100. However, that value may not reach
        the ratio with tone. For example, there is no color darker than T0.

        Args:
            tone: Tone return value must contrast with.
                Range is 0 to 100. Invalid values will result in 0 being returned.
            ratio: Desired contrast ratio of return value and tone parameter.
                Range is 1 to 21, invalid values have undefined behavior.

        Returns:
            Tone value that achieves the desired contrast ratio, or 0 if not possible
        """
        darker_safe = Contrast.darker(tone, ratio)
        return 0.0 if darker_safe < 0.0 else darker_safe
# dynamic_color.py

from typing import Callable, Optional, TypeVar
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.palettes.tones import TonalPalette
from PyMCUlib_cpp.utils.utils import Argb
from PyMCUlib_cpp.contrast.contrast import (
    ratio_of_tones, lighter_unsafe, darker_unsafe,
    lighter, darker
)
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib_cpp.dynamiccolor.contrast_curve import ContrastCurve
from PyMCUlib_cpp.dynamiccolor.tone_delta_pair import ToneDeltaPair, TonePolarity

T = TypeVar('T')
U = TypeVar('U')

def foreground_tone(bg_tone: float, ratio: float) -> float:
    """
    Given a background tone, find a foreground tone, while ensuring they reach
    a contrast ratio that is as close to [ratio] as possible.

    Args:
        bg_tone: Tone in HCT. Range is 0 to 100, undefined behavior when it falls
            outside that range.
        ratio: The contrast ratio desired between [bg_tone] and the return value.

    Returns:
        A tone (0-100) that provides the desired contrast ratio with bg_tone.
    """
    lighter_tone = lighter_unsafe(bg_tone, ratio)
    darker_tone = darker_unsafe(bg_tone, ratio)
    lighter_ratio = ratio_of_tones(lighter_tone, bg_tone)
    darker_ratio = ratio_of_tones(darker_tone, bg_tone)
    prefer_lighter = tone_prefers_light_foreground(bg_tone)

    if prefer_lighter:
        negligible_difference = (
            abs(lighter_ratio - darker_ratio) < 0.1 and 
            lighter_ratio < ratio and 
            darker_ratio < ratio
        )
        return (lighter_tone if lighter_ratio >= ratio or 
                lighter_ratio >= darker_ratio or 
                negligible_difference else darker_tone)
    else:
        return (darker_tone if darker_ratio >= ratio or 
                darker_ratio >= lighter_ratio else lighter_tone)

def enable_light_foreground(tone: float) -> float:
    """
    Adjust a tone such that white has 4.5 contrast, if the tone is
    reasonably close to supporting it.

    Args:
        tone: Input tone

    Returns:
        Adjusted tone
    """
    if tone_prefers_light_foreground(tone) and not tone_allows_light_foreground(tone):
        return 49.0
    return tone

def tone_prefers_light_foreground(tone: float) -> bool:
    """
    Returns whether [tone] prefers a light foreground.

    People prefer white foregrounds on ~T60-70. Observed over time, and also
    by Andrew Somers during research for APCA.

    T60 used as to create the smallest discontinuity possible when skipping
    down to T49 in order to ensure light foregrounds.

    Since `tertiaryContainer` in dark monochrome scheme requires a tone of
    60, it should not be adjusted. Therefore, 60 is excluded here.

    Args:
        tone: The tone to test

    Returns:
        Whether the tone prefers a light foreground
    """
    return round(tone) < 60

def tone_allows_light_foreground(tone: float) -> bool:
    """
    Returns whether [tone] can reach a contrast ratio of 4.5 with a lighter
    color.

    Args:
        tone: The tone to test

    Returns:
        Whether the tone allows a light foreground
    """
    return round(tone) <= 49

def _safe_call(
        f: Optional[Callable[[T], Optional[U]]], x: T
) -> Optional[U]:
    """Helper for safely calling an optional function that may return an optional value."""
    if f is None:
        return None
    else:
        return f(x)

def _safe_call_clean_result(
        f: Optional[Callable[[T], U]], x: T
) -> Optional[U]:
    """Helper for safely calling an optional function."""
    if f is None:
        return None
    else:
        return f(x)

class DynamicColor:
    """
    A color that adjusts itself based on UI state, such as dark theme.
    
    Attributes:
        name: The name of the dynamic color.
        palette: Function that provides a TonalPalette given
            DynamicScheme. A TonalPalette is defined by a hue and chroma, so this
            replaces the need to specify hue/chroma. By providing a tonal palette, when
            contrast adjustments are made, intended chroma can be preserved.
        tone: Function that provides a tone given DynamicScheme.
        is_background: Whether this dynamic color is a background, with
            some other color as the foreground.
        background: The background of the dynamic color (as a function of a
            `DynamicScheme`), if it exists.
        second_background: A second background of the dynamic color (as a
            function of a `DynamicScheme`), if it exists.
        contrast_curve: A `ContrastCurve` object specifying how its contrast
            against its background should behave in various contrast levels options.
        tone_delta_pair: A `ToneDeltaPair` object specifying a tone delta
            constraint between two colors. One of them must be the color being
            constructed.
    """

    @staticmethod
    def from_palette(
            name: str,
            palette: Callable[[DynamicScheme], TonalPalette],
            tone: Callable[[DynamicScheme], float]
    ) -> 'DynamicColor':
        """
        A convenience constructor, only requiring name, palette, and tone.
        
        Args:
            name: The name of the dynamic color
            palette: Function providing a tonal palette based on a scheme
            tone: Function providing a tone based on a scheme
            
        Returns:
            A new DynamicColor instance
        """
        return DynamicColor(
            name=name,
            palette=palette,
            tone=tone,
            is_background=False,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None
        )

    def __init__(
            self,
            name: str,
            palette: Callable[[DynamicScheme], TonalPalette],
            tone: Callable[[DynamicScheme], float],
            is_background: bool,
            background: Optional[Callable[[DynamicScheme], 'DynamicColor']],
            second_background: Optional[Callable[[DynamicScheme], 'DynamicColor']],
            contrast_curve: Optional[ContrastCurve],
            tone_delta_pair: Optional[Callable[[DynamicScheme], ToneDeltaPair]]
    ):
        """
        The default constructor.
        
        Args:
            name: The name of the dynamic color.
            palette: Function that provides a TonalPalette given DynamicScheme.
            tone: Function that provides a tone given DynamicScheme.
            is_background: Whether this is a background color.
            background: The background of this color, if it exists.
            second_background: The second background of this color, if it exists.
            contrast_curve: The contrast curve for this color.
            tone_delta_pair: The tone delta pair for this color.
        """
        self.name = name
        self.palette = palette
        self.tone = tone
        self.is_background = is_background
        self.background = background
        self.second_background = second_background
        self.contrast_curve = contrast_curve
        self.tone_delta_pair = tone_delta_pair

    def get_argb(self, scheme: DynamicScheme) -> Argb:
        """
        Returns the ARGB representation of this color in the given scheme.
        
        Args:
            scheme: The scheme to use for resolving the color
            
        Returns:
            ARGB representation of the color
        """
        return self.palette(scheme).get(self.get_tone(scheme))

    def get_hct(self, scheme: DynamicScheme) -> Hct:
        """
        Returns the HCT representation of this color in the given scheme.
        
        Args:
            scheme: The scheme to use for resolving the color
            
        Returns:
            HCT representation of the color
        """
        return Hct.from_int(self.get_argb(scheme))

    def get_tone(self, scheme: DynamicScheme) -> float:
        """
        Returns the tone of this color in the given scheme.
        
        Args:
            scheme: The scheme to use for resolving the tone
            
        Returns:
            Tone value
        """
        decreasing_contrast = scheme.contrast_level < 0

        # Case 1: dual foreground, pair of colors with delta constraint.
        if self.tone_delta_pair is not None:
            tone_delta_pair = self.tone_delta_pair(scheme)
            role_a = tone_delta_pair.role_a
            role_b = tone_delta_pair.role_b
            delta = tone_delta_pair.delta
            polarity = tone_delta_pair.polarity
            stay_together = tone_delta_pair.stay_together

            bg = self.background(scheme)
            bg_tone = bg.get_tone(scheme)

            a_is_nearer = (
                polarity == TonePolarity.NEARER or
                (polarity == TonePolarity.LIGHTER and not scheme.is_dark) or
                (polarity == TonePolarity.DARKER and scheme.is_dark)
            )
            nearer = role_a if a_is_nearer else role_b
            farther = role_b if a_is_nearer else role_a
            am_nearer = self.name == nearer.name
            expansion_dir = 1 if scheme.is_dark else -1

            # 1st round: solve to min, each
            n_contrast = nearer.contrast_curve.get(scheme.contrast_level)
            f_contrast = farther.contrast_curve.get(scheme.contrast_level)

            # If a color is good enough, it is not adjusted.
            # Initial and adjusted tones for `nearer`
            n_initial_tone = nearer.tone(scheme)
            n_tone = (n_initial_tone if ratio_of_tones(bg_tone, n_initial_tone) >= n_contrast
                     else foreground_tone(bg_tone, n_contrast))

            # Initial and adjusted tones for `farther`
            f_initial_tone = farther.tone(scheme)
            f_tone = (f_initial_tone if ratio_of_tones(bg_tone, f_initial_tone) >= f_contrast
                     else foreground_tone(bg_tone, f_contrast))

            if decreasing_contrast:
                # If decreasing contrast, adjust color to the "bare minimum"
                # that satisfies contrast.
                n_tone = foreground_tone(bg_tone, n_contrast)
                f_tone = foreground_tone(bg_tone, f_contrast)

            if (f_tone - n_tone) * expansion_dir >= delta:
                # Good! Tones satisfy the constraint; no change needed.
                pass
            else:
                # 2nd round: expand farther to match delta.
                f_tone = max(0.0, min(100.0, n_tone + delta * expansion_dir))
                if (f_tone - n_tone) * expansion_dir >= delta:
                    # Good! Tones now satisfy the constraint; no change needed.
                    pass
                else:
                    # 3rd round: contract nearer to match delta.
                    n_tone = max(0.0, min(100.0, f_tone - delta * expansion_dir))

            # Avoids the 50-59 awkward zone.
            if 50 <= n_tone < 60:
                # If `nearer` is in the awkward zone, move it away, together with
                # `farther`.
                if expansion_dir > 0:
                    n_tone = 60
                    f_tone = max(f_tone, n_tone + delta * expansion_dir)
                else:
                    n_tone = 49
                    f_tone = min(f_tone, n_tone + delta * expansion_dir)
            elif 50 <= f_tone < 60:
                if stay_together:
                    # Fixes both, to avoid two colors on opposite sides of the "awkward
                    # zone".
                    if expansion_dir > 0:
                        n_tone = 60
                        f_tone = max(f_tone, n_tone + delta * expansion_dir)
                    else:
                        n_tone = 49
                        f_tone = min(f_tone, n_tone + delta * expansion_dir)
                else:
                    # Not required to stay together; fixes just one.
                    if expansion_dir > 0:
                        f_tone = 60
                    else:
                        f_tone = 49

            # Returns `n_tone` if this color is `nearer`, otherwise `f_tone`.
            return n_tone if am_nearer else f_tone
        else:
            # Case 2: No contrast pair; just solve for itself.
            answer = self.tone(scheme)

            if self.background is None:
                return answer  # No adjustment for colors with no background.

            bg_tone = self.background(scheme).get_tone(scheme)
            desired_ratio = self.contrast_curve.get(scheme.contrast_level)

            if ratio_of_tones(bg_tone, answer) >= desired_ratio:
                # Don't "improve" what's good enough.
                pass
            else:
                # Rough improvement.
                answer = foreground_tone(bg_tone, desired_ratio)

            if decreasing_contrast:
                answer = foreground_tone(bg_tone, desired_ratio)

            if self.is_background and 50 <= answer < 60:
                # Must adjust
                if ratio_of_tones(49, bg_tone) >= desired_ratio:
                    answer = 49
                else:
                    answer = 60

            if self.second_background is not None:
                # Case 3: Adjust for dual backgrounds.
                bg_tone_1 = self.background(scheme).get_tone(scheme)
                bg_tone_2 = self.second_background(scheme).get_tone(scheme)

                upper = max(bg_tone_1, bg_tone_2)
                lower = min(bg_tone_1, bg_tone_2)

                if (ratio_of_tones(upper, answer) >= desired_ratio and
                    ratio_of_tones(lower, answer) >= desired_ratio):
                    return answer

                # The darkest light tone that satisfies the desired ratio,
                # or -1 if such ratio cannot be reached.
                light_option = lighter(upper, desired_ratio)

                # The lightest dark tone that satisfies the desired ratio,
                # or -1 if such ratio cannot be reached.
                dark_option = darker(lower, desired_ratio)

                # Tones suitable for the foreground.
                availables = []
                if light_option != -1:
                    availables.append(light_option)
                if dark_option != -1:
                    availables.append(dark_option)

                prefers_light = (tone_prefers_light_foreground(bg_tone_1) or
                                tone_prefers_light_foreground(bg_tone_2))
                if prefers_light:
                    return 100 if light_option < 0 else light_option
                if len(availables) == 1:
                    return availables[0]
                return 0 if dark_option < 0 else dark_option

            return answer
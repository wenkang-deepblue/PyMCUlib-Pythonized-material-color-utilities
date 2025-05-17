# dynamiccolor/dynamic_color.py

from __future__ import annotations
from typing import Callable, Dict, Optional, Protocol, TypedDict, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from .dynamic_scheme import DynamicScheme

from PyMCUlib.dynamiccolor.color_spec_delegate import SpecVersion
from PyMCUlib.dynamiccolor.contrast_curve import ContrastCurve
from PyMCUlib.dynamiccolor.tone_delta_pair import ToneDeltaPair
from PyMCUlib.contrast.contrast import Contrast
from PyMCUlib.hct.hct import Hct
from PyMCUlib.palettes.tonal_palette import TonalPalette
from PyMCUlib.utils import math_utils


class FromPaletteOptions(TypedDict, total=False):
    """
    Options for creating a DynamicColor from a palette.
    
    Args:
        name: The name of the dynamic color. Defaults to empty.
        palette: Function that provides a TonalPalette given DynamicScheme.
        tone: Function that provides a tone given DynamicScheme.
        chroma_multiplier: A factor that multiplies the chroma for this color.
        is_background: Whether this dynamic color is a background, with some other color as the foreground.
        background: The background of the dynamic color (as a function of a DynamicScheme), if it exists.
        second_background: A second background of the dynamic color (as a function of a DynamicScheme), if it exists.
        contrast_curve: A ContrastCurve object specifying how its contrast against its background should behave.
        tone_delta_pair: A ToneDeltaPair object specifying a tone delta constraint between two colors.
    """
    name: str
    palette: Callable[["DynamicScheme"], TonalPalette]
    tone: Callable[["DynamicScheme"], float]
    chroma_multiplier: Callable[["DynamicScheme"], float]
    is_background: bool
    background: Callable[["DynamicScheme"], Optional[DynamicColor]]
    second_background: Callable[["DynamicScheme"], Optional[DynamicColor]]
    contrast_curve: Callable[["DynamicScheme"], Optional[ContrastCurve]]
    tone_delta_pair: Callable[["DynamicScheme"], Optional[ToneDeltaPair]]


class ColorCalculationDelegate(Protocol):
    """
    A delegate that provides the HCT and tone of a DynamicColor.

    This is used to allow different implementations of the color calculation
    logic for different spec versions.
    """
    def get_hct(self, scheme: "DynamicScheme", color: DynamicColor) -> Hct:
        ...

    def get_tone(self, scheme: "DynamicScheme", color: DynamicColor) -> float:
        ...


def validate_extended_color(
        original_color: DynamicColor, spec_version: SpecVersion,
        extended_color: DynamicColor) -> None:
    """
    Validates that an extended color is compatible with the original color.
    
    Args:
        original_color: The original color.
        spec_version: The spec version to extend.
        extended_color: The color with the values to extend.
        
    Raises:
        ValueError: If the extended color is not compatible with the original color.
    """
    if original_color.name != extended_color.name:
        raise ValueError(
            f"Attempting to extend color {original_color.name} with color "
            f"{extended_color.name} of different name for spec version {spec_version}.")
    
    if original_color.is_background != extended_color.is_background:
        raise ValueError(
            f"Attempting to extend color {original_color.name} as a "
            f"{'background' if original_color.is_background else 'foreground'} with color "
            f"{extended_color.name} as a "
            f"{'background' if extended_color.is_background else 'foreground'} "
            f"for spec version {spec_version}.")


def extend_spec_version(
        original_color: DynamicColor, spec_version: SpecVersion,
        extended_color: DynamicColor) -> DynamicColor:
    """
    Returns a new DynamicColor that is the same as the original color, but with
    the extended dynamic color's constraints for the given spec version.

    Args:
        original_color: The original color.
        spec_version: The spec version to extend.
        extended_color: The color with the values to extend.
        
    Returns:
        A new DynamicColor that extends the original color.
    """
    validate_extended_color(original_color, spec_version, extended_color)

    return DynamicColor.from_palette({
        'name': original_color.name,
        'palette': lambda s: extended_color.palette(s) if s.spec_version == spec_version else original_color.palette(s),
        'tone': lambda s: extended_color.tone(s) if s.spec_version == spec_version else original_color.tone(s),
        'is_background': original_color.is_background,
        'chroma_multiplier': lambda s: (
            (extended_color.chroma_multiplier(s) if extended_color.chroma_multiplier is not None else 1)
            if s.spec_version == spec_version else
            (original_color.chroma_multiplier(s) if original_color.chroma_multiplier is not None else 1)
        ),
        'background': lambda s: (
            (extended_color.background(s) if extended_color.background is not None else None)
            if s.spec_version == spec_version else
            (original_color.background(s) if original_color.background is not None else None)
        ),
        'second_background': lambda s: (
            (extended_color.second_background(s) if extended_color.second_background is not None else None)
            if s.spec_version == spec_version else
            (original_color.second_background(s) if original_color.second_background is not None else None)
        ),
        'contrast_curve': lambda s: (
            (extended_color.contrast_curve(s) if extended_color.contrast_curve is not None else None)
            if s.spec_version == spec_version else
            (original_color.contrast_curve(s) if original_color.contrast_curve is not None else None)
        ),
        'tone_delta_pair': lambda s: (
            (extended_color.tone_delta_pair(s) if extended_color.tone_delta_pair is not None else None)
            if s.spec_version == spec_version else
            (original_color.tone_delta_pair(s) if original_color.tone_delta_pair is not None else None)
        ),
    })


class DynamicColor:
    """
    A color that adjusts itself based on UI state provided by DynamicScheme.

    Colors without backgrounds do not change tone when contrast changes. Colors
    with backgrounds become closer to their background as contrast lowers, and
    further when contrast increases.

    Prefer static constructors. They require either a hexcode, a palette and
    tone, or a hue and chroma. Optionally, they can provide a background
    DynamicColor.
    """

    @staticmethod
    def from_palette(args: FromPaletteOptions) -> DynamicColor:
        """
        Create a DynamicColor defined by a TonalPalette and HCT tone.

        Args:
            args: Functions with DynamicScheme as input. Must provide a palette
                and tone. May provide a background DynamicColor and ToneDeltaPair.
                
        Returns:
            A new DynamicColor instance.
        """
        return DynamicColor(
            args.get('name', ''),
            args['palette'],
            args.get('tone', DynamicColor.get_initial_tone_from_background(args.get('background'))),
            args.get('is_background', False),
            args.get('chroma_multiplier'),
            args.get('background'),
            args.get('second_background'),
            args.get('contrast_curve'),
            args.get('tone_delta_pair'),
        )

    @staticmethod
    def get_initial_tone_from_background(
            background: Optional[Callable[["DynamicScheme"], Optional[DynamicColor]]]) -> Callable[["DynamicScheme"], float]:
        """
        Gets the initial tone from a background function.
        
        Args:
            background: A function that returns a background color given a DynamicScheme.
            
        Returns:
            A function that returns the initial tone.
        """
        if background is None:
            return lambda s: 50.0
        
        return lambda s: background(s).get_tone(s) if background(s) else 50.0

    def __init__(
            self,
            name: str,
            palette: Callable[["DynamicScheme"], TonalPalette],
            tone: Callable[["DynamicScheme"], float],
            is_background: bool,
            chroma_multiplier: Optional[Callable[["DynamicScheme"], float]] = None,
            background: Optional[Callable[["DynamicScheme"], Optional[DynamicColor]]] = None,
            second_background: Optional[Callable[["DynamicScheme"], Optional[DynamicColor]]] = None,
            contrast_curve: Optional[Callable[["DynamicScheme"], Optional[ContrastCurve]]] = None,
            tone_delta_pair: Optional[Callable[["DynamicScheme"], Optional[ToneDeltaPair]]] = None,
    ):
        """
        The base constructor for DynamicColor.

        Strongly prefer using one of the convenience constructors. This class is
        arguably too flexible to ensure it can support any scenario. Functional
        arguments allow overriding without risks that come with subclasses.

        For example, the default behavior of adjust tone at max contrast
        to be at a 7.0 ratio with its background is principled and
        matches accessibility guidance. That does not mean it's the desired
        approach for every design system, and every color pairing,
        always, in every case.

        Args:
            name: The name of the dynamic color. Defaults to empty.
            palette: Function that provides a TonalPalette given DynamicScheme.
            tone: Function that provides a tone, given a DynamicScheme.
            is_background: Whether this dynamic color is a background, with some
                other color as the foreground.
            chroma_multiplier: A factor that multiplies the chroma for this color.
            background: The background of the dynamic color (as a function of a
                DynamicScheme), if it exists.
            second_background: A second background of the dynamic color (as a
                function of a DynamicScheme), if it exists.
            contrast_curve: A ContrastCurve object specifying how its contrast
                against its background should behave.
            tone_delta_pair: A ToneDeltaPair object specifying a tone delta
                constraint between two colors.
        """
        self.name = name
        self.palette = palette
        self.tone = tone
        self.is_background = is_background
        self.chroma_multiplier = chroma_multiplier
        self.background = background
        self.second_background = second_background
        self.contrast_curve = contrast_curve
        self.tone_delta_pair = tone_delta_pair
        self.hct_cache: Dict["DynamicScheme", Hct] = {}
        
        if (not background) and second_background:
            raise ValueError(
                f"Color {name} has second_background defined, but background is not defined.")
        
        if (not background) and contrast_curve:
            raise ValueError(
                f"Color {name} has contrast_curve defined, but background is not defined.")
        
        if background and not contrast_curve:
            raise ValueError(
                f"Color {name} has background defined, but contrast_curve is not defined.")

    def clone(self) -> DynamicColor:
        """
        Returns a deep copy of this DynamicColor.
        
        Returns:
            A new DynamicColor instance with the same properties.
        """
        return DynamicColor.from_palette({
            'name': self.name,
            'palette': self.palette,
            'tone': self.tone,
            'is_background': self.is_background,
            'chroma_multiplier': self.chroma_multiplier,
            'background': self.background,
            'second_background': self.second_background,
            'contrast_curve': self.contrast_curve,
            'tone_delta_pair': self.tone_delta_pair,
        })

    def clear_cache(self) -> None:
        """
        Clears the cache of HCT values for this color. For testing or debugging
        purposes.
        """
        self.hct_cache.clear()

    def get_argb(self, scheme: "DynamicScheme") -> int:
        """
        Returns a ARGB integer (i.e. a hex code).

        Args:
            scheme: Defines the conditions of the user interface, for example,
                whether or not it is dark mode or light mode, and what the desired
                contrast level is.
                
        Returns:
            An ARGB color as an integer.
        """
        return self.get_hct(scheme).to_int()

    def get_hct(self, scheme: "DynamicScheme") -> Hct:
        """
        Returns a color, expressed in the HCT color space, that this
        DynamicColor is under the conditions in scheme.

        Args:
            scheme: Defines the conditions of the user interface, for example,
                whether or not it is dark mode or light mode, and what the desired
                contrast level is.
                
        Returns:
            An HCT color.
        """
        cached_answer = self.hct_cache.get(scheme)
        if cached_answer is not None:
            return cached_answer
        
        answer = get_spec(scheme.spec_version).get_hct(scheme, self)
        
        if len(self.hct_cache) > 4:
            self.hct_cache.clear()
        
        self.hct_cache[scheme] = answer
        return answer

    def get_tone(self, scheme: "DynamicScheme") -> float:
        """
        Returns a tone, T in the HCT color space, that this DynamicColor is under
        the conditions in scheme.

        Args:
            scheme: Defines the conditions of the user interface, for example,
                whether or not it is dark mode or light mode, and what the desired
                contrast level is.
                
        Returns:
            A tone value between 0 and 100.
        """
        return get_spec(scheme.spec_version).get_tone(scheme, self)

    @staticmethod
    def foreground_tone(bg_tone: float, ratio: float) -> float:
        """
        Given a background tone, finds a foreground tone, while ensuring they reach
        a contrast ratio that is as close to [ratio] as possible.

        Args:
            bg_tone: Tone in HCT. Range is 0 to 100, undefined behavior when it
                falls outside that range.
            ratio: The contrast ratio desired between bgTone and the return
                value.
                
        Returns:
            A tone value between 0 and 100.
        """
        lighter_tone = Contrast.lighter_unsafe(bg_tone, ratio)
        darker_tone = Contrast.darker_unsafe(bg_tone, ratio)
        lighter_ratio = Contrast.ratio_of_tones(lighter_tone, bg_tone)
        darker_ratio = Contrast.ratio_of_tones(darker_tone, bg_tone)
        prefer_lighter = DynamicColor.tone_prefers_light_foreground(bg_tone)

        if prefer_lighter:
            # This handles an edge case where the initial contrast ratio is high
            # (ex. 13.0), and the ratio passed to the function is that high
            # ratio, and both the lighter and darker ratio fails to pass that
            # ratio.
            #
            # This was observed with Tonal Spot's On Primary Container turning
            # black momentarily between high and max contrast in light mode. PC's
            # standard tone was T90, OPC's was T10, it was light mode, and the
            # contrast value was 0.6568521221032331.
            negligible_difference = (abs(lighter_ratio - darker_ratio) < 0.1 and
                                    lighter_ratio < ratio and darker_ratio < ratio)
            return (lighter_tone if (lighter_ratio >= ratio or 
                                    lighter_ratio >= darker_ratio or 
                                    negligible_difference) 
                    else darker_tone)
        else:
            return darker_tone if (darker_ratio >= ratio or darker_ratio >= lighter_ratio) else lighter_tone

    @staticmethod
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
            tone: A tone value between 0 and 100.
            
        Returns:
            True if the tone prefers a light foreground, False otherwise.
        """
        return math.floor(tone + 0.5) < 60.0

    @staticmethod
    def tone_allows_light_foreground(tone: float) -> bool:
        """
        Returns whether [tone] can reach a contrast ratio of 4.5 with a lighter
        color.
        
        Args:
            tone: A tone value between 0 and 100.
            
        Returns:
            True if the tone allows a light foreground, False otherwise.
        """
        return math.floor(tone + 0.5) <= 49.0

    @staticmethod
    def enable_light_foreground(tone: float) -> float:
        """
        Adjusts a tone such that white has 4.5 contrast, if the tone is
        reasonably close to supporting it.
        
        Args:
            tone: A tone value between 0 and 100.
            
        Returns:
            An adjusted tone value between 0 and 100.
        """
        if (DynamicColor.tone_prefers_light_foreground(tone) and
                not DynamicColor.tone_allows_light_foreground(tone)):
            return 49.0
        return tone


class ColorCalculationDelegateImpl2021(ColorCalculationDelegate):
    """
    A delegate for the color calculation of a DynamicScheme in the 2021 spec.
    """

    def get_hct(self, scheme: "DynamicScheme", color: DynamicColor) -> Hct:
        """
        Get the HCT color for the given scheme and color.
        
        Args:
            scheme: The dynamic scheme.
            color: The dynamic color.
            
        Returns:
            An HCT color.
        """
        tone = color.get_tone(scheme)
        palette = color.palette(scheme)
        return palette.get_hct(tone)

    def get_tone(self, scheme: "DynamicScheme", color: DynamicColor) -> float:
        """
        Get the tone for the given scheme and color.
        
        Args:
            scheme: The dynamic scheme.
            color: The dynamic color.
            
        Returns:
            A tone value between 0 and 100.
        """
        decreasing_contrast = scheme.contrast_level < 0
        tone_delta_pair = color.tone_delta_pair(scheme) if color.tone_delta_pair else None

        # Case 1: dual foreground, pair of colors with delta constraint.
        if tone_delta_pair:
            role_a = tone_delta_pair.role_a
            role_b = tone_delta_pair.role_b
            delta = tone_delta_pair.delta
            polarity = tone_delta_pair.polarity
            stay_together = tone_delta_pair.stay_together

            a_is_nearer = (polarity == 'nearer' or
                          (polarity == 'lighter' and not scheme.is_dark) or
                          (polarity == 'darker' and scheme.is_dark))
            nearer = role_a if a_is_nearer else role_b
            farther = role_b if a_is_nearer else role_a
            am_nearer = color.name == nearer.name
            expansion_dir = 1 if scheme.is_dark else -1
            n_tone = nearer.tone(scheme)
            f_tone = farther.tone(scheme)

            # 1st round: solve to min for each, if background and contrast curve
            # are defined.
            if color.background and nearer.contrast_curve and farther.contrast_curve:
                bg = color.background(scheme)
                n_contrast_curve = nearer.contrast_curve(scheme)
                f_contrast_curve = farther.contrast_curve(scheme)
                if bg and n_contrast_curve and f_contrast_curve:
                    bg_tone = bg.get_tone(scheme)
                    n_contrast = n_contrast_curve.get(scheme.contrast_level)
                    f_contrast = f_contrast_curve.get(scheme.contrast_level)
                    # If a color is good enough, it is not adjusted.
                    # Initial and adjusted tones for `nearer`
                    if Contrast.ratio_of_tones(bg_tone, n_tone) < n_contrast:
                        n_tone = DynamicColor.foreground_tone(bg_tone, n_contrast)
                    # Initial and adjusted tones for `farther`
                    if Contrast.ratio_of_tones(bg_tone, f_tone) < f_contrast:
                        f_tone = DynamicColor.foreground_tone(bg_tone, f_contrast)
                    if decreasing_contrast:
                        # If decreasing contrast, adjust color to the "bare minimum"
                        # that satisfies contrast.
                        n_tone = DynamicColor.foreground_tone(bg_tone, n_contrast)
                        f_tone = DynamicColor.foreground_tone(bg_tone, f_contrast)

            if (f_tone - n_tone) * expansion_dir < delta:
                # 2nd round: expand farther to match delta, if contrast is not
                # satisfied.
                f_tone = math_utils.clamp_double(0, 100, n_tone + delta * expansion_dir)
                if (f_tone - n_tone) * expansion_dir >= delta:
                    # Good! Tones now satisfy the constraint; no change needed.
                    pass
                else:
                    # 3rd round: contract nearer to match delta.
                    n_tone = math_utils.clamp_double(0, 100, f_tone - delta * expansion_dir)

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
            answer = color.tone(scheme)

            if (color.background is None or
                    color.background(scheme) is None or
                    color.contrast_curve is None or
                    color.contrast_curve(scheme) is None):
                return answer  # No adjustment for colors with no background.

            bg_tone = color.background(scheme).get_tone(scheme)
            desired_ratio = color.contrast_curve(scheme).get(scheme.contrast_level)

            if Contrast.ratio_of_tones(bg_tone, answer) >= desired_ratio:
                # Don't "improve" what's good enough.
                pass
            else:
                # Rough improvement.
                answer = DynamicColor.foreground_tone(bg_tone, desired_ratio)

            if decreasing_contrast:
                answer = DynamicColor.foreground_tone(bg_tone, desired_ratio)

            if color.is_background and 50 <= answer < 60:
                # Must adjust
                if Contrast.ratio_of_tones(49, bg_tone) >= desired_ratio:
                    answer = 49
                else:
                    answer = 60

            if (color.second_background is None or
                    color.second_background(scheme) is None):
                return answer

            # Case 3: Adjust for dual backgrounds.
            bg1, bg2 = color.background, color.second_background
            bg_tone1, bg_tone2 = bg1(scheme).get_tone(scheme), bg2(scheme).get_tone(scheme)
            upper, lower = max(bg_tone1, bg_tone2), min(bg_tone1, bg_tone2)

            if (Contrast.ratio_of_tones(upper, answer) >= desired_ratio and
                    Contrast.ratio_of_tones(lower, answer) >= desired_ratio):
                return answer

            # The darkest light tone that satisfies the desired ratio,
            # or -1 if such ratio cannot be reached.
            light_option = Contrast.lighter(upper, desired_ratio)

            # The lightest dark tone that satisfies the desired ratio,
            # or -1 if such ratio cannot be reached.
            dark_option = Contrast.darker(lower, desired_ratio)

            # Tones suitable for the foreground.
            availables = []
            if light_option != -1:
                availables.append(light_option)
            if dark_option != -1:
                availables.append(dark_option)

            prefers_light = (DynamicColor.tone_prefers_light_foreground(bg_tone1) or
                            DynamicColor.tone_prefers_light_foreground(bg_tone2))
            if prefers_light:
                return 100 if light_option < 0 else light_option
            if len(availables) == 1:
                return availables[0]
            return 0 if dark_option < 0 else dark_option


class ColorCalculationDelegateImpl2025(ColorCalculationDelegate):
    """
    A delegate for the color calculation of a DynamicScheme in the 2025 spec.
    """

    def get_hct(self, scheme: "DynamicScheme", color: DynamicColor) -> Hct:
        """
        Get the HCT color for the given scheme and color.
        
        Args:
            scheme: The dynamic scheme.
            color: The dynamic color.
            
        Returns:
            An HCT color.
        """
        palette = color.palette(scheme)
        tone = color.get_tone(scheme)
        hue = palette.hue
        chroma = palette.chroma * (color.chroma_multiplier(scheme) if color.chroma_multiplier else 1)

        return Hct.from_hct(hue, chroma, tone)

    def get_tone(self, scheme: "DynamicScheme", color: DynamicColor) -> float:
        """
        Get the tone for the given scheme and color.
        
        Args:
            scheme: The dynamic scheme.
            color: The dynamic color.
            
        Returns:
            A tone value between 0 and 100.
        """
        tone_delta_pair = color.tone_delta_pair(scheme) if color.tone_delta_pair else None

        # Case 0: tone delta constraint.
        if tone_delta_pair:
            role_a = tone_delta_pair.role_a
            role_b = tone_delta_pair.role_b
            polarity = tone_delta_pair.polarity
            constraint = tone_delta_pair.constraint
            absolute_delta = (-tone_delta_pair.delta if polarity == 'darker' or
                            (polarity == 'relative_lighter' and scheme.is_dark) or
                            (polarity == 'relative_darker' and not scheme.is_dark)
                            else tone_delta_pair.delta)

            am_role_a = color.name == role_a.name
            self_role = role_a if am_role_a else role_b
            ref_role = role_b if am_role_a else role_a
            self_tone = self_role.tone(scheme)
            ref_tone = ref_role.get_tone(scheme)
            relative_delta = absolute_delta * (1 if am_role_a else -1)

            if constraint == 'exact':
                self_tone = math_utils.clamp_double(0, 100, ref_tone + relative_delta)
            elif constraint == 'nearer':
                if relative_delta > 0:
                    self_tone = math_utils.clamp_double(
                        0, 100,
                        math_utils.clamp_double(ref_tone, ref_tone + relative_delta, self_tone))
                else:
                    self_tone = math_utils.clamp_double(
                        0, 100,
                        math_utils.clamp_double(ref_tone + relative_delta, ref_tone, self_tone))
            elif constraint == 'farther':
                if relative_delta > 0:
                    self_tone = math_utils.clamp_double(ref_tone + relative_delta, 100, self_tone)
                else:
                    self_tone = math_utils.clamp_double(0, ref_tone + relative_delta, self_tone)

            if color.background and color.contrast_curve:
                background = color.background(scheme)
                contrast_curve = color.contrast_curve(scheme)
                if background and contrast_curve:
                    # Adjust the tones for contrast, if background and contrast curve
                    # are defined.
                    bg_tone = background.get_tone(scheme)
                    self_contrast = contrast_curve.get(scheme.contrast_level)
                    self_tone = (self_tone if Contrast.ratio_of_tones(bg_tone, self_tone) >= self_contrast and
                                scheme.contrast_level >= 0 else
                                DynamicColor.foreground_tone(bg_tone, self_contrast))

            # This can avoid the awkward tones for background colors including the
            # access fixed colors. Accent fixed dim colors should not be adjusted.
            if color.is_background and not color.name.endswith('_fixed_dim'):
                if self_tone >= 57:
                    self_tone = math_utils.clamp_double(65, 100, self_tone)
                else:
                    self_tone = math_utils.clamp_double(0, 49, self_tone)

            return self_tone
        else:
            # Case 1: No tone delta pair; just solve for itself.
            answer = color.tone(scheme)

            if (color.background is None or
                    color.background(scheme) is None or
                    color.contrast_curve is None or
                    color.contrast_curve(scheme) is None):
                return answer  # No adjustment for colors with no background.

            bg_tone = color.background(scheme).get_tone(scheme)
            desired_ratio = color.contrast_curve(scheme).get(scheme.contrast_level)

            # Recalculate the tone from desired contrast ratio if the current
            # contrast ratio is not enough or desired contrast level is decreasing
            # (<0).
            answer = (answer if Contrast.ratio_of_tones(bg_tone, answer) >= desired_ratio and
                     scheme.contrast_level >= 0 else
                     DynamicColor.foreground_tone(bg_tone, desired_ratio))

            # This can avoid the awkward tones for background colors including the
            # access fixed colors. Accent fixed dim colors should not be adjusted.
            if color.is_background and not color.name.endswith('_fixed_dim'):
                if answer >= 57:
                    answer = math_utils.clamp_double(65, 100, answer)
                else:
                    answer = math_utils.clamp_double(0, 49, answer)

            if (color.second_background is None or
                    color.second_background(scheme) is None):
                return answer

            # Case 2: Adjust for dual backgrounds.
            bg1, bg2 = color.background, color.second_background
            bg_tone1, bg_tone2 = bg1(scheme).get_tone(scheme), bg2(scheme).get_tone(scheme)
            upper, lower = max(bg_tone1, bg_tone2), min(bg_tone1, bg_tone2)

            if (Contrast.ratio_of_tones(upper, answer) >= desired_ratio and
                    Contrast.ratio_of_tones(lower, answer) >= desired_ratio):
                return answer

            # The darkest light tone that satisfies the desired ratio,
            # or -1 if such ratio cannot be reached.
            light_option = Contrast.lighter(upper, desired_ratio)

            # The lightest dark tone that satisfies the desired ratio,
            # or -1 if such ratio cannot be reached.
            dark_option = Contrast.darker(lower, desired_ratio)

            # Tones suitable for the foreground.
            availables = []
            if light_option != -1:
                availables.append(light_option)
            if dark_option != -1:
                availables.append(dark_option)

            prefers_light = (DynamicColor.tone_prefers_light_foreground(bg_tone1) or
                            DynamicColor.tone_prefers_light_foreground(bg_tone2))
            if prefers_light:
                return 100 if light_option < 0 else light_option
            if len(availables) == 1:
                return availables[0]
            return 0 if dark_option < 0 else dark_option


# Global delegates for different spec versions
spec2021 = ColorCalculationDelegateImpl2021()
spec2025 = ColorCalculationDelegateImpl2025()


def get_spec(spec_version: SpecVersion) -> ColorCalculationDelegate:
    """
    Returns the ColorCalculationDelegate for the given spec version.
    
    Args:
        spec_version: The spec version.
        
    Returns:
        A ColorCalculationDelegate.
    """
    return spec2025 if spec_version == '2025' else spec2021
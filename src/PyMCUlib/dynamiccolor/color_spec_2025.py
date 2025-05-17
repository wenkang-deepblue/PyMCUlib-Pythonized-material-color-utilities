# dynamiccolor/color_spec_2025.py

from typing import Optional, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from PyMCUlib.palettes.tonal_palette import TonalPalette
    from PyMCUlib.dynamiccolor.dynamic_color import DynamicColor

from PyMCUlib.hct.hct import Hct
from PyMCUlib.utils import math_utils

from PyMCUlib.dynamiccolor.color_spec_2021 import ColorSpecDelegateImpl2021
from PyMCUlib.dynamiccolor.contrast_curve import ContrastCurve
from PyMCUlib.dynamiccolor.dynamic_color import DynamicColor, extend_spec_version
from PyMCUlib.dynamiccolor.tone_delta_pair import ToneDeltaPair

def _clone_light(scheme):
    # 浅拷贝 scheme 对象，并将 is_dark 强制设为 False（轻色模式）
    new = copy.copy(scheme)
    new.is_dark = False
    return new

def _t_max_c(
        palette: 'TonalPalette', 
        lower_bound: float = 0, 
        upper_bound: float = 100,
        chroma_multiplier: float = 1) -> float:
    """
    Returns the maximum tone for a given chroma in the palette.

    Args:
        palette: The tonal palette to use.
        lower_bound: The lower bound of the tone.
        upper_bound: The upper bound of the tone.
        chroma_multiplier: The multiplier for the chroma.
    """
    answer = _find_best_tone_for_chroma(
        palette.hue, palette.chroma * chroma_multiplier, 100, True)
    return math_utils.clamp_double(lower_bound, upper_bound, answer)


def _t_min_c(
        palette: 'TonalPalette', 
        lower_bound: float = 0,
        upper_bound: float = 100) -> float:
    """
    Returns the minimum tone for a given chroma in the palette.

    Args:
        palette: The tonal palette to use.
        lower_bound: The lower bound of the tone.
        upper_bound: The upper bound of the tone.
    """
    answer = _find_best_tone_for_chroma(palette.hue, palette.chroma, 0, False)
    return math_utils.clamp_double(lower_bound, upper_bound, answer)


def _find_best_tone_for_chroma(
        hue: float, chroma: float, tone: float,
        by_decreasing_tone: bool) -> float:
    """
    Searches for the best tone with a given chroma from a given tone at a
    specific hue.

    Args:
        hue: The given hue.
        chroma: The target chroma.
        tone: The tone to start with.
        by_decreasing_tone: Whether to search for lower tones.
    """
    answer = tone
    best_candidate = Hct.from_hct(hue, chroma, answer)
    
    while best_candidate.chroma < chroma:
        if tone < 0 or tone > 100:
            break
        tone += -1.0 if by_decreasing_tone else 1.0
        new_candidate = Hct.from_hct(hue, chroma, tone)
        if best_candidate.chroma < new_candidate.chroma:
            best_candidate = new_candidate
            answer = tone

    return answer


def _get_curve(default_contrast: float) -> ContrastCurve:
    """
    Returns the contrast curve for a given default contrast.

    Args:
        default_contrast: The default contrast to use.
    """
    if default_contrast == 1.5:
        return ContrastCurve(1.5, 1.5, 3, 4.5)
    elif default_contrast == 3:
        return ContrastCurve(3, 3, 4.5, 7)
    elif default_contrast == 4.5:
        return ContrastCurve(4.5, 4.5, 7, 11)
    elif default_contrast == 6:
        return ContrastCurve(6, 6, 7, 11)
    elif default_contrast == 7:
        return ContrastCurve(7, 7, 11, 21)
    elif default_contrast == 9:
        return ContrastCurve(9, 9, 11, 21)
    elif default_contrast == 11:
        return ContrastCurve(11, 11, 21, 21)
    elif default_contrast == 21:
        return ContrastCurve(21, 21, 21, 21)
    else:
        # Shouldn't happen.
        return ContrastCurve(default_contrast, default_contrast, 7, 21)


class ColorSpecDelegateImpl2025(ColorSpecDelegateImpl2021):
    """
    A delegate for the dynamic color spec of a DynamicScheme in the 2025 spec.
    """

    ################################################################
    # Surfaces [S]                                               #
    ################################################################

    def surface(self) -> 'DynamicColor':
        base = super().surface()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: (
                base.tone(s),
                4 if s.platform == 'phone' and s.is_dark else (
                    99 if s.platform == 'phone' and Hct.is_yellow(s.neutral_palette.hue) else
                    97 if s.platform == 'phone' and s.variant == 'VIBRANT' else
                    98 if s.platform == 'phone' else 0
                )
            )[1],
            'is_background': True,
        })
        return extend_spec_version(base, '2025', color2025)

    def surface_dim(self) -> 'DynamicColor':
        base = super().surface_dim()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface_dim',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: (
                4 if s.is_dark else (
                    90 if Hct.is_yellow(s.neutral_palette.hue) else
                    85 if s.variant == 'VIBRANT' else
                    87
                )
            ),
            'is_background': True,
            'chroma_multiplier': lambda s: (
                1 if s.is_dark else (
                    2.5 if s.variant == 'NEUTRAL' else
                    1.7 if s.variant == 'TONAL_SPOT' else
                    2.7 if s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                    1.75 if s.variant == 'EXPRESSIVE' else
                    1.36 if s.variant == 'VIBRANT' else 1
                )
            ),
        })
        return extend_spec_version(base, '2025', color2025)

    def surface_bright(self) -> 'DynamicColor':
        base = super().surface_bright()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface_bright',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: (
                18 if s.is_dark else (
                    99 if Hct.is_yellow(s.neutral_palette.hue) else
                    97 if s.variant == 'VIBRANT' else
                    98
                )
            ),
            'is_background': True,
            'chroma_multiplier': lambda s: (
                2.5 if s.is_dark and s.variant == 'NEUTRAL' else
                1.7 if s.is_dark and s.variant == 'TONAL_SPOT' else
                2.7 if s.is_dark and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                1.75 if s.is_dark and s.variant == 'EXPRESSIVE' else
                1.36 if s.is_dark and s.variant == 'VIBRANT' else 1
            ),
        })
        return extend_spec_version(base, '2025', color2025)

    def surface_container_lowest(self) -> 'DynamicColor':
        base = super().surface_container_lowest()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface_container_lowest',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 0 if s.is_dark else 100,
            'is_background': True,
        })
        return extend_spec_version(base, '2025', color2025)

    def surface_container_low(self) -> 'DynamicColor':
        base = super().surface_container_low()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface_container_low',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: (
                6 if s.platform == 'phone' and s.is_dark else
                98 if s.platform == 'phone' and Hct.is_yellow(s.neutral_palette.hue) else
                95 if s.platform == 'phone' and s.variant == 'VIBRANT' else
                96 if s.platform == 'phone' else 15
            ),
            'is_background': True,
            'chroma_multiplier': lambda s: (
                1.3 if s.platform == 'phone' and s.variant == 'NEUTRAL' else
                1.25 if s.platform == 'phone' and s.variant == 'TONAL_SPOT' else
                1.3 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                1.15 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' else
                1.08 if s.platform == 'phone' and s.variant == 'VIBRANT' else 1
            ),
        })
        return extend_spec_version(base, '2025', color2025)

    def surface_container(self) -> 'DynamicColor':
        base = super().surface_container()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface_container',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: (
                9 if s.platform == 'phone' and s.is_dark else
                96 if s.platform == 'phone' and Hct.is_yellow(s.neutral_palette.hue) else
                92 if s.platform == 'phone' and s.variant == 'VIBRANT' else
                94 if s.platform == 'phone' else 20
            ),
            'is_background': True,
            'chroma_multiplier': lambda s: (
                1.6 if s.platform == 'phone' and s.variant == 'NEUTRAL' else
                1.4 if s.platform == 'phone' and s.variant == 'TONAL_SPOT' else
                1.6 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                1.3 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' else
                1.15 if s.platform == 'phone' and s.variant == 'VIBRANT' else 1
            ),
        })
        return extend_spec_version(base, '2025', color2025)

    def surface_container_high(self) -> 'DynamicColor':
        base = super().surface_container_high()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface_container_high',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: (
                12 if s.platform == 'phone' and s.is_dark else
                94 if s.platform == 'phone' and Hct.is_yellow(s.neutral_palette.hue) else
                90 if s.platform == 'phone' and s.variant == 'VIBRANT' else
                92 if s.platform == 'phone' else 25
            ),
            'is_background': True,
            'chroma_multiplier': lambda s: (
                1.9 if s.platform == 'phone' and s.variant == 'NEUTRAL' else
                1.5 if s.platform == 'phone' and s.variant == 'TONAL_SPOT' else
                1.95 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                1.45 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' else
                1.22 if s.platform == 'phone' and s.variant == 'VIBRANT' else 1
            ),
        })
        return extend_spec_version(base, '2025', color2025)

    def surface_container_highest(self) -> 'DynamicColor':
        base = super().surface_container_highest()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface_container_highest',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: (
                15 if s.is_dark else
                92 if Hct.is_yellow(s.neutral_palette.hue) else
                88 if s.variant == 'VIBRANT' else 90
            ),
            'is_background': True,
            'chroma_multiplier': lambda s: (
                2.2 if s.variant == 'NEUTRAL' else
                1.7 if s.variant == 'TONAL_SPOT' else
                2.3 if s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                1.6 if s.variant == 'EXPRESSIVE' else
                1.29 if s.variant == 'VIBRANT' else 1
            ),
        })
        return extend_spec_version(base, '2025', color2025)

    def on_surface(self) -> 'DynamicColor':
        base = super().on_surface()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_surface',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: (
                _t_max_c(s.neutral_palette, 0, 100, 1.1) if s.variant == 'VIBRANT' else
                DynamicColor.get_initial_tone_from_background(
                    lambda s: self.highest_surface(s) if s.platform == 'phone' else self.surface_container_high()
                )(s)
            ),
            'chroma_multiplier': lambda s: (
                2.2 if s.platform == 'phone' and s.variant == 'NEUTRAL' else
                1.7 if s.platform == 'phone' and s.variant == 'TONAL_SPOT' else
                3.0 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) and s.is_dark else
                2.3 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                1.6 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' else 1
            ),
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(11) if s.is_dark else _get_curve(9),
        })
        return extend_spec_version(base, '2025', color2025)

    def on_surface_variant(self) -> 'DynamicColor':
        base = super().on_surface_variant()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_surface_variant',
            'palette': lambda s: s.neutral_palette,
            'chroma_multiplier': lambda s: (
                2.2 if s.platform == 'phone' and s.variant == 'NEUTRAL' else
                1.7 if s.platform == 'phone' and s.variant == 'TONAL_SPOT' else
                3.0 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) and s.is_dark else
                2.3 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                1.6 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' else 1
            ),
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(4.5) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def outline(self) -> 'DynamicColor':
        base = super().outline()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'outline',
            'palette': lambda s: s.neutral_palette,
            'chroma_multiplier': lambda s: (
                2.2 if s.platform == 'phone' and s.variant == 'NEUTRAL' else
                1.7 if s.platform == 'phone' and s.variant == 'TONAL_SPOT' else
                3.0 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) and s.is_dark else
                2.3 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                1.6 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' else 1
            ),
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(3) if s.platform == 'phone' else _get_curve(4.5),
        })
        return extend_spec_version(base, '2025', color2025)

    def outline_variant(self) -> 'DynamicColor':
        base = super().outline_variant()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'outline_variant',
            'palette': lambda s: s.neutral_palette,
            'chroma_multiplier': lambda s: (
                2.2 if s.platform == 'phone' and s.variant == 'NEUTRAL' else
                1.7 if s.platform == 'phone' and s.variant == 'TONAL_SPOT' else
                3.0 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) and s.is_dark else
                2.3 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' and Hct.is_yellow(s.neutral_palette.hue) else
                1.6 if s.platform == 'phone' and s.variant == 'EXPRESSIVE' else 1
            ),
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(1.5) if s.platform == 'phone' else _get_curve(3),
        })
        return extend_spec_version(base, '2025', color2025)

    def inverse_surface(self) -> 'DynamicColor':
        base = super().inverse_surface()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'inverse_surface',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 98 if s.is_dark else 4,
            'is_background': True,
        })
        return extend_spec_version(base, '2025', color2025)

    def inverse_on_surface(self) -> 'DynamicColor':
        base = super().inverse_on_surface()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'inverse_on_surface',
            'palette': lambda s: s.neutral_palette,
            'background': lambda s: self.inverse_surface(),
            'contrast_curve': lambda s: _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    ################################################################
    # Primaries [P]                                              #
    ################################################################

    def primary(self) -> 'DynamicColor':
        base = super().primary()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'primary',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: (
                90 if s.variant == 'NEUTRAL' and s.platform != 'phone' else
                80 if s.variant == 'NEUTRAL' and s.platform == 'phone' and s.is_dark else
                40 if s.variant == 'NEUTRAL' and s.platform == 'phone' else
                _t_max_c(s.primary_palette, 0, 90) if s.variant == 'TONAL_SPOT' and s.platform != 'phone' else
                80 if s.variant == 'TONAL_SPOT' and s.platform == 'phone' and s.is_dark else
                _t_max_c(s.primary_palette) if s.variant == 'TONAL_SPOT' and s.platform == 'phone' else
                _t_max_c(
                    s.primary_palette, 0,
                    25 if Hct.is_yellow(s.primary_palette.hue) else
                    88 if Hct.is_cyan(s.primary_palette.hue) else 98
                ) if s.variant == 'EXPRESSIVE' else
                _t_max_c(
                    s.primary_palette, 0, 
                    88 if Hct.is_cyan(s.primary_palette.hue) else 98
                ) if s.variant == 'VIBRANT' else
                base.tone(s)
            ),
            'is_background': True,
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(4.5) if s.platform == 'phone' else _get_curve(7),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.primary_container(), self.primary(), 5, 'relative_lighter',
                True, 'farther'
            ) if s.platform == 'phone' else None,
        })
        return extend_spec_version(base, '2025', color2025)

    def primary_dim(self) -> Optional['DynamicColor']:
        return DynamicColor.from_palette({
            'name': 'primary_dim',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: (
                85 if s.variant == 'NEUTRAL' else
                _t_max_c(s.primary_palette, 0, 90) if s.variant == 'TONAL_SPOT' else
                _t_max_c(s.primary_palette)
            ),
            'is_background': True,
            'background': lambda s: self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.primary_dim(), self.primary(), 5, 'darker', True, 'farther'),
        })

    def on_primary(self) -> 'DynamicColor':
        base = super().on_primary()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_primary',
            'palette': lambda s: s.primary_palette,
            'background': lambda s: self.primary_dim() if s.platform != 'phone' else self.primary(),
            'contrast_curve': lambda s: _get_curve(6) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def primary_container(self) -> 'DynamicColor':
        base = super().primary_container()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'primary_container',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: (
                30 if s.platform == 'watch' else
                30 if s.variant == 'NEUTRAL' and s.is_dark else
                90 if s.variant == 'NEUTRAL' else
                _t_min_c(s.primary_palette, 35, 93) if s.variant == 'TONAL_SPOT' and s.is_dark else
                _t_max_c(s.primary_palette, 0, 90) if s.variant == 'TONAL_SPOT' else
                _t_max_c(s.primary_palette, 30, 93) if s.variant == 'EXPRESSIVE' and s.is_dark else
                _t_max_c(
                    s.primary_palette, 78,
                    88 if Hct.is_cyan(s.primary_palette.hue) else 90
                ) if s.variant == 'EXPRESSIVE' else
                _t_min_c(s.primary_palette, 66, 93) if s.variant == 'VIBRANT' and s.is_dark else
                _t_max_c(
                    s.primary_palette, 66,
                    88 if Hct.is_cyan(s.primary_palette.hue) else 93
                ) if s.variant == 'VIBRANT' else
                base.tone(s)
            ),
            'is_background': True,
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else None,
            'tone_delta_pair': lambda s: (
                None if s.platform == 'phone' else
                ToneDeltaPair(
                    self.primary_container(), self.primary_dim(), 10, 'darker', True,
                    'farther'
                )
            ),
            'contrast_curve': lambda s: _get_curve(1.5) if s.platform == 'phone' and s.contrast_level > 0 else None,
        })
        return extend_spec_version(base, '2025', color2025)

    def on_primary_container(self) -> 'DynamicColor':
        base = super().on_primary_container()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_primary_container',
            'palette': lambda s: s.primary_palette,
            'background': lambda s: self.primary_container(),
            'contrast_curve': lambda s: _get_curve(6) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def primary_fixed(self) -> 'DynamicColor':
        base = super().primary_fixed()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'primary_fixed',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: self.primary_container().get_tone(_clone_light(s)),
            'is_background': True,
        })
        return extend_spec_version(base, '2025', color2025)

    def primary_fixed_dim(self) -> 'DynamicColor':
        base = super().primary_fixed_dim()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'primary_fixed_dim',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: self.primary_fixed().get_tone(s),
            'is_background': True,
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.primary_fixed_dim(), self.primary_fixed(), 5, 'darker', True,
                'exact'),
        })
        return extend_spec_version(base, '2025', color2025)

    def on_primary_fixed(self) -> 'DynamicColor':
        base = super().on_primary_fixed()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_primary_fixed',
            'palette': lambda s: s.primary_palette,
            'background': lambda s: self.primary_fixed_dim(),
            'contrast_curve': lambda s: _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def on_primary_fixed_variant(self) -> 'DynamicColor':
        base = super().on_primary_fixed_variant()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_primary_fixed_variant',
            'palette': lambda s: s.primary_palette,
            'background': lambda s: self.primary_fixed_dim(),
            'contrast_curve': lambda s: _get_curve(4.5),
        })
        return extend_spec_version(base, '2025', color2025)

    def inverse_primary(self) -> 'DynamicColor':
        base = super().inverse_primary()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'inverse_primary',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: _t_max_c(s.primary_palette),
            'background': lambda s: self.inverse_surface(),
            'contrast_curve': lambda s: _get_curve(6) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    ################################################################
    # Secondaries [Q]                                            #
    ################################################################

    def secondary(self) -> 'DynamicColor':
        base = super().secondary()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'secondary',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: (
                90 if s.platform == 'watch' and s.variant == 'NEUTRAL' else
                _t_max_c(s.secondary_palette, 0, 90) if s.platform == 'watch' else
                _t_min_c(s.secondary_palette, 0, 98) if s.variant == 'NEUTRAL' and s.is_dark else
                _t_max_c(s.secondary_palette) if s.variant == 'NEUTRAL' else
                _t_max_c(s.secondary_palette, 0, 98 if s.is_dark else 90) if s.variant == 'VIBRANT' else
                80 if s.is_dark else _t_max_c(s.secondary_palette)
            ),
            'is_background': True,
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(4.5) if s.platform == 'phone' else _get_curve(7),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.secondary_container(), self.secondary(), 5,
                'relative_lighter', True, 'farther'
            ) if s.platform == 'phone' else None,
        })
        return extend_spec_version(base, '2025', color2025)

    def secondary_dim(self) -> Optional['DynamicColor']:
        return DynamicColor.from_palette({
            'name': 'secondary_dim',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: (
                85 if s.variant == 'NEUTRAL' else
                _t_max_c(s.secondary_palette, 0, 90)
            ),
            'is_background': True,
            'background': lambda s: self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.secondary_dim(), self.secondary(), 5, 'darker', True, 'farther'),
        })
        
    def on_secondary(self) -> 'DynamicColor':
        base = super().on_secondary()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_secondary',
            'palette': lambda s: s.secondary_palette,
            'background': lambda s: self.secondary() if s.platform == 'phone' else self.secondary_dim(),
            'contrast_curve': lambda s: _get_curve(6) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def secondary_container(self) -> 'DynamicColor':
        base = super().secondary_container()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'secondary_container',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: (
                30 if s.platform == 'watch' else
                _t_min_c(s.secondary_palette, 30, 40) if s.variant == 'VIBRANT' and s.is_dark else
                _t_max_c(s.secondary_palette, 84, 90) if s.variant == 'VIBRANT' else
                15 if s.variant == 'EXPRESSIVE' and s.is_dark else
                _t_max_c(s.secondary_palette, 90, 95) if s.variant == 'EXPRESSIVE' else
                25 if s.is_dark else 90
            ),
            'is_background': True,
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else None,
            'tone_delta_pair': lambda s: (
                ToneDeltaPair(
                    self.secondary_container(), self.secondary_dim(), 10, 'darker',
                    True, 'farther'
                ) if s.platform == 'watch' else None
            ),
            'contrast_curve': lambda s: _get_curve(1.5) if s.platform == 'phone' and s.contrast_level > 0 else None,
        })
        return extend_spec_version(base, '2025', color2025)

    def on_secondary_container(self) -> 'DynamicColor':
        base = super().on_secondary_container()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_secondary_container',
            'palette': lambda s: s.secondary_palette,
            'background': lambda s: self.secondary_container(),
            'contrast_curve': lambda s: _get_curve(6) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def secondary_fixed(self) -> 'DynamicColor':
        base = super().secondary_fixed()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'secondary_fixed',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: self.secondary_container().get_tone(_clone_light(s)),
            'is_background': True,
        })
        return extend_spec_version(base, '2025', color2025)

    def secondary_fixed_dim(self) -> 'DynamicColor':
        base = super().secondary_fixed_dim()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'secondary_fixed_dim',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: self.secondary_fixed().get_tone(s),
            'is_background': True,
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.secondary_fixed_dim(), self.secondary_fixed(), 5, 'darker', True,
                'exact'),
        })
        return extend_spec_version(base, '2025', color2025)

    def on_secondary_fixed(self) -> 'DynamicColor':
        base = super().on_secondary_fixed()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_secondary_fixed',
            'palette': lambda s: s.secondary_palette,
            'background': lambda s: self.secondary_fixed_dim(),
            'contrast_curve': lambda s: _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def on_secondary_fixed_variant(self) -> 'DynamicColor':
        base = super().on_secondary_fixed_variant()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_secondary_fixed_variant',
            'palette': lambda s: s.secondary_palette,
            'background': lambda s: self.secondary_fixed_dim(),
            'contrast_curve': lambda s: _get_curve(4.5),
        })
        return extend_spec_version(base, '2025', color2025)

    ################################################################
    # Tertiaries [T]                                             #
    ################################################################

    def tertiary(self) -> 'DynamicColor':
        base = super().tertiary()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'tertiary',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: (
                _t_max_c(s.tertiary_palette, 0, 90) if s.platform == 'watch' and s.variant == 'TONAL_SPOT' else
                _t_max_c(s.tertiary_palette) if s.platform == 'watch' else
                _t_max_c(
                    s.tertiary_palette, 0,
                    88 if Hct.is_cyan(s.tertiary_palette.hue) else (s.is_dark and 98 or 100)
                ) if s.variant in ('EXPRESSIVE', 'VIBRANT') else
                _t_max_c(s.tertiary_palette, 0, 98) if s.variant in ('NEUTRAL', 'TONAL_SPOT') and s.is_dark else
                _t_max_c(s.tertiary_palette)
            ),
            'is_background': True,
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(4.5) if s.platform == 'phone' else _get_curve(7),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.tertiary_container(), self.tertiary(), 5, 'relative_lighter',
                True, 'farther'
            ) if s.platform == 'phone' else None,
        })
        return extend_spec_version(base, '2025', color2025)

    def tertiary_dim(self) -> Optional['DynamicColor']:
        return DynamicColor.from_palette({
            'name': 'tertiary_dim',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: (
                _t_max_c(s.tertiary_palette, 0, 90) if s.variant == 'TONAL_SPOT' else
                _t_max_c(s.tertiary_palette)
            ),
            'is_background': True,
            'background': lambda s: self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.tertiary_dim(), self.tertiary(), 5, 'darker', True, 'farther'),
        })

    def on_tertiary(self) -> 'DynamicColor':
        base = super().on_tertiary()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_tertiary',
            'palette': lambda s: s.tertiary_palette,
            'background': lambda s: self.tertiary() if s.platform == 'phone' else self.tertiary_dim(),
            'contrast_curve': lambda s: _get_curve(6) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def tertiary_container(self) -> 'DynamicColor':
        base = super().tertiary_container()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'tertiary_container',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: (
                _t_max_c(s.tertiary_palette, 0, 90) if s.platform == 'watch' and s.variant == 'TONAL_SPOT' else
                _t_max_c(s.tertiary_palette) if s.platform == 'watch' else
                _t_max_c(s.tertiary_palette, 0, 93) if s.variant == 'NEUTRAL' and s.is_dark else
                _t_max_c(s.tertiary_palette, 0, 96) if s.variant == 'NEUTRAL' else
                _t_max_c(s.tertiary_palette, 0, 93 if s.is_dark else 100) if s.variant == 'TONAL_SPOT' else
                _t_max_c(
                    s.tertiary_palette, 75,
                    88 if Hct.is_cyan(s.tertiary_palette.hue) else (s.is_dark and 93 or 100)
                ) if s.variant == 'EXPRESSIVE' else
                _t_max_c(s.tertiary_palette, 0, 93) if s.variant == 'VIBRANT' and s.is_dark else
                _t_max_c(s.tertiary_palette, 72, 100)
            ),
            'is_background': True,
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else None,
            'tone_delta_pair': lambda s: (
                ToneDeltaPair(
                    self.tertiary_container(), self.tertiary_dim(), 10, 'darker', True,
                    'farther'
                ) if s.platform == 'watch' else None
            ),
            'contrast_curve': lambda s: _get_curve(1.5) if s.platform == 'phone' and s.contrast_level > 0 else None,
        })
        return extend_spec_version(base, '2025', color2025)

    def on_tertiary_container(self) -> 'DynamicColor':
        base = super().on_tertiary_container()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_tertiary_container',
            'palette': lambda s: s.tertiary_palette,
            'background': lambda s: self.tertiary_container(),
            'contrast_curve': lambda s: _get_curve(6) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def tertiary_fixed(self) -> 'DynamicColor':
        base = super().tertiary_fixed()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'tertiary_fixed',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: self.tertiary_container().get_tone(_clone_light(s)),
            'is_background': True,
        })
        return extend_spec_version(base, '2025', color2025)

    def tertiary_fixed_dim(self) -> 'DynamicColor':
        base = super().tertiary_fixed_dim()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'tertiary_fixed_dim',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: self.tertiary_fixed().get_tone(s),
            'is_background': True,
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.tertiary_fixed_dim(), self.tertiary_fixed(), 5, 'darker', True,
                'exact'),
        })
        return extend_spec_version(base, '2025', color2025)

    def on_tertiary_fixed(self) -> 'DynamicColor':
        base = super().on_tertiary_fixed()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_tertiary_fixed',
            'palette': lambda s: s.tertiary_palette,
            'background': lambda s: self.tertiary_fixed_dim(),
            'contrast_curve': lambda s: _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def on_tertiary_fixed_variant(self) -> 'DynamicColor':
        base = super().on_tertiary_fixed_variant()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_tertiary_fixed_variant',
            'palette': lambda s: s.tertiary_palette,
            'background': lambda s: self.tertiary_fixed_dim(),
            'contrast_curve': lambda s: _get_curve(4.5),
        })
        return extend_spec_version(base, '2025', color2025)

    ################################################################
    # Errors [E]                                                 #
    ################################################################

    def error(self) -> 'DynamicColor':
        base = super().error()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'error',
            'palette': lambda s: s.error_palette,
            'tone': lambda s: (
                _t_min_c(s.error_palette, 0, 98) if s.platform == 'phone' and s.is_dark else
                _t_max_c(s.error_palette) if s.platform == 'phone' else
                _t_min_c(s.error_palette)
            ),
            'is_background': True,
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(4.5) if s.platform == 'phone' else _get_curve(7),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.error_container(), self.error(), 5, 'relative_lighter', True,
                'farther'
            ) if s.platform == 'phone' else None,
        })
        return extend_spec_version(base, '2025', color2025)

    def error_dim(self) -> Optional['DynamicColor']:
        return DynamicColor.from_palette({
            'name': 'error_dim',
            'palette': lambda s: s.error_palette,
            'tone': lambda s: _t_min_c(s.error_palette),
            'is_background': True,
            'background': lambda s: self.surface_container_high(),
            'contrast_curve': lambda s: _get_curve(4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.error_dim(), self.error(), 5, 'darker', True, 'farther'),
        })

    def on_error(self) -> 'DynamicColor':
        base = super().on_error()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_error',
            'palette': lambda s: s.error_palette,
            'background': lambda s: self.error() if s.platform == 'phone' else self.error_dim(),
            'contrast_curve': lambda s: _get_curve(6) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    def error_container(self) -> 'DynamicColor':
        base = super().error_container()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'error_container',
            'palette': lambda s: s.error_palette,
            'tone': lambda s: (
                30 if s.platform == 'watch' else
                _t_min_c(s.error_palette, 30, 93) if s.is_dark else
                _t_max_c(s.error_palette, 0, 90)
            ),
            'is_background': True,
            'background': lambda s: self.highest_surface(s) if s.platform == 'phone' else None,
            'tone_delta_pair': lambda s: (
                ToneDeltaPair(
                    self.error_container(), self.error_dim(), 10, 'darker', True,
                    'farther'
                ) if s.platform == 'watch' else None
            ),
            'contrast_curve': lambda s: _get_curve(1.5) if s.platform == 'phone' and s.contrast_level > 0 else None,
        })
        return extend_spec_version(base, '2025', color2025)

    def on_error_container(self) -> 'DynamicColor':
        base = super().on_error_container()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_error_container',
            'palette': lambda s: s.error_palette,
            'background': lambda s: self.error_container(),
            'contrast_curve': lambda s: _get_curve(4.5) if s.platform == 'phone' else _get_curve(7),
        })
        return extend_spec_version(base, '2025', color2025)

    #################################################################
    # Remapped Colors                                             #
    #################################################################

    def surface_variant(self) -> 'DynamicColor':
        base = super().surface_variant()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface_variant',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: self.surface_container_highest().get_tone(s),
            'is_background': True,
        })
        return extend_spec_version(base, '2025', color2025)

    def surface_tint(self) -> 'DynamicColor':
        base = super().surface_tint()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'surface_tint',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: self.primary().get_tone(s),
            'is_background': True,
        })
        return extend_spec_version(base, '2025', color2025)

    def background(self) -> 'DynamicColor':
        base = super().background()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'background',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: self.surface().get_tone(s),
            'is_background': True,
        })
        return extend_spec_version(base, '2025', color2025)

    def on_background(self) -> 'DynamicColor':
        base = super().on_background()
        color2025: DynamicColor = DynamicColor.from_palette({
            'name': 'on_background',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: self.on_surface().get_tone(s),
            'background': lambda s: self.background(),
            'contrast_curve': lambda s: self.on_surface().contrast_curve(s),
        })
        return extend_spec_version(base, '2025', color2025)
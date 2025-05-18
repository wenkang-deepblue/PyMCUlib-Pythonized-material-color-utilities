# color_spec_2021.py

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyMCUlib.dynamiccolor.dynamic_color import DynamicColor
    from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme

from PyMCUlib.dislike.dislike_analyzer import DislikeAnalyzer
from PyMCUlib.hct.hct import Hct
from PyMCUlib.dynamiccolor.color_spec_delegate import ColorSpecDelegate
from PyMCUlib.dynamiccolor.contrast_curve import ContrastCurve
from PyMCUlib.dynamiccolor.tone_delta_pair import ToneDeltaPair


def _is_fidelity(scheme: 'DynamicScheme') -> bool:
    """
    Returns true if the scheme is Fidelity or Content.
    """
    from .variant import Variant
    return scheme.variant == Variant.FIDELITY or scheme.variant == Variant.CONTENT


def _is_monochrome(scheme: 'DynamicScheme') -> bool:
    """
    Returns true if the scheme is Monochrome.
    """
    from .variant import Variant
    return scheme.variant == Variant.MONOCHROME


def _find_desired_chroma_by_tone(
        hue: float, chroma: float, tone: float,
        by_decreasing_tone: bool) -> float:
    """
    Returns the desired chroma for a given tone at a specific hue.

    Args:
        hue: The given hue.
        chroma: The target chroma.
        tone: The tone to start with.
        by_decreasing_tone: Whether to search for lower tones.
    """
    answer = tone

    closest_to_chroma = Hct.from_hct(hue, chroma, tone)
    if closest_to_chroma.chroma < chroma:
        chroma_peak = closest_to_chroma.chroma
        while closest_to_chroma.chroma < chroma:
            answer += -1.0 if by_decreasing_tone else 1.0
            potential_solution = Hct.from_hct(hue, chroma, answer)
            if chroma_peak > potential_solution.chroma:
                break
            if abs(potential_solution.chroma - chroma) < 0.4:
                break

            potential_delta = abs(potential_solution.chroma - chroma)
            current_delta = abs(closest_to_chroma.chroma - chroma)
            if potential_delta < current_delta:
                closest_to_chroma = potential_solution
            chroma_peak = max(chroma_peak, potential_solution.chroma)

    return answer


class ColorSpecDelegateImpl2021(ColorSpecDelegate):
    """
    A delegate for the dynamic color spec of a DynamicScheme in the 2021 spec.
    """

    ################################################################
    # Main Palettes                                              #
    ################################################################

    def primary_palette_key_color(self) -> 'DynamicColor':
        # Delayed import to avoid circular dependency
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'primary_palette_key_color',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: s.primary_palette.key_color.tone,
        })

    def secondary_palette_key_color(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'secondary_palette_key_color',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: s.secondary_palette.key_color.tone,
        })

    def tertiary_palette_key_color(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'tertiary_palette_key_color',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: s.tertiary_palette.key_color.tone,
        })

    def neutral_palette_key_color(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'neutral_palette_key_color',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: s.neutral_palette.key_color.tone,
        })

    def neutral_variant_palette_key_color(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'neutral_variant_palette_key_color',
            'palette': lambda s: s.neutral_variant_palette,
            'tone': lambda s: s.neutral_variant_palette.key_color.tone,
        })

    def error_palette_key_color(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'error_palette_key_color',
            'palette': lambda s: s.error_palette,
            'tone': lambda s: s.error_palette.key_color.tone,
        })

    ################################################################
    # Surfaces [S]                                               #
    ################################################################

    def background(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'background',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 6 if s.is_dark else 98,
            'is_background': True,
        })

    def on_background(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_background',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 90 if s.is_dark else 10,
            'background': lambda s: self.background(),
            'contrast_curve': lambda s: ContrastCurve(3, 3, 4.5, 7),
        })

    def surface(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 6 if s.is_dark else 98,
            'is_background': True,
        })

    def surface_dim(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface_dim',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 6 if s.is_dark else ContrastCurve(87, 87, 80, 75).get(s.contrast_level),
            'is_background': True,
        })

    def surface_bright(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface_bright',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: ContrastCurve(24, 24, 29, 34).get(s.contrast_level) if s.is_dark else 98,
            'is_background': True,
        })

    def surface_container_lowest(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface_container_lowest',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: ContrastCurve(4, 4, 2, 0).get(s.contrast_level) if s.is_dark else 100,
            'is_background': True,
        })

    def surface_container_low(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface_container_low',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: ContrastCurve(10, 10, 11, 12).get(s.contrast_level) if s.is_dark else ContrastCurve(96, 96, 96, 95).get(s.contrast_level),
            'is_background': True,
        })

    def surface_container(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface_container',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: ContrastCurve(12, 12, 16, 20).get(s.contrast_level) if s.is_dark else ContrastCurve(94, 94, 92, 90).get(s.contrast_level),
            'is_background': True,
        })

    def surface_container_high(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface_container_high',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: ContrastCurve(17, 17, 21, 25).get(s.contrast_level) if s.is_dark else ContrastCurve(92, 92, 88, 85).get(s.contrast_level),
            'is_background': True,
        })

    def surface_container_highest(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface_container_highest',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: ContrastCurve(22, 22, 26, 30).get(s.contrast_level) if s.is_dark else ContrastCurve(90, 90, 84, 80).get(s.contrast_level),
            'is_background': True,
        })

    def on_surface(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_surface',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 90 if s.is_dark else 10,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(4.5, 7, 11, 21),
        })

    def surface_variant(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface_variant',
            'palette': lambda s: s.neutral_variant_palette,
            'tone': lambda s: 30 if s.is_dark else 90,
            'is_background': True,
        })

    def on_surface_variant(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_surface_variant',
            'palette': lambda s: s.neutral_variant_palette,
            'tone': lambda s: 80 if s.is_dark else 30,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 11),
        })

    def inverse_surface(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'inverse_surface',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 90 if s.is_dark else 20,
            'is_background': True,
        })

    def inverse_on_surface(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'inverse_on_surface',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 20 if s.is_dark else 95,
            'background': lambda s: self.inverse_surface(),
            'contrast_curve': lambda s: ContrastCurve(4.5, 7, 11, 21),
        })

    def outline(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'outline',
            'palette': lambda s: s.neutral_variant_palette,
            'tone': lambda s: 60 if s.is_dark else 50,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1.5, 3, 4.5, 7),
        })

    def outline_variant(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'outline_variant',
            'palette': lambda s: s.neutral_variant_palette,
            'tone': lambda s: 30 if s.is_dark else 80,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
        })

    def shadow(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'shadow',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 0,
        })

    def scrim(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'scrim',
            'palette': lambda s: s.neutral_palette,
            'tone': lambda s: 0,
        })

    def surface_tint(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'surface_tint',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: 80 if s.is_dark else 40,
            'is_background': True,
        })

    ################################################################
    # Primary [P].                                               #
    ################################################################

    def primary(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'primary',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: 100 if _is_monochrome(s) and s.is_dark else 0 if _is_monochrome(s) else 80 if s.is_dark else 40,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 7),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.primary_container(), self.primary(), 10, 'nearer', False),
        })

    def primary_dim(self) -> 'DynamicColor':
        return None

    def on_primary(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_primary',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: 10 if _is_monochrome(s) and s.is_dark else 90 if _is_monochrome(s) else 20 if s.is_dark else 100,
            'background': lambda s: self.primary(),
            'contrast_curve': lambda s: ContrastCurve(4.5, 7, 11, 21),
        })

    def primary_container(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'primary_container',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: s.source_color_hct.tone if _is_fidelity(s) else 85 if _is_monochrome(s) and s.is_dark else 25 if _is_monochrome(s) else 30 if s.is_dark else 90,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.primary_container(), self.primary(), 10, 'nearer', False),
        })

    def on_primary_container(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_primary_container',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: DynamicColor.foreground_tone(
                self.primary_container().tone(s), 4.5
              ) if _is_fidelity(s)
              else 0    if _is_monochrome(s) and s.is_dark
              else 100  if _is_monochrome(s)
              else 90   if s.is_dark
              else 30,
            'background': lambda s: self.primary_container(),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 11),
        })

    def inverse_primary(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'inverse_primary',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: 40 if s.is_dark else 80,
            'background': lambda s: self.inverse_surface(),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 7),
        })

    #################################################################
    # Secondary [Q].                                              #
    #################################################################

    def secondary(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'secondary',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: 80 if s.is_dark else 40,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 7),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.secondary_container(), self.secondary(), 10, 'nearer', False),
        })

    def secondary_dim(self) -> 'DynamicColor':
        return None

    def on_secondary(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_secondary',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: 10 if _is_monochrome(s) and s.is_dark else 100 if _is_monochrome(s) else 20 if s.is_dark else 100,
            'background': lambda s: self.secondary(),
            'contrast_curve': lambda s: ContrastCurve(4.5, 7, 11, 21),
        })

    def secondary_container(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'secondary_container',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: 30 if _is_monochrome(s) and s.is_dark else 85 if _is_monochrome(s) else 30 if s.is_dark else 90 if not _is_fidelity(s) else _find_desired_chroma_by_tone(
                s.secondary_palette.hue, s.secondary_palette.chroma, 30 if s.is_dark else 90,
                s.is_dark is False),
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.secondary_container(), self.secondary(), 10, 'nearer', False),
        })

    def on_secondary_container(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_secondary_container',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: 90   if _is_monochrome(s) and s.is_dark
              else 10   if _is_monochrome(s)
              else 90   if s.is_dark
              else 30   if not _is_fidelity(s)
              else DynamicColor.foreground_tone(
                  self.secondary_container().tone(s), 4.5
              ),
            'background': lambda s: self.secondary_container(),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 11),
        })

    #################################################################
    # Tertiary [T].                                               #
    #################################################################

    def tertiary(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'tertiary',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: 90 if _is_monochrome(s) and s.is_dark else 25 if _is_monochrome(s) else 80 if s.is_dark else 40,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 7),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.tertiary_container(), self.tertiary(), 10, 'nearer', False),
        })

    def tertiary_dim(self) -> 'DynamicColor':
        return None

    def on_tertiary(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_tertiary',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: 10 if _is_monochrome(s) and s.is_dark else 90 if _is_monochrome(s) else 20 if s.is_dark else 100,
            'background': lambda s: self.tertiary(),
            'contrast_curve': lambda s: ContrastCurve(4.5, 7, 11, 21),
        })

    def tertiary_container(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'tertiary_container',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: 60 if _is_monochrome(s) and s.is_dark else 49 if _is_monochrome(s) else 30 if s.is_dark else 90 if not _is_fidelity(s) else DislikeAnalyzer.fix_if_disliked(
                s.tertiary_palette.get_hct(s.source_color_hct.tone)).tone,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.tertiary_container(), self.tertiary(), 10, 'nearer', False),
        })

    def on_tertiary_container(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_tertiary_container',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s:  0   if _is_monochrome(s) and s.is_dark
              else 100  if _is_monochrome(s)
              else  90  if s.is_dark
              else  30  if not _is_fidelity(s)
              else DynamicColor.foreground_tone(
                  self.tertiary_container().tone(s), 4.5
              ),
            'background': lambda s: self.tertiary_container(),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 11),
        })

    #################################################################
    # Error [E].                                                   #
    #################################################################

    def error(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'error',
            'palette': lambda s: s.error_palette,
            'tone': lambda s: 80 if s.is_dark else 40,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 7),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.error_container(), self.error(), 10, 'nearer', False),
        })

    def error_dim(self) -> 'DynamicColor':
        return None

    def on_error(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_error',
            'palette': lambda s: s.error_palette,
            'tone': lambda s: 20 if s.is_dark else 100,
            'background': lambda s: self.error(),
            'contrast_curve': lambda s: ContrastCurve(4.5, 7, 11, 21),
        })

    def error_container(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'error_container',
            'palette': lambda s: s.error_palette,
            'tone': lambda s: 30 if s.is_dark else 90,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.error_container(), self.error(), 10, 'nearer', False),
        })

    def on_error_container(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_error_container',
            'palette': lambda s: s.error_palette,
            'tone': lambda s: 90   if _is_monochrome(s) and s.is_dark
              else 10   if _is_monochrome(s)
              else 90   if s.is_dark
              else 30,
            'background': lambda s: self.error_container(),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 11),
        })

    #################################################################
    # Primary Fixed [PF]                                           #
    #################################################################

    def primary_fixed(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'primary_fixed',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: 40.0 if _is_monochrome(s) else 90.0,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.primary_fixed(), self.primary_fixed_dim(), 10, 'lighter', True),
        })

    def primary_fixed_dim(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'primary_fixed_dim',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: 30.0 if _is_monochrome(s) else 80.0,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.primary_fixed(), self.primary_fixed_dim(), 10, 'lighter', True),
        })

    def on_primary_fixed(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_primary_fixed',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: 100.0 if _is_monochrome(s) else 10.0,
            'background': lambda s: self.primary_fixed_dim(),
            'second_background': lambda s: self.primary_fixed(),
            'contrast_curve': lambda s: ContrastCurve(4.5, 7, 11, 21),
        })

    def on_primary_fixed_variant(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_primary_fixed_variant',
            'palette': lambda s: s.primary_palette,
            'tone': lambda s: 90.0 if _is_monochrome(s) else 30.0,
            'background': lambda s: self.primary_fixed_dim(),
            'second_background': lambda s: self.primary_fixed(),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 11),
        })

    #################################################################
    # Secondary Fixed [QF]                                          #
    #################################################################

    def secondary_fixed(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'secondary_fixed',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: 80.0 if _is_monochrome(s) else 90.0,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.secondary_fixed(), self.secondary_fixed_dim(), 10, 'lighter', True),
        })

    def secondary_fixed_dim(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'secondary_fixed_dim',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: 70.0 if _is_monochrome(s) else 80.0,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.secondary_fixed(), self.secondary_fixed_dim(), 10, 'lighter', True),
        })

    def on_secondary_fixed(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_secondary_fixed',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: 10.0,
            'background': lambda s: self.secondary_fixed_dim(),
            'second_background': lambda s: self.secondary_fixed(),
            'contrast_curve': lambda s: ContrastCurve(4.5, 7, 11, 21),
        })

    def on_secondary_fixed_variant(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_secondary_fixed_variant',
            'palette': lambda s: s.secondary_palette,
            'tone': lambda s: 25.0 if _is_monochrome(s) else 30.0,
            'background': lambda s: self.secondary_fixed_dim(),
            'second_background': lambda s: self.secondary_fixed(),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 11),
        })

    #################################################################
    # Tertiary Fixed [TF]                                         #
    #################################################################

    def tertiary_fixed(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'tertiary_fixed',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: 40.0 if _is_monochrome(s) else 90.0,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.tertiary_fixed(), self.tertiary_fixed_dim(), 10, 'lighter', True),
        })

    def tertiary_fixed_dim(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'tertiary_fixed_dim',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: 30.0 if _is_monochrome(s) else 80.0,
            'is_background': True,
            'background': lambda s: self.highest_surface(s),
            'contrast_curve': lambda s: ContrastCurve(1, 1, 3, 4.5),
            'tone_delta_pair': lambda s: ToneDeltaPair(
                self.tertiary_fixed(), self.tertiary_fixed_dim(), 10, 'lighter', True),
        })

    def on_tertiary_fixed(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_tertiary_fixed',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: 100.0 if _is_monochrome(s) else 10.0,
            'background': lambda s: self.tertiary_fixed_dim(),
            'second_background': lambda s: self.tertiary_fixed(),
            'contrast_curve': lambda s: ContrastCurve(4.5, 7, 11, 21),
        })

    def on_tertiary_fixed_variant(self) -> 'DynamicColor':
        from .dynamic_color import DynamicColor
        return DynamicColor.from_palette({
            'name': 'on_tertiary_fixed_variant',
            'palette': lambda s: s.tertiary_palette,
            'tone': lambda s: 90.0 if _is_monochrome(s) else 30.0,
            'background': lambda s: self.tertiary_fixed_dim(),
            'second_background': lambda s: self.tertiary_fixed(),
            'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 11),
        })

    #################################################################
    # Other                                                      #
    #################################################################

    def highest_surface(self, s: 'DynamicScheme') -> 'DynamicColor':
        return self.surface_bright() if s.is_dark else self.surface_dim()
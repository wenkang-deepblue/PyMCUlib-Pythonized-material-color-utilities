# material_dynamic_colors.py

import math
from PyMCUlib_cpp.cam.cam import cam_from_int, cam_from_xyz_and_viewing_conditions
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.cam.viewing_conditions import DEFAULT_VIEWING_CONDITIONS
from PyMCUlib_cpp.dislike.dislike import fix_if_disliked
from PyMCUlib_cpp.dynamiccolor.contrast_curve import ContrastCurve
from PyMCUlib_cpp.dynamiccolor.dynamic_color import DynamicColor, foreground_tone
from PyMCUlib_cpp.dynamiccolor.tone_delta_pair import ToneDeltaPair, TonePolarity
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.utils.utils import lstar_from_y

def is_fidelity(scheme):
    """Determines if a scheme is a fidelity scheme."""
    return (scheme.variant == Variant.FIDELITY or
            scheme.variant == Variant.CONTENT)

def is_monochrome(scheme):
    """Determines if a scheme is monochrome."""
    return scheme.variant == Variant.MONOCHROME

def xyz_in_viewing_conditions(cam, viewing_conditions):
    """
    Converts CAM16 color to XYZ coordinates in specified viewing conditions.
    
    Args:
        cam: The CAM16 color
        viewing_conditions: The viewing conditions
        
    Returns:
        XYZ coordinates as a Vec3
    """
    alpha = (0.0 if cam.chroma == 0.0 or cam.j == 0.0
             else cam.chroma / math.sqrt(cam.j / 100.0))
    
    t = pow(
        alpha / pow(1.64 - pow(0.29,
                               viewing_conditions.background_y_to_white_point_y),
                    0.73),
        1.0 / 0.9)
    
    h_rad = cam.hue * math.pi / 180.0
    
    e_hue = 0.25 * (math.cos(h_rad + 2.0) + 3.8)
    ac = (viewing_conditions.aw *
          pow(cam.j / 100.0, 1.0 / viewing_conditions.c / viewing_conditions.z))
    p1 = e_hue * (50000.0 / 13.0) * viewing_conditions.n_c * viewing_conditions.ncb
    
    p2 = (ac / viewing_conditions.nbb)
    
    h_sin = math.sin(h_rad)
    h_cos = math.cos(h_rad)
    
    gamma = 23.0 * (p2 + 0.305) * t / (23.0 * p1 + 11 * t * h_cos + 108.0 * t * h_sin)
    a = gamma * h_cos
    b = gamma * h_sin
    r_a = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0
    g_a = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0
    b_a = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0
    
    from PyMCUlib_cpp.utils.utils import signum
    
    r_c_base = max(0, (27.13 * abs(r_a)) / (400.0 - abs(r_a)))
    r_c = signum(r_a) * (100.0 / viewing_conditions.fl) * pow(r_c_base, 1.0 / 0.42)
    g_c_base = max(0, (27.13 * abs(g_a)) / (400.0 - abs(g_a)))
    g_c = signum(g_a) * (100.0 / viewing_conditions.fl) * pow(g_c_base, 1.0 / 0.42)
    b_c_base = max(0, (27.13 * abs(b_a)) / (400.0 - abs(b_a)))
    b_c = signum(b_a) * (100.0 / viewing_conditions.fl) * pow(b_c_base, 1.0 / 0.42)
    r_f = r_c / viewing_conditions.rgb_d[0]
    g_f = g_c / viewing_conditions.rgb_d[1]
    b_f = b_c / viewing_conditions.rgb_d[2]
    
    x = 1.86206786 * r_f - 1.01125463 * g_f + 0.14918677 * b_f
    y = 0.38752654 * r_f + 0.62144744 * g_f - 0.00897398 * b_f
    z = -0.01584150 * r_f - 0.03412294 * g_f + 1.04996444 * b_f
    
    from PyMCUlib_cpp.utils.utils import Vec3
    return Vec3(x, y, z)

def in_viewing_conditions(hct, vc):
    """
    Transforms a color from default viewing conditions to specified viewing conditions.
    
    Args:
        hct: The HCT color
        vc: The viewing conditions
        
    Returns:
        HCT color transformed to specified viewing conditions
    """
    # 1. Use CAM16 to find XYZ coordinates of color in specified VC.
    cam16 = cam_from_int(hct.to_int())
    viewed_in_vc = xyz_in_viewing_conditions(cam16, vc)
    
    # 2. Create CAM16 of those XYZ coordinates in default VC.
    recast_in_vc = cam_from_xyz_and_viewing_conditions(
        viewed_in_vc.a, viewed_in_vc.b, viewed_in_vc.c, DEFAULT_VIEWING_CONDITIONS)
    
    # 3. Create HCT from:
    # - CAM16 using default VC with XYZ coordinates in specified VC.
    # - L* converted from Y in XYZ coordinates in specified VC.
    recast_hct = Hct.from_hct(
        recast_in_vc.hue, recast_in_vc.chroma, lstar_from_y(viewed_in_vc.b))
    
    return recast_hct

def find_desired_chroma_by_tone(hue, chroma, tone, by_decreasing_tone):
    """
    Finds the desired chroma for a given tone.
    
    Args:
        hue: The hue
        chroma: The target chroma
        tone: The tone
        by_decreasing_tone: Whether to decrease tone to find max chroma
        
    Returns:
        The tone that can achieve the desired chroma
    """
    answer = tone
    
    closest_to_chroma = Hct.from_hct(hue, chroma, tone)
    if closest_to_chroma.get_chroma() < chroma:
        chroma_peak = closest_to_chroma.get_chroma()
        while closest_to_chroma.get_chroma() < chroma:
            answer += -1.0 if by_decreasing_tone else 1.0
            potential_solution = Hct.from_hct(hue, chroma, answer)
            if chroma_peak > potential_solution.get_chroma():
                break
            if abs(potential_solution.get_chroma() - chroma) < 0.4:
                break
            
            potential_delta = abs(potential_solution.get_chroma() - chroma)
            current_delta = abs(closest_to_chroma.get_chroma() - chroma)
            if potential_delta < current_delta:
                closest_to_chroma = potential_solution
            chroma_peak = max(chroma_peak, potential_solution.get_chroma())
    
    return answer

# Constants
CONTENT_ACCENT_TONE_DELTA = 15.0

def highest_surface(s):
    """Returns the highest surface in a scheme."""
    return MaterialDynamicColors.surface_bright() if s.is_dark else MaterialDynamicColors.surface_dim()

class MaterialDynamicColors:
    """
    Material dynamic colors - provides a color scheme for dynamic colors.
    """
    
    # Compatibility Keys Colors for Android
    @staticmethod
    def primary_palette_key_color():
        """Returns the key color for the primary palette."""
        return DynamicColor.from_palette(
            "primary_palette_key_color",
            lambda s: s.primary_palette,
            lambda s: s.primary_palette.get_key_color().get_tone())
    
    @staticmethod
    def secondary_palette_key_color():
        """Returns the key color for the secondary palette."""
        return DynamicColor.from_palette(
            "secondary_palette_key_color",
            lambda s: s.secondary_palette,
            lambda s: s.secondary_palette.get_key_color().get_tone())
    
    @staticmethod
    def tertiary_palette_key_color():
        """Returns the key color for the tertiary palette."""
        return DynamicColor.from_palette(
            "tertiary_palette_key_color",
            lambda s: s.tertiary_palette,
            lambda s: s.tertiary_palette.get_key_color().get_tone())
    
    @staticmethod
    def neutral_palette_key_color():
        """Returns the key color for the neutral palette."""
        return DynamicColor.from_palette(
            "neutral_palette_key_color",
            lambda s: s.neutral_palette,
            lambda s: s.neutral_palette.get_key_color().get_tone())
    
    @staticmethod
    def neutral_variant_palette_key_color():
        """Returns the key color for the neutral variant palette."""
        return DynamicColor.from_palette(
            "neutral_variant_palette_key_color",
            lambda s: s.neutral_variant_palette,
            lambda s: s.neutral_variant_palette.get_key_color().get_tone())
    
    @staticmethod
    def background():
        """Returns the background dynamic color."""
        return DynamicColor(
            name="background",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: 6.0 if s.is_dark else 98.0,
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def on_background():
        """Returns the on-background dynamic color."""
        return DynamicColor(
            name="on_background",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: 90.0 if s.is_dark else 10.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.background(),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 3.0, 4.5, 7.0),
            tone_delta_pair=None)
    
    @staticmethod
    def surface():
        """Returns the surface dynamic color."""
        return DynamicColor(
            name="surface",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: 6.0 if s.is_dark else 98.0,
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def surface_dim():
        """Returns the dim surface dynamic color."""
        return DynamicColor(
            name="surface_dim",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: 6.0 if s.is_dark else
                ContrastCurve(87.0, 87.0, 80.0, 75.0).get(s.contrast_level),
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def surface_bright():
        """Returns the bright surface dynamic color."""
        return DynamicColor(
            name="surface_bright",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: ContrastCurve(24.0, 24.0, 29.0, 34.0).get(s.contrast_level)
                if s.is_dark else 98.0,
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def surface_container_lowest():
        """Returns the lowest container surface dynamic color."""
        return DynamicColor(
            name="surface_container_lowest",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: ContrastCurve(4.0, 4.0, 2.0, 0.0).get(s.contrast_level)
                if s.is_dark else 100.0,
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def surface_container_low():
        """Returns the low container surface dynamic color."""
        return DynamicColor(
            name="surface_container_low",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: ContrastCurve(10.0, 10.0, 11.0, 12.0).get(s.contrast_level)
                if s.is_dark else ContrastCurve(96.0, 96.0, 96.0, 95.0).get(s.contrast_level),
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def surface_container():
        """Returns the container surface dynamic color."""
        return DynamicColor(
            name="surface_container",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: ContrastCurve(12.0, 12.0, 16.0, 20.0).get(s.contrast_level)
                if s.is_dark else ContrastCurve(94.0, 94.0, 92.0, 90.0).get(s.contrast_level),
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def surface_container_high():
        """Returns the high container surface dynamic color."""
        return DynamicColor(
            name="surface_container_high",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: ContrastCurve(17.0, 17.0, 21.0, 25.0).get(s.contrast_level)
                if s.is_dark else ContrastCurve(92.0, 92.0, 88.0, 85.0).get(s.contrast_level),
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def surface_container_highest():
        """Returns the highest container surface dynamic color."""
        return DynamicColor(
            name="surface_container_highest",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: ContrastCurve(22.0, 22.0, 26.0, 30.0).get(s.contrast_level)
                if s.is_dark else ContrastCurve(90.0, 90.0, 84.0, 80.0).get(s.contrast_level),
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def on_surface():
        """Returns the on-surface dynamic color."""
        return DynamicColor(
            name="on_surface",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: 90.0 if s.is_dark else 10.0,
            is_background=False,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=None)
    
    @staticmethod
    def surface_variant():
        """Returns the surface variant dynamic color."""
        return DynamicColor(
            name="surface_variant",
            palette=lambda s: s.neutral_variant_palette,
            tone=lambda s: 30.0 if s.is_dark else 90.0,
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def on_surface_variant():
        """Returns the on-surface variant dynamic color."""
        return DynamicColor(
            name="on_surface_variant",
            palette=lambda s: s.neutral_variant_palette,
            tone=lambda s: 80.0 if s.is_dark else 30.0,
            is_background=False,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None)
    
    @staticmethod
    def inverse_surface():
        """Returns the inverse surface dynamic color."""
        return DynamicColor(
            name="inverse_surface",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: 90.0 if s.is_dark else 20.0,
            is_background=False,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def inverse_on_surface():
        """Returns the inverse on-surface dynamic color."""
        return DynamicColor(
            name="inverse_on_surface",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: 20.0 if s.is_dark else 95.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.inverse_surface(),
            second_background=None,
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=None)
    
    @staticmethod
    def outline():
        """Returns the outline dynamic color."""
        return DynamicColor(
            name="outline",
            palette=lambda s: s.neutral_variant_palette,
            tone=lambda s: 60.0 if s.is_dark else 50.0,
            is_background=False,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.5, 3.0, 4.5, 7.0),
            tone_delta_pair=None)
    
    @staticmethod
    def outline_variant():
        """Returns the outline variant dynamic color."""
        return DynamicColor(
            name="outline_variant",
            palette=lambda s: s.neutral_variant_palette,
            tone=lambda s: 30.0 if s.is_dark else 80.0,
            is_background=False,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=None)
    
    @staticmethod
    def shadow():
        """Returns the shadow dynamic color."""
        return DynamicColor(
            name="shadow",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: 0.0,
            is_background=False,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def scrim():
        """Returns the scrim dynamic color."""
        return DynamicColor(
            name="scrim",
            palette=lambda s: s.neutral_palette,
            tone=lambda s: 0.0,
            is_background=False,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def surface_tint():
        """Returns the surface tint dynamic color."""
        return DynamicColor(
            name="surface_tint",
            palette=lambda s: s.primary_palette,
            tone=lambda s: 80.0 if s.is_dark else 40.0,
            is_background=True,
            background=None,
            second_background=None,
            contrast_curve=None,
            tone_delta_pair=None)
    
    @staticmethod
    def primary():
        """Returns the primary dynamic color."""
        return DynamicColor(
            name="primary",
            palette=lambda s: s.primary_palette,
            tone=lambda s: 100.0 if is_monochrome(s) and s.is_dark else
                  0.0 if is_monochrome(s) else
                  80.0 if s.is_dark else 40.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 7.0),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.primary_container(),
                MaterialDynamicColors.primary(),
                10.0, TonePolarity.NEARER, False))
    
    @staticmethod
    def on_primary():
        """Returns the on-primary dynamic color."""
        return DynamicColor(
            name="on_primary",
            palette=lambda s: s.primary_palette,
            tone=lambda s: 10.0 if is_monochrome(s) and s.is_dark else
                  90.0 if is_monochrome(s) else
                  20.0 if s.is_dark else 100.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.primary(),
            second_background=None,
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=None)
    
    @staticmethod
    def primary_container():
        """Returns the primary container dynamic color."""
        return DynamicColor(
            name="primary_container",
            palette=lambda s: s.primary_palette,
            tone=lambda s: s.source_color_hct.get_tone() if is_fidelity(s) else
                  85.0 if is_monochrome(s) and s.is_dark else
                  25.0 if is_monochrome(s) else
                  30.0 if s.is_dark else 90.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.primary_container(),
                MaterialDynamicColors.primary(),
                10.0, TonePolarity.NEARER, False))
    
    @staticmethod
    def on_primary_container():
        """Returns the on-primary-container dynamic color."""
        return DynamicColor(
            name="on_primary_container",
            palette=lambda s: s.primary_palette,
            tone=lambda s: foreground_tone(
                MaterialDynamicColors.primary_container().tone(s), 4.5
            ) if is_fidelity(s) else
                0.0 if is_monochrome(s) and s.is_dark else
                100.0 if is_monochrome(s) else
                90.0 if s.is_dark else 30.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.primary_container(),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None)
    
    @staticmethod
    def inverse_primary():
        """Returns the inverse primary dynamic color."""
        return DynamicColor(
            name="inverse_primary",
            palette=lambda s: s.primary_palette,
            tone=lambda s: 40.0 if s.is_dark else 80.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.inverse_surface(),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 7.0),
            tone_delta_pair=None)
    
    @staticmethod
    def secondary():
        """Returns the secondary dynamic color."""
        return DynamicColor(
            name="secondary",
            palette=lambda s: s.secondary_palette,
            tone=lambda s: 80.0 if s.is_dark else 40.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 7.0),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.secondary_container(),
                MaterialDynamicColors.secondary(),
                10.0, TonePolarity.NEARER, False))
    
    @staticmethod
    def on_secondary():
        """Returns the on-secondary dynamic color."""
        return DynamicColor(
            name="on_secondary",
            palette=lambda s: s.secondary_palette,
            tone=lambda s: 10.0 if is_monochrome(s) and s.is_dark else
                  100.0 if is_monochrome(s) else
                  20.0 if s.is_dark else 100.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.secondary(),
            second_background=None,
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=None)
    
    @staticmethod
    def secondary_container():
        """Returns the secondary container dynamic color."""
        return DynamicColor(
            name="secondary_container",
            palette=lambda s: s.secondary_palette,
            tone=lambda s: 30.0 if is_monochrome(s) and s.is_dark else
                  85.0 if is_monochrome(s) else
                  find_desired_chroma_by_tone(
                      s.secondary_palette.get_hue(),
                      s.secondary_palette.get_chroma(),
                      90.0 if not s.is_dark else 30.0,
                      not s.is_dark
                  ) if is_fidelity(s) else
                  30.0 if s.is_dark else 90.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.secondary_container(),
                MaterialDynamicColors.secondary(),
                10.0, TonePolarity.NEARER, False))
    
    @staticmethod
    def on_secondary_container():
        """Returns the on-secondary-container dynamic color."""
        return DynamicColor(
            name="on_secondary_container",
            palette=lambda s: s.secondary_palette,
            tone=lambda s: 90.0 if is_monochrome(s) and s.is_dark else
                  10.0 if is_monochrome(s) else
                  foreground_tone(MaterialDynamicColors.secondary_container().tone(s), 4.5)
                  if is_fidelity(s) else
                  90.0 if s.is_dark else 30.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.secondary_container(),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None)
    
    @staticmethod
    def tertiary():
        """Returns the tertiary dynamic color."""
        return DynamicColor(
            name="tertiary",
            palette=lambda s: s.tertiary_palette,
            tone=lambda s: 90.0 if is_monochrome(s) and s.is_dark else
                  25.0 if is_monochrome(s) else
                  80.0 if s.is_dark else 40.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 7.0),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.tertiary_container(),
                MaterialDynamicColors.tertiary(),
                10.0, TonePolarity.NEARER, False))
    
    @staticmethod
    def on_tertiary():
        """Returns the on-tertiary dynamic color."""
        return DynamicColor(
            name="on_tertiary",
            palette=lambda s: s.tertiary_palette,
            tone=lambda s: 10.0 if is_monochrome(s) and s.is_dark else
                  90.0 if is_monochrome(s) else
                  20.0 if s.is_dark else 100.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.tertiary(),
            second_background=None,
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=None)
    
    @staticmethod
    def tertiary_container():
        """Returns the tertiary container dynamic color."""
        return DynamicColor(
            name="tertiary_container",
            palette=lambda s: s.tertiary_palette,
            tone=lambda s: 60.0 if is_monochrome(s) and s.is_dark else
                  49.0 if is_monochrome(s) else
                  fix_if_disliked(
                      Hct.from_int(s.tertiary_palette.get(s.source_color_hct.get_tone()))
                  ).get_tone() if is_fidelity(s) else
                  30.0 if s.is_dark else 90.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.tertiary_container(),
                MaterialDynamicColors.tertiary(),
                10.0, TonePolarity.NEARER, False))
    
    @staticmethod
    def on_tertiary_container():
        """Returns the on-tertiary-container dynamic color."""
        return DynamicColor(
            name="on_tertiary_container",
            palette=lambda s: s.tertiary_palette,
            tone=lambda s: 0.0 if is_monochrome(s) and s.is_dark else
                  100.0 if is_monochrome(s) else
                  foreground_tone(MaterialDynamicColors.tertiary_container().tone(s), 4.5)
                  if is_fidelity(s) else
                  90.0 if s.is_dark else 30.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.tertiary_container(),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None)
    
    @staticmethod
    def error():
        """Returns the error dynamic color."""
        return DynamicColor(
            name="error",
            palette=lambda s: s.error_palette,
            tone=lambda s: 80.0 if s.is_dark else 40.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 7.0),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.error_container(),
                MaterialDynamicColors.error(),
                10.0, TonePolarity.NEARER, False))
    
    @staticmethod
    def on_error():
        """Returns the on-error dynamic color."""
        return DynamicColor(
            name="on_error",
            palette=lambda s: s.error_palette,
            tone=lambda s: 20.0 if s.is_dark else 100.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.error(),
            second_background=None,
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=None)
    
    @staticmethod
    def error_container():
        """Returns the error container dynamic color."""
        return DynamicColor(
            name="error_container",
            palette=lambda s: s.error_palette,
            tone=lambda s: 30.0 if s.is_dark else 90.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.error_container(),
                MaterialDynamicColors.error(),
                10.0, TonePolarity.NEARER, False))
    
    @staticmethod
    def on_error_container():
        """Returns the on-error-container dynamic color."""
        return DynamicColor(
            name="on_error_container",
            palette=lambda s: s.error_palette,
            tone=lambda s: 90.0 if is_monochrome(s) and s.is_dark else
                  10.0 if is_monochrome(s) else
                  90.0 if s.is_dark else 30.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.error_container(),
            second_background=None,
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None)
    
    @staticmethod
    def primary_fixed():
        """Returns the primary fixed dynamic color."""
        return DynamicColor(
            name="primary_fixed",
            palette=lambda s: s.primary_palette,
            tone=lambda s: 40.0 if is_monochrome(s) else 90.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.primary_fixed(),
                MaterialDynamicColors.primary_fixed_dim(),
                10.0, TonePolarity.LIGHTER, True))
    
    @staticmethod
    def primary_fixed_dim():
        """Returns the primary fixed dim dynamic color."""
        return DynamicColor(
            name="primary_fixed_dim",
            palette=lambda s: s.primary_palette,
            tone=lambda s: 30.0 if is_monochrome(s) else 80.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.primary_fixed(),
                MaterialDynamicColors.primary_fixed_dim(),
                10.0, TonePolarity.LIGHTER, True))
    
    @staticmethod
    def on_primary_fixed():
        """Returns the on-primary-fixed dynamic color."""
        return DynamicColor(
            name="on_primary_fixed",
            palette=lambda s: s.primary_palette,
            tone=lambda s: 100.0 if is_monochrome(s) else 10.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.primary_fixed_dim(),
            second_background=lambda s: MaterialDynamicColors.primary_fixed(),
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=None)
    
    @staticmethod
    def on_primary_fixed_variant():
        """Returns the on-primary-fixed-variant dynamic color."""
        return DynamicColor(
            name="on_primary_fixed_variant",
            palette=lambda s: s.primary_palette,
            tone=lambda s: 90.0 if is_monochrome(s) else 30.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.primary_fixed_dim(),
            second_background=lambda s: MaterialDynamicColors.primary_fixed(),
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None)
    
    @staticmethod
    def secondary_fixed():
        """Returns the secondary fixed dynamic color."""
        return DynamicColor(
            name="secondary_fixed",
            palette=lambda s: s.secondary_palette,
            tone=lambda s: 80.0 if is_monochrome(s) else 90.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.secondary_fixed(),
                MaterialDynamicColors.secondary_fixed_dim(),
                10.0, TonePolarity.LIGHTER, True))
    
    @staticmethod
    def secondary_fixed_dim():
        """Returns the secondary fixed dim dynamic color."""
        return DynamicColor(
            name="secondary_fixed_dim",
            palette=lambda s: s.secondary_palette,
            tone=lambda s: 70.0 if is_monochrome(s) else 80.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.secondary_fixed(),
                MaterialDynamicColors.secondary_fixed_dim(),
                10.0, TonePolarity.LIGHTER, True))
    
    @staticmethod
    def on_secondary_fixed():
        """Returns the on-secondary-fixed dynamic color."""
        return DynamicColor(
            name="on_secondary_fixed",
            palette=lambda s: s.secondary_palette,
            tone=lambda s: 10.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.secondary_fixed_dim(),
            second_background=lambda s: MaterialDynamicColors.secondary_fixed(),
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=None)
    
    @staticmethod
    def on_secondary_fixed_variant():
        """Returns the on-secondary-fixed-variant dynamic color."""
        return DynamicColor(
            name="on_secondary_fixed_variant",
            palette=lambda s: s.secondary_palette,
            tone=lambda s: 25.0 if is_monochrome(s) else 30.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.secondary_fixed_dim(),
            second_background=lambda s: MaterialDynamicColors.secondary_fixed(),
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None)
    
    @staticmethod
    def tertiary_fixed():
        """Returns the tertiary fixed dynamic color."""
        return DynamicColor(
            name="tertiary_fixed",
            palette=lambda s: s.tertiary_palette,
            tone=lambda s: 40.0 if is_monochrome(s) else 90.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.tertiary_fixed(),
                MaterialDynamicColors.tertiary_fixed_dim(),
                10.0, TonePolarity.LIGHTER, True))
    
    @staticmethod
    def tertiary_fixed_dim():
        """Returns the tertiary fixed dim dynamic color."""
        return DynamicColor(
            name="tertiary_fixed_dim",
            palette=lambda s: s.tertiary_palette,
            tone=lambda s: 30.0 if is_monochrome(s) else 80.0,
            is_background=True,
            background=lambda s: highest_surface(s),
            second_background=None,
            contrast_curve=ContrastCurve(1.0, 1.0, 3.0, 4.5),
            tone_delta_pair=lambda s: ToneDeltaPair(
                MaterialDynamicColors.tertiary_fixed(),
                MaterialDynamicColors.tertiary_fixed_dim(),
                10.0, TonePolarity.LIGHTER, True))
    
    @staticmethod
    def on_tertiary_fixed():
        """Returns the on-tertiary-fixed dynamic color."""
        return DynamicColor(
            name="on_tertiary_fixed",
            palette=lambda s: s.tertiary_palette,
            tone=lambda s: 100.0 if is_monochrome(s) else 10.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.tertiary_fixed_dim(),
            second_background=lambda s: MaterialDynamicColors.tertiary_fixed(),
            contrast_curve=ContrastCurve(4.5, 7.0, 11.0, 21.0),
            tone_delta_pair=None)
    
    @staticmethod
    def on_tertiary_fixed_variant():
        """Returns the on-tertiary-fixed-variant dynamic color."""
        return DynamicColor(
            name="on_tertiary_fixed_variant",
            palette=lambda s: s.tertiary_palette,
            tone=lambda s: 90.0 if is_monochrome(s) else 30.0,
            is_background=False,
            background=lambda s: MaterialDynamicColors.tertiary_fixed_dim(),
            second_background=lambda s: MaterialDynamicColors.tertiary_fixed(),
            contrast_curve=ContrastCurve(3.0, 4.5, 7.0, 11.0),
            tone_delta_pair=None)
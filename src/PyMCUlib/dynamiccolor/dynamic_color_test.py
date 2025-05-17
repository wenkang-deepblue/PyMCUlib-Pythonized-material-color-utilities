# dynamiccolor/dynamic_color_test.py

import unittest
from typing import List

from PyMCUlib.contrast.contrast import Contrast
from PyMCUlib.dynamiccolor.contrast_curve import ContrastCurve
from PyMCUlib.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from PyMCUlib.hct.hct import Hct
from PyMCUlib.scheme.scheme_content import SchemeContent
from PyMCUlib.scheme.scheme_expressive import SchemeExpressive
from PyMCUlib.scheme.scheme_fidelity import SchemeFidelity
from PyMCUlib.scheme.scheme_monochrome import SchemeMonochrome
from PyMCUlib.scheme.scheme_neutral import SchemeNeutral
from PyMCUlib.scheme.scheme_tonal_spot import SchemeTonalSpot
from PyMCUlib.scheme.scheme_vibrant import SchemeVibrant
from PyMCUlib.utils import color_utils

class Pair:
    """A pair of foreground and background colors."""
    def __init__(self, fg_name: str, bg_name: str):
        self.fg_name = fg_name
        self.bg_name = bg_name


class DynamicColorTest(unittest.TestCase):
    def setUp(self):
        # Generate seed colors
        self.seed_colors = [
            Hct.from_int(0xFFFF0000),
            Hct.from_int(0xFFFFFF00),
            Hct.from_int(0xFF00FF00),
            Hct.from_int(0xFF0000FF),
        ]

        # Define MaterialDynamicColors
        self.colors = [
            MaterialDynamicColors.background,
            MaterialDynamicColors.on_background,
            MaterialDynamicColors.surface,
            MaterialDynamicColors.surface_dim,
            MaterialDynamicColors.surface_bright,
            MaterialDynamicColors.surface_container_lowest,
            MaterialDynamicColors.surface_container_low,
            MaterialDynamicColors.surface_container,
            MaterialDynamicColors.surface_container_high,
            MaterialDynamicColors.surface_container_highest,
            MaterialDynamicColors.on_surface,
            MaterialDynamicColors.surface_variant,
            MaterialDynamicColors.on_surface_variant,
            MaterialDynamicColors.inverse_surface,
            MaterialDynamicColors.inverse_on_surface,
            MaterialDynamicColors.outline,
            MaterialDynamicColors.outline_variant,
            MaterialDynamicColors.shadow,
            MaterialDynamicColors.scrim,
            MaterialDynamicColors.surface_tint,
            MaterialDynamicColors.primary,
            MaterialDynamicColors.on_primary,
            MaterialDynamicColors.primary_container,
            MaterialDynamicColors.on_primary_container,
            MaterialDynamicColors.inverse_primary,
            MaterialDynamicColors.secondary,
            MaterialDynamicColors.on_secondary,
            MaterialDynamicColors.secondary_container,
            MaterialDynamicColors.on_secondary_container,
            MaterialDynamicColors.tertiary,
            MaterialDynamicColors.on_tertiary,
            MaterialDynamicColors.tertiary_container,
            MaterialDynamicColors.on_tertiary_container,
            MaterialDynamicColors.error,
            MaterialDynamicColors.on_error,
            MaterialDynamicColors.error_container,
            MaterialDynamicColors.on_error_container,
            MaterialDynamicColors.primary_fixed,
            MaterialDynamicColors.primary_fixed_dim,
            MaterialDynamicColors.on_primary_fixed,
            MaterialDynamicColors.on_primary_fixed_variant,
            MaterialDynamicColors.secondary_fixed,
            MaterialDynamicColors.secondary_fixed_dim,
            MaterialDynamicColors.on_secondary_fixed,
            MaterialDynamicColors.on_secondary_fixed_variant,
            MaterialDynamicColors.tertiary_fixed,
            MaterialDynamicColors.tertiary_fixed_dim,
            MaterialDynamicColors.on_tertiary_fixed,
            MaterialDynamicColors.on_tertiary_fixed_variant,
        ]

        # Create a name-to-color map
        self.color_by_name = {color.name: color for color in self.colors}

        # Define text-surface pairs for testing
        self.text_surface_pairs = [
            Pair("on_primary", "primary"),
            Pair("on_primary_container", "primary_container"),
            Pair("on_secondary", "secondary"),
            Pair("on_secondary_container", "secondary_container"),
            Pair("on_tertiary", "tertiary"),
            Pair("on_tertiary_container", "tertiary_container"),
            Pair("on_error", "error"),
            Pair("on_error_container", "error_container"),
            Pair("on_background", "background"),
            Pair("on_surface_variant", "surface_bright"),
            Pair("on_surface_variant", "surface_dim"),
        ]

        # Generate all schemes for testing
        self.schemes = []
        for color in self.seed_colors:
            for contrast_level in [-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0]:
                for is_dark in [False, True]:
                    self.schemes.extend([
                        SchemeContent(color, is_dark, contrast_level),
                        SchemeExpressive(color, is_dark, contrast_level),
                        SchemeFidelity(color, is_dark, contrast_level),
                        SchemeMonochrome(color, is_dark, contrast_level),
                        SchemeNeutral(color, is_dark, contrast_level),
                        SchemeTonalSpot(color, is_dark, contrast_level),
                        SchemeVibrant(color, is_dark, contrast_level),
                    ])

    def test_generates_colors_respecting_contrast(self):
        """Test that dynamic schemes respect contrast between text-surface pairs."""
        for scheme in self.schemes:
            for pair in self.text_surface_pairs:
                # Get color names
                fg_name = pair.fg_name
                bg_name = pair.bg_name
                
                # Get foreground and background tones
                foreground_tone = self.color_by_name[fg_name].get_hct(scheme).tone
                background_tone = self.color_by_name[bg_name].get_hct(scheme).tone
                
                # Calculate contrast
                contrast = Contrast.ratio_of_tones(foreground_tone, background_tone)
                
                # Determine minimum requirement based on contrast level
                minimum_requirement = 4.5 if scheme.contrast_level >= 0.0 else 3.0
                
                # Assert that the contrast meets the requirement
                self.assertGreaterEqual(
                    contrast, 
                    minimum_requirement, 
                    f"{fg_name} on {bg_name} is {contrast}, needed {minimum_requirement}"
                )

    def get_min_requirement(self, curve: ContrastCurve, level: float) -> float:
        """Helper function to get minimum contrast requirement based on level."""
        if level >= 1:
            return curve.high
        if level >= 0.5:
            return curve.medium
        if level >= 0:
            return curve.normal
        return curve.low

    def get_pairs(self, resp: bool, fores: List[str], backs: List[str]) -> List[List[str]]:
        """Helper function to generate testing pairs."""
        ans = []
        if resp:
            for i in range(len(fores)):
                ans.append([fores[i], backs[i]])
        else:
            for f in fores:
                for b in backs:
                    ans.append([f, b])
        return ans

    def test_constraint_conformance(self):
        """Test that color constraints are satisfied."""
        # Define limiting surfaces for testing
        limiting_surfaces = [
            'surface_dim',
            'surface_bright',
        ]

        # Define constraints for testing
        constraints = [
            # Contrast constraints
            {
                'kind': 'Contrast',
                'values': ContrastCurve(4.5, 7, 11, 21),
                'fore': ['on_surface'],
                'back': limiting_surfaces,
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(3, 4.5, 7, 11),
                'fore': ['on_surface_variant'],
                'back': limiting_surfaces,
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(3, 4.5, 7, 7),
                'fore': ['primary', 'secondary', 'tertiary', 'error'],
                'back': limiting_surfaces,
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(1.5, 3, 4.5, 7),
                'fore': ['outline'],
                'back': limiting_surfaces,
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(0, 0, 3, 4.5),
                'fore': [
                    'primary_container',
                    'primary_fixed',
                    'primary_fixed_dim',
                    'secondary_container',
                    'secondary_fixed',
                    'secondary_fixed_dim',
                    'tertiary_container',
                    'tertiary_fixed',
                    'tertiary_fixed_dim',
                    'error_container',
                    'outline_variant',
                ],
                'back': limiting_surfaces,
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(4.5, 7, 11, 21),
                'fore': ['inverse_on_surface'],
                'back': ['inverse_surface'],
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(3, 4.5, 7, 7),
                'fore': ['inverse_primary'],
                'back': ['inverse_surface'],
            },
            # Accent contrast constraints
            {
                'kind': 'Contrast',
                'respectively': True,
                'values': ContrastCurve(4.5, 7, 11, 21),
                'fore': [
                    'on_primary',
                    'on_secondary',
                    'on_tertiary',
                    'on_error',
                ],
                'back': [
                    'primary',
                    'secondary',
                    'tertiary',
                    'error',
                ],
            },
            {
                'kind': 'Contrast',
                'respectively': True,
                'values': ContrastCurve(3, 4.5, 7, 11),
                'fore': [
                    'on_primary_container',
                    'on_secondary_container',
                    'on_tertiary_container',
                    'on_error_container',
                ],
                'back': [
                    'primary_container',
                    'secondary_container',
                    'tertiary_container',
                    'error_container',
                ],
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(4.5, 7, 11, 21),
                'fore': ['on_primary_fixed'],
                'back': ['primary_fixed', 'primary_fixed_dim'],
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(4.5, 7, 11, 21),
                'fore': ['on_secondary_fixed'],
                'back': ['secondary_fixed', 'secondary_fixed_dim'],
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(4.5, 7, 11, 21),
                'fore': ['on_tertiary_fixed'],
                'back': ['tertiary_fixed', 'tertiary_fixed_dim'],
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(3, 4.5, 7, 11),
                'fore': ['on_primary_fixed_variant'],
                'back': ['primary_fixed', 'primary_fixed_dim'],
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(3, 4.5, 7, 11),
                'fore': ['on_secondary_fixed_variant'],
                'back': ['secondary_fixed', 'secondary_fixed_dim'],
            },
            {
                'kind': 'Contrast',
                'values': ContrastCurve(3, 4.5, 7, 11),
                'fore': ['on_tertiary_fixed_variant'],
                'back': ['tertiary_fixed', 'tertiary_fixed_dim'],
            },
            # Delta constraints
            {
                'kind': 'Delta',
                'delta': 10,
                'respectively': True,
                'fore': [
                    'primary',
                    'secondary',
                    'tertiary',
                    'error',
                ],
                'back': [
                    'primary_container',
                    'secondary_container',
                    'tertiary_container',
                    'error_container',
                ],
                'polarity': 'farther',
            },
            {
                'kind': 'Delta',
                'delta': 10,
                'respectively': True,
                'fore': [
                    'primary_fixed_dim',
                    'secondary_fixed_dim',
                    'tertiary_fixed_dim',
                ],
                'back': [
                    'primary_fixed',
                    'secondary_fixed',
                    'tertiary_fixed',
                ],
                'polarity': 'darker',
            },
            # Background constraints
            {
                'kind': 'Background',
                'objects': [
                    'background',
                    'error',
                    'error_container',
                    'primary',
                    'primary_container',
                    'primary_fixed',
                    'primary_fixed_dim',
                    'secondary',
                    'secondary_container',
                    'secondary_fixed',
                    'secondary_fixed_dim',
                    'surface',
                    'surface_bright',
                    'surface_container',
                    'surface_container_high',
                    'surface_container_highest',
                    'surface_container_low',
                    'surface_container_lowest',
                    'surface_dim',
                    'surface_tint',
                    'surface_variant',
                    'tertiary',
                    'tertiary_container',
                    'tertiary_fixed',
                    'tertiary_fixed_dim',
                ],
            }
        ]

        # Test every scheme against all constraints
        for scheme in self.schemes:
            prec = 2  # Precision for floating-point comparisons
            
            # Get resolved colors
            resolved_colors = {color.name: color.get_argb(scheme) for color in self.colors}
            
            # Test each constraint
            for cstr in constraints:
                if cstr['kind'] == 'Contrast':
                    contrast_tolerance = 0.05
                    min_requirement = self.get_min_requirement(cstr['values'], scheme.contrast_level)
                    respectively = cstr.get('respectively', False)
                    pairs = self.get_pairs(respectively, cstr['fore'], cstr['back'])
                    
                    # Check each pair
                    for pair in pairs:
                        fore, back = pair
                        ftone = color_utils.lstar_from_argb(resolved_colors[fore])
                        btone = color_utils.lstar_from_argb(resolved_colors[back])
                        contrast = Contrast.ratio_of_tones(ftone, btone)
                        
                        # Determine if the test is failing
                        failing = False
                        if min_requirement <= 4.5:
                            failing = contrast < min_requirement - contrast_tolerance
                        else:
                            failing = (ftone != 0 and btone != 0 and ftone != 100 and btone != 100 and
                                      contrast < min_requirement - contrast_tolerance)
                        
                        # Assert based on different criteria
                        if contrast < min_requirement - contrast_tolerance and min_requirement <= 4.5:
                            self.fail(f"Contrast {fore} {ftone:.{prec}f} {back} {btone:.{prec}f} "
                                     f"{contrast:.{prec}f} {min_requirement}")
                        
                        if failing and min_requirement > 4.5:
                            self.fail(f"Contrast(stretch-goal) {fore} {ftone:.{prec}f} {back} "
                                     f"{btone:.{prec}f} {contrast:.{prec}f} {min_requirement}")
                
                elif cstr['kind'] == 'Delta':
                    respectively = cstr.get('respectively', False)
                    pairs = self.get_pairs(respectively, cstr['fore'], cstr['back'])
                    polarity = cstr['polarity']

                    # Assert polarity value is one of the allowed ones
                    self.assertIn(
                        polarity,
                        ('nearer', 'farther', 'lighter', 'darker'),
                        f"Invalid polarity value: {polarity}"
                    )
                    
                    # Check each delta constraint
                    for pair in pairs:
                        fore, back = pair
                        ftone = color_utils.lstar_from_argb(resolved_colors[fore])
                        btone = color_utils.lstar_from_argb(resolved_colors[back])
                        
                        is_lighter = (polarity == 'lighter' or
                                     (polarity == 'nearer' and not scheme.is_dark) or
                                     (polarity == 'farther' and scheme.is_dark))
                        
                        observed_delta = ftone - btone if is_lighter else btone - ftone
                        
                        if observed_delta < cstr['delta'] - 0.5:  # lenient check
                            self.fail(f"Delta {fore} {ftone:.{prec}f} {back} {btone:.{prec}f} "
                                     f"{observed_delta:.{prec}f} {cstr['delta']}")
                
                elif cstr['kind'] == 'Background':
                    # Check backgrounds aren't in the "awkward zone"
                    for bg in cstr['objects']:
                        bgtone = color_utils.lstar_from_argb(resolved_colors[bg])
                        if 50.5 <= bgtone < 59.5:  # lenient check
                            self.fail(f"Background {bg} {bgtone:.{prec}f}")
                
                else:
                    self.fail(f"Bad constraint kind = {cstr['kind']}")


if __name__ == '__main__':
    unittest.main()
"""
Material Color Utilities Python Library

A Python library for color operations and conversions, providing the HCT color space,
CAM16 color appearance model, and color blending tools.
"""

__version__ = "0.1.0"

# CAM and HCT
from PyMCUlib.cam.cam import (
    Cam, cam_from_int, int_from_cam, cam_from_ucs_and_viewing_conditions,
    ViewingConditions, DEFAULT_VIEWING_CONDITIONS, cam_from_jch_and_viewing_conditions,
    int_from_hcl, cam_from_xyz_and_viewing_conditions, cam_distance
)
from PyMCUlib.cam.hct import Hct
from PyMCUlib.cam.viewing_conditions import create_viewing_conditions, default_with_background_lstar
from PyMCUlib.cam.hct_solver import solve_to_int, solve_to_cam

# Blend
from PyMCUlib.blend.blend import blend_harmonize, blend_hct_hue, blend_cam16_ucs

# Utils
from PyMCUlib.utils.utils import (
    Argb, Vec3, PI, argb_from_rgb, red_from_int, green_from_int, blue_from_int,
    alpha_from_int, is_opaque, linearized, delinearized, lstar_from_argb,
    lstar_from_y, y_from_lstar, argb_from_linrgb, sanitize_degrees_int,
    sanitize_degrees_double, diff_degrees, rotation_direction, hex_from_argb,
    int_from_lstar, signum, lerp, matrix_multiply
)
from PyMCUlib.utils.image_utils import (
    source_color_from_image, source_color_from_image_bytes,
    source_color_from_file, source_color_from_bytes
)

# Quantize
from PyMCUlib.quantize.lab import Lab, lab_from_int, int_from_lab
from PyMCUlib.quantize.wu import quantize_wu
from PyMCUlib.quantize.wsmeans import QuantizerResult, quantize_wsmeans
from PyMCUlib.quantize.celebi import quantize_celebi

# Schemes
from PyMCUlib.scheme.monochrome import SchemeMonochrome
from PyMCUlib.scheme.neutral import SchemeNeutral
from PyMCUlib.scheme.tonal_spot import SchemeTonalSpot
from PyMCUlib.scheme.vibrant import SchemeVibrant
from PyMCUlib.scheme.expressive import SchemeExpressive
from PyMCUlib.scheme.fidelity import SchemeFidelity
from PyMCUlib.scheme.content import SchemeContent
from PyMCUlib.scheme.rainbow import SchemeRainbow
from PyMCUlib.scheme.fruit_salad import SchemeFruitSalad

# Dynamic colors
from PyMCUlib.dynamiccolor.contrast_curve import ContrastCurve
from PyMCUlib.dynamiccolor.tone_delta_pair import TonePolarity, ToneDeltaPair
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.dynamiccolor.dynamic_color import (
    DynamicColor, foreground_tone, enable_light_foreground,
    tone_prefers_light_foreground, tone_allows_light_foreground
)
from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib.dynamiccolor.material_dynamic_colors import (
    MaterialDynamicColors, is_fidelity, is_monochrome
)

# Temperature
from PyMCUlib.temperature.temperature_cache import TemperatureCache

# Score
from PyMCUlib.score.score import ScoreOptions, ranked_suggestions

# Palettes
from PyMCUlib.palettes.tones import TonalPalette, KeyColor
from PyMCUlib.palettes.core import CorePalettes

# Contrast
from PyMCUlib.contrast.contrast import (
    ratio_of_ys, ratio_of_tones, lighter, darker,
    lighter_unsafe, darker_unsafe
)

# Dislike
from PyMCUlib.dislike.dislike import is_disliked, fix_if_disliked

# Define public APIs
__all__ = [
    # Version
    "__version__",
    
    # CAM and HCT
    "Cam", "cam_from_int", "int_from_cam", "cam_from_ucs_and_viewing_conditions",
    "cam_from_jch_and_viewing_conditions", "int_from_hcl", "cam_from_xyz_and_viewing_conditions",
    "cam_distance", "ViewingConditions", "DEFAULT_VIEWING_CONDITIONS",
    "Hct", "create_viewing_conditions", "default_with_background_lstar",
    "solve_to_int", "solve_to_cam",
    
    # Blend
    "blend_harmonize", "blend_hct_hue", "blend_cam16_ucs",
    
    # Utils
    "Argb", "Vec3", "PI", "argb_from_rgb", "red_from_int", "green_from_int", "blue_from_int",
    "alpha_from_int", "is_opaque", "linearized", "delinearized", "lstar_from_argb",
    "lstar_from_y", "y_from_lstar", "argb_from_linrgb", "sanitize_degrees_int",
    "sanitize_degrees_double", "diff_degrees", "rotation_direction", "hex_from_argb",
    "argb_from_hex", "int_from_lstar", "signum", "lerp", "matrix_multiply", "WHITE_POINT_D65",
    "source_color_from_image", "source_color_from_image_bytes",
    "source_color_from_file", "source_color_from_bytes",
    
    # Quantize
    "Lab", "lab_from_int", "int_from_lab", "quantize_wu", 
    "QuantizerResult", "quantize_wsmeans", "quantize_celebi",
    
    # Schemes
    "SchemeMonochrome", "SchemeNeutral", "SchemeTonalSpot", "SchemeVibrant",
    "SchemeExpressive", "SchemeFidelity", "SchemeContent", "SchemeRainbow", "SchemeFruitSalad",
    
    # Dynamic colors
    "ContrastCurve", "TonePolarity", "ToneDeltaPair", "Variant",
    "DynamicColor", "foreground_tone", "enable_light_foreground",
    "tone_prefers_light_foreground", "tone_allows_light_foreground",
    "DynamicScheme", "MaterialDynamicColors", "is_fidelity", "is_monochrome",
    
    # Temperature
    "TemperatureCache",
    
    # Score
    "ScoreOptions", "ranked_suggestions",
    
    # Palettes
    "TonalPalette", "KeyColor", "CorePalettes",
    
    # Contrast
    "ratio_of_ys", "ratio_of_tones", "lighter", "darker", "lighter_unsafe", "darker_unsafe",
    
    # Dislike
    "is_disliked", "fix_if_disliked"
]
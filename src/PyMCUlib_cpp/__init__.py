"""
Material Color Utilities Python Library

A Python library for color operations and conversions, providing the HCT color space,
CAM16 color appearance model, and color blending tools.
"""

__version__ = "1.0.3"

# CAM and HCT
from PyMCUlib_cpp.cam.cam import (
    Cam, cam_from_int, int_from_cam, cam_from_ucs_and_viewing_conditions,
    ViewingConditions, DEFAULT_VIEWING_CONDITIONS, cam_from_jch_and_viewing_conditions,
    int_from_hcl, cam_from_xyz_and_viewing_conditions, cam_distance
)
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.cam.viewing_conditions import create_viewing_conditions, default_with_background_lstar
from PyMCUlib_cpp.cam.hct_solver import solve_to_int, solve_to_cam

# Blend
from PyMCUlib_cpp.blend.blend import blend_harmonize, blend_hct_hue, blend_cam16_ucs

# Utils
from PyMCUlib_cpp.utils.utils import (
    Argb, Vec3, PI, argb_from_rgb, red_from_int, green_from_int, blue_from_int,
    alpha_from_int, is_opaque, linearized, delinearized, lstar_from_argb,
    lstar_from_y, y_from_lstar, argb_from_linrgb, sanitize_degrees_int,
    sanitize_degrees_double, diff_degrees, rotation_direction, hex_from_argb,
    int_from_lstar, signum, lerp, matrix_multiply, clamp_int, clamp_double,
    WHITE_POINT_D65
)
from PyMCUlib_cpp.utils.image_utils import (
    source_color_from_image, source_color_from_image_bytes,
    source_color_from_file, source_color_from_bytes
)

# Quantize
from PyMCUlib_cpp.quantize.lab import Lab, lab_from_int, int_from_lab
from PyMCUlib_cpp.quantize.wu import quantize_wu
from PyMCUlib_cpp.quantize.wsmeans import QuantizerResult, quantize_wsmeans
from PyMCUlib_cpp.quantize.celebi import quantize_celebi

# Schemes
from PyMCUlib_cpp.scheme.monochrome import SchemeMonochrome
from PyMCUlib_cpp.scheme.neutral import SchemeNeutral
from PyMCUlib_cpp.scheme.tonal_spot import SchemeTonalSpot
from PyMCUlib_cpp.scheme.vibrant import SchemeVibrant
from PyMCUlib_cpp.scheme.expressive import SchemeExpressive
from PyMCUlib_cpp.scheme.fidelity import SchemeFidelity
from PyMCUlib_cpp.scheme.content import SchemeContent
from PyMCUlib_cpp.scheme.rainbow import SchemeRainbow
from PyMCUlib_cpp.scheme.fruit_salad import SchemeFruitSalad

# Dynamic colors
from PyMCUlib_cpp.dynamiccolor.contrast_curve import ContrastCurve
from PyMCUlib_cpp.dynamiccolor.tone_delta_pair import TonePolarity, ToneDeltaPair
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.dynamiccolor.dynamic_color import (
    DynamicColor, foreground_tone, enable_light_foreground,
    tone_prefers_light_foreground, tone_allows_light_foreground
)
from PyMCUlib_cpp.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import (
    MaterialDynamicColors, is_fidelity, is_monochrome
)

# Temperature
from PyMCUlib_cpp.temperature.temperature_cache import TemperatureCache

# Score
from PyMCUlib_cpp.score.score import ScoreOptions, ranked_suggestions

# Palettes
from PyMCUlib_cpp.palettes.tones import TonalPalette, KeyColor
from PyMCUlib_cpp.palettes.core import CorePalettes

# Contrast
from PyMCUlib_cpp.contrast.contrast import (
    ratio_of_ys, ratio_of_tones, lighter, darker,
    lighter_unsafe, darker_unsafe
)

# Dislike
from PyMCUlib_cpp.dislike.dislike import is_disliked, fix_if_disliked

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
    "clamp_int", "clamp_double", "source_color_from_image", "source_color_from_image_bytes",
    "source_color_from_file", "source_color_from_bytes", "WHITE_POINT_D65",
    
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
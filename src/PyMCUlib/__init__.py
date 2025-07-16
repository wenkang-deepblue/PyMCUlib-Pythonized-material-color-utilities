"""
Material Color Utilities Python Library

A Python library for color operations and conversions, providing the HCT color space,
CAM16 color appearance model, and color blending tools.
"""

__version__ = "1.0.3"

# --- blend ---
from PyMCUlib.blend import Blend

# --- contrast ---
from PyMCUlib.contrast import Contrast

# --- dislike ---
from PyMCUlib.dislike import DislikeAnalyzer

# --- dynamiccolor ---
from PyMCUlib.dynamiccolor import (
    ColorSpecDelegate,
    SpecVersion,
    get_spec,
    ContrastCurve,
    DynamicColor,
    extend_spec_version,
    validate_extended_color,
    DynamicScheme,
    MaterialDynamicColors,
    ToneDeltaPair,
    DeltaConstraint,
    TonePolarity,
    Variant,
)

# --- hct ---
from PyMCUlib.hct import ViewingConditions, Cam16, HctSolver, Hct

# --- palettes ---
from PyMCUlib.palettes import TonalPalette, KeyColor, CorePalette, CorePalettes

# --- quantize ---
from PyMCUlib.quantize import (
    PointProvider,
    LabPointProvider,
    QuantizerMap,
    QuantizerWu,
    QuantizerWsmeans,
    QuantizerCelebi,
)

# --- scheme ---
from PyMCUlib.scheme import (
    Scheme,
    SchemeAndroid,
    SchemeNeutral,
    SchemeExpressive,
    SchemeTonalSpot,
    SchemeRainbow,
    SchemeContent,
    SchemeFidelity,
    SchemeVibrant,
    SchemeMonochrome,
    SchemeFruitSalad,
)

# --- score ---
from PyMCUlib.score import Score, ScoreOptions

# --- temperature ---
from PyMCUlib.temperature import TemperatureCache

# --- utils ---
from PyMCUlib.utils import (
    argb_from_rgb,
    argb_from_linrgb,
    alpha_from_argb,
    red_from_argb,
    green_from_argb,
    blue_from_argb,
    is_opaque,
    argb_from_xyz,
    xyz_from_argb,
    argb_from_lab,
    lab_from_argb,
    argb_from_lstar,
    lstar_from_argb,
    y_from_lstar,
    lstar_from_y,
    linearized,
    delinearized,
    white_point_d65,
    hex_from_argb,
    argb_from_hex,
    source_color_from_image,
    source_color_from_image_bytes,
    source_color_from_file,
    signum,
    lerp,
    clamp_int,
    clamp_double,
    sanitize_degrees_int,
    sanitize_degrees_double,
    rotation_direction,
    difference_degrees,
    matrix_multiply,
    CustomColor,
    ColorGroup,
    CustomColorGroup,
    Theme,
    ApplyThemeOptions,
    theme_from_source_color,
    theme_from_image,
    custom_color,
    apply_theme,
    set_scheme_properties,
)

__all__ = [
    # Version
    "__version__",

    # blend
    "Blend",

    # contrast
    "Contrast",

    # dislike
    "DislikeAnalyzer",

    # dynamiccolor
    "ColorSpecDelegate",
    "SpecVersion",
    "get_spec",
    "ContrastCurve",
    "DynamicColor",
    "extend_spec_version",
    "validate_extended_color",
    "DynamicScheme",
    "MaterialDynamicColors",
    "ToneDeltaPair",
    "DeltaConstraint",
    "TonePolarity",
    "Variant",

    # hct
    "ViewingConditions",
    "Cam16",
    "HctSolver",
    "Hct",

    # palettes
    "TonalPalette",
    "KeyColor",
    "CorePalette",
    "CorePalettes",

    # quantize
    "PointProvider",
    "LabPointProvider",
    "QuantizerMap",
    "QuantizerWu",
    "QuantizerWsmeans",
    "QuantizerCelebi",

    # scheme
    "Scheme",
    "SchemeAndroid",
    "SchemeNeutral",
    "SchemeExpressive",
    "SchemeTonalSpot",
    "SchemeRainbow",
    "SchemeContent",
    "SchemeFidelity",
    "SchemeVibrant",
    "SchemeMonochrome",
    "SchemeFruitSalad",

    # score
    "Score",
    "ScoreOptions",

    # temperature
    "TemperatureCache",

    # utils
    "argb_from_rgb",
    "argb_from_linrgb",
    "alpha_from_argb",
    "red_from_argb",
    "green_from_argb",
    "blue_from_argb",
    "is_opaque",
    "argb_from_xyz",
    "xyz_from_argb",
    "argb_from_lab",
    "lab_from_argb",
    "argb_from_lstar",
    "lstar_from_argb",
    "y_from_lstar",
    "lstar_from_y",
    "linearized",
    "delinearized",
    "white_point_d65",
    "hex_from_argb",
    "argb_from_hex",
    "source_color_from_image",
    "source_color_from_image_bytes",
    "source_color_from_file",
    "signum",
    "lerp",
    "clamp_int",
    "clamp_double",
    "sanitize_degrees_int",
    "sanitize_degrees_double",
    "rotation_direction",
    "difference_degrees",
    "matrix_multiply",
    "CustomColor",
    "ColorGroup",
    "CustomColorGroup",
    "Theme",
    "ApplyThemeOptions",
    "theme_from_source_color",
    "theme_from_image",
    "custom_color",
    "apply_theme",
    "set_scheme_properties",
]
# utils/__init__.py

# --- color_utils ---
from PyMCUlib.utils.color_utils import (
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
)

# --- string_utils ---
from PyMCUlib.utils.string_utils import (
    hex_from_argb,
    argb_from_hex,
)

# --- image_utils ---
from PyMCUlib.utils.image_utils import (
    source_color_from_image,
    source_color_from_image_bytes,
    source_color_from_file,
)

# --- math_utils ---
from PyMCUlib.utils.math_utils import (
    signum,
    lerp,
    clamp_int,
    clamp_double,
    sanitize_degrees_int,
    sanitize_degrees_double,
    rotation_direction,
    difference_degrees,
    matrix_multiply,
)

__all__ = [
    # color_utils
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
    # string_utils
    "hex_from_argb",
    "argb_from_hex",
    # image_utils
    "source_color_from_image",
    "source_color_from_image_bytes",
    "source_color_from_file",
    # math_utils
    "signum",
    "lerp",
    "clamp_int",
    "clamp_double",
    "sanitize_degrees_int",
    "sanitize_degrees_double",
    "rotation_direction",
    "difference_degrees",
    "matrix_multiply",
    # theme_utils
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

def theme_from_source_color(source: int, custom_colors=None):
    from PyMCUlib.utils.theme_utils import theme_from_source_color as _f
    return _f(source, custom_colors)

def theme_from_image(image, custom_colors=None):
    from PyMCUlib.utils.theme_utils import theme_from_image as _f
    return _f(image, custom_colors)

def custom_color(source: int, color):
    from PyMCUlib.utils.theme_utils import custom_color as _f
    return _f(source, color)

def apply_theme(theme, options=None):
    from PyMCUlib.utils.theme_utils import apply_theme as _f
    return _f(theme, options)

def set_scheme_properties(css_vars, scheme, suffix=""):
    from PyMCUlib.utils.theme_utils import set_scheme_properties as _f
    return _f(css_vars, scheme, suffix)

def __getattr__(name):
    if name == "CustomColor":
        from PyMCUlib.utils.theme_utils import CustomColor
        return CustomColor
    if name == "ColorGroup":
        from PyMCUlib.utils.theme_utils import ColorGroup
        return ColorGroup
    if name == "CustomColorGroup":
        from PyMCUlib.utils.theme_utils import CustomColorGroup
        return CustomColorGroup
    if name == "Theme":
        from PyMCUlib.utils.theme_utils import Theme
        return Theme
    if name == "ApplyThemeOptions":
        from PyMCUlib.utils.theme_utils import ApplyThemeOptions
        return ApplyThemeOptions
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __dir__():
    return sorted(list(globals().keys()) + __all__)
# utils/theme_utils.py

from typing import List, Dict, Any, TypedDict, Optional, Union
import re
from PIL import Image
from PyMCUlib.palettes.core_palette import CorePalette
from PyMCUlib.scheme.scheme import Scheme
from PyMCUlib.palettes.tonal_palette import TonalPalette
from PyMCUlib.blend.blend import Blend
from PyMCUlib.utils import image_utils
from PyMCUlib.utils import string_utils


class CustomColor(TypedDict):
    """Custom color used to pair with a theme"""
    value: int
    name: str
    blend: bool


class ColorGroup(TypedDict):
    """Color group containing main colors and container colors"""
    color: int
    onColor: int
    colorContainer: int
    onColorContainer: int


class CustomColorGroup(TypedDict):
    """Custom color group containing light and dark variants"""
    color: CustomColor
    value: int
    light: ColorGroup
    dark: ColorGroup


class Theme(TypedDict):
    """Theme containing color schemes and palettes"""
    source: int
    schemes: Dict[str, Any]  # Contains light and dark schemes
    palettes: Dict[str, TonalPalette]  # Contains various palettes
    customColors: List[CustomColorGroup]

class ApplyThemeOptions(TypedDict, total=False):
    """Options for apply_theme"""
    dark: bool
    target: Any
    brightnessSuffix: bool
    paletteTones: List[int]


def theme_from_source_color(
        source: int, custom_colors: List[CustomColor] = None) -> Theme:
    """
    Generate a theme from a source color

    Args:
        source: Source color in ARGB format
        custom_colors: Array of custom colors (optional)

    Returns:
        Theme object
    """
    if custom_colors is None:
        custom_colors = []

    palette = CorePalette.of(source)
    return {
        "source": source,
        "schemes": {
            "light": Scheme.light(source),
            "dark": Scheme.dark(source),
        },
        "palettes": {
            "primary": palette.a1,
            "secondary": palette.a2,
            "tertiary": palette.a3,
            "neutral": palette.n1,
            "neutralVariant": palette.n2,
            "error": palette.error,
        },
        "customColors": [custom_color(source, c) for c in custom_colors],
    }


def theme_from_image(
    image: Union[str, bytes, Image.Image],
    custom_colors: Optional[List[CustomColor]] = None) -> Theme:
    """
    Generate a theme from an image source

    Args:
        image: Image data (file path, bytes, or PIL Image)
        custom_colors: Array of custom colors (optional)

    Returns:
        Theme object
    """
    if custom_colors is None:
        custom_colors = []

    source = image_utils.source_color_from_image(image)
    return theme_from_source_color(source, custom_colors)


def custom_color(source: int, color: CustomColor) -> CustomColorGroup:
    """
    Generate custom color group from source and target color

    Args:
        source: Source color in ARGB format
        color: Custom color definition

    Returns:
        Custom color group

    Link: https://m3.material.io/styles/color/the-color-system/color-roles
    """
    value = color["value"]
    from_color = value
    to_color = source
    if color["blend"]:
        value = Blend.harmonize(from_color, to_color)

    palette = CorePalette.of(value)
    tones = palette.a1
    
    return {
        "color": color,
        "value": value,
        "light": {
            "color": tones.tone(40),
            "onColor": tones.tone(100),
            "colorContainer": tones.tone(90),
            "onColorContainer": tones.tone(10),
        },
        "dark": {
            "color": tones.tone(80),
            "onColor": tones.tone(20),
            "colorContainer": tones.tone(30),
            "onColorContainer": tones.tone(90),
        },
    }


def apply_theme(
    theme: Theme,
    options: Optional[ApplyThemeOptions] = None) -> Dict[str, str]:
    """
    Apply a theme to a target.
    
    This function is platform-specific and needs adaptation depending on
    the environment (web, mobile, etc.).

    Args:
        theme: Theme object
        options: Options for applying the theme
            - dark: Whether to use dark scheme (default: False)
            - target: Target to apply the theme to (platform-specific)
            - brightnessSuffix: Whether to add brightness suffixes (default: False)
            - paletteTones: List of tone values to include (optional)

    Returns:
        Dictionary of CSS variables
    """
    if options is None:
        options = {}
    
    # This is a placeholder implementation that returns CSS variables
    # The actual implementation will depend on the target platform
    
    is_dark = options.get("dark", False)
    scheme = theme["schemes"]["dark"] if is_dark else theme["schemes"]["light"]
    
    css_vars = {}
    
    # Add scheme properties
    for key, value in scheme.to_json().items():
        token = re.sub(r'([a-z])([A-Z])', r'\1-\2', key).lower()
        color = string_utils.hex_from_argb(value)
        css_vars[f"--md-sys-color-{token}"] = color
    
    # Add brightness suffix if specified
    if options.get("brightnessSuffix", False):
        for key, value in theme["schemes"]["dark"].to_json().items():
            token = re.sub(r'([a-z])([A-Z])', r'\1-\2', key).lower()
            color = string_utils.hex_from_argb(value)
            css_vars[f"--md-sys-color-{token}-dark"] = color
            
        for key, value in theme["schemes"]["light"].to_json().items():
            token = re.sub(r'([a-z])([A-Z])', r'\1-\2', key).lower()
            color = string_utils.hex_from_argb(value)
            css_vars[f"--md-sys-color-{token}-light"] = color
    
    # Add palette tones if specified
    palette_tones = options.get("paletteTones", [])
    if palette_tones:
        for key, palette in theme["palettes"].items():
            palette_key = re.sub(r'([a-z])([A-Z])', r'\1-\2', key).lower()
            for tone in palette_tones:
                token = f"--md-ref-palette-{palette_key}-{palette_key}{tone}"
                color = string_utils.hex_from_argb(palette.tone(tone))
                css_vars[token] = color
    
    return css_vars


def set_scheme_properties(
        css_vars: Dict[str, str],
        scheme: Any,
        suffix: str = "") -> Dict[str, str]:
    """
    Helper function to set CSS properties for a color scheme

    Args:
        css_vars: Dictionary of CSS variables to update
        scheme: Color scheme
        suffix: Optional suffix to append to CSS variable names

    Returns:
        Updated CSS variables dictionary
    """
    for key, value in scheme.to_json().items():
        token = re.sub(r'([a-z])([A-Z])', r'\1-\2', key).lower()
        color = string_utils.hex_from_argb(value)
        css_vars[f"--md-sys-color-{token}{suffix}"] = color
    
    return css_vars
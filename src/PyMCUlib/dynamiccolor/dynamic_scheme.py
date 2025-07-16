# dynamiccolor/dynamic_scheme.py

from typing import List, Literal, Optional, TypedDict

from PyMCUlib.dynamiccolor.color_spec import get_spec
from PyMCUlib.dynamiccolor.color_spec_delegate import SpecVersion
from PyMCUlib.dynamiccolor.dynamic_color import DynamicColor
from PyMCUlib.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from PyMCUlib.dynamiccolor.variant import Variant
from PyMCUlib.dislike.dislike_analyzer import DislikeAnalyzer
from PyMCUlib.hct.hct import Hct
from PyMCUlib.palettes.tonal_palette import TonalPalette
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.utils import math_utils


# The platform on which this scheme is intended to be used. Only used in the
# 2025 spec.
Platform = Literal['phone', 'watch']


class DynamicSchemeOptions(TypedDict, total=False):
    """
    Options for creating a DynamicScheme.
    
    Args:
        source_color_hct: The source color of the theme as an HCT color.
        variant: The variant, or style, of the theme.
        contrast_level: Value from -1 to 1. -1 represents minimum contrast, 0
            represents standard (i.e. the design as spec'd), and 1 represents maximum
            contrast.
        is_dark: Whether the scheme is in dark mode or light mode.
        platform: The platform on which this scheme is intended to be used.
        spec_version: The version of the design spec that this scheme is based on.
        primary_palette: Given a tone, produces a color. Hue and chroma of the
            color are specified in the design specification of the variant.
        secondary_palette: Given a tone, produces a color.
        tertiary_palette: Given a tone, produces a color.
        neutral_palette: Given a tone, produces a color.
        neutral_variant_palette: Given a tone, produces a color.
        error_palette: Given a tone, produces a color.
    """
    source_color_hct: Hct
    variant: Variant
    contrast_level: float
    is_dark: bool
    platform: Platform
    spec_version: SpecVersion
    primary_palette: TonalPalette
    secondary_palette: TonalPalette
    tertiary_palette: TonalPalette
    neutral_palette: TonalPalette
    neutral_variant_palette: TonalPalette
    error_palette: TonalPalette


class DynamicSchemePalettesDelegate:
    """
    A delegate that provides the palettes of a DynamicScheme.

    This is used to allow different implementations of the palette calculation
    logic for different spec versions.
    """
    def get_primary_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the primary palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        ...

    def get_secondary_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the secondary palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        ...

    def get_tertiary_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the tertiary palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        ...

    def get_neutral_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the neutral palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        ...

    def get_neutral_variant_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the neutral variant palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        ...

    def get_error_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> Optional[TonalPalette]:
        """
        Get the error palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette, or None if there's no error palette.
        """
        ...


class DynamicScheme:
    """
    Constructed by a set of values representing the current UI state (such as
    whether or not its dark theme, what the theme style is, etc.), and
    provides a set of TonalPalettes that can create colors that fit in
    with the theme style. Used by DynamicColor to resolve into a color.
    """

    def __init__(self, args: DynamicSchemeOptions):
        """
        Initialize a dynamic scheme.
        
        Args:
            args: Options for creating a DynamicScheme.
        """
        self.source_color_argb = args['source_color_hct'].to_int()
        self.variant = args['variant']
        self.contrast_level = args['contrast_level']
        self.is_dark = args['is_dark']
        self.platform = args.get('platform', 'phone')
        self.spec_version = args.get('spec_version', '2021')
        self.source_color_hct = args['source_color_hct']
        self.primary_palette = args.get('primary_palette') or get_spec(self.spec_version).get_primary_palette(
            self.variant, args['source_color_hct'], self.is_dark, self.platform,
            self.contrast_level)
        self.secondary_palette = args.get('secondary_palette') or get_spec(self.spec_version).get_secondary_palette(
            self.variant, args['source_color_hct'], self.is_dark, self.platform,
            self.contrast_level)
        self.tertiary_palette = args.get('tertiary_palette') or get_spec(self.spec_version).get_tertiary_palette(
            self.variant, args['source_color_hct'], self.is_dark, self.platform,
            self.contrast_level)
        self.neutral_palette = args.get('neutral_palette') or get_spec(self.spec_version).get_neutral_palette(
            self.variant, args['source_color_hct'], self.is_dark, self.platform,
            self.contrast_level)
        self.neutral_variant_palette = args.get('neutral_variant_palette') or get_spec(
            self.spec_version).get_neutral_variant_palette(
            self.variant, args['source_color_hct'], self.is_dark, self.platform,
            self.contrast_level)
        error_palette = args.get('error_palette') or get_spec(self.spec_version).get_error_palette(
            self.variant, args['source_color_hct'], self.is_dark, self.platform,
            self.contrast_level)
        self.error_palette = error_palette if error_palette else TonalPalette.from_hue_and_chroma(25.0, 84.0)
        
        self.colors = MaterialDynamicColors()

    def __str__(self) -> str:
        """
        Returns a string representation of the scheme.
        
        Returns:
            A string representation of the scheme.
        """
        return (
            f"Scheme: variant={Variant(self.variant).name}, "
            f"mode={'dark' if self.is_dark else 'light'}, "
            f"platform={self.platform}, "
            f"contrastLevel={self.contrast_level:.1f}, "
            f"seed={self.source_color_hct}, "
            f"specVersion={self.spec_version}"
        )

    @staticmethod
    def get_piecewise_hue(
            source_color_hct: Hct, hue_breakpoints: List[float], hues: List[float]) -> float:
        """
        Returns a new hue based on a piecewise function and input color hue.

        For example, for the following function:
        result = 26 if 0 <= hue < 101
        result = 39 if 101 <= hue < 210
        result = 28 if 210 <= hue < 360

        call the function as:

        hue_breakpoints = [0, 101, 210, 360]
        hues = [26, 39, 28]
        result = scheme.piecewise(hue, hue_breakpoints, hues)

        Args:
            source_color_hct: The input value.
            hue_breakpoints: The breakpoints, in sorted order. No default lower or
                upper bounds are assumed.
            hues: The hues that should be applied when source color's hue is >=
                the same index in hueBrakpoints array, and < the hue at the next index
                in hueBrakpoints array. Otherwise, the source color's hue is returned.
                
        Returns:
            A hue value.
        """
        size = min(len(hue_breakpoints) - 1, len(hues))
        source_hue = source_color_hct.hue
        for i in range(size):
            if source_hue >= hue_breakpoints[i] and source_hue < hue_breakpoints[i + 1]:
                return math_utils.sanitize_degrees_double(hues[i])
        # No condition matched, return the source hue.
        return source_hue

    @staticmethod
    def get_rotated_hue(
            source_color_hct: Hct, hue_breakpoints: List[float],
            rotations: List[float]) -> float:
        """
        Returns a shifted hue based on a piecewise function and input color hue.

        For example, for the following function:
        result = hue + 26 if 0 <= hue < 101
        result = hue - 39 if 101 <= hue < 210
        result = hue + 28 if 210 <= hue < 360

        call the function as:

        hue_breakpoints = [0, 101, 210, 360]
        hues = [26, -39, 28]
        result = scheme.get_rotated_hue(hue, hue_breakpoints, hues)

        Args:
            source_color_hct: the source color of the theme, in HCT.
            hue_breakpoints: The "breakpoints", i.e. the hues at which a rotation
                should be apply. No default lower or upper bounds are assumed.
            rotations: The rotation that should be applied when source color's
                hue is >= the same index in hues array, and < the hue at the next
                index in hues array. Otherwise, the source color's hue is returned.
                
        Returns:
            A hue value.
        """
        rotation = DynamicScheme.get_piecewise_hue(
            source_color_hct, hue_breakpoints, rotations)
        if min(len(hue_breakpoints) - 1, len(rotations)) <= 0:
            # No condition matched, return the source hue.
            rotation = 0
        return math_utils.sanitize_degrees_double(source_color_hct.hue + rotation)

    def get_argb(self, dynamic_color: DynamicColor) -> int:
        """
        Get the ARGB color for the given dynamic color.
        
        Args:
            dynamic_color: The dynamic color.
            
        Returns:
            An ARGB color as an integer.
        """
        return dynamic_color.get_argb(self)

    def get_hct(self, dynamic_color: DynamicColor) -> Hct:
        """
        Get the HCT color for the given dynamic color.
        
        Args:
            dynamic_color: The dynamic color.
            
        Returns:
            An HCT color.
        """
        return dynamic_color.get_hct(self)

    # Palette key colors

    @property
    def primary_palette_key_color(self) -> int:
        """
        Get the primary palette key color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.primary_palette_key_color())

    @property
    def secondary_palette_key_color(self) -> int:
        """
        Get the secondary palette key color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.secondary_palette_key_color())

    @property
    def tertiary_palette_key_color(self) -> int:
        """
        Get the tertiary palette key color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.tertiary_palette_key_color())

    @property
    def neutral_palette_key_color(self) -> int:
        """
        Get the neutral palette key color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.neutral_palette_key_color())

    @property
    def neutral_variant_palette_key_color(self) -> int:
        """
        Get the neutral variant palette key color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.neutral_variant_palette_key_color())

    @property
    def error_palette_key_color(self) -> int:
        """
        Get the error palette key color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.error_palette_key_color())

    # Surface colors

    @property
    def background(self) -> int:
        """
        Get the background color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.background())

    @property
    def on_background(self) -> int:
        """
        Get the on-background color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_background())

    @property
    def surface(self) -> int:
        """
        Get the surface color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface())

    @property
    def surface_dim(self) -> int:
        """
        Get the dim surface color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface_dim())

    @property
    def surface_bright(self) -> int:
        """
        Get the bright surface color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface_bright())

    @property
    def surface_container_lowest(self) -> int:
        """
        Get the lowest surface container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface_container_lowest())

    @property
    def surface_container_low(self) -> int:
        """
        Get the low surface container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface_container_low())

    @property
    def surface_container(self) -> int:
        """
        Get the surface container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface_container())

    @property
    def surface_container_high(self) -> int:
        """
        Get the high surface container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface_container_high())

    @property
    def surface_container_highest(self) -> int:
        """
        Get the highest surface container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface_container_highest())

    @property
    def on_surface(self) -> int:
        """
        Get the on-surface color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_surface())

    @property
    def surface_variant(self) -> int:
        """
        Get the surface variant color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface_variant())

    @property
    def on_surface_variant(self) -> int:
        """
        Get the on-surface variant color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_surface_variant())

    @property
    def inverse_surface(self) -> int:
        """
        Get the inverse surface color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.inverse_surface())

    @property
    def inverse_on_surface(self) -> int:
        """
        Get the inverse on-surface color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.inverse_on_surface())

    @property
    def outline(self) -> int:
        """
        Get the outline color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.outline())

    @property
    def outline_variant(self) -> int:
        """
        Get the outline variant color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.outline_variant())

    @property
    def shadow(self) -> int:
        """
        Get the shadow color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.shadow())

    @property
    def scrim(self) -> int:
        """
        Get the scrim color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.scrim())

    @property
    def surface_tint(self) -> int:
        """
        Get the surface tint color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.surface_tint())

    # Primary colors

    @property
    def primary(self) -> int:
        """
        Get the primary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.primary())

    @property
    def primary_dim(self) -> int:
        """
        Get the dim primary color.
        
        Returns:
            An ARGB color as an integer.
            
        Raises:
            ValueError: If the primary_dim color is undefined.
        """
        primary_dim = self.colors.primary_dim()
        if primary_dim is None:
            raise ValueError("`primary_dim` color is undefined prior to 2025 spec.")
        return self.get_argb(primary_dim)

    @property
    def on_primary(self) -> int:
        """
        Get the on-primary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_primary())

    @property
    def primary_container(self) -> int:
        """
        Get the primary container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.primary_container())

    @property
    def on_primary_container(self) -> int:
        """
        Get the on-primary container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_primary_container())

    @property
    def primary_fixed(self) -> int:
        """
        Get the fixed primary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.primary_fixed())

    @property
    def primary_fixed_dim(self) -> int:
        """
        Get the dim fixed primary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.primary_fixed_dim())

    @property
    def on_primary_fixed(self) -> int:
        """
        Get the on-fixed primary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_primary_fixed())

    @property
    def on_primary_fixed_variant(self) -> int:
        """
        Get the on-fixed variant primary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_primary_fixed_variant())

    @property
    def inverse_primary(self) -> int:
        """
        Get the inverse primary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.inverse_primary())

    # Secondary colors

    @property
    def secondary(self) -> int:
        """
        Get the secondary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.secondary())

    @property
    def secondary_dim(self) -> int:
        """
        Get the dim secondary color.
        
        Returns:
            An ARGB color as an integer.
            
        Raises:
            ValueError: If the secondary_dim color is undefined.
        """
        secondary_dim = self.colors.secondary_dim()
        if secondary_dim is None:
            raise ValueError("`secondary_dim` color is undefined prior to 2025 spec.")
        return self.get_argb(secondary_dim)

    @property
    def on_secondary(self) -> int:
        """
        Get the on-secondary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_secondary())

    @property
    def secondary_container(self) -> int:
        """
        Get the secondary container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.secondary_container())

    @property
    def on_secondary_container(self) -> int:
        """
        Get the on-secondary container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_secondary_container())

    @property
    def secondary_fixed(self) -> int:
        """
        Get the fixed secondary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.secondary_fixed())

    @property
    def secondary_fixed_dim(self) -> int:
        """
        Get the dim fixed secondary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.secondary_fixed_dim())

    @property
    def on_secondary_fixed(self) -> int:
        """
        Get the on-fixed secondary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_secondary_fixed())

    @property
    def on_secondary_fixed_variant(self) -> int:
        """
        Get the on-fixed variant secondary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_secondary_fixed_variant())

    # Tertiary colors

    @property
    def tertiary(self) -> int:
        """
        Get the tertiary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.tertiary())

    @property
    def tertiary_dim(self) -> int:
        """
        Get the dim tertiary color.
        
        Returns:
            An ARGB color as an integer.
            
        Raises:
            ValueError: If the tertiary_dim color is undefined.
        """
        tertiary_dim = self.colors.tertiary_dim()
        if tertiary_dim is None:
            raise ValueError("`tertiary_dim` color is undefined prior to 2025 spec.")
        return self.get_argb(tertiary_dim)

    @property
    def on_tertiary(self) -> int:
        """
        Get the on-tertiary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_tertiary())

    @property
    def tertiary_container(self) -> int:
        """
        Get the tertiary container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.tertiary_container())

    @property
    def on_tertiary_container(self) -> int:
        """
        Get the on-tertiary container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_tertiary_container())

    @property
    def tertiary_fixed(self) -> int:
        """
        Get the fixed tertiary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.tertiary_fixed())

    @property
    def tertiary_fixed_dim(self) -> int:
        """
        Get the dim fixed tertiary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.tertiary_fixed_dim())

    @property
    def on_tertiary_fixed(self) -> int:
        """
        Get the on-fixed tertiary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_tertiary_fixed())

    @property
    def on_tertiary_fixed_variant(self) -> int:
        """
        Get the on-fixed variant tertiary color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_tertiary_fixed_variant())

    # Error colors

    @property
    def error(self) -> int:
        """
        Get the error color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.error())

    @property
    def error_dim(self) -> int:
        """
        Get the dim error color.
        
        Returns:
            An ARGB color as an integer.
            
        Raises:
            ValueError: If the error_dim color is undefined.
        """
        error_dim = self.colors.error_dim()
        if error_dim is None:
            raise ValueError("`error_dim` color is undefined prior to 2025 spec.")
        return self.get_argb(error_dim)

    @property
    def on_error(self) -> int:
        """
        Get the on-error color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_error())

    @property
    def error_container(self) -> int:
        """
        Get the error container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.error_container())

    @property
    def on_error_container(self) -> int:
        """
        Get the on-error container color.
        
        Returns:
            An ARGB color as an integer.
        """
        return self.get_argb(self.colors.on_error_container())


class DynamicSchemePalettesDelegateImpl2021(DynamicSchemePalettesDelegate):
    """
    A delegate for the palettes of a DynamicScheme in the 2021 spec.
    """

    def get_primary_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the primary palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.CONTENT or variant == Variant.FIDELITY:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, source_color_hct.chroma)
        elif variant == Variant.FRUIT_SALAD:
            return TonalPalette.from_hue_and_chroma(
                math_utils.sanitize_degrees_double(source_color_hct.hue - 50.0), 48.0)
        elif variant == Variant.MONOCHROME:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 0.0)
        elif variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 12.0)
        elif variant == Variant.RAINBOW:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 48.0)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 36.0)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                math_utils.sanitize_degrees_double(source_color_hct.hue + 240), 40)
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 200.0)
        else:
            raise ValueError(f"Unsupported variant: {variant}")

    def get_secondary_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the secondary palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.CONTENT or variant == Variant.FIDELITY:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue,
                max(source_color_hct.chroma - 32.0, source_color_hct.chroma * 0.5))
        elif variant == Variant.FRUIT_SALAD:
            return TonalPalette.from_hue_and_chroma(
                math_utils.sanitize_degrees_double(source_color_hct.hue - 50.0), 36.0)
        elif variant == Variant.MONOCHROME:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 0.0)
        elif variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 8.0)
        elif variant == Variant.RAINBOW:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 16.0)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 16.0)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 21, 51, 121, 151, 191, 271, 321, 360],
                    [45, 95, 45, 20, 45, 90, 45, 45, 45]),
                24.0)
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 41, 61, 101, 131, 181, 251, 301, 360],
                    [18, 15, 10, 12, 15, 18, 15, 12, 12]),
                24.0)
        else:
            raise ValueError(f"Unsupported variant: {variant}")

    def get_tertiary_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the tertiary palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.CONTENT:
            return TonalPalette.from_hct(DislikeAnalyzer.fix_if_disliked(
                TemperatureCache(source_color_hct).analogous(3, 6)[2]))
        elif variant == Variant.FIDELITY:
            return TonalPalette.from_hct(DislikeAnalyzer.fix_if_disliked(
                TemperatureCache(source_color_hct).complement))
        elif variant == Variant.FRUIT_SALAD:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 36.0)
        elif variant == Variant.MONOCHROME:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 0.0)
        elif variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 16.0)
        elif variant == Variant.RAINBOW or variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(
                math_utils.sanitize_degrees_double(source_color_hct.hue + 60.0), 24.0)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 21, 51, 121, 151, 191, 271, 321, 360],
                    [120, 120, 20, 45, 20, 15, 20, 120, 120]),
                32.0)
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 41, 61, 101, 131, 181, 251, 301, 360],
                    [35, 30, 20, 25, 30, 35, 30, 25, 25]),
                32.0)
        else:
            raise ValueError(f"Unsupported variant: {variant}")

    def get_neutral_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the neutral palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.CONTENT or variant == Variant.FIDELITY:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, source_color_hct.chroma / 8.0)
        elif variant == Variant.FRUIT_SALAD:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 10.0)
        elif variant == Variant.MONOCHROME:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 0.0)
        elif variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 2.0)
        elif variant == Variant.RAINBOW:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 0.0)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 6.0)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                math_utils.sanitize_degrees_double(source_color_hct.hue + 15), 8)
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 10)
        else:
            raise ValueError(f"Unsupported variant: {variant}")

    def get_neutral_variant_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the neutral variant palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.CONTENT:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, (source_color_hct.chroma / 8.0) + 4.0)
        elif variant == Variant.FIDELITY:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, (source_color_hct.chroma / 8.0) + 4.0)
        elif variant == Variant.FRUIT_SALAD:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 16.0)
        elif variant == Variant.MONOCHROME:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 0.0)
        elif variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 2.0)
        elif variant == Variant.RAINBOW:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 0.0)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 8.0)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                math_utils.sanitize_degrees_double(source_color_hct.hue + 15), 12)
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 12)
        else:
            raise ValueError(f"Unsupported variant: {variant}")

    def get_error_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> Optional[TonalPalette]:
        """
        Get the error palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            None, as there's no error palette in the 2021 spec.
        """
        return None


class DynamicSchemePalettesDelegateImpl2025(DynamicSchemePalettesDelegateImpl2021):
    """
    A delegate for the palettes of a DynamicScheme in the 2025 spec.
    """

    def get_primary_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the primary palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue,
                12 if platform == 'phone' and Hct.is_blue(source_color_hct.hue) else
                8 if platform == 'phone' else
                16 if Hct.is_blue(source_color_hct.hue) else 12)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, 26 if platform == 'phone' and is_dark else 32)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, 36 if platform == 'phone' and is_dark else
                48 if platform == 'phone' else 40)
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, 74 if platform == 'phone' else 56)
        else:
            return super().get_primary_palette(
                variant, source_color_hct, is_dark, platform, contrast_level)

    def get_secondary_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the secondary palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue,
                6 if platform == 'phone' and Hct.is_blue(source_color_hct.hue) else
                4 if platform == 'phone' else
                10 if Hct.is_blue(source_color_hct.hue) else 6)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(source_color_hct.hue, 16)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 105, 140, 204, 253, 278, 300, 333, 360],
                    [-160, 155, -100, 96, -96, -156, -165, -160]),
                16 if platform == 'phone' and is_dark else 24 if platform == 'phone' else 24)
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 38, 105, 140, 333, 360],
                    [-14, 10, -14, 10, -14]),
                56 if platform == 'phone' else 36)
        else:
            return super().get_secondary_palette(
                variant, source_color_hct, is_dark, platform, contrast_level)

    def get_tertiary_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the tertiary palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 38, 105, 161, 204, 278, 333, 360],
                    [-32, 26, 10, -39, 24, -15, -32]),
                20 if platform == 'phone' else 36)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 20, 71, 161, 333, 360],
                    [-40, 48, -32, 40, -32]),
                28 if platform == 'phone' else 32)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 105, 140, 204, 253, 278, 300, 333, 360],
                    [-165, 160, -105, 101, -101, -160, -170, -165]),
                48)
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(
                DynamicScheme.get_rotated_hue(
                    source_color_hct, [0, 38, 71, 105, 140, 161, 253, 333, 360],
                    [-72, 35, 24, -24, 62, 50, 62, -72]),
                56)
        else:
            return super().get_tertiary_palette(
                variant, source_color_hct, is_dark, platform, contrast_level)

    @staticmethod
    def _get_expressive_neutral_hue(source_color_hct: Hct) -> float:
        """
        Get the expressive neutral hue for the given source color.
        
        Args:
            source_color_hct: The source color.
            
        Returns:
            A hue value.
        """
        hue = DynamicScheme.get_rotated_hue(
            source_color_hct, [0, 71, 124, 253, 278, 300, 360],
            [10, 0, 10, 0, 10, 0])
        return hue

    @staticmethod
    def _get_expressive_neutral_chroma(
            source_color_hct: Hct, is_dark: bool, platform: Platform) -> float:
        """
        Get the expressive neutral chroma for the given parameters.
        
        Args:
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            
        Returns:
            A chroma value.
        """
        neutral_hue = DynamicSchemePalettesDelegateImpl2025._get_expressive_neutral_hue(
            source_color_hct)
        return (6 if platform == 'phone' and is_dark and Hct.is_yellow(neutral_hue) else
               14 if platform == 'phone' and is_dark else
               18 if platform == 'phone' else 12)

    @staticmethod
    def _get_vibrant_neutral_hue(source_color_hct: Hct) -> float:
        """
        Get the vibrant neutral hue for the given source color.
        
        Args:
            source_color_hct: The source color.
            
        Returns:
            A hue value.
        """
        return DynamicScheme.get_rotated_hue(
            source_color_hct, [0, 38, 105, 140, 333, 360], [-14, 10, -14, 10, -14])

    @staticmethod
    def _get_vibrant_neutral_chroma(source_color_hct: Hct, platform: Platform) -> float:
        """
        Get the vibrant neutral chroma for the given parameters.
        
        Args:
            source_color_hct: The source color.
            platform: The platform.
            
        Returns:
            A chroma value.
        """
        neutral_hue = DynamicSchemePalettesDelegateImpl2025._get_vibrant_neutral_hue(
            source_color_hct)
        return (28 if platform == 'phone' else
               28 if Hct.is_blue(neutral_hue) else 20)

    def get_neutral_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the neutral palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, 1.4 if platform == 'phone' else 6)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, 5 if platform == 'phone' else 10)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                self._get_expressive_neutral_hue(source_color_hct),
                self._get_expressive_neutral_chroma(source_color_hct, is_dark, platform))
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(
                self._get_vibrant_neutral_hue(source_color_hct),
                self._get_vibrant_neutral_chroma(source_color_hct, platform))
        else:
            return super().get_neutral_palette(
                variant, source_color_hct, is_dark, platform, contrast_level)

    def get_neutral_variant_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> TonalPalette:
        """
        Get the neutral variant palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        if variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, (1.4 if platform == 'phone' else 6) * 2.2)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(
                source_color_hct.hue, (5 if platform == 'phone' else 10) * 1.7)
        elif variant == Variant.EXPRESSIVE:
            expressive_neutral_hue = self._get_expressive_neutral_hue(source_color_hct)
            expressive_neutral_chroma = self._get_expressive_neutral_chroma(
                source_color_hct, is_dark, platform)
            return TonalPalette.from_hue_and_chroma(
                expressive_neutral_hue,
                expressive_neutral_chroma * (
                    1.6 if expressive_neutral_hue >= 105 and expressive_neutral_hue < 125 else 2.3),
            )
        elif variant == Variant.VIBRANT:
            vibrant_neutral_hue = self._get_vibrant_neutral_hue(source_color_hct)
            vibrant_neutral_chroma = self._get_vibrant_neutral_chroma(source_color_hct, platform)
            return TonalPalette.from_hue_and_chroma(
                vibrant_neutral_hue, vibrant_neutral_chroma * 1.29)
        else:
            return super().get_neutral_variant_palette(
                variant, source_color_hct, is_dark, platform, contrast_level)

    def get_error_palette(
            self, variant: Variant, source_color_hct: Hct, is_dark: bool,
            platform: Platform, contrast_level: float) -> Optional[TonalPalette]:
        """
        Get the error palette for the given parameters.
        
        Args:
            variant: The variant.
            source_color_hct: The source color.
            is_dark: Whether the scheme is in dark mode.
            platform: The platform.
            contrast_level: The contrast level.
            
        Returns:
            A tonal palette.
        """
        error_hue = DynamicScheme.get_piecewise_hue(
            source_color_hct, [0, 3, 13, 23, 33, 43, 153, 273, 360],
            [12, 22, 32, 12, 22, 32, 22, 12])
        if variant == Variant.NEUTRAL:
            return TonalPalette.from_hue_and_chroma(
                error_hue, 50 if platform == 'phone' else 40)
        elif variant == Variant.TONAL_SPOT:
            return TonalPalette.from_hue_and_chroma(
                error_hue, 60 if platform == 'phone' else 48)
        elif variant == Variant.EXPRESSIVE:
            return TonalPalette.from_hue_and_chroma(
                error_hue, 64 if platform == 'phone' else 48)
        elif variant == Variant.VIBRANT:
            return TonalPalette.from_hue_and_chroma(
                error_hue, 80 if platform == 'phone' else 60)
        else:
            return super().get_error_palette(
                variant, source_color_hct, is_dark, platform, contrast_level)


# Global delegates for different spec versions
spec2021 = DynamicSchemePalettesDelegateImpl2021()
spec2025 = DynamicSchemePalettesDelegateImpl2025()


def get_spec(spec_version: SpecVersion) -> DynamicSchemePalettesDelegate:
    """
    Returns the DynamicSchemePalettesDelegate for the given spec version.
    
    Args:
        spec_version: The spec version.
        
    Returns:
        A DynamicSchemePalettesDelegate.
    """
    return spec2025 if spec_version == '2025' else spec2021
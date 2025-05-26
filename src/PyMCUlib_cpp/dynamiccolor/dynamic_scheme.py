# dynamic_scheme.py

from typing import List, Optional
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dynamiccolor.variant import Variant
from PyMCUlib_cpp.palettes.tones import TonalPalette
from PyMCUlib_cpp.utils.utils import Argb, sanitize_degrees_double

class DynamicScheme:
    """
    A scheme that defines dynamic colors.
    
    Contains both the colors themselves, and information about what generated them.
    """
    
    def __init__(
        self,
        source_color_hct: Hct,
        variant: Variant,
        contrast_level: float,
        is_dark: bool,
        primary_palette: TonalPalette,
        secondary_palette: TonalPalette,
        tertiary_palette: TonalPalette,
        neutral_palette: TonalPalette,
        neutral_variant_palette: TonalPalette,
        error_palette: Optional[TonalPalette] = None
    ):
        """
        Create a dynamic color scheme.
        
        Args:
            source_color_hct: Source color of the scheme in HCT
            variant: Variant algorithm for the scheme
            contrast_level: Level of contrast between colors
            is_dark: Whether the scheme is dark or light
            primary_palette: Tonal palette for primary colors
            secondary_palette: Tonal palette for secondary colors
            tertiary_palette: Tonal palette for tertiary colors
            neutral_palette: Tonal palette for neutral colors
            neutral_variant_palette: Tonal palette for neutral variant colors
            error_palette: Tonal palette for error colors (optional)
        """
        self.source_color_hct = source_color_hct
        self.variant = variant
        self.is_dark = is_dark
        self.contrast_level = contrast_level
        
        self.primary_palette = primary_palette
        self.secondary_palette = secondary_palette
        self.tertiary_palette = tertiary_palette
        self.neutral_palette = neutral_palette
        self.neutral_variant_palette = neutral_variant_palette
        
        # Default error palette if not provided
        if error_palette is None:
            self.error_palette = TonalPalette(25.0, 84.0)
        else:
            self.error_palette = error_palette
    
    @staticmethod
    def get_rotated_hue(source_color: Hct, hues: List[float], rotations: List[float]) -> float:
        """
        Rotates the hue of a color by a provided angle determined by the source color's hue.
        
        Args:
            source_color: Source color to rotate.
            hues: List of hue angles in degrees.
            rotations: List of rotation angles in degrees. Must have same length as hues.
            
        Returns:
            Rotated hue in degrees.
        """
        source_hue = source_color.get_hue()
        
        if len(rotations) == 1:
            return sanitize_degrees_double(source_color.get_hue() + rotations[0])
        
        size = len(hues)
        for i in range(size - 1):
            this_hue = hues[i]
            next_hue = hues[i + 1]
            if this_hue < source_hue and source_hue < next_hue:
                return sanitize_degrees_double(source_hue + rotations[i])
        
        return source_hue
    
    def source_color_argb(self) -> Argb:
        """Returns the ARGB representation of the source color."""
        return self.source_color_hct.to_int()
    
    def get_primary_palette_key_color(self) -> Argb:
        """Returns the ARGB representation of the primary palette's key color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.primary_palette_key_color().get_argb(self)
    
    def get_secondary_palette_key_color(self) -> Argb:
        """Returns the ARGB representation of the secondary palette's key color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.secondary_palette_key_color().get_argb(self)
    
    def get_tertiary_palette_key_color(self) -> Argb:
        """Returns the ARGB representation of the tertiary palette's key color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.tertiary_palette_key_color().get_argb(self)
    
    def get_neutral_palette_key_color(self) -> Argb:
        """Returns the ARGB representation of the neutral palette's key color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.neutral_palette_key_color().get_argb(self)
    
    def get_neutral_variant_palette_key_color(self) -> Argb:
        """Returns the ARGB representation of the neutral variant palette's key color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.neutral_variant_palette_key_color().get_argb(self)
    
    # Surface colors
    def get_background(self) -> Argb:
        """Returns the ARGB representation of the background color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.background().get_argb(self)
    
    def get_on_background(self) -> Argb:
        """Returns the ARGB representation of the on-background color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_background().get_argb(self)
    
    def get_surface(self) -> Argb:
        """Returns the ARGB representation of the surface color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface().get_argb(self)
    
    def get_surface_dim(self) -> Argb:
        """Returns the ARGB representation of the dim surface color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface_dim().get_argb(self)
    
    def get_surface_bright(self) -> Argb:
        """Returns the ARGB representation of the bright surface color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface_bright().get_argb(self)
    
    def get_surface_container_lowest(self) -> Argb:
        """Returns the ARGB representation of the lowest surface container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface_container_lowest().get_argb(self)
    
    def get_surface_container_low(self) -> Argb:
        """Returns the ARGB representation of the low surface container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface_container_low().get_argb(self)
    
    def get_surface_container(self) -> Argb:
        """Returns the ARGB representation of the main surface container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface_container().get_argb(self)
    
    def get_surface_container_high(self) -> Argb:
        """Returns the ARGB representation of the high surface container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface_container_high().get_argb(self)
    
    def get_surface_container_highest(self) -> Argb:
        """Returns the ARGB representation of the highest surface container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface_container_highest().get_argb(self)
    
    def get_on_surface(self) -> Argb:
        """Returns the ARGB representation of the on-surface color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_surface().get_argb(self)
    
    def get_surface_variant(self) -> Argb:
        """Returns the ARGB representation of the surface variant color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface_variant().get_argb(self)
    
    def get_on_surface_variant(self) -> Argb:
        """Returns the ARGB representation of the on-surface-variant color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_surface_variant().get_argb(self)
    
    def get_inverse_surface(self) -> Argb:
        """Returns the ARGB representation of the inverse surface color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.inverse_surface().get_argb(self)
    
    def get_inverse_on_surface(self) -> Argb:
        """Returns the ARGB representation of the inverse on-surface color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.inverse_on_surface().get_argb(self)
    
    def get_outline(self) -> Argb:
        """Returns the ARGB representation of the outline color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.outline().get_argb(self)
    
    def get_outline_variant(self) -> Argb:
        """Returns the ARGB representation of the outline variant color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.outline_variant().get_argb(self)
    
    def get_shadow(self) -> Argb:
        """Returns the ARGB representation of the shadow color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.shadow().get_argb(self)
    
    def get_scrim(self) -> Argb:
        """Returns the ARGB representation of the scrim color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.scrim().get_argb(self)
    
    def get_surface_tint(self) -> Argb:
        """Returns the ARGB representation of the surface tint color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.surface_tint().get_argb(self)
    
    # Primary colors
    def get_primary(self) -> Argb:
        """Returns the ARGB representation of the primary color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.primary().get_argb(self)
    
    def get_on_primary(self) -> Argb:
        """Returns the ARGB representation of the on-primary color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_primary().get_argb(self)
    
    def get_primary_container(self) -> Argb:
        """Returns the ARGB representation of the primary container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.primary_container().get_argb(self)
    
    def get_on_primary_container(self) -> Argb:
        """Returns the ARGB representation of the on-primary-container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_primary_container().get_argb(self)
    
    def get_inverse_primary(self) -> Argb:
        """Returns the ARGB representation of the inverse primary color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.inverse_primary().get_argb(self)
    
    # Secondary colors
    def get_secondary(self) -> Argb:
        """Returns the ARGB representation of the secondary color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.secondary().get_argb(self)
    
    def get_on_secondary(self) -> Argb:
        """Returns the ARGB representation of the on-secondary color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_secondary().get_argb(self)
    
    def get_secondary_container(self) -> Argb:
        """Returns the ARGB representation of the secondary container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.secondary_container().get_argb(self)
    
    def get_on_secondary_container(self) -> Argb:
        """Returns the ARGB representation of the on-secondary-container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_secondary_container().get_argb(self)
    
    # Tertiary colors
    def get_tertiary(self) -> Argb:
        """Returns the ARGB representation of the tertiary color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.tertiary().get_argb(self)
    
    def get_on_tertiary(self) -> Argb:
        """Returns the ARGB representation of the on-tertiary color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_tertiary().get_argb(self)
    
    def get_tertiary_container(self) -> Argb:
        """Returns the ARGB representation of the tertiary container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.tertiary_container().get_argb(self)
    
    def get_on_tertiary_container(self) -> Argb:
        """Returns the ARGB representation of the on-tertiary-container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_tertiary_container().get_argb(self)
    
    # Error colors
    def get_error(self) -> Argb:
        """Returns the ARGB representation of the error color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.error().get_argb(self)
    
    def get_on_error(self) -> Argb:
        """Returns the ARGB representation of the on-error color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_error().get_argb(self)
    
    def get_error_container(self) -> Argb:
        """Returns the ARGB representation of the error container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.error_container().get_argb(self)
    
    def get_on_error_container(self) -> Argb:
        """Returns the ARGB representation of the on-error-container color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_error_container().get_argb(self)
    
    # Fixed colors
    def get_primary_fixed(self) -> Argb:
        """Returns the ARGB representation of the primary fixed color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.primary_fixed().get_argb(self)
    
    def get_primary_fixed_dim(self) -> Argb:
        """Returns the ARGB representation of the primary fixed dim color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.primary_fixed_dim().get_argb(self)
    
    def get_on_primary_fixed(self) -> Argb:
        """Returns the ARGB representation of the on-primary-fixed color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_primary_fixed().get_argb(self)
    
    def get_on_primary_fixed_variant(self) -> Argb:
        """Returns the ARGB representation of the on-primary-fixed-variant color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_primary_fixed_variant().get_argb(self)
    
    def get_secondary_fixed(self) -> Argb:
        """Returns the ARGB representation of the secondary fixed color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.secondary_fixed().get_argb(self)
    
    def get_secondary_fixed_dim(self) -> Argb:
        """Returns the ARGB representation of the secondary fixed dim color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.secondary_fixed_dim().get_argb(self)
    
    def get_on_secondary_fixed(self) -> Argb:
        """Returns the ARGB representation of the on-secondary-fixed color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_secondary_fixed().get_argb(self)
    
    def get_on_secondary_fixed_variant(self) -> Argb:
        """Returns the ARGB representation of the on-secondary-fixed-variant color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_secondary_fixed_variant().get_argb(self)
    
    def get_tertiary_fixed(self) -> Argb:
        """Returns the ARGB representation of the tertiary fixed color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.tertiary_fixed().get_argb(self)
    
    def get_tertiary_fixed_dim(self) -> Argb:
        """Returns the ARGB representation of the tertiary fixed dim color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.tertiary_fixed_dim().get_argb(self)
    
    def get_on_tertiary_fixed(self) -> Argb:
        """Returns the ARGB representation of the on-tertiary-fixed color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_tertiary_fixed().get_argb(self)
    
    def get_on_tertiary_fixed_variant(self) -> Argb:
        """Returns the ARGB representation of the on-tertiary-fixed-variant color."""
        from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
        return MaterialDynamicColors.on_tertiary_fixed_variant().get_argb(self)
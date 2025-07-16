# dynamiccolor/material_dynamic_colors.py

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme

from PyMCUlib.dynamiccolor.color_spec_2025 import ColorSpecDelegateImpl2025
from PyMCUlib.dynamiccolor.dynamic_color import DynamicColor


class MaterialDynamicColors:
    """
    DynamicColors for the colors in the Material Design system.
    """
    content_accent_tone_delta = 15.0
    
    _color_spec = ColorSpecDelegateImpl2025()
    
    def highest_surface(self, s: 'DynamicScheme') -> DynamicColor:
        """
        Returns the highest surface color for the given scheme.
        
        Args:
            s: The dynamic scheme to get the highest surface for
            
        Returns:
            The highest surface dynamic color
        """
        return MaterialDynamicColors._color_spec.highest_surface(s)
    
    ################################################################
    # Main Palettes                                              #
    ################################################################
    
    def primary_palette_key_color(self) -> DynamicColor:
        """
        Returns the primary palette key color.
        
        Returns:
            The primary palette key dynamic color
        """
        return MaterialDynamicColors._color_spec.primary_palette_key_color()
    
    def secondary_palette_key_color(self) -> DynamicColor:
        """
        Returns the secondary palette key color.
        
        Returns:
            The secondary palette key dynamic color
        """
        return MaterialDynamicColors._color_spec.secondary_palette_key_color()
    
    def tertiary_palette_key_color(self) -> DynamicColor:
        """
        Returns the tertiary palette key color.
        
        Returns:
            The tertiary palette key dynamic color
        """
        return MaterialDynamicColors._color_spec.tertiary_palette_key_color()
    
    def neutral_palette_key_color(self) -> DynamicColor:
        """
        Returns the neutral palette key color.
        
        Returns:
            The neutral palette key dynamic color
        """
        return MaterialDynamicColors._color_spec.neutral_palette_key_color()
    
    def neutral_variant_palette_key_color(self) -> DynamicColor:
        """
        Returns the neutral variant palette key color.
        
        Returns:
            The neutral variant palette key dynamic color
        """
        return MaterialDynamicColors._color_spec.neutral_variant_palette_key_color()
    
    def error_palette_key_color(self) -> DynamicColor:
        """
        Returns the error palette key color.
        
        Returns:
            The error palette key dynamic color
        """
        return MaterialDynamicColors._color_spec.error_palette_key_color()
    
    ################################################################
    # Surfaces [S]                                               #
    ################################################################
    
    def background(self) -> DynamicColor:
        """
        Returns the background color.
        
        Returns:
            The background dynamic color
        """
        return MaterialDynamicColors._color_spec.background()
    
    def on_background(self) -> DynamicColor:
        """
        Returns the on background color.
        
        Returns:
            The on background dynamic color
        """
        return MaterialDynamicColors._color_spec.on_background()
    
    def surface(self) -> DynamicColor:
        """
        Returns the surface color.
        
        Returns:
            The surface dynamic color
        """
        return MaterialDynamicColors._color_spec.surface()
    
    def surface_dim(self) -> DynamicColor:
        """
        Returns the surface dim color.
        
        Returns:
            The surface dim dynamic color
        """
        return MaterialDynamicColors._color_spec.surface_dim()
    
    def surface_bright(self) -> DynamicColor:
        """
        Returns the surface bright color.
        
        Returns:
            The surface bright dynamic color
        """
        return MaterialDynamicColors._color_spec.surface_bright()
    
    def surface_container_lowest(self) -> DynamicColor:
        """
        Returns the surface container lowest color.
        
        Returns:
            The surface container lowest dynamic color
        """
        return MaterialDynamicColors._color_spec.surface_container_lowest()
    
    def surface_container_low(self) -> DynamicColor:
        """
        Returns the surface container low color.
        
        Returns:
            The surface container low dynamic color
        """
        return MaterialDynamicColors._color_spec.surface_container_low()
    
    def surface_container(self) -> DynamicColor:
        """
        Returns the surface container color.
        
        Returns:
            The surface container dynamic color
        """
        return MaterialDynamicColors._color_spec.surface_container()
    
    def surface_container_high(self) -> DynamicColor:
        """
        Returns the surface container high color.
        
        Returns:
            The surface container high dynamic color
        """
        return MaterialDynamicColors._color_spec.surface_container_high()
    
    def surface_container_highest(self) -> DynamicColor:
        """
        Returns the surface container highest color.
        
        Returns:
            The surface container highest dynamic color
        """
        return MaterialDynamicColors._color_spec.surface_container_highest()
    
    def on_surface(self) -> DynamicColor:
        """
        Returns the on surface color.
        
        Returns:
            The on surface dynamic color
        """
        return MaterialDynamicColors._color_spec.on_surface()
    
    def surface_variant(self) -> DynamicColor:
        """
        Returns the surface variant color.
        
        Returns:
            The surface variant dynamic color
        """
        return MaterialDynamicColors._color_spec.surface_variant()
    
    def on_surface_variant(self) -> DynamicColor:
        """
        Returns the on surface variant color.
        
        Returns:
            The on surface variant dynamic color
        """
        return MaterialDynamicColors._color_spec.on_surface_variant()
    
    def outline(self) -> DynamicColor:
        """
        Returns the outline color.
        
        Returns:
            The outline dynamic color
        """
        return MaterialDynamicColors._color_spec.outline()
    
    def outline_variant(self) -> DynamicColor:
        """
        Returns the outline variant color.
        
        Returns:
            The outline variant dynamic color
        """
        return MaterialDynamicColors._color_spec.outline_variant()
    
    def inverse_surface(self) -> DynamicColor:
        """
        Returns the inverse surface color.
        
        Returns:
            The inverse surface dynamic color
        """
        return MaterialDynamicColors._color_spec.inverse_surface()
    
    def inverse_on_surface(self) -> DynamicColor:
        """
        Returns the inverse on surface color.
        
        Returns:
            The inverse on surface dynamic color
        """
        return MaterialDynamicColors._color_spec.inverse_on_surface()
    
    def shadow(self) -> DynamicColor:
        """
        Returns the shadow color.
        
        Returns:
            The shadow dynamic color
        """
        return MaterialDynamicColors._color_spec.shadow()
    
    def scrim(self) -> DynamicColor:
        """
        Returns the scrim color.
        
        Returns:
            The scrim dynamic color
        """
        return MaterialDynamicColors._color_spec.scrim()
    
    def surface_tint(self) -> DynamicColor:
        """
        Returns the surface tint color.
        
        Returns:
            The surface tint dynamic color
        """
        return MaterialDynamicColors._color_spec.surface_tint()
    
    ################################################################
    # Primaries [P]                                              #
    ################################################################
    
    def primary(self) -> DynamicColor:
        """
        Returns the primary color.
        
        Returns:
            The primary dynamic color
        """
        return MaterialDynamicColors._color_spec.primary()
    
    def primary_dim(self) -> Optional[DynamicColor]:
        """
        Returns the primary dim color.
        
        Returns:
            The primary dim dynamic color or None if not available
        """
        return MaterialDynamicColors._color_spec.primary_dim()
    
    def on_primary(self) -> DynamicColor:
        """
        Returns the on primary color.
        
        Returns:
            The on primary dynamic color
        """
        return MaterialDynamicColors._color_spec.on_primary()
    
    def primary_container(self) -> DynamicColor:
        """
        Returns the primary container color.
        
        Returns:
            The primary container dynamic color
        """
        return MaterialDynamicColors._color_spec.primary_container()
    
    def on_primary_container(self) -> DynamicColor:
        """
        Returns the on primary container color.
        
        Returns:
            The on primary container dynamic color
        """
        return MaterialDynamicColors._color_spec.on_primary_container()
    
    def inverse_primary(self) -> DynamicColor:
        """
        Returns the inverse primary color.
        
        Returns:
            The inverse primary dynamic color
        """
        return MaterialDynamicColors._color_spec.inverse_primary()
    
    #################################################################
    # Primary Fixed [PF]                                          #
    #################################################################
    
    def primary_fixed(self) -> DynamicColor:
        """
        Returns the primary fixed color.
        
        Returns:
            The primary fixed dynamic color
        """
        return MaterialDynamicColors._color_spec.primary_fixed()
    
    def primary_fixed_dim(self) -> DynamicColor:
        """
        Returns the primary fixed dim color.
        
        Returns:
            The primary fixed dim dynamic color
        """
        return MaterialDynamicColors._color_spec.primary_fixed_dim()
    
    def on_primary_fixed(self) -> DynamicColor:
        """
        Returns the on primary fixed color.
        
        Returns:
            The on primary fixed dynamic color
        """
        return MaterialDynamicColors._color_spec.on_primary_fixed()
    
    def on_primary_fixed_variant(self) -> DynamicColor:
        """
        Returns the on primary fixed variant color.
        
        Returns:
            The on primary fixed variant dynamic color
        """
        return MaterialDynamicColors._color_spec.on_primary_fixed_variant()
    
    ################################################################
    # Secondaries [Q]                                            #
    ################################################################
    
    def secondary(self) -> DynamicColor:
        """
        Returns the secondary color.
        
        Returns:
            The secondary dynamic color
        """
        return MaterialDynamicColors._color_spec.secondary()
    
    def secondary_dim(self) -> Optional[DynamicColor]:
        """
        Returns the secondary dim color.
        
        Returns:
            The secondary dim dynamic color or None if not available
        """
        return MaterialDynamicColors._color_spec.secondary_dim()
    
    def on_secondary(self) -> DynamicColor:
        """
        Returns the on secondary color.
        
        Returns:
            The on secondary dynamic color
        """
        return MaterialDynamicColors._color_spec.on_secondary()
    
    def secondary_container(self) -> DynamicColor:
        """
        Returns the secondary container color.
        
        Returns:
            The secondary container dynamic color
        """
        return MaterialDynamicColors._color_spec.secondary_container()
    
    def on_secondary_container(self) -> DynamicColor:
        """
        Returns the on secondary container color.
        
        Returns:
            The on secondary container dynamic color
        """
        return MaterialDynamicColors._color_spec.on_secondary_container()
    
    #################################################################
    # Secondary Fixed [QF]                                        #
    #################################################################
    
    def secondary_fixed(self) -> DynamicColor:
        """
        Returns the secondary fixed color.
        
        Returns:
            The secondary fixed dynamic color
        """
        return MaterialDynamicColors._color_spec.secondary_fixed()
    
    def secondary_fixed_dim(self) -> DynamicColor:
        """
        Returns the secondary fixed dim color.
        
        Returns:
            The secondary fixed dim dynamic color
        """
        return MaterialDynamicColors._color_spec.secondary_fixed_dim()
    
    def on_secondary_fixed(self) -> DynamicColor:
        """
        Returns the on secondary fixed color.
        
        Returns:
            The on secondary fixed dynamic color
        """
        return MaterialDynamicColors._color_spec.on_secondary_fixed()
    
    def on_secondary_fixed_variant(self) -> DynamicColor:
        """
        Returns the on secondary fixed variant color.
        
        Returns:
            The on secondary fixed variant dynamic color
        """
        return MaterialDynamicColors._color_spec.on_secondary_fixed_variant()
    
    ################################################################
    # Tertiaries [T]                                             #
    ################################################################
    
    def tertiary(self) -> DynamicColor:
        """
        Returns the tertiary color.
        
        Returns:
            The tertiary dynamic color
        """
        return MaterialDynamicColors._color_spec.tertiary()
    
    def tertiary_dim(self) -> Optional[DynamicColor]:
        """
        Returns the tertiary dim color.
        
        Returns:
            The tertiary dim dynamic color or None if not available
        """
        return MaterialDynamicColors._color_spec.tertiary_dim()
    
    def on_tertiary(self) -> DynamicColor:
        """
        Returns the on tertiary color.
        
        Returns:
            The on tertiary dynamic color
        """
        return MaterialDynamicColors._color_spec.on_tertiary()
    
    def tertiary_container(self) -> DynamicColor:
        """
        Returns the tertiary container color.
        
        Returns:
            The tertiary container dynamic color
        """
        return MaterialDynamicColors._color_spec.tertiary_container()
    
    def on_tertiary_container(self) -> DynamicColor:
        """
        Returns the on tertiary container color.
        
        Returns:
            The on tertiary container dynamic color
        """
        return MaterialDynamicColors._color_spec.on_tertiary_container()
    
    #################################################################
    # Tertiary Fixed [TF]                                         #
    #################################################################
    
    def tertiary_fixed(self) -> DynamicColor:
        """
        Returns the tertiary fixed color.
        
        Returns:
            The tertiary fixed dynamic color
        """
        return MaterialDynamicColors._color_spec.tertiary_fixed()
    
    def tertiary_fixed_dim(self) -> DynamicColor:
        """
        Returns the tertiary fixed dim color.
        
        Returns:
            The tertiary fixed dim dynamic color
        """
        return MaterialDynamicColors._color_spec.tertiary_fixed_dim()
    
    def on_tertiary_fixed(self) -> DynamicColor:
        """
        Returns the on tertiary fixed color.
        
        Returns:
            The on tertiary fixed dynamic color
        """
        return MaterialDynamicColors._color_spec.on_tertiary_fixed()
    
    def on_tertiary_fixed_variant(self) -> DynamicColor:
        """
        Returns the on tertiary fixed variant color.
        
        Returns:
            The on tertiary fixed variant dynamic color
        """
        return MaterialDynamicColors._color_spec.on_tertiary_fixed_variant()
    
    ################################################################
    # Errors [E]                                                 #
    ################################################################
    
    def error(self) -> DynamicColor:
        """
        Returns the error color.
        
        Returns:
            The error dynamic color
        """
        return MaterialDynamicColors._color_spec.error()
    
    def error_dim(self) -> Optional[DynamicColor]:
        """
        Returns the error dim color.
        
        Returns:
            The error dim dynamic color or None if not available
        """
        return MaterialDynamicColors._color_spec.error_dim()
    
    def on_error(self) -> DynamicColor:
        """
        Returns the on error color.
        
        Returns:
            The on error dynamic color
        """
        return MaterialDynamicColors._color_spec.on_error()
    
    def error_container(self) -> DynamicColor:
        """
        Returns the error container color.
        
        Returns:
            The error container dynamic color
        """
        return MaterialDynamicColors._color_spec.error_container()
    
    def on_error_container(self) -> DynamicColor:
        """
        Returns the on error container color.
        
        Returns:
            The on error container dynamic color
        """
        return MaterialDynamicColors._color_spec.on_error_container()
    
    ################################################################
    # All Colors                                                 #
    ################################################################
    
    @property
    def all_colors(self) -> List[DynamicColor]:
        """
        List of all available dynamic colors.
        
        Returns:
            List of all non-undefined dynamic colors
        """
        colors = [
            self.background(),
            self.on_background(),
            self.surface(),
            self.surface_dim(),
            self.surface_bright(),
            self.surface_container_lowest(),
            self.surface_container_low(),
            self.surface_container(),
            self.surface_container_high(),
            self.surface_container_highest(),
            self.on_surface(),
            self.on_surface_variant(),
            self.outline(),
            self.outline_variant(),
            self.inverse_surface(),
            self.inverse_on_surface(),
            self.primary(),
            self.primary_dim(),
            self.on_primary(),
            self.primary_container(),
            self.on_primary_container(),
            self.primary_fixed(),
            self.primary_fixed_dim(),
            self.on_primary_fixed(),
            self.on_primary_fixed_variant(),
            self.inverse_primary(),
            self.secondary(),
            self.secondary_dim(),
            self.on_secondary(),
            self.secondary_container(),
            self.on_secondary_container(),
            self.secondary_fixed(),
            self.secondary_fixed_dim(),
            self.on_secondary_fixed(),
            self.on_secondary_fixed_variant(),
            self.tertiary(),
            self.tertiary_dim(),
            self.on_tertiary(),
            self.tertiary_container(),
            self.on_tertiary_container(),
            self.tertiary_fixed(),
            self.tertiary_fixed_dim(),
            self.on_tertiary_fixed(),
            self.on_tertiary_fixed_variant(),
            self.error(),
            self.error_dim(),
            self.on_error(),
            self.error_container(),
            self.on_error_container(),
        ]
        return [c for c in colors if c is not None]
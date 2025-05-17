# dynamiccolor/color_spec_delegate.py

from abc import ABC, abstractmethod
from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from PyMCUlib.dynamiccolor.dynamic_color import DynamicColor
    from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme

# define specification version type
SpecVersion = Literal['2021', '2025']


class ColorSpecDelegate(ABC):
    """
    A delegate that provides the dynamic color constraints for
    MaterialDynamicColors.

    This is used to allow for different color constraints for different spec
    versions.
    """

    ################################################################
    # Main Palettes                                              #
    ################################################################

    @abstractmethod
    def primary_palette_key_color(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def secondary_palette_key_color(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def tertiary_palette_key_color(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def neutral_palette_key_color(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def neutral_variant_palette_key_color(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def error_palette_key_color(self) -> 'DynamicColor':
        pass

    ################################################################
    # Surfaces [S]                                               #
    ################################################################

    @abstractmethod
    def background(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_background(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface_dim(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface_bright(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface_container_lowest(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface_container_low(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface_container(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface_container_high(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface_container_highest(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_surface(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface_variant(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_surface_variant(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def inverse_surface(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def inverse_on_surface(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def outline(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def outline_variant(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def shadow(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def scrim(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def surface_tint(self) -> 'DynamicColor':
        pass

    ################################################################
    # Primaries [P]                                              #
    ################################################################

    @abstractmethod
    def primary(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def primary_dim(self) -> Optional['DynamicColor']:
        pass

    @abstractmethod
    def on_primary(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def primary_container(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_primary_container(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def inverse_primary(self) -> 'DynamicColor':
        pass

    ################################################################
    # Secondaries [Q]                                            #
    ################################################################

    @abstractmethod
    def secondary(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def secondary_dim(self) -> Optional['DynamicColor']:
        pass

    @abstractmethod
    def on_secondary(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def secondary_container(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_secondary_container(self) -> 'DynamicColor':
        pass

    ################################################################
    # Tertiaries [T]                                             #
    ################################################################

    @abstractmethod
    def tertiary(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def tertiary_dim(self) -> Optional['DynamicColor']:
        pass

    @abstractmethod
    def on_tertiary(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def tertiary_container(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_tertiary_container(self) -> 'DynamicColor':
        pass

    ################################################################
    # Errors [E]                                                 #
    ################################################################

    @abstractmethod
    def error(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def error_dim(self) -> Optional['DynamicColor']:
        pass

    @abstractmethod
    def on_error(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def error_container(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_error_container(self) -> 'DynamicColor':
        pass

    ################################################################
    # Primary Fixed Colors [PF]                                  #
    ################################################################

    @abstractmethod
    def primary_fixed(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def primary_fixed_dim(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_primary_fixed(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_primary_fixed_variant(self) -> 'DynamicColor':
        pass

    ################################################################
    # Secondary Fixed Colors [QF]                                #
    ################################################################

    @abstractmethod
    def secondary_fixed(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def secondary_fixed_dim(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_secondary_fixed(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_secondary_fixed_variant(self) -> 'DynamicColor':
        pass

    ################################################################
    # Tertiary Fixed Colors [TF]                                 #
    ################################################################

    @abstractmethod
    def tertiary_fixed(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def tertiary_fixed_dim(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_tertiary_fixed(self) -> 'DynamicColor':
        pass

    @abstractmethod
    def on_tertiary_fixed_variant(self) -> 'DynamicColor':
        pass

    ################################################################
    # Other                                                      #
    ################################################################

    @abstractmethod
    def highest_surface(self, s: 'DynamicScheme') -> 'DynamicColor':
        pass
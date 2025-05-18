# scheme/scheme.py

from typing import Dict
from PyMCUlib.palettes.core_palette import CorePalette


class Scheme:
    """
    DEPRECATED. The `Scheme` class is deprecated in favor of `DynamicScheme`.

    Represents a Material color scheme, a mapping of color roles to colors.
    """

    def __init__(self, props: Dict[str, int]) -> None:
        """
        Private constructor for Scheme class.

        Args:
            props: A dictionary containing all color properties for the scheme.
        """
        self._props = props

    @property
    def primary(self) -> int:
        """Primary color."""
        return self._props["primary"]

    @property
    def on_primary(self) -> int:
        """Color used for text and icons on primary color."""
        return self._props["on_primary"]

    @property
    def primary_container(self) -> int:
        """Container color for the primary color."""
        return self._props["primary_container"]

    @property
    def on_primary_container(self) -> int:
        """Color used for text and icons on primary_container color."""
        return self._props["on_primary_container"]

    @property
    def secondary(self) -> int:
        """Secondary color."""
        return self._props["secondary"]

    @property
    def on_secondary(self) -> int:
        """Color used for text and icons on secondary color."""
        return self._props["on_secondary"]

    @property
    def secondary_container(self) -> int:
        """Container color for the secondary color."""
        return self._props["secondary_container"]

    @property
    def on_secondary_container(self) -> int:
        """Color used for text and icons on secondary_container color."""
        return self._props["on_secondary_container"]

    @property
    def tertiary(self) -> int:
        """Tertiary color."""
        return self._props["tertiary"]

    @property
    def on_tertiary(self) -> int:
        """Color used for text and icons on tertiary color."""
        return self._props["on_tertiary"]

    @property
    def tertiary_container(self) -> int:
        """Container color for the tertiary color."""
        return self._props["tertiary_container"]

    @property
    def on_tertiary_container(self) -> int:
        """Color used for text and icons on tertiary_container color."""
        return self._props["on_tertiary_container"]

    @property
    def error(self) -> int:
        """Error color."""
        return self._props["error"]

    @property
    def on_error(self) -> int:
        """Color used for text and icons on error color."""
        return self._props["on_error"]

    @property
    def error_container(self) -> int:
        """Container color for the error color."""
        return self._props["error_container"]

    @property
    def on_error_container(self) -> int:
        """Color used for text and icons on error_container color."""
        return self._props["on_error_container"]

    @property
    def background(self) -> int:
        """Background color."""
        return self._props["background"]

    @property
    def on_background(self) -> int:
        """Color used for text and icons on background color."""
        return self._props["on_background"]

    @property
    def surface(self) -> int:
        """Surface color."""
        return self._props["surface"]

    @property
    def on_surface(self) -> int:
        """Color used for text and icons on surface color."""
        return self._props["on_surface"]

    @property
    def surface_variant(self) -> int:
        """Surface variant color."""
        return self._props["surface_variant"]

    @property
    def on_surface_variant(self) -> int:
        """Color used for text and icons on surface_variant color."""
        return self._props["on_surface_variant"]

    @property
    def outline(self) -> int:
        """Outline color."""
        return self._props["outline"]

    @property
    def outline_variant(self) -> int:
        """Outline variant color."""
        return self._props["outline_variant"]

    @property
    def shadow(self) -> int:
        """Shadow color."""
        return self._props["shadow"]

    @property
    def scrim(self) -> int:
        """Scrim color."""
        return self._props["scrim"]

    @property
    def inverse_surface(self) -> int:
        """Inverse surface color."""
        return self._props["inverse_surface"]

    @property
    def inverse_on_surface(self) -> int:
        """Color used for text and icons on inverse_surface color."""
        return self._props["inverse_on_surface"]

    @property
    def inverse_primary(self) -> int:
        """Inverse primary color."""
        return self._props["inverse_primary"]

    @staticmethod
    def light(argb: int) -> 'Scheme':
        """
        Creates a light Material color scheme, based on the color's hue.

        Args:
            argb: ARGB representation of a color.

        Returns:
            Light Material color scheme, based on the color's hue.
        """
        return Scheme.light_from_core_palette(CorePalette.of(argb))

    @staticmethod
    def dark(argb: int) -> 'Scheme':
        """
        Creates a dark Material color scheme, based on the color's hue.

        Args:
            argb: ARGB representation of a color.

        Returns:
            Dark Material color scheme, based on the color's hue.
        """
        return Scheme.dark_from_core_palette(CorePalette.of(argb))

    @staticmethod
    def light_content(argb: int) -> 'Scheme':
        """
        Creates a light Material content color scheme, based on the color's hue.

        Args:
            argb: ARGB representation of a color.

        Returns:
            Light Material content color scheme, based on the color's hue.
        """
        return Scheme.light_from_core_palette(CorePalette.content_of(argb))

    @staticmethod
    def dark_content(argb: int) -> 'Scheme':
        """
        Creates a dark Material content color scheme, based on the color's hue.

        Args:
            argb: ARGB representation of a color.

        Returns:
            Dark Material content color scheme, based on the color's hue.
        """
        return Scheme.dark_from_core_palette(CorePalette.content_of(argb))

    @staticmethod
    def light_from_core_palette(core: CorePalette) -> 'Scheme':
        """
        Creates a light scheme from a core palette.

        Args:
            core: A CorePalette.

        Returns:
            A light scheme.
        """
        return Scheme({
            "primary": core.a1.tone(40),
            "on_primary": core.a1.tone(100),
            "primary_container": core.a1.tone(90),
            "on_primary_container": core.a1.tone(10),
            "secondary": core.a2.tone(40),
            "on_secondary": core.a2.tone(100),
            "secondary_container": core.a2.tone(90),
            "on_secondary_container": core.a2.tone(10),
            "tertiary": core.a3.tone(40),
            "on_tertiary": core.a3.tone(100),
            "tertiary_container": core.a3.tone(90),
            "on_tertiary_container": core.a3.tone(10),
            "error": core.error.tone(40),
            "on_error": core.error.tone(100),
            "error_container": core.error.tone(90),
            "on_error_container": core.error.tone(10),
            "background": core.n1.tone(99),
            "on_background": core.n1.tone(10),
            "surface": core.n1.tone(99),
            "on_surface": core.n1.tone(10),
            "surface_variant": core.n2.tone(90),
            "on_surface_variant": core.n2.tone(30),
            "outline": core.n2.tone(50),
            "outline_variant": core.n2.tone(80),
            "shadow": core.n1.tone(0),
            "scrim": core.n1.tone(0),
            "inverse_surface": core.n1.tone(20),
            "inverse_on_surface": core.n1.tone(95),
            "inverse_primary": core.a1.tone(80)
        })

    @staticmethod
    def dark_from_core_palette(core: CorePalette) -> 'Scheme':
        """
        Creates a dark scheme from a core palette.

        Args:
            core: A CorePalette.

        Returns:
            A dark scheme.
        """
        return Scheme({
            "primary": core.a1.tone(80),
            "on_primary": core.a1.tone(20),
            "primary_container": core.a1.tone(30),
            "on_primary_container": core.a1.tone(90),
            "secondary": core.a2.tone(80),
            "on_secondary": core.a2.tone(20),
            "secondary_container": core.a2.tone(30),
            "on_secondary_container": core.a2.tone(90),
            "tertiary": core.a3.tone(80),
            "on_tertiary": core.a3.tone(20),
            "tertiary_container": core.a3.tone(30),
            "on_tertiary_container": core.a3.tone(90),
            "error": core.error.tone(80),
            "on_error": core.error.tone(20),
            "error_container": core.error.tone(30),
            "on_error_container": core.error.tone(80),
            "background": core.n1.tone(10),
            "on_background": core.n1.tone(90),
            "surface": core.n1.tone(10),
            "on_surface": core.n1.tone(90),
            "surface_variant": core.n2.tone(30),
            "on_surface_variant": core.n2.tone(80),
            "outline": core.n2.tone(60),
            "outline_variant": core.n2.tone(30),
            "shadow": core.n1.tone(0),
            "scrim": core.n1.tone(0),
            "inverse_surface": core.n1.tone(90),
            "inverse_on_surface": core.n1.tone(20),
            "inverse_primary": core.a1.tone(40)
        })

    def to_json(self) -> Dict[str, int]:
        """
        Convert the scheme to a JSON serializable dictionary.

        Returns:
            A dictionary representation of the scheme.
        """
        return {**self._props}
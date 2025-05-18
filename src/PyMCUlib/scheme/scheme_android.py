# scheme/scheme_android.py
"""
Represents an Android 12 color scheme, a mapping of color roles to colors.
"""

from typing import Dict
from PyMCUlib.palettes.core_palette import CorePalette


class SchemeAndroid:
    """
    Represents an Android 12 color scheme, a mapping of color roles to colors.
    """

    def __init__(self, props: Dict[str, int]):
        """
        Private constructor for SchemeAndroid class.

        Args:
            props: A dictionary containing all color properties for the scheme.
        """
        self._props = props

    @property
    def color_accent_primary(self) -> int:
        """Color accent primary."""
        return self._props["color_accent_primary"]

    @property
    def color_accent_primary_variant(self) -> int:
        """Color accent primary variant."""
        return self._props["color_accent_primary_variant"]

    @property
    def color_accent_secondary(self) -> int:
        """Color accent secondary."""
        return self._props["color_accent_secondary"]

    @property
    def color_accent_secondary_variant(self) -> int:
        """Color accent secondary variant."""
        return self._props["color_accent_secondary_variant"]

    @property
    def color_accent_tertiary(self) -> int:
        """Color accent tertiary."""
        return self._props["color_accent_tertiary"]

    @property
    def color_accent_tertiary_variant(self) -> int:
        """Color accent tertiary variant."""
        return self._props["color_accent_tertiary_variant"]

    @property
    def text_color_primary(self) -> int:
        """Text color primary."""
        return self._props["text_color_primary"]

    @property
    def text_color_secondary(self) -> int:
        """Text color secondary."""
        return self._props["text_color_secondary"]

    @property
    def text_color_tertiary(self) -> int:
        """Text color tertiary."""
        return self._props["text_color_tertiary"]

    @property
    def text_color_primary_inverse(self) -> int:
        """Text color primary inverse."""
        return self._props["text_color_primary_inverse"]

    @property
    def text_color_secondary_inverse(self) -> int:
        """Text color secondary inverse."""
        return self._props["text_color_secondary_inverse"]

    @property
    def text_color_tertiary_inverse(self) -> int:
        """Text color tertiary inverse."""
        return self._props["text_color_tertiary_inverse"]

    @property
    def color_background(self) -> int:
        """Color background."""
        return self._props["color_background"]

    @property
    def color_background_floating(self) -> int:
        """Color background floating."""
        return self._props["color_background_floating"]

    @property
    def color_surface(self) -> int:
        """Color surface."""
        return self._props["color_surface"]

    @property
    def color_surface_variant(self) -> int:
        """Color surface variant."""
        return self._props["color_surface_variant"]

    @property
    def color_surface_highlight(self) -> int:
        """Color surface highlight."""
        return self._props["color_surface_highlight"]

    @property
    def surface_header(self) -> int:
        """Surface header."""
        return self._props["surface_header"]

    @property
    def under_surface(self) -> int:
        """Under surface."""
        return self._props["under_surface"]

    @property
    def off_state(self) -> int:
        """Off state."""
        return self._props["off_state"]

    @property
    def accent_surface(self) -> int:
        """Accent surface."""
        return self._props["accent_surface"]

    @property
    def text_primary_on_accent(self) -> int:
        """Text primary on accent."""
        return self._props["text_primary_on_accent"]

    @property
    def text_secondary_on_accent(self) -> int:
        """Text secondary on accent."""
        return self._props["text_secondary_on_accent"]

    @property
    def volume_background(self) -> int:
        """Volume background."""
        return self._props["volume_background"]

    @property
    def scrim(self) -> int:
        """Scrim."""
        return self._props["scrim"]

    @staticmethod
    def light(argb: int) -> 'SchemeAndroid':
        """
        Creates a light Android color scheme, based on the color's hue.

        Args:
            argb: ARGB representation of a color.

        Returns:
            Light Android color scheme, based on the color's hue.
        """
        core = CorePalette.of(argb)
        return SchemeAndroid.light_from_core_palette(core)

    @staticmethod
    def dark(argb: int) -> 'SchemeAndroid':
        """
        Creates a dark Android color scheme, based on the color's hue.

        Args:
            argb: ARGB representation of a color.

        Returns:
            Dark Android color scheme, based on the color's hue.
        """
        core = CorePalette.of(argb)
        return SchemeAndroid.dark_from_core_palette(core)

    @staticmethod
    def light_content(argb: int) -> 'SchemeAndroid':
        """
        Creates a light Android content color scheme, based on the color's hue.

        Args:
            argb: ARGB representation of a color.

        Returns:
            Light Android content color scheme, based on the color's hue.
        """
        core = CorePalette.content_of(argb)
        return SchemeAndroid.light_from_core_palette(core)

    @staticmethod
    def dark_content(argb: int) -> 'SchemeAndroid':
        """
        Creates a dark Android content color scheme, based on the color's hue.

        Args:
            argb: ARGB representation of a color.

        Returns:
            Dark Android content color scheme, based on the color's hue.
        """
        core = CorePalette.content_of(argb)
        return SchemeAndroid.dark_from_core_palette(core)

    @staticmethod
    def light_from_core_palette(core: CorePalette) -> 'SchemeAndroid':
        """
        Creates a light scheme from a core palette.

        Args:
            core: A CorePalette.

        Returns:
            A light Android scheme.
        """
        return SchemeAndroid({
            "color_accent_primary": core.a1.tone(90),
            "color_accent_primary_variant": core.a1.tone(40),
            "color_accent_secondary": core.a2.tone(90),
            "color_accent_secondary_variant": core.a2.tone(40),
            "color_accent_tertiary": core.a3.tone(90),
            "color_accent_tertiary_variant": core.a3.tone(40),
            "text_color_primary": core.n1.tone(10),
            "text_color_secondary": core.n2.tone(30),
            "text_color_tertiary": core.n2.tone(50),
            "text_color_primary_inverse": core.n1.tone(95),
            "text_color_secondary_inverse": core.n1.tone(80),
            "text_color_tertiary_inverse": core.n1.tone(60),
            "color_background": core.n1.tone(95),
            "color_background_floating": core.n1.tone(98),
            "color_surface": core.n1.tone(98),
            "color_surface_variant": core.n1.tone(90),
            "color_surface_highlight": core.n1.tone(100),
            "surface_header": core.n1.tone(90),
            "under_surface": core.n1.tone(0),
            "off_state": core.n1.tone(20),
            "accent_surface": core.a2.tone(95),
            "text_primary_on_accent": core.n1.tone(10),
            "text_secondary_on_accent": core.n2.tone(30),
            "volume_background": core.n1.tone(25),
            "scrim": core.n1.tone(80),
        })

    @staticmethod
    def dark_from_core_palette(core: CorePalette) -> 'SchemeAndroid':
        """
        Creates a dark scheme from a core palette.

        Args:
            core: A CorePalette.

        Returns:
            A dark Android scheme.
        """
        return SchemeAndroid({
            "color_accent_primary": core.a1.tone(90),
            "color_accent_primary_variant": core.a1.tone(70),
            "color_accent_secondary": core.a2.tone(90),
            "color_accent_secondary_variant": core.a2.tone(70),
            "color_accent_tertiary": core.a3.tone(90),
            "color_accent_tertiary_variant": core.a3.tone(70),
            "text_color_primary": core.n1.tone(95),
            "text_color_secondary": core.n2.tone(80),
            "text_color_tertiary": core.n2.tone(60),
            "text_color_primary_inverse": core.n1.tone(10),
            "text_color_secondary_inverse": core.n1.tone(30),
            "text_color_tertiary_inverse": core.n1.tone(50),
            "color_background": core.n1.tone(10),
            "color_background_floating": core.n1.tone(10),
            "color_surface": core.n1.tone(20),
            "color_surface_variant": core.n1.tone(30),
            "color_surface_highlight": core.n1.tone(35),
            "surface_header": core.n1.tone(30),
            "under_surface": core.n1.tone(0),
            "off_state": core.n1.tone(20),
            "accent_surface": core.a2.tone(95),
            "text_primary_on_accent": core.n1.tone(10),
            "text_secondary_on_accent": core.n2.tone(30),
            "volume_background": core.n1.tone(25),
            "scrim": core.n1.tone(80),
        })

    def to_json(self) -> Dict[str, int]:
        """
        Convert the scheme to a JSON serializable dictionary.

        Returns:
            A dictionary representation of the scheme.
        """
        return {**self._props}
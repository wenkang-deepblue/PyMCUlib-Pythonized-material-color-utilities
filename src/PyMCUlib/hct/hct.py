# hct/hct.py

"""
A color system built using CAM16 hue and chroma, and L* from
L*a*b*.

Using L* creates a link between the color system, contrast, and thus
accessibility. Contrast ratio depends on relative luminance, or Y in the XYZ
color space. L*, or perceptual luminance can be calculated from Y.

Unlike Y, L* is linear to human perception, allowing trivial creation of
accurate color tones.

Unlike contrast ratio, measuring contrast in L* is linear, and simple to
calculate. A difference of 40 in HCT tone guarantees a contrast ratio >= 3.0,
and a difference of 50 guarantees a contrast ratio >= 4.5.
"""

from PyMCUlib.utils import color_utils
from PyMCUlib.hct.cam16 import Cam16
from PyMCUlib.hct.hct_solver import HctSolver
from PyMCUlib.hct.viewing_conditions import ViewingConditions


class Hct:
    """
    HCT, hue, chroma, and tone. A color system that provides a perceptually
    accurate color measurement system that can also accurately render what colors
    will appear as in different lighting environments.
    """

    @classmethod
    def from_hct(cls, hue: float, chroma: float, tone: float) -> "Hct":
        """
        Create an HCT color from hue, chroma, and tone.
        
        Args:
            hue: 0 <= hue < 360; invalid values are corrected.
            chroma: 0 <= chroma < ?; Informally, colorfulness. The color
                returned may be lower than the requested chroma. Chroma has a different
                maximum for any given hue and tone.
            tone: 0 <= tone <= 100; invalid values are corrected.
        
        Returns:
            HCT representation of a color in default viewing conditions.
        """
        return cls(HctSolver.solve_to_int(hue, chroma, tone))

    @classmethod
    def from_int(cls, argb: int) -> "Hct":
        """
        Create an HCT color from an ARGB integer.
        
        Args:
            argb: ARGB representation of a color.
        
        Returns:
            HCT representation of a color in default viewing conditions
        """
        return cls(argb)

    def to_int(self) -> int:
        """
        Convert to ARGB integer representation.
        
        Returns:
            ARGB representation of the color
        """
        return self.argb

    @property
    def hue(self) -> float:
        """
        A number, in degrees, representing ex. red, orange, yellow, etc.
        Ranges from 0 <= hue < 360.
        """
        return self.internal_hue

    @hue.setter
    def hue(self, new_hue: float) -> None:
        """
        Set the hue of the color.
        
        Args:
            new_hue: 0 <= new_hue < 360; invalid values are corrected.
                Chroma may decrease because chroma has a different maximum for any given
                hue and tone.
        """
        self._set_internal_state(
            HctSolver.solve_to_int(
                new_hue,
                self.internal_chroma,
                self.internal_tone,
            ),
        )

    @property
    def chroma(self) -> float:
        """
        Get the chroma of the color.
        """
        return self.internal_chroma

    @chroma.setter
    def chroma(self, new_chroma: float) -> None:
        """
        Set the chroma of the color.
        
        Args:
            new_chroma: 0 <= new_chroma < ?
                Chroma may decrease because chroma has a different maximum for any given
                hue and tone.
        """
        self._set_internal_state(
            HctSolver.solve_to_int(
                self.internal_hue,
                new_chroma,
                self.internal_tone,
            ),
        )

    @property
    def tone(self) -> float:
        """
        Lightness. Ranges from 0 to 100.
        """
        return self.internal_tone

    @tone.setter
    def tone(self, new_tone: float) -> None:
        """
        Set the tone of the color.
        
        Args:
            new_tone: 0 <= new_tone <= 100; invalid values are corrected.
                Chroma may decrease because chroma has a different maximum for any given
                hue and tone.
        """
        self._set_internal_state(
            HctSolver.solve_to_int(
                self.internal_hue,
                self.internal_chroma,
                new_tone,
            ),
        )

    def set_value(self, property_name: str, value: float) -> None:
        """
        Sets a property of the Hct object.
        
        Args:
            property_name: String, property to set
            value: Value to set for the property
        """
        setattr(self, property_name, value)

    def __str__(self) -> str:
        """
        Returns a string representation of the color.
        
        Returns:
            String representation of the color
        """
        return f"HCT({int(self.hue)}, {int(self.chroma)}, {int(self.tone)})"

    @staticmethod
    def is_blue(hue: float) -> bool:
        """
        Check if the hue represents a blue color.
        
        Args:
            hue: Hue in degrees
            
        Returns:
            True if the hue is in the blue range
        """
        return hue >= 250 and hue < 270

    @staticmethod
    def is_yellow(hue: float) -> bool:
        """
        Check if the hue represents a yellow color.
        
        Args:
            hue: Hue in degrees
            
        Returns:
            True if the hue is in the yellow range
        """
        return hue >= 105 and hue < 125

    @staticmethod
    def is_cyan(hue: float) -> bool:
        """
        Check if the hue represents a cyan color.
        
        Args:
            hue: Hue in degrees
            
        Returns:
            True if the hue is in the cyan range
        """
        return hue >= 170 and hue < 207

    def __init__(self, argb: int) -> None:
        """
        Create an HCT color from an ARGB integer.
        
        Args:
            argb: ARGB representation of a color.
        """
        cam = Cam16.from_int(argb)
        self.internal_hue = cam.hue
        self.internal_chroma = cam.chroma
        self.internal_tone = color_utils.lstar_from_argb(argb)
        self.argb = argb

    def _set_internal_state(self, argb: int) -> None:
        """
        Update the internal state of the HCT object.
        
        Args:
            argb: ARGB representation of a color.
        """
        cam = Cam16.from_int(argb)
        self.internal_hue = cam.hue
        self.internal_chroma = cam.chroma
        self.internal_tone = color_utils.lstar_from_argb(argb)
        self.argb = argb

    def in_viewing_conditions(self, vc: ViewingConditions) -> "Hct":
        """
        Translates a color into different ViewingConditions.

        Colors change appearance. They look different with lights on versus off,
        the same color, as in hex code, on white looks different when on black.
        This is called color relativity, most famously explicated by Josef Albers
        in Interaction of Color.

        In color science, color appearance models can account for this and
        calculate the appearance of a color in different settings. HCT is based on
        CAM16, a color appearance model, and uses it to make these calculations.
        
        Args:
            vc: ViewingConditions object representing the viewing environment
            
        Returns:
            Hct object representing the color in the new viewing conditions
        
        See:
            ViewingConditions.make for parameters affecting color appearance.
        """
        # 1. Use CAM16 to find XYZ coordinates of color in specified VC.
        cam = Cam16.from_int(self.to_int())
        viewed_in_vc = cam.xyz_in_viewing_conditions(vc)

        # 2. Create CAM16 of those XYZ coordinates in default VC.
        recast_in_vc = Cam16.from_xyz_in_viewing_conditions(
            viewed_in_vc[0],
            viewed_in_vc[1],
            viewed_in_vc[2],
            ViewingConditions.make(),
        )

        # 3. Create HCT from:
        # - CAM16 using default VC with XYZ coordinates in specified VC.
        # - L* converted from Y in XYZ coordinates in specified VC.
        recast_hct = Hct.from_hct(
            recast_in_vc.hue,
            recast_in_vc.chroma,
            color_utils.lstar_from_y(viewed_in_vc[1]),
        )
        return recast_hct
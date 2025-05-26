# hct.py

from dataclasses import dataclass
from PyMCUlib_cpp.utils.utils import Argb, lstar_from_argb
from PyMCUlib_cpp.cam.cam import cam_from_int
from PyMCUlib_cpp.cam.hct_solver import solve_to_int

@dataclass
class Hct:
    """
    HCT: hue, chroma, and tone.
    
    A color system built using CAM16 hue and chroma, and L* (lightness) from
    the L*a*b* color space, providing a perceptually accurate
    color measurement system that can also accurately render what colors
    will appear as in different lighting environments.
    
    Using L* creates a link between the color system, contrast, and thus
    accessibility. Contrast ratio depends on relative luminance, or Y in the XYZ
    color space. L*, or perceptual luminance can be calculated from Y.
    
    Unlike Y, L* is linear to human perception, allowing trivial creation of
    accurate color tones.
    
    Unlike contrast ratio, measuring contrast in L* is linear, and simple to
    calculate. A difference of 40 in HCT tone guarantees a contrast ratio >= 3.0,
    and a difference of 50 guarantees a contrast ratio >= 4.5.
    """
    
    # Private attributes
    _hue: float = 0.0
    _chroma: float = 0.0
    _tone: float = 0.0
    _argb: int = 0
    
    @staticmethod
    def from_hct(hue: float, chroma: float, tone: float) -> 'Hct':
        """
        Creates an HCT color from hue, chroma, and tone.
        
        Args:
            hue: 0 <= hue < 360; invalid values are corrected.
            chroma: >= 0; the maximum value of chroma depends on the hue
            and tone. May be lower than the requested chroma.
            tone: 0 <= tone <= 100; invalid values are corrected.
        
        Returns:
            HCT representation of a color in default viewing conditions.
        """
        argb = solve_to_int(hue, chroma, tone)
        return Hct.from_int(argb)
    
    @staticmethod
    def from_int(argb: int) -> 'Hct':
        """
        Creates an HCT color from a color.
        
        Args:
            argb: ARGB representation of a color.
        
        Returns:
            HCT representation of a color in default viewing conditions
        """
        hct = Hct()
        hct._set_internal_state(argb)
        return hct
    
    def get_hue(self) -> float:
        """
        Returns the hue of the color.
        
        Returns:
            hue of the color, in degrees.
        """
        return self._hue
    
    def get_chroma(self) -> float:
        """
        Returns the chroma of the color.
        
        Returns:
            chroma of the color.
        """
        return self._chroma
    
    def get_tone(self) -> float:
        """
        Returns the tone of the color.
        
        Returns:
            tone of the color, satisfying 0 <= tone <= 100.
        """
        return self._tone
    
    def to_int(self) -> int:
        """
        Returns the color in ARGB format.
        
        Returns:
            an integer, representing the color in ARGB format.
        """
        return self._argb
    
    def set_hue(self, hue: float) -> None:
        """
        Sets the hue of this color. Chroma may decrease because chroma has a
        different maximum for any given hue and tone.
        
        Args:
            hue: 0 <= hue < 360; invalid values are corrected.
        """
        self._set_internal_state(solve_to_int(hue, self._chroma, self._tone))
    
    def set_chroma(self, chroma: float) -> None:
        """
        Sets the chroma of this color. Chroma may decrease because chroma has a
        different maximum for any given hue and tone.
        
        Args:
            chroma: 0 <= chroma < ?
        """
        self._set_internal_state(solve_to_int(self._hue, chroma, self._tone))
    
    def set_tone(self, tone: float) -> None:
        """
        Sets the tone of this color. Chroma may decrease because chroma has a
        different maximum for any given hue and tone.
        
        Args:
            tone: 0 <= tone <= 100; invalid valids are corrected.
        """
        self._set_internal_state(solve_to_int(self._hue, self._chroma, tone))
    
    def _set_internal_state(self, argb: int) -> None:
        """
        Sets the Hct object to represent an sRGB color.
        
        Args:
            argb: the new color as an integer in ARGB format.
        """
        self._argb = argb
        cam = cam_from_int(argb)
        self._hue = cam.hue
        self._chroma = cam.chroma
        self._tone = lstar_from_argb(argb)

    def __eq__(self, other):
        """
        Compares this Hct object with another for equality.
        
        Two Hct objects are considered equal if all their components 
        (hue, chroma, tone, and argb) are equal.
        
        Args:
            other: The object to compare with
            
        Returns:
            True if the objects are equal, False otherwise
        """
        if not isinstance(other, Hct):
            return False
        return (self._hue == other._hue and 
                self._chroma == other._chroma and 
                self._tone == other._tone and
                self._argb == other._argb)

    def __hash__(self):
        """
        Generates a hash value for this Hct object.
        
        The hash is based on all components (hue, chroma, tone, and argb)
        to ensure that two equal Hct objects have the same hash value.
        
        Returns:
            A hash value for this object
        """
        return hash((self._hue, self._chroma, self._tone, self._argb))
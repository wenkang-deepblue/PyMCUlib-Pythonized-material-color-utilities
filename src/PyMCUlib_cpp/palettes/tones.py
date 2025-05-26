# tones.py

from typing import Dict
from PyMCUlib_cpp.utils.utils import Argb
from PyMCUlib_cpp.cam.cam import cam_from_int, int_from_hcl
from PyMCUlib_cpp.cam.hct import Hct

class KeyColor:
    """
    Key color is a color that represents the hue and chroma of a tonal palette
    """
    def __init__(self, hue: float, requested_chroma: float):
        self._hue = hue
        self._requested_chroma = requested_chroma
        self._max_chroma_value = 200.0
        self._chroma_cache: Dict[float, float] = {}

    def max_chroma(self, tone: float) -> float:
        """
        Calculates the maximum achievable chroma for a given tone.
        
        Args:
            tone: The tone value
            
        Returns:
            Maximum achievable chroma
        """
        if tone in self._chroma_cache:
            return self._chroma_cache[tone]

        chroma = Hct.from_hct(self._hue, self._max_chroma_value, tone).get_chroma()
        self._chroma_cache[tone] = chroma
        return chroma

    def create(self) -> Hct:
        """
        Creates a key color from a [hue] and a [chroma].
        The key color is the first tone, starting from T50, matching the given hue
        and chroma.
        
        Returns:
            Key color in Hct.
        """
        # Pivot around T50 because T50 has the most chroma available, on
        # average. Thus it is most likely to have a direct answer.
        pivot_tone = 50
        tone_step_size = 1
        # Epsilon to accept values slightly higher than the requested chroma.
        epsilon = 0.01

        # Binary search to find the tone that can provide a chroma that is closest
        # to the requested chroma.
        lower_tone = 0
        upper_tone = 100
        while lower_tone < upper_tone:
            mid_tone = (lower_tone + upper_tone) // 2
            is_ascending = self.max_chroma(mid_tone) < self.max_chroma(mid_tone + tone_step_size)
            sufficient_chroma = self.max_chroma(mid_tone) >= self._requested_chroma - epsilon

            if sufficient_chroma:
                # Either range [lower_tone, mid_tone] or [mid_tone, upper_tone] has
                # the answer, so search in the range that is closer the pivot tone.
                if abs(lower_tone - pivot_tone) < abs(upper_tone - pivot_tone):
                    upper_tone = mid_tone
                else:
                    if lower_tone == mid_tone:
                        return Hct.from_hct(self._hue, self._requested_chroma, lower_tone)
                    lower_tone = mid_tone
            else:
                # As there's no sufficient chroma in the mid_tone, follow the direction
                # to the chroma peak.
                if is_ascending:
                    lower_tone = mid_tone + tone_step_size
                else:
                    # Keep mid_tone for potential chroma peak.
                    upper_tone = mid_tone

        return Hct.from_hct(self._hue, self._requested_chroma, lower_tone)

class TonalPalette:
    """
    A convenience class for retrieving colors that are constant in hue and chroma, but vary in tone.
    """
    
    def __init__(self, arg1, arg2=None, arg3=None):
        """
        Initialize a TonalPalette from various inputs:
        1. TonalPalette(argb) - from ARGB color
        2. TonalPalette(hct) - from HCT color
        3. TonalPalette(hue, chroma) - from hue and chroma values
        4. TonalPalette(hue, chroma, key_color) - from hue, chroma and key color
        """
        if arg2 is None and arg3 is None:
            if isinstance(arg1, int):
                # TonalPalette(argb)
                self._init_from_argb(arg1)
            else:
                # TonalPalette(hct)
                self._init_from_hct(arg1)
        elif arg3 is None:
            # TonalPalette(hue, chroma)
            self._init_from_hue_chroma(arg1, arg2)
        else:
            # TonalPalette(hue, chroma, key_color)
            self._init_from_hue_chroma_key(arg1, arg2, arg3)
    
    def _init_from_argb(self, argb: Argb):
        """Initialize from ARGB value"""
        cam = cam_from_int(argb)
        self._hue = cam.hue
        self._chroma = cam.chroma
        self._key_color = KeyColor(cam.hue, cam.chroma).create()
    
    def _init_from_hct(self, hct: Hct):
        """Initialize from HCT object"""
        self._hue = hct.get_hue()
        self._chroma = hct.get_chroma()
        self._key_color = hct
    
    def _init_from_hue_chroma(self, hue: float, chroma: float):
        """Initialize from hue and chroma values"""
        self._hue = hue
        self._chroma = chroma
        self._key_color = KeyColor(hue, chroma).create()
    
    def _init_from_hue_chroma_key(self, hue: float, chroma: float, key_color: Hct):
        """Initialize from hue, chroma and key color"""
        self._hue = hue
        self._chroma = chroma
        self._key_color = key_color
    
    def get(self, tone: float) -> Argb:
        """
        Returns the color for a given tone in this palette.
        
        Args:
            tone: 0.0 <= tone <= 100.0
            
        Returns:
            a color as an integer, in ARGB format.
        """
        return int_from_hcl(self._hue, self._chroma, tone)
    
    def get_hue(self) -> float:
        """Returns the hue of this palette."""
        return self._hue
    
    def get_chroma(self) -> float:
        """Returns the chroma of this palette."""
        return self._chroma
    
    def get_key_color(self) -> Hct:
        """Returns the key color of this palette."""
        return self._key_color
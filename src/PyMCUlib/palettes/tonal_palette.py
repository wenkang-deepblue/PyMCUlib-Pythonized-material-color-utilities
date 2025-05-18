# palettes/tonal_palette.py

"""
A convenience class for retrieving colors that are constant in hue and
chroma, but vary in tone.
"""

from PyMCUlib.hct.hct import Hct


class TonalPalette:
    """
    A convenience class for retrieving colors that are constant in hue and
    chroma, but vary in tone.
    """

    def __init__(self, hue: float, chroma: float, key_color: Hct) -> None:
        """
        Initialize a TonalPalette with specific hue, chroma, and key color.
        
        Args:
            hue: HCT hue
            chroma: HCT chroma
            key_color: Hct object that represents the key color
        """
        self.hue = hue
        self.chroma = chroma
        self.key_color = key_color
        self._cache = {}

    @staticmethod
    def from_int(argb: int) -> 'TonalPalette':
        """
        Create a TonalPalette from an ARGB integer.
        
        Args:
            argb: ARGB representation of a color
            
        Returns:
            Tones matching that color's hue and chroma.
        """
        hct = Hct.from_int(argb)
        return TonalPalette.from_hct(hct)

    @staticmethod
    def from_hct(hct: Hct) -> 'TonalPalette':
        """
        Create a TonalPalette from an Hct object.
        
        Args:
            hct: Hct object
            
        Returns:
            Tones matching that color's hue and chroma.
        """
        return TonalPalette(hct.hue, hct.chroma, hct)

    @staticmethod
    def from_hue_and_chroma(hue: float, chroma: float) -> 'TonalPalette':
        """
        Create a TonalPalette from hue and chroma values.
        
        Args:
            hue: HCT hue
            chroma: HCT chroma
            
        Returns:
            Tones matching hue and chroma.
        """
        key_color = KeyColor(hue, chroma).create()
        return TonalPalette(hue, chroma, key_color)

    def tone(self, tone: float) -> int:
        """
        Get the ARGB representation of a color with specified tone.
        
        Args:
            tone: HCT tone, measured from 0 to 100.
            
        Returns:
            ARGB representation of a color with that tone.
        """
        if tone not in self._cache:
            self._cache[tone] = Hct.from_hct(self.hue, self.chroma, tone).to_int()
        return self._cache[tone]

    def get_hct(self, tone: float) -> Hct:
        """
        Get the HCT representation of a color with specified tone.
        
        Args:
            tone: HCT tone.
            
        Returns:
            HCT representation of a color with that tone.
        """
        return Hct.from_int(self.tone(tone))


class KeyColor:
    """
    Key color is a color that represents the hue and chroma of a tonal palette
    """

    def __init__(self, hue: float, requested_chroma: float) -> None:
        """
        Initialize a KeyColor with specific hue and requested chroma.
        
        Args:
            hue: HCT hue
            requested_chroma: HCT chroma
        """
        self.hue = hue
        self.requested_chroma = requested_chroma
        self._chroma_cache = {}
        self._max_chroma_value = 200.0

    def create(self) -> Hct:
        """
        Creates a key color from a hue and a chroma.
        The key color is the first tone, starting from T50, matching the given hue
        and chroma.
        
        Returns:
            Key color Hct
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
            mid_tone = int((lower_tone + upper_tone) / 2)
            is_ascending = self._max_chroma(mid_tone) < self._max_chroma(mid_tone + tone_step_size)
            sufficient_chroma = self._max_chroma(mid_tone) >= self.requested_chroma - epsilon

            if sufficient_chroma:
                # Either range [lower_tone, mid_tone] or [mid_tone, upper_tone] has
                # the answer, so search in the range that is closer the pivot tone.
                if abs(lower_tone - pivot_tone) < abs(upper_tone - pivot_tone):
                    upper_tone = mid_tone
                else:
                    if lower_tone == mid_tone:
                        return Hct.from_hct(self.hue, self.requested_chroma, lower_tone)
                    lower_tone = mid_tone
            else:
                # As there is no sufficient chroma in the mid_tone, follow the direction
                # to the chroma peak.
                if is_ascending:
                    lower_tone = mid_tone + tone_step_size
                else:
                    # Keep mid_tone for potential chroma peak.
                    upper_tone = mid_tone

        return Hct.from_hct(self.hue, self.requested_chroma, lower_tone)

    def _max_chroma(self, tone: float) -> float:
        """
        Find the maximum chroma for a given tone.
        
        Args:
            tone: HCT tone
            
        Returns:
            Maximum available chroma for the given tone
        """
        if tone in self._chroma_cache:
            return self._chroma_cache[tone]
        
        chroma = Hct.from_hct(self.hue, self._max_chroma_value, tone).chroma
        self._chroma_cache[tone] = chroma
        return chroma
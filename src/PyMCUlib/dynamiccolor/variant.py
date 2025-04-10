# variant.py

from enum import Enum

class Variant(Enum):
    """
    Variants for Dynamic Colors.
    
    Different color schemes that determine how colors are arranged in the UI.
    """
    MONOCHROME = 0
    NEUTRAL = 1
    TONAL_SPOT = 2
    VIBRANT = 3
    EXPRESSIVE = 4
    FIDELITY = 5
    CONTENT = 6
    RAINBOW = 7
    FRUIT_SALAD = 8
# dynamiccolor/variant.py

"""
Set of themes supported by Dynamic Color.
Instantiate the corresponding subclass, ex. SchemeTonalSpot, to create
colors corresponding to the theme.
"""

from enum import IntEnum

class Variant(IntEnum):
    """
    Set of themes supported by Dynamic Color.
    Instantiate the corresponding subclass, ex. SchemeTonalSpot, to create
    colors corresponding to the theme.
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
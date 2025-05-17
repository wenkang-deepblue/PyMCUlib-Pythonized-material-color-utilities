# dynamiccolor/contrast_curve.py

"""
A class containing a value that changes with the contrast level.

Usually represents the contrast requirements for a dynamic color on its
background. The four values correspond to values for contrast levels -1.0,
0.0, 0.5, and 1.0, respectively.
"""

from PyMCUlib.utils import math_utils

class ContrastCurve:
    """
    A class containing a value that changes with the contrast level.

    Usually represents the contrast requirements for a dynamic color on its
    background. The four values correspond to values for contrast levels -1.0,
    0.0, 0.5, and 1.0, respectively.
    """

    def __init__(self, low: float, normal: float, medium: float, high: float):
        """
        Creates a `ContrastCurve` object.

        Args:
            low: Value for contrast level -1.0
            normal: Value for contrast level 0.0
            medium: Value for contrast level 0.5
            high: Value for contrast level 1.0
        """
        self.low = low
        self.normal = normal
        self.medium = medium
        self.high = high

    def get(self, contrast_level: float) -> float:
        """
        Returns the value at a given contrast level.

        Args:
            contrast_level: The contrast level. 0.0 is the default (normal); -1.0
                is the lowest; 1.0 is the highest.

        Returns:
            The value. For contrast ratios, a number between 1.0 and 21.0.
        """
        if contrast_level <= -1.0:
            return self.low
        elif contrast_level < 0.0:
            return math_utils.lerp(self.low, self.normal, (contrast_level - (-1)) / 1)
        elif contrast_level < 0.5:
            return math_utils.lerp(self.normal, self.medium, (contrast_level - 0) / 0.5)
        elif contrast_level < 1.0:
            return math_utils.lerp(self.medium, self.high, (contrast_level - 0.5) / 0.5)
        else:
            return self.high
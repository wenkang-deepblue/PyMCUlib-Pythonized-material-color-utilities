# quantize/point_provider.py

from abc import ABC, abstractmethod
from typing import List


class PointProvider(ABC):
    """
    An interface to allow use of different color spaces by
    quantizers.
    """

    @abstractmethod
    def to_int(self, point: List[float]) -> int:
        """
        Converts a point in a color space to an ARGB integer.
        
        Args:
            point: Color coordinates in the color space
            
        Returns:
            The color represented as an ARGB integer
        """
        pass

    @abstractmethod
    def from_int(self, argb: int) -> List[float]:
        """
        Converts an ARGB integer to a point in a color space.
        
        Args:
            argb: The color represented as an ARGB integer
            
        Returns:
            Color coordinates in the color space
        """
        pass

    @abstractmethod
    def distance(self, from_point: List[float], to_point: List[float]) -> float:
        """
        Calculates the distance between two points in a color space.
        
        Args:
            from_point: The first point in the color space
            to_point: The second point in the color space
            
        Returns:
            The distance between the two points
        """
        pass
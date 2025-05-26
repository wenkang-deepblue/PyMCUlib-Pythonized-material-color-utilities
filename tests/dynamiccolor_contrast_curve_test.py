# test_contrast_curve.py

import unittest
from PyMCUlib_cpp.dynamiccolor.contrast_curve import ContrastCurve

class TestContrastCurve(unittest.TestCase):
    
    def test_contrast_curve_initialization(self):
        """Test that contrast curve can be properly initialized."""
        curve = ContrastCurve(1.0, 2.0, 3.0, 4.0)
        self.assertEqual(curve.low, 1.0)
        self.assertEqual(curve.normal, 2.0)
        self.assertEqual(curve.medium, 3.0)
        self.assertEqual(curve.high, 4.0)
    
    def test_get_at_defined_levels(self):
        """Test that get() returns the exact values at defined contrast levels."""
        curve = ContrastCurve(1.0, 2.0, 3.0, 4.0)
        self.assertEqual(curve.get(-1.0), 1.0)  # low
        self.assertEqual(curve.get(0.0), 2.0)   # normal
        self.assertEqual(curve.get(0.5), 3.0)   # medium
        self.assertEqual(curve.get(1.0), 4.0)   # high
    
    def test_get_beyond_boundaries(self):
        """Test that get() handles values beyond the defined range."""
        curve = ContrastCurve(1.0, 2.0, 3.0, 4.0)
        self.assertEqual(curve.get(-2.0), 1.0)  # below low
        self.assertEqual(curve.get(2.0), 4.0)   # above high
    
    def test_get_interpolation(self):
        """Test that get() properly interpolates between defined levels."""
        curve = ContrastCurve(1.0, 2.0, 3.0, 4.0)
        # Test interpolation between low and normal
        self.assertEqual(curve.get(-0.5), 1.5)  
        # Test interpolation between normal and medium
        self.assertEqual(curve.get(0.25), 2.5)  
        # Test interpolation between medium and high
        self.assertEqual(curve.get(0.75), 3.5)  

if __name__ == "__main__":
    unittest.main()
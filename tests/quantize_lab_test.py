# lab_test.py

import unittest
from PyMCUlib.quantize.lab import Lab, int_from_lab, lab_from_int
import PyMCUlib.utils.utils as utils

class LabTest(unittest.TestCase):
    def test_lab_from_int(self):
        """Tests converting from ARGB to Lab."""
        # Test with a blue color
        lab = lab_from_int(0xFF0000FF)
        self.assertAlmostEqual(lab.l, 32.302586, delta=0.05)
        self.assertAlmostEqual(lab.a, 79.196655, delta=0.05)
        self.assertAlmostEqual(lab.b, -107.863681, delta=0.05)
        
        # Test with a red color
        lab = lab_from_int(0xFFFF0000)
        self.assertAlmostEqual(lab.l, 53.237103, delta=0.05)
        self.assertAlmostEqual(lab.a, 80.092781, delta=0.05)
        self.assertAlmostEqual(lab.b, 67.203003, delta=0.05)
        
        # Test with white
        lab = lab_from_int(0xFFFFFFFF)
        self.assertAlmostEqual(lab.l, 100.0, delta=0.05)
        self.assertAlmostEqual(lab.a, 0.0, delta=0.05)
        self.assertAlmostEqual(lab.b, 0.0, delta=0.05)
        
        # Test with black
        lab = lab_from_int(0xFF000000)
        self.assertAlmostEqual(lab.l, 0.0, delta=0.05)
        self.assertAlmostEqual(lab.a, 0.0, delta=0.05)
        self.assertAlmostEqual(lab.b, 0.0, delta=0.05)

    def test_int_from_lab(self):
        """Tests converting from Lab to ARGB."""
        # Test with a blue-like Lab color
        argb = int_from_lab(Lab(32.302586, 79.196655, -107.863681))
        self.assertEqual(argb & 0xFF000000, 0xFF000000)  # Alpha should be 0xFF
        self.assertLess(argb & 0x00FF0000, 0x00100000)   # Red should be small
        self.assertLess(argb & 0x0000FF00, 0x00001000)   # Green should be small
        self.assertGreater(argb & 0x000000FF, 0x000000F0) # Blue should be large
        
        # Test with a red-like Lab color
        argb = int_from_lab(Lab(53.237103, 80.092781, 67.203003))
        self.assertEqual(argb & 0xFF000000, 0xFF000000)  # Alpha should be 0xFF
        self.assertGreater(argb & 0x00FF0000, 0x00F00000) # Red should be large
        self.assertLess(argb & 0x0000FF00, 0x00001000)    # Green should be small
        self.assertLess(argb & 0x000000FF, 0x00000010)    # Blue should be small
        
        # Test white
        argb = int_from_lab(Lab(100.0, 0.0, 0.0))
        self.assertEqual(argb, 0xFFFFFFFF)
        
        # Test black
        argb = int_from_lab(Lab(0.0, 0.0, 0.0))
        self.assertEqual(argb, 0xFF000000)

    def test_lab_roundtrip(self):
        """Tests round-trip conversion from ARGB to Lab and back to ARGB."""
        original_colors = [
            0xFF000000,  # Black
            0xFFFFFFFF,  # White
            0xFF0000FF,  # Blue
            0xFFFF0000,  # Red
            0xFF00FF00,  # Green
            0xFFFFFF00,  # Yellow
            0xFF800080,  # Purple
            0xFF123456,  # Random color
        ]
        
        for original in original_colors:
            lab = lab_from_int(original)
            roundtrip = int_from_lab(lab)
            
            # Extract RGB components for comparison (ignoring alpha)
            original_r = utils.red_from_int(original)
            original_g = utils.green_from_int(original)
            original_b = utils.blue_from_int(original)
            
            roundtrip_r = utils.red_from_int(roundtrip)
            roundtrip_g = utils.green_from_int(roundtrip)
            roundtrip_b = utils.blue_from_int(roundtrip)
            
            # Allow for small differences due to floating point precision
            self.assertLess(abs(original_r - roundtrip_r), 2)
            self.assertLess(abs(original_g - roundtrip_g), 2)
            self.assertLess(abs(original_b - roundtrip_b), 2)
    
    def test_delta_e(self):
        """Tests the delta_e method of the Lab class."""
        lab1 = Lab(50.0, 20.0, 30.0)
        lab2 = Lab(55.0, 25.0, 35.0)
        
        expected_delta_e = 5*5 + 5*5 + 5*5  # 75.0
        self.assertAlmostEqual(lab1.delta_e(lab2), expected_delta_e, delta=0.001)
        
        # Test symmetry
        self.assertAlmostEqual(lab1.delta_e(lab2), lab2.delta_e(lab1), delta=0.001)
    
    def test_string_representation(self):
        """Tests the string representation of Lab."""
        lab = Lab(50.0, 20.0, 30.0)
        expected_str = "Lab: L* 50.0 a* 20.0 b* 30.0"
        self.assertEqual(str(lab), expected_str)

if __name__ == "__main__":
    unittest.main()
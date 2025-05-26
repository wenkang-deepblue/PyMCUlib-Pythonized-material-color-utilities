# utils_test.py

import unittest
import math
from PyMCUlib_cpp.utils.utils import (
    Argb, Vec3, PI, argb_from_rgb, red_from_int, green_from_int, blue_from_int,
    alpha_from_int, is_opaque, linearized, delinearized, lstar_from_argb,
    lstar_from_y, y_from_lstar, argb_from_linrgb, sanitize_degrees_int,
    sanitize_degrees_double, diff_degrees, rotation_direction, hex_from_argb,
    argb_from_hex, int_from_lstar, signum, lerp, matrix_multiply
)

class UtilsTest(unittest.TestCase):
    
    # Define constants for tests
    MATRIX = [
        [1, 2, 3],
        [-4, 5, -6],
        [-7, -8, -9]
    ]
    
    def test_argb_from_rgb_black(self):
        """Tests ARGB conversion from RGB for black."""
        self.assertEqual(argb_from_rgb(0, 0, 0), 0xff000000)
        self.assertEqual(argb_from_rgb(0, 0, 0), 4278190080)
    
    def test_argb_from_rgb_white(self):
        """Tests ARGB conversion from RGB for white."""
        self.assertEqual(argb_from_rgb(255, 255, 255), 0xffffffff)
        self.assertEqual(argb_from_rgb(255, 255, 255), 4294967295)
    
    def test_argb_from_rgb_random_color(self):
        """Tests ARGB conversion from RGB for a random color."""
        self.assertEqual(argb_from_rgb(50, 150, 250), 0xff3296fa)
        self.assertEqual(argb_from_rgb(50, 150, 250), 4281505530)
    
    def test_signum(self):
        """Tests signum function."""
        self.assertEqual(signum(0.001), 1)
        self.assertEqual(signum(3.0), 1)
        self.assertEqual(signum(100.0), 1)
        self.assertEqual(signum(-0.002), -1)
        self.assertEqual(signum(-4.0), -1)
        self.assertEqual(signum(-101.0), -1)
        self.assertEqual(signum(0.0), 0)
    
    def test_rotation_direction_positive_for_counterclockwise(self):
        """Tests rotation direction for counterclockwise rotations."""
        self.assertEqual(rotation_direction(0.0, 30.0), 1.0)
        self.assertEqual(rotation_direction(0.0, 60.0), 1.0)
        self.assertEqual(rotation_direction(0.0, 150.0), 1.0)
        self.assertEqual(rotation_direction(90.0, 240.0), 1.0)
        self.assertEqual(rotation_direction(300.0, 30.0), 1.0)
        self.assertEqual(rotation_direction(270.0, 60.0), 1.0)
        self.assertEqual(rotation_direction(360.0 * 2, 15.0), 1.0)
        self.assertEqual(rotation_direction(360.0 * 3 + 15.0, -360.0 * 4 + 30.0), 1.0)
    
    def test_rotation_direction_negative_for_clockwise(self):
        """Tests rotation direction for clockwise rotations."""
        self.assertEqual(rotation_direction(30.0, 0.0), -1.0)
        self.assertEqual(rotation_direction(60.0, 0.0), -1.0)
        self.assertEqual(rotation_direction(150.0, 0.0), -1.0)
        self.assertEqual(rotation_direction(240.0, 90.0), -1.0)
        self.assertEqual(rotation_direction(30.0, 300.0), -1.0)
        self.assertEqual(rotation_direction(60.0, 270.0), -1.0)
        self.assertEqual(rotation_direction(15.0, -360.0 * 2), -1.0)
        self.assertEqual(rotation_direction(-360.0 * 4 + 270.0, 360.0 * 5 + 180.0), -1.0)
    
    def test_angle_difference(self):
        """Tests difference between angles."""
        self.assertEqual(diff_degrees(0.0, 30.0), 30.0)
        self.assertEqual(diff_degrees(0.0, 60.0), 60.0)
        self.assertEqual(diff_degrees(0.0, 150.0), 150.0)
        self.assertEqual(diff_degrees(90.0, 240.0), 150.0)
        self.assertEqual(diff_degrees(300.0, 30.0), 90.0)
        self.assertEqual(diff_degrees(270.0, 60.0), 150.0)
        
        self.assertEqual(diff_degrees(30.0, 0.0), 30.0)
        self.assertEqual(diff_degrees(60.0, 0.0), 60.0)
        self.assertEqual(diff_degrees(150.0, 0.0), 150.0)
        self.assertEqual(diff_degrees(240.0, 90.0), 150.0)
        self.assertEqual(diff_degrees(30.0, 300.0), 90.0)
        self.assertEqual(diff_degrees(60.0, 270.0), 150.0)
    
    def test_angle_sanitation(self):
        """Tests sanitation of angle values."""
        # Integer values
        self.assertEqual(sanitize_degrees_int(30), 30)
        self.assertEqual(sanitize_degrees_int(240), 240)
        self.assertEqual(sanitize_degrees_int(360), 0)
        self.assertEqual(sanitize_degrees_int(-30), 330)
        self.assertEqual(sanitize_degrees_int(-750), 330)
        self.assertEqual(sanitize_degrees_int(-54321), 39)
        
        # Double values
        self.assertAlmostEqual(sanitize_degrees_double(30.0), 30.0, delta=1e-4)
        self.assertAlmostEqual(sanitize_degrees_double(240.0), 240.0, delta=1e-4)
        self.assertAlmostEqual(sanitize_degrees_double(360.0), 0.0, delta=1e-4)
        self.assertAlmostEqual(sanitize_degrees_double(-30.0), 330.0, delta=1e-4)
        self.assertAlmostEqual(sanitize_degrees_double(-750.0), 330.0, delta=1e-4)
        self.assertAlmostEqual(sanitize_degrees_double(-54321.0), 39.0, delta=1e-4)
        self.assertAlmostEqual(sanitize_degrees_double(360.125), 0.125, delta=1e-4)
        self.assertAlmostEqual(sanitize_degrees_double(-11111.11), 48.89, delta=1e-4)
    
    def test_matrix_multiply(self):
        """Tests matrix multiplication."""
        vector_one = matrix_multiply(Vec3(1, 3, 5), self.MATRIX)
        self.assertAlmostEqual(vector_one.a, 22, delta=1e-4)
        self.assertAlmostEqual(vector_one.b, -19, delta=1e-4)
        self.assertAlmostEqual(vector_one.c, -76, delta=1e-4)
        
        vector_two = matrix_multiply(Vec3(-11.1, 22.2, -33.3), self.MATRIX)
        self.assertAlmostEqual(vector_two.a, -66.6, delta=1e-4)
        self.assertAlmostEqual(vector_two.b, 355.2, delta=1e-4)
        self.assertAlmostEqual(vector_two.c, 199.8, delta=1e-4)
    
    def test_alpha_from_int(self):
        """Tests extracting alpha from ARGB."""
        self.assertEqual(alpha_from_int(0xff123456), 0xff)
        self.assertEqual(alpha_from_int(0xffabcdef), 0xff)
    
    def test_red_from_int(self):
        """Tests extracting red from ARGB."""
        self.assertEqual(red_from_int(0xff123456), 0x12)
        self.assertEqual(red_from_int(0xffabcdef), 0xab)
    
    def test_green_from_int(self):
        """Tests extracting green from ARGB."""
        self.assertEqual(green_from_int(0xff123456), 0x34)
        self.assertEqual(green_from_int(0xffabcdef), 0xcd)
    
    def test_blue_from_int(self):
        """Tests extracting blue from ARGB."""
        self.assertEqual(blue_from_int(0xff123456), 0x56)
        self.assertEqual(blue_from_int(0xffabcdef), 0xef)
    
    def test_opaqueness(self):
        """Tests if a color is opaque."""
        self.assertTrue(is_opaque(0xff123456))
        self.assertFalse(is_opaque(0xf0123456))
        self.assertFalse(is_opaque(0x00123456))
    
    def test_linearized_components(self):
        """Tests linearization of RGB components."""
        self.assertAlmostEqual(linearized(0), 0.0, delta=1e-4)
        self.assertAlmostEqual(linearized(1), 0.0303527, delta=1e-4)
        self.assertAlmostEqual(linearized(2), 0.0607054, delta=1e-4)
        self.assertAlmostEqual(linearized(8), 0.242822, delta=1e-4)
        self.assertAlmostEqual(linearized(9), 0.273174, delta=1e-4)
        self.assertAlmostEqual(linearized(16), 0.518152, delta=1e-4)
        self.assertAlmostEqual(linearized(32), 1.44438, delta=1e-4)
        self.assertAlmostEqual(linearized(64), 5.12695, delta=1e-4)
        self.assertAlmostEqual(linearized(128), 21.5861, delta=1e-4)
        self.assertAlmostEqual(linearized(255), 100.0, delta=1e-4)
    
    def test_delinearized_components(self):
        """Tests delinearization of RGB components."""
        self.assertEqual(delinearized(0.0), 0)
        self.assertEqual(delinearized(0.0303527), 1)
        self.assertEqual(delinearized(0.0607054), 2)
        self.assertEqual(delinearized(0.242822), 8)
        self.assertEqual(delinearized(0.273174), 9)
        self.assertEqual(delinearized(0.518152), 16)
        self.assertEqual(delinearized(1.44438), 32)
        self.assertEqual(delinearized(5.12695), 64)
        self.assertEqual(delinearized(21.5861), 128)
        self.assertEqual(delinearized(100.0), 255)
        
        self.assertEqual(delinearized(25.0), 137)
        self.assertEqual(delinearized(50.0), 188)
        self.assertEqual(delinearized(75.0), 225)
        
        # Delinearized clamps out-of-range inputs
        self.assertEqual(delinearized(-1.0), 0)
        self.assertEqual(delinearized(-10000.0), 0)
        self.assertEqual(delinearized(101.0), 255)
        self.assertEqual(delinearized(10000.0), 255)
    
    def test_delinearized_is_left_inverse_of_linearized(self):
        """Tests that delinearized is left inverse of linearized."""
        self.assertEqual(delinearized(linearized(0)), 0)
        self.assertEqual(delinearized(linearized(1)), 1)
        self.assertEqual(delinearized(linearized(2)), 2)
        self.assertEqual(delinearized(linearized(8)), 8)
        self.assertEqual(delinearized(linearized(9)), 9)
        self.assertEqual(delinearized(linearized(16)), 16)
        self.assertEqual(delinearized(linearized(32)), 32)
        self.assertEqual(delinearized(linearized(64)), 64)
        self.assertEqual(delinearized(linearized(128)), 128)
        self.assertEqual(delinearized(linearized(255)), 255)
    
    def test_argb_from_linrgb(self):
        """Tests conversion from linear RGB to ARGB."""
        self.assertEqual(argb_from_linrgb(Vec3(25.0, 50.0, 75.0)), 0xff89bce1)
        self.assertEqual(argb_from_linrgb(Vec3(0.03, 0.06, 0.12)), 0xff010204)
    
    def test_lstar_from_argb(self):
        """Tests extraction of L* from ARGB."""
        self.assertAlmostEqual(lstar_from_argb(0xff89bce1), 74.011, delta=1e-3)
        self.assertAlmostEqual(lstar_from_argb(0xff010204), 0.529651, delta=1e-3)
    
    def test_hex_from_argb(self):
        """Tests conversion from ARGB to hex string."""
        self.assertEqual(hex_from_argb(0xff89bce1), "ff89bce1")
        self.assertEqual(hex_from_argb(0xff010204), "ff010204")

    def test_argb_from_hex(self):
        """Tests conversion from hex string to ARGB."""
        # Test with 3 digit hex
        self.assertEqual(argb_from_hex("#123"), 0xff112233)
        self.assertEqual(argb_from_hex("123"), 0xff112233)
        
        # Test with 6 digit hex
        self.assertEqual(argb_from_hex("#123456"), 0xff123456)
        self.assertEqual(argb_from_hex("123456"), 0xff123456)
        
        # Test with 8 digit hex (with alpha)
        self.assertEqual(argb_from_hex("#FF123456"), 0xff123456)
        self.assertEqual(argb_from_hex("80123456"), 0x80123456)
        
        # Test with different cases
        self.assertEqual(argb_from_hex("#4285f4"), 0xff4285f4)
        self.assertEqual(argb_from_hex("#4285F4"), 0xff4285f4)
        
        # Test special cases
        self.assertEqual(argb_from_hex("#fff"), 0xffffffff)
        self.assertEqual(argb_from_hex("#000"), 0xff000000)
        
        # Test error case
        with self.assertRaises(ValueError):
            argb_from_hex("#12345")  # Invalid length
    
    def test_int_from_lstar(self):
        """Tests conversion from L* to ARGB."""
        # Given an L* brightness value in [0, 100], IntFromLstar returns a greyscale
        # color in ARGB format with that brightness.
        # For L* outside the domain [0, 100], returns black or white.
        
        self.assertEqual(int_from_lstar(0.0), 0xff000000)
        self.assertEqual(int_from_lstar(0.25), 0xff010101)
        self.assertEqual(int_from_lstar(0.5), 0xff020202)
        self.assertEqual(int_from_lstar(1.0), 0xff040404)
        self.assertEqual(int_from_lstar(2.0), 0xff070707)
        self.assertEqual(int_from_lstar(4.0), 0xff0e0e0e)
        self.assertEqual(int_from_lstar(8.0), 0xff181818)
        self.assertEqual(int_from_lstar(25.0), 0xff3b3b3b)
        self.assertEqual(int_from_lstar(50.0), 0xff777777)
        self.assertEqual(int_from_lstar(75.0), 0xffb9b9b9)
        self.assertEqual(int_from_lstar(99.0), 0xfffcfcfc)
        self.assertEqual(int_from_lstar(100.0), 0xffffffff)
        
        self.assertEqual(int_from_lstar(-1.0), 0xff000000)
        self.assertEqual(int_from_lstar(-2.0), 0xff000000)
        self.assertEqual(int_from_lstar(-3.0), 0xff000000)
        self.assertEqual(int_from_lstar(-9999999.0), 0xff000000)
        
        self.assertEqual(int_from_lstar(101.0), 0xffffffff)
        self.assertEqual(int_from_lstar(111.0), 0xffffffff)
        self.assertEqual(int_from_lstar(9999999.0), 0xffffffff)
    
    def test_lstar_argb_roundtrip_property(self):
        """Tests L* -> ARGB -> L* roundtrip."""
        # Confirms that L* -> ARGB -> L* preserves original value
        # (taking ARGB rounding into consideration).
        self.assertAlmostEqual(lstar_from_argb(int_from_lstar(0.0)), 0.0, delta=1.0)
        self.assertAlmostEqual(lstar_from_argb(int_from_lstar(1.0)), 1.0, delta=1.0)
        self.assertAlmostEqual(lstar_from_argb(int_from_lstar(2.0)), 2.0, delta=1.0)
        self.assertAlmostEqual(lstar_from_argb(int_from_lstar(8.0)), 8.0, delta=1.0)
        self.assertAlmostEqual(lstar_from_argb(int_from_lstar(25.0)), 25.0, delta=1.0)
        self.assertAlmostEqual(lstar_from_argb(int_from_lstar(50.0)), 50.0, delta=1.0)
        self.assertAlmostEqual(lstar_from_argb(int_from_lstar(75.0)), 75.0, delta=1.0)
        self.assertAlmostEqual(lstar_from_argb(int_from_lstar(99.0)), 99.0, delta=1.0)
        self.assertAlmostEqual(lstar_from_argb(int_from_lstar(100.0)), 100.0, delta=1.0)
    
    def test_argb_lstar_roundtrip_property(self):
        """Tests ARGB -> L* -> ARGB roundtrip."""
        # Confirms that ARGB -> L* -> ARGB preserves original value
        # for greyscale colors.
        self.assertEqual(int_from_lstar(lstar_from_argb(0xff000000)), 0xff000000)
        self.assertEqual(int_from_lstar(lstar_from_argb(0xff010101)), 0xff010101)
        self.assertEqual(int_from_lstar(lstar_from_argb(0xff020202)), 0xff020202)
        self.assertEqual(int_from_lstar(lstar_from_argb(0xff111111)), 0xff111111)
        self.assertEqual(int_from_lstar(lstar_from_argb(0xff333333)), 0xff333333)
        self.assertEqual(int_from_lstar(lstar_from_argb(0xff777777)), 0xff777777)
        self.assertEqual(int_from_lstar(lstar_from_argb(0xffbbbbbb)), 0xffbbbbbb)
        self.assertEqual(int_from_lstar(lstar_from_argb(0xfffefefe)), 0xfffefefe)
        self.assertEqual(int_from_lstar(lstar_from_argb(0xffffffff)), 0xffffffff)
    
    def test_y_from_lstar(self):
        """Tests conversion from L* to Y."""
        self.assertAlmostEqual(y_from_lstar(0.0), 0.0, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(0.1), 0.0110705, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(0.2), 0.0221411, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(0.3), 0.0332116, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(0.4), 0.0442822, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(0.5), 0.0553528, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(1.0), 0.1107056, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(2.0), 0.2214112, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(3.0), 0.3321169, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(4.0), 0.4428225, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(5.0), 0.5535282, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(8.0), 0.8856451, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(10.0), 1.1260199, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(15.0), 1.9085832, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(20.0), 2.9890524, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(25.0), 4.4154767, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(30.0), 6.2359055, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(40.0), 11.2509737, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(50.0), 18.4186518, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(60.0), 28.1233342, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(70.0), 40.7494157, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(80.0), 56.6812907, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(90.0), 76.3033539, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(95.0), 87.6183294, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(99.0), 97.4360239, delta=1e-5)
        self.assertAlmostEqual(y_from_lstar(100.0), 100.0, delta=1e-5)
    
    def test_lstar_from_y(self):
        """Tests conversion from Y to L*."""
        self.assertAlmostEqual(lstar_from_y(0.0), 0.0, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(0.1), 0.9032962, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(0.2), 1.8065925, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(0.3), 2.7098888, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(0.4), 3.6131851, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(0.5), 4.5164814, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(0.8856451), 8.0, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(1.0), 8.9914424, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(2.0), 15.4872443, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(3.0), 20.0438970, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(4.0), 23.6714419, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(5.0), 26.7347653, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(10.0), 37.8424304, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(15.0), 45.6341970, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(20.0), 51.8372115, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(25.0), 57.0754208, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(30.0), 61.6542222, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(40.0), 69.4695307, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(50.0), 76.0692610, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(60.0), 81.8381891, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(70.0), 86.9968642, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(80.0), 91.6848609, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(90.0), 95.9967686, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(95.0), 98.0335184, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(99.0), 99.6120372, delta=1e-5)
        self.assertAlmostEqual(lstar_from_y(100.0), 100.0, delta=1e-5)
    
    def test_y_lstar_roundtrip_property(self):
        """Tests Y -> L* -> Y roundtrip."""
        # Confirms that Y -> L* -> Y preserves original value.
        for y in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0, 2.0, 5.0, 10.0, 
                 20.0, 50.0, 75.0, 95.0, 99.0, 100.0]:
            lstar = lstar_from_y(y)
            reconstructed_y = y_from_lstar(lstar)
            self.assertAlmostEqual(reconstructed_y, y, delta=1e-8)
    
    def test_lstar_y_roundtrip_property(self):
        """Tests L* -> Y -> L* roundtrip."""
        # Confirms that L* -> Y -> L* preserves original value.
        for lstar in [0.0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 
                     20.0, 50.0, 75.0, 95.0, 99.0, 100.0]:
            y = y_from_lstar(lstar)
            reconstructed_lstar = lstar_from_y(y)
            self.assertAlmostEqual(reconstructed_lstar, lstar, delta=1e-8)

if __name__ == '__main__':
    unittest.main()
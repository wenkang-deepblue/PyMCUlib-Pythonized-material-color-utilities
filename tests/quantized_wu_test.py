# wu_test.py

import unittest
from PyMCUlib_cpp.quantize.wu import quantize_wu

class WuTest(unittest.TestCase):
    def test_full_image(self):
        """Test quantizing a larger set of colors."""
        pixels = [i % 8000 for i in range(12544)]
        max_colors = 128
        
        result = quantize_wu(pixels, max_colors)
        self.assertGreater(len(result), 0)
        
    def test_two_red_three_green(self):
        """Test quantizing with two distinct colors."""
        pixels = [0xffff0000, 0xffff0000, 0xffff0000, 0xff00ff00, 0xff00ff00]
        result = quantize_wu(pixels, 256)
        self.assertEqual(len(result), 2)
        
    def test_one_red(self):
        """Test quantizing a single red color."""
        pixels = [0xffff0000]
        result = quantize_wu(pixels, 256)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0xffff0000)
        
    def test_one_green(self):
        """Test quantizing a single green color."""
        pixels = [0xff00ff00]
        result = quantize_wu(pixels, 256)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0xff00ff00)
        
    def test_one_blue(self):
        """Test quantizing a single blue color."""
        pixels = [0xff0000ff]
        result = quantize_wu(pixels, 256)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0xff0000ff)
        
    def test_five_blue(self):
        """Test quantizing five identical blue colors."""
        pixels = [0xff0000ff] * 5
        result = quantize_wu(pixels, 256)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0xff0000ff)
        
    def test_one_red_and_o(self):
        """Test quantizing a dark color."""
        pixels = [0xff141216]
        result = quantize_wu(pixels, 256)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0xff141216)
        
    def test_red_green_blue(self):
        """Test quantizing with three distinct colors."""
        pixels = [0xffff0000, 0xff00ff00, 0xff0000ff]
        result = quantize_wu(pixels, 256)
        self.assertEqual(len(result), 3)
        self.assertIn(0xffff0000, result)
        self.assertIn(0xff00ff00, result)
        self.assertIn(0xff0000ff, result)
        
    def test_testonly(self):
        """Test with a specific set of colors."""
        pixels = [0xff010203, 0xff665544, 0xff708090, 0xffc0ffee, 0xfffedcba]
        result = quantize_wu(pixels, 256)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
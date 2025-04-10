# celebi_test.py

import unittest
import time
from PyMCUlib.quantize.celebi import quantize_celebi

class CelebiTest(unittest.TestCase):
    
    def test_full_image(self):
        """Test quantizing an image with many colors."""
        pixels = [i % 8000 for i in range(12544)]
        
        iterations = 1
        max_colors = 128
        
        # Measure performance
        start_time = time.time()
        for _ in range(iterations):
            quantize_celebi(pixels, max_colors)
        end_time = time.time()
        
        # No explicit assertion here as this is primarily a performance test
    
    def test_one_red(self):
        """Test quantizing with a single red color."""
        pixels = [0xffff0000]
        result = quantize_celebi(pixels, 256)
        self.assertEqual(len(result.color_to_count), 1)
        self.assertEqual(result.color_to_count.get(0xffff0000), 1)
    
    def test_one_green(self):
        """Test quantizing with a single green color."""
        pixels = [0xff00ff00]
        result = quantize_celebi(pixels, 256)
        self.assertEqual(len(result.color_to_count), 1)
        self.assertEqual(result.color_to_count.get(0xff00ff00), 1)
    
    def test_one_blue(self):
        """Test quantizing with a single blue color."""
        pixels = [0xff0000ff]
        result = quantize_celebi(pixels, 256)
        self.assertEqual(len(result.color_to_count), 1)
        self.assertEqual(result.color_to_count.get(0xff0000ff), 1)
    
    def test_five_blue(self):
        """Test quantizing with five identical blue colors."""
        pixels = [0xff0000ff] * 5
        result = quantize_celebi(pixels, 256)
        self.assertEqual(len(result.color_to_count), 1)
        self.assertEqual(result.color_to_count.get(0xff0000ff), 5)
    
    def test_one_red_one_green_one_blue(self):
        """Test quantizing with red, green, and blue colors."""
        pixels = [0xffff0000, 0xff00ff00, 0xff0000ff]
        result = quantize_celebi(pixels, 256)
        self.assertEqual(len(result.color_to_count), 3)
        self.assertEqual(result.color_to_count.get(0xffff0000), 1)
        self.assertEqual(result.color_to_count.get(0xff00ff00), 1)
        self.assertEqual(result.color_to_count.get(0xff0000ff), 1)
    
    def test_two_red_three_green(self):
        """Test quantizing with multiple red and green colors."""
        pixels = [0xffff0000, 0xffff0000, 0xff00ff00, 0xff00ff00, 0xff00ff00]
        result = quantize_celebi(pixels, 256)
        self.assertEqual(len(result.color_to_count), 2)
        self.assertEqual(result.color_to_count.get(0xffff0000), 2)
        self.assertEqual(result.color_to_count.get(0xff00ff00), 3)
    
    def test_no_colors(self):
        """Test quantizing with no colors."""
        pixels = [0xFFFFFFFF]  # Adding a pixel for the test
        result = quantize_celebi(pixels, 0)
        self.assertEqual(len(result.color_to_count), 0)
        self.assertEqual(len(result.input_pixel_to_cluster_pixel), 0)
    
    def test_single_transparent(self):
        """Test quantizing with a single transparent color."""
        pixels = [0x20F93013]
        result = quantize_celebi(pixels, 1)
        self.assertEqual(len(result.color_to_count), 0)
        self.assertEqual(len(result.input_pixel_to_cluster_pixel), 0)
    
    def test_too_many_colors(self):
        """Test quantizing with too many colors requested."""
        pixels = []  # Empty list of pixels
        result = quantize_celebi(pixels, 32767)
        self.assertEqual(len(result.color_to_count), 0)
        self.assertEqual(len(result.input_pixel_to_cluster_pixel), 0)

if __name__ == '__main__':
    unittest.main()
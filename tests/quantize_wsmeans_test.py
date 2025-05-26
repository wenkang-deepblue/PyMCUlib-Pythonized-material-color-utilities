# wsmeans_test.py

import unittest
from PyMCUlib_cpp.quantize.wsmeans import quantize_wsmeans

class WsmeansTest(unittest.TestCase):
    def test_full_image(self):
        """Test with a large number of colors."""
        pixels = [i % 8000 for i in range(12544)]
        starting_clusters = []
        
        max_colors = 128
        result = quantize_wsmeans(pixels, starting_clusters, max_colors)
        self.assertTrue(len(result.color_to_count) > 0)

    def test_one_red_and_o(self):
        """Test with a single dark color."""
        pixels = [0xff141216]
        starting_clusters = []
        result = quantize_wsmeans(pixels, starting_clusters, 256)
        self.assertEqual(len(result.color_to_count), 1)
        self.assertEqual(result.color_to_count[0xff141216], 1)

    def test_one_red(self):
        """Test with a single red color."""
        pixels = [0xffff0000]
        starting_clusters = []
        result = quantize_wsmeans(pixels, starting_clusters, 256)
        self.assertEqual(len(result.color_to_count), 1)
        self.assertEqual(result.color_to_count[0xffff0000], 1)

    def test_one_green(self):
        """Test with a single green color."""
        pixels = [0xff00ff00]
        starting_clusters = []
        result = quantize_wsmeans(pixels, starting_clusters, 256)
        self.assertEqual(len(result.color_to_count), 1)
        self.assertEqual(result.color_to_count[0xff00ff00], 1)

    def test_one_blue(self):
        """Test with a single blue color."""
        pixels = [0xff0000ff]
        starting_clusters = []
        result = quantize_wsmeans(pixels, starting_clusters, 256)
        self.assertEqual(len(result.color_to_count), 1)
        self.assertEqual(result.color_to_count[0xff0000ff], 1)

    def test_five_blue(self):
        """Test with five identical blue colors."""
        pixels = [0xff0000ff for _ in range(5)]
        starting_clusters = []
        result = quantize_wsmeans(pixels, starting_clusters, 256)
        self.assertEqual(len(result.color_to_count), 1)
        self.assertEqual(result.color_to_count[0xff0000ff], 5)

if __name__ == "__main__":
    unittest.main()
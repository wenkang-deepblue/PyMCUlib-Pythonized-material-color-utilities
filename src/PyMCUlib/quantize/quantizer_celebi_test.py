# quantize/quantizer_celebi_test.py

import unittest
from PyMCUlib.quantize.quantizer_celebi import QuantizerCelebi

# Define color constants
RED = 0xffff0000
GREEN = 0xff00ff00
BLUE = 0xff0000ff


class QuantizerCelebiTest(unittest.TestCase):
    """Test cases for the QuantizerCelebi class."""

    def test_1r(self):
        """Test quantization of a single red pixel."""
        answer = QuantizerCelebi.quantize([RED], 128)
        self.assertEqual(len(answer), 1, "Result should contain exactly one color")
        self.assertEqual(answer.get(RED), 1, "Result should contain one red pixel")

    def test_1g(self):
        """Test quantization of a single green pixel."""
        answer = QuantizerCelebi.quantize([GREEN], 128)
        self.assertEqual(len(answer), 1, "Result should contain exactly one color")
        self.assertEqual(answer.get(GREEN), 1, "Result should contain one green pixel")

    def test_1b(self):
        """Test quantization of a single blue pixel."""
        answer = QuantizerCelebi.quantize([BLUE], 128)
        self.assertEqual(len(answer), 1, "Result should contain exactly one color")
        self.assertEqual(answer.get(BLUE), 1, "Result should contain one blue pixel")

    def test_5b(self):
        """Test quantization of five blue pixels."""
        answer = QuantizerCelebi.quantize([BLUE, BLUE, BLUE, BLUE, BLUE], 128)
        self.assertEqual(len(answer), 1, "Result should contain exactly one color")
        self.assertEqual(answer.get(BLUE), 5, "Result should contain five blue pixels")

    def test_2r_3g(self):
        """Test quantization of two red and three green pixels."""
        answer = QuantizerCelebi.quantize([RED, RED, GREEN, GREEN, GREEN], 128)
        self.assertEqual(len(answer), 2, "Result should contain exactly two colors")
        self.assertEqual(answer.get(RED), 2, "Result should contain two red pixels")
        self.assertEqual(answer.get(GREEN), 3, "Result should contain three green pixels")

    def test_1r_1g_1b(self):
        """Test quantization of one red, one green, and one blue pixel."""
        answer = QuantizerCelebi.quantize([RED, GREEN, BLUE], 128)
        self.assertEqual(len(answer), 3, "Result should contain exactly three colors")
        self.assertEqual(answer.get(RED), 1, "Result should contain one red pixel")
        self.assertEqual(answer.get(GREEN), 1, "Result should contain one green pixel")
        self.assertEqual(answer.get(BLUE), 1, "Result should contain one blue pixel")


if __name__ == "__main__":
    unittest.main()
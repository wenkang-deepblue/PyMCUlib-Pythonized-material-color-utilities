# test_image_utils.py

import unittest
from PIL import Image
import numpy as np
from io import BytesIO
import os

from PyMCUlib_cpp.utils.image_utils import (
    source_color_from_image,
    source_color_from_image_bytes,
    source_color_from_file,
    source_color_from_bytes
)

class TestImageUtils(unittest.TestCase):
    def setUp(self):
        # create test image - a simple red square
        self.red_image = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        
        # create test image - a green square with 50% opacity
        self.green_with_alpha = Image.new('RGBA', (100, 100), (0, 255, 0, 128))
        
        # create test image - an image with a blue and yellow split
        self.split_image = Image.new('RGBA', (100, 100), (0, 0, 255, 255))
        for x in range(50, 100):
            for y in range(100):
                self.split_image.putpixel((x, y), (255, 255, 0, 255))
    
    def test_source_color_from_image(self):
        # test pure red image
        color = source_color_from_image(self.red_image)
        self.assertEqual(color & 0x00FFFFFF, 0x00FF0000, "Should extract red as the dominant color")
        
        # test area cropping - still should be red
        color = source_color_from_image(self.red_image, (10, 10, 50, 50))
        self.assertEqual(color & 0x00FFFFFF, 0x00FF0000, "Should extract red from the cropped area")
    
    def test_source_color_from_image_bytes(self):
        # convert image to byte data and test
        rgba_data = np.array(self.red_image)
        image_bytes = rgba_data.flatten()
        
        color = source_color_from_image_bytes(image_bytes)
        self.assertEqual(color & 0x00FFFFFF, 0x00FF0000, "Should extract red from RGBA bytes")
    
    def test_alpha_transparency_handling(self):
        # if the function correctly handles the alpha channel, this assertion should succeed
        with self.assertRaises(ValueError) as context:
            source_color_from_image(self.green_with_alpha)
        self.assertTrue("No valid pixels found in the image" in str(context.exception),
                        "Should raise error for images with only transparent pixels")
    
    def test_split_image(self):
        # test image with two obvious colors
        # the result may be blue or yellow, depending on the quantizer and scorer
        color = source_color_from_image(self.split_image)
        # only verify it's blue or yellow
        hex_color = color & 0x00FFFFFF
        self.assertTrue(
            hex_color == 0x0000FF or hex_color == 0x00FFFF00,
            f"Should extract either blue or yellow (got: {hex(color)})"
        )
        
        # test area cropping to get only the blue part
        color = source_color_from_image(self.split_image, (0, 0, 50, 100))
        self.assertEqual(color & 0x00FFFFFF, 0x0000FF, "Should extract blue from the left half")
        
        # test area cropping to get only the yellow part
        color = source_color_from_image(self.split_image, (50, 0, 50, 100))
        self.assertEqual(color & 0x00FFFFFF, 0x00FFFF00, "Should extract yellow from the right half")
    
    def test_source_color_from_file(self):
        # save test image to a temporary file
        temp_file = "temp_test_image.png"
        self.red_image.save(temp_file)
        
        try:
            color = source_color_from_file(temp_file)
            self.assertEqual(color & 0x00FFFFFF, 0x00FF0000, "Should extract red from file")
        finally:
            # clean up temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_source_color_from_bytes(self):
        # convert image to raw bytes and test
        buffer = BytesIO()
        self.red_image.save(buffer, format="PNG")
        raw_bytes = buffer.getvalue()
        
        color = source_color_from_bytes(raw_bytes)
        self.assertEqual(color & 0x00FFFFFF, 0x00FF0000, "Should extract red from raw bytes")
    
    def test_error_handling(self):
        # test invalid image
        with self.assertRaises(ValueError):
            source_color_from_image("not_an_image")
        
        # test invalid area: should raise error
        with self.assertRaises(ValueError) as context:
            source_color_from_image(self.red_image, (-10, -10, 5, 5))
        self.assertTrue("No valid pixels found" in str(context.exception) or
                        "Invalid area" in str(context.exception),
                        "Should raise error for invalid crop area")
        
        # test invalid file
        with self.assertRaises(FileNotFoundError):
            source_color_from_file("non_existent_file.png")
        
        # test invalid bytes
        with self.assertRaises(ValueError):
            source_color_from_bytes(b"not_an_image")


if __name__ == "__main__":
    unittest.main()
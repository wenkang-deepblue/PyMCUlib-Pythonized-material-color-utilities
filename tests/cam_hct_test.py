# hct_test.py

import unittest
import itertools
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.cam.cam import cam_from_int
from PyMCUlib_cpp.utils.utils import lstar_from_argb

def is_on_boundary(rgb_component):
    """Returns whether the RGB component is on the boundary (0 or 255)."""
    return rgb_component == 0 or rgb_component == 255

def color_is_on_boundary(argb):
    """Returns whether the color has at least one RGB component on the boundary."""
    red = (argb & 0x00ff0000) >> 16
    green = (argb & 0x0000ff00) >> 8
    blue = (argb & 0x000000ff)
    return is_on_boundary(red) or is_on_boundary(green) or is_on_boundary(blue)

class HctTest(unittest.TestCase):
    
    def test_limited_to_srgb(self):
        """Ensures that the HCT class can only represent sRGB colors."""
        # An impossibly high chroma is used
        hct = Hct.from_hct(120.0, 200.0, 50.0)
        argb = hct.to_int()
        
        # The hue, chroma, and tone members of hct should actually
        # represent the sRGB color.
        self.assertEqual(cam_from_int(argb).hue, hct.get_hue())
        self.assertEqual(cam_from_int(argb).chroma, hct.get_chroma())
        self.assertEqual(lstar_from_argb(argb), hct.get_tone())
    
    def test_truncates_colors(self):
        """Ensures that HCT truncates colors."""
        hct = Hct.from_hct(120.0, 60.0, 50.0)
        chroma = hct.get_chroma()
        self.assertLess(chroma, 60.0)
        
        # The new chroma should be lower than the original.
        hct.set_tone(180.0)
        self.assertLess(hct.get_chroma(), chroma)
    
    def test_correctness(self):
        """Tests correctness of HCT conversions for various colors."""
        # Create parameters for testing
        hues = [15, 45, 75, 105, 135, 165, 195, 225, 255, 285, 315, 345]
        chromas = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        tones = [20, 30, 40, 50, 60, 70, 80]
        
        # Generate all combinations of parameters
        for hue, chroma, tone in itertools.product(hues, chromas, tones):
            hct_color = Hct.from_hct(hue, chroma, tone)
            
            # Test hue correctness
            if chroma > 0:
                self.assertAlmostEqual(hct_color.get_hue(), hue, delta=4.0)
            
            # Test chroma truncation
            self.assertLess(hct_color.get_chroma(), chroma + 2.5)
            
            # Test chroma on boundary
            if hct_color.get_chroma() < chroma - 2.5:
                self.assertTrue(color_is_on_boundary(hct_color.to_int()))
            
            # Test tone correctness
            self.assertAlmostEqual(hct_color.get_tone(), tone, delta=0.5)

if __name__ == '__main__':
    unittest.main()
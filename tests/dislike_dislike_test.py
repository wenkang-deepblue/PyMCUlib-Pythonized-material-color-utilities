# dislike_test.py

import unittest
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dislike.dislike import is_disliked, fix_if_disliked

class DislikeTest(unittest.TestCase):
    
    def test_monk_skin_tone_scale_colors_liked(self):
        # Test that monk skin tone scale colors are liked
        skin_tone_colors = [
            0xfff6ede4, 0xfff3e7db, 0xfff7ead0, 0xffeadaba,
            0xffd7bd96, 0xffa07e56, 0xff825c43, 0xff604134,
            0xff3a312a, 0xff292420
        ]
        
        for argb in skin_tone_colors:
            hct = Hct.from_int(argb)
            self.assertFalse(is_disliked(hct))
    
    def test_bile_colors_disliked(self):
        # Test that bile colors are disliked
        bile_colors = [
            0xff95884B, 0xff716B40, 0xffB08E00, 0xff4C4308,
            0xff464521
        ]
        
        for argb in bile_colors:
            hct = Hct.from_int(argb)
            self.assertTrue(is_disliked(hct))
    
    def test_bile_colors_fixed(self):
        # Test that bile colors are fixed
        bile_colors = [
            0xff95884B, 0xff716B40, 0xffB08E00, 0xff4C4308,
            0xff464521
        ]
        
        for argb in bile_colors:
            bile_color = Hct.from_int(argb)
            self.assertTrue(is_disliked(bile_color))
            fixed_bile_color = fix_if_disliked(bile_color)
            self.assertFalse(is_disliked(fixed_bile_color))
    
    def test_tone67_liked(self):
        # Test that a color with tone 67 is liked
        color = Hct.from_hct(100.0, 50.0, 67.0)
        self.assertFalse(is_disliked(color))
        # Test that fixing a color that's not disliked doesn't change it
        self.assertEqual(fix_if_disliked(color).to_int(), color.to_int())

if __name__ == "__main__":
    unittest.main()
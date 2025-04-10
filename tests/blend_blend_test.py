# blend_test.py

import unittest
from PyMCUlib.blend.blend import blend_hct_hue
from PyMCUlib.utils.utils import hex_from_argb

class BlendTest(unittest.TestCase):
    def test_red_to_blue(self):
        blended = blend_hct_hue(0xffff0000, 0xff0000ff, 0.8)
        self.assertEqual(hex_from_argb(blended), "ff905eff")

if __name__ == "__main__":
    unittest.main()
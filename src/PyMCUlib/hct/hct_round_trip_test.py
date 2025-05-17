# hct/hct_round_trip_test.py

import unittest
from PyMCUlib.utils import color_utils
from PyMCUlib.hct.hct import Hct

class HctRoundTripTest(unittest.TestCase):
    def test_hct_preserves_original_color(self):
        """
        Test that HCT round trip conversion preserves the original color.
        Testing 512 out of 16,777,216 colors.
        """
        for r in range(0, 296, 37):
            for g in range(0, 296, 37):
                for b in range(0, 296, 37):
                    argb = color_utils.argb_from_rgb(
                        min(255, r),
                        min(255, g),
                        min(255, b),
                    )
                    
                    hct = Hct.from_int(argb)
                    reconstructed = Hct.from_hct(
                        hct.hue,
                        hct.chroma,
                        hct.tone,
                    ).to_int()
                    
                    self.assertEqual(reconstructed, argb)

if __name__ == '__main__':
    unittest.main()
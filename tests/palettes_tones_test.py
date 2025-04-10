# tones_test.py

import unittest
from PyMCUlib.palettes.tones import TonalPalette, KeyColor
from PyMCUlib.cam.hct import Hct
from PyMCUlib.utils.utils import hex_from_argb

class TonesTest(unittest.TestCase):
    def test_blue(self):
        color = 0xff0000ff
        tonal_palette = TonalPalette(color)
        self.assertEqual(hex_from_argb(tonal_palette.get(100)), "ffffffff")
        self.assertEqual(hex_from_argb(tonal_palette.get(95)), "fff1efff")
        self.assertEqual(hex_from_argb(tonal_palette.get(90)), "ffe0e0ff")
        self.assertEqual(hex_from_argb(tonal_palette.get(80)), "ffbec2ff")
        self.assertEqual(hex_from_argb(tonal_palette.get(70)), "ff9da3ff")
        self.assertEqual(hex_from_argb(tonal_palette.get(60)), "ff7c84ff")
        self.assertEqual(hex_from_argb(tonal_palette.get(50)), "ff5a64ff")
        self.assertEqual(hex_from_argb(tonal_palette.get(40)), "ff343dff")
        self.assertEqual(hex_from_argb(tonal_palette.get(30)), "ff0000ef")
        self.assertEqual(hex_from_argb(tonal_palette.get(20)), "ff0001ac")
        self.assertEqual(hex_from_argb(tonal_palette.get(10)), "ff00006e")
        self.assertEqual(hex_from_argb(tonal_palette.get(0)), "ff000000")

class KeyColorTests(unittest.TestCase):
    def test_exact_chroma_available(self):
        # Requested chroma is exactly achievable at a certain tone.
        palette = TonalPalette(50.0, 60.0)
        result = palette.get_key_color()

        self.assertLess(abs(result.get_hue() - 50.0), 10.0)
        self.assertLess(abs(result.get_chroma() - 60.0), 0.5)
        # Tone might vary, but should be within the range from 0 to 100.
        self.assertGreater(result.get_tone(), 0)
        self.assertLess(result.get_tone(), 100)

    def test_unusually_high_chroma(self):
        # Requested chroma is above what is achievable. For Hue 149, chroma peak
        # is 89.6 at Tone 87.9. The result key color's chroma should be close to the
        # chroma peak.
        palette = TonalPalette(149.0, 200.0)
        result = palette.get_key_color()

        self.assertLess(abs(result.get_hue() - 149.0), 10.0)
        self.assertGreater(result.get_chroma(), 89.0)
        # Tone might vary, but should be within the range from 0 to 100.
        self.assertGreater(result.get_tone(), 0)
        self.assertLess(result.get_tone(), 100)

    def test_unusually_low_chroma(self):
        # By definition, the key color should be the first tone, starting from Tone
        # 50, matching the given hue and chroma. When requesting a very low chroma,
        # the result should be close to Tone 50, since most tones can produce a low
        # chroma.
        palette = TonalPalette(50.0, 3.0)
        result = palette.get_key_color()

        # Higher error tolerance for hue when the requested chroma is unusually low.
        self.assertLess(abs(result.get_hue() - 50.0), 10.0)
        self.assertLess(abs(result.get_chroma() - 3.0), 0.5)
        self.assertLess(abs(result.get_tone() - 50.0), 0.5)

if __name__ == "__main__":
    unittest.main()
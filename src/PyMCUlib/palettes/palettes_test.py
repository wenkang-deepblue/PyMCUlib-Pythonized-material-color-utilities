# palettes/palettes_test.py

import unittest

from PyMCUlib.palettes.tonal_palette import TonalPalette
from PyMCUlib.palettes.core_palette import CorePalette


class TonalPaletteTest(unittest.TestCase):
    def test_of_blue(self):
        # Test TonalPalette with blue color
        blue = TonalPalette.from_int(0xff0000ff)

        self.assertEqual(blue.tone(100), 0xffffffff)
        self.assertEqual(blue.tone(95), 0xfff1efff)
        self.assertEqual(blue.tone(90), 0xffe0e0ff)
        self.assertEqual(blue.tone(80), 0xffbec2ff)
        self.assertEqual(blue.tone(70), 0xff9da3ff)
        self.assertEqual(blue.tone(60), 0xff7c84ff)
        self.assertEqual(blue.tone(50), 0xff5a64ff)
        self.assertEqual(blue.tone(40), 0xff343dff)
        self.assertEqual(blue.tone(30), 0xff0000ef)
        self.assertEqual(blue.tone(20), 0xff0001ac)
        self.assertEqual(blue.tone(10), 0xff00006e)
        self.assertEqual(blue.tone(0), 0xff000000)


class CorePaletteTest(unittest.TestCase):
    def test_of_blue(self):
        # Test CorePalette.of with blue color
        core = CorePalette.of(0xff0000ff)

        self.assertEqual(core.a1.tone(100), 0xffffffff)
        self.assertEqual(core.a1.tone(95), 0xfff1efff)
        self.assertEqual(core.a1.tone(90), 0xffe0e0ff)
        self.assertEqual(core.a1.tone(80), 0xffbec2ff)
        self.assertEqual(core.a1.tone(70), 0xff9da3ff)
        self.assertEqual(core.a1.tone(60), 0xff7c84ff)
        self.assertEqual(core.a1.tone(50), 0xff5a64ff)
        self.assertEqual(core.a1.tone(40), 0xff343dff)
        self.assertEqual(core.a1.tone(30), 0xff0000ef)
        self.assertEqual(core.a1.tone(20), 0xff0001ac)
        self.assertEqual(core.a1.tone(10), 0xff00006e)
        self.assertEqual(core.a1.tone(0), 0xff000000)

        self.assertEqual(core.a2.tone(100), 0xffffffff)
        self.assertEqual(core.a2.tone(95), 0xfff1efff)
        self.assertEqual(core.a2.tone(90), 0xffe1e0f9)
        self.assertEqual(core.a2.tone(80), 0xffc5c4dd)
        self.assertEqual(core.a2.tone(70), 0xffa9a9c1)
        self.assertEqual(core.a2.tone(60), 0xff8f8fa6)
        self.assertEqual(core.a2.tone(50), 0xff75758b)
        self.assertEqual(core.a2.tone(40), 0xff5c5d72)
        self.assertEqual(core.a2.tone(30), 0xff444559)
        self.assertEqual(core.a2.tone(20), 0xff2e2f42)
        self.assertEqual(core.a2.tone(10), 0xff191a2c)
        self.assertEqual(core.a2.tone(0), 0xff000000)

    def test_content_of_blue(self):
        # Test CorePalette.contentOf with blue color
        core = CorePalette.content_of(0xff0000ff)

        self.assertEqual(core.a1.tone(100), 0xffffffff)
        self.assertEqual(core.a1.tone(95), 0xfff1efff)
        self.assertEqual(core.a1.tone(90), 0xffe0e0ff)
        self.assertEqual(core.a1.tone(80), 0xffbec2ff)
        self.assertEqual(core.a1.tone(70), 0xff9da3ff)
        self.assertEqual(core.a1.tone(60), 0xff7c84ff)
        self.assertEqual(core.a1.tone(50), 0xff5a64ff)
        self.assertEqual(core.a1.tone(40), 0xff343dff)
        self.assertEqual(core.a1.tone(30), 0xff0000ef)
        self.assertEqual(core.a1.tone(20), 0xff0001ac)
        self.assertEqual(core.a1.tone(10), 0xff00006e)
        self.assertEqual(core.a1.tone(0), 0xff000000)

        self.assertEqual(core.a2.tone(100), 0xffffffff)
        self.assertEqual(core.a2.tone(95), 0xfff1efff)
        self.assertEqual(core.a2.tone(90), 0xffe0e0ff)
        self.assertEqual(core.a2.tone(80), 0xffc1c3f4)
        self.assertEqual(core.a2.tone(70), 0xffa5a7d7)
        self.assertEqual(core.a2.tone(60), 0xff8b8dbb)
        self.assertEqual(core.a2.tone(50), 0xff7173a0)
        self.assertEqual(core.a2.tone(40), 0xff585b86)
        self.assertEqual(core.a2.tone(30), 0xff40436d)
        self.assertEqual(core.a2.tone(20), 0xff2a2d55)
        self.assertEqual(core.a2.tone(10), 0xff14173f)
        self.assertEqual(core.a2.tone(0), 0xff000000)


class KeyColorTest(unittest.TestCase):
    def test_key_color_with_exact_chroma(self):
        # Requested chroma is exactly achievable at a certain tone.
        palette = TonalPalette.from_hue_and_chroma(50.0, 60.0)
        result = palette.key_color

        hue_difference = abs(result.hue - 50.0)
        self.assertLess(hue_difference, 10.0)
        chroma_difference = abs(result.chroma - 60.0)
        self.assertLess(chroma_difference, 0.5)
        # Tone might vary, but should be within the range from 0 to 100.
        self.assertGreater(result.tone, 0)
        self.assertLess(result.tone, 100)

    def test_key_color_with_unusually_high_chroma(self):
        # Requested chroma is above what is achievable. For Hue 149, chroma peak
        # is 89.6 at Tone 87.9. The result key color's chroma should be close to
        # the chroma peak.
        palette = TonalPalette.from_hue_and_chroma(149.0, 200.0)
        result = palette.key_color

        hue_difference = abs(result.hue - 149.0)
        self.assertLess(hue_difference, 10.0)
        self.assertGreater(result.chroma, 89.0)
        # Tone might vary, but should be within the range from 0 to 100.
        self.assertGreater(result.tone, 0)
        self.assertLess(result.tone, 100)

    def test_key_color_with_unusually_low_chroma(self):
        # By definition, the key color should be the first tone, starting from
        # Tone 50, matching the given hue and chroma. When requesting a very low
        # chroma, the result should be close to Tone 50, since most tones can
        # produce a low chroma.
        palette = TonalPalette.from_hue_and_chroma(50.0, 3.0)
        result = palette.key_color

        hue_difference = abs(result.hue - 50.0)
        self.assertLess(hue_difference, 10.0)
        chroma_difference = abs(result.chroma - 3.0)
        self.assertLess(chroma_difference, 0.5)
        tone_difference = abs(result.tone - 50.0)
        self.assertLess(tone_difference, 0.5)


if __name__ == '__main__':
    unittest.main()
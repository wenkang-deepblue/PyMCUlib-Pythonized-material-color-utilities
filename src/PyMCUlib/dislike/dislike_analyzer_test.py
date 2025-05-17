# dislike/dislike_analyzer_test.py

import unittest
from PyMCUlib.hct.hct import Hct
from PyMCUlib.dislike.dislike_analyzer import DislikeAnalyzer


class DislikeAnalyzerTest(unittest.TestCase):
    def test_likes_monk_skin_tone_scale_colors(self):
        # From https://skintone.google#/get-started
        monk_skin_tone_scale_colors = [
            0xfff6ede4,
            0xfff3e7db,
            0xfff7ead0,
            0xffeadaba,
            0xffd7bd96,
            0xffa07e56,
            0xff825c43,
            0xff604134,
            0xff3a312a,
            0xff292420,
        ]
        for color in monk_skin_tone_scale_colors:
            self.assertFalse(DislikeAnalyzer.is_disliked(Hct.from_int(color)))

    def test_dislikes_bile_colors(self):
        unlikable = [
            0xff95884B,
            0xff716B40,
            0xffB08E00,
            0xff4C4308,
            0xff464521,
        ]
        for color in unlikable:
            self.assertTrue(DislikeAnalyzer.is_disliked(Hct.from_int(color)))

    def test_makes_bile_colors_likable(self):
        unlikable = [
            0xff95884B,
            0xff716B40,
            0xffB08E00,
            0xff4C4308,
            0xff464521,
        ]
        for color in unlikable:
            hct = Hct.from_int(color)
            self.assertTrue(DislikeAnalyzer.is_disliked(hct))
            likable = DislikeAnalyzer.fix_if_disliked(hct)
            self.assertFalse(DislikeAnalyzer.is_disliked(likable))

    def test_likes_tone_67_colors(self):
        color = Hct.from_hct(100.0, 50.0, 67.0)
        self.assertFalse(DislikeAnalyzer.is_disliked(color))
        self.assertEqual(
            DislikeAnalyzer.fix_if_disliked(color).to_int(),
            color.to_int()
        )


if __name__ == '__main__':
    unittest.main()
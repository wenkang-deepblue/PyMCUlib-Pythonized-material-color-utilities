# score_test.py

import unittest
from typing import Dict

from PyMCUlib.score.score import ranked_suggestions, ScoreOptions
from PyMCUlib.utils.utils import Argb

class ScoreTest(unittest.TestCase):
    
    def test_prioritizes_chroma(self):
        argb_to_population: Dict[int, int] = {
            0xff000000: 1, 0xffffffff: 1, 0xff0000ff: 1
        }
        
        ranked = ranked_suggestions(argb_to_population, ScoreOptions(desired=4))
        
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0], 0xff0000ff)
    
    def test_prioritizes_chroma_when_proportions_equal(self):
        argb_to_population: Dict[int, int] = {
            0xffff0000: 1, 0xff00ff00: 1, 0xff0000ff: 1
        }
        
        ranked = ranked_suggestions(argb_to_population, ScoreOptions(desired=4))
        
        self.assertEqual(len(ranked), 3)
        self.assertEqual(ranked[0], 0xffff0000)
        self.assertEqual(ranked[1], 0xff00ff00)
        self.assertEqual(ranked[2], 0xff0000ff)
    
    def test_generates_gblue_when_no_colors_available(self):
        argb_to_population: Dict[int, int] = {0xff000000: 1}
        
        ranked = ranked_suggestions(argb_to_population, ScoreOptions(desired=4))
        
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0], 0xff4285f4)
    
    def test_dedupes_nearby_hues(self):
        argb_to_population: Dict[int, int] = {
            0xff008772: 1,  # H 180 C 42 T 50
            0xff318477: 1   # H 184 C 35 T 50
        }
        
        ranked = ranked_suggestions(argb_to_population, ScoreOptions(desired=4))
        
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0], 0xff008772)
    
    def test_maximizes_hue_distance(self):
        argb_to_population: Dict[int, int] = {
            0xff008772: 1,  # H 180 C 42 T 50
            0xff008587: 1,  # H 198 C 50 T 50
            0xff007ebc: 1   # H 245 C 50 T 50
        }
        
        ranked = ranked_suggestions(argb_to_population, ScoreOptions(desired=2))
        
        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0], 0xff007ebc)
        self.assertEqual(ranked[1], 0xff008772)
    
    def test_generated_scenario_one(self):
        argb_to_population: Dict[int, int] = {
            0xff7ea16d: 67,
            0xffd8ccae: 67,
            0xff835c0d: 49,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=3, fallback_color_argb=0xff8d3819, filter=False)
        )
        
        self.assertEqual(len(ranked), 3)
        self.assertEqual(ranked[0], 0xff7ea16d)
        self.assertEqual(ranked[1], 0xffd8ccae)
        self.assertEqual(ranked[2], 0xff835c0d)
    
    def test_generated_scenario_two(self):
        argb_to_population: Dict[int, int] = {
            0xffd33881: 14,
            0xff3205cc: 77,
            0xff0b48cf: 36,
            0xffa08f5d: 81,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=4, fallback_color_argb=0xff7d772b, filter=True)
        )
        
        self.assertEqual(len(ranked), 3)
        self.assertEqual(ranked[0], 0xff3205cc)
        self.assertEqual(ranked[1], 0xffa08f5d)
        self.assertEqual(ranked[2], 0xffd33881)
    
    def test_generated_scenario_three(self):
        argb_to_population: Dict[int, int] = {
            0xffbe94a6: 23,
            0xffc33fd7: 42,
            0xff899f36: 90,
            0xff94c574: 82,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=3, fallback_color_argb=0xffaa79a4, filter=True)
        )
        
        self.assertEqual(len(ranked), 3)
        self.assertEqual(ranked[0], 0xff94c574)
        self.assertEqual(ranked[1], 0xffc33fd7)
        self.assertEqual(ranked[2], 0xffbe94a6)
    
    def test_generated_scenario_four(self):
        argb_to_population: Dict[int, int] = {
            0xffdf241c: 85, 0xff685859: 44, 0xffd06d5f: 34,
            0xff561c54: 27, 0xff713090: 88,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=5, fallback_color_argb=0xff58c19c, filter=False)
        )
        
        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0], 0xffdf241c)
        self.assertEqual(ranked[1], 0xff561c54)
    
    def test_generated_scenario_five(self):
        argb_to_population: Dict[int, int] = {
            0xffbe66f8: 41, 0xff4bbda9: 88, 0xff80f6f9: 44,
            0xffab8017: 43, 0xffe89307: 65,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=3, fallback_color_argb=0xff916691, filter=False)
        )
        
        self.assertEqual(len(ranked), 3)
        self.assertEqual(ranked[0], 0xffab8017)
        self.assertEqual(ranked[1], 0xff4bbda9)
        self.assertEqual(ranked[2], 0xffbe66f8)
    
    def test_generated_scenario_six(self):
        argb_to_population: Dict[int, int] = {
            0xff18ea8f: 93, 0xff327593: 18, 0xff066a18: 53,
            0xfffa8a23: 74, 0xff04ca1f: 62,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=2, fallback_color_argb=0xff4c377a, filter=False)
        )
        
        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0], 0xff18ea8f)
        self.assertEqual(ranked[1], 0xfffa8a23)
    
    def test_generated_scenario_seven(self):
        argb_to_population: Dict[int, int] = {
            0xff2e05ed: 23, 0xff153e55: 90, 0xff9ab220: 23,
            0xff153379: 66, 0xff68bcc3: 81,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=2, fallback_color_argb=0xfff588dc, filter=True)
        )
        
        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0], 0xff2e05ed)
        self.assertEqual(ranked[1], 0xff9ab220)
    
    def test_generated_scenario_eight(self):
        argb_to_population: Dict[int, int] = {
            0xff816ec5: 24,
            0xff6dcb94: 19,
            0xff3cae91: 98,
            0xff5b542f: 25,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=1, fallback_color_argb=0xff84b0fd, filter=False)
        )
        
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0], 0xff3cae91)
    
    def test_generated_scenario_nine(self):
        argb_to_population: Dict[int, int] = {
            0xff206f86: 52, 0xff4a620d: 96, 0xfff51401: 85,
            0xff2b8ebf: 3, 0xff277766: 59,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=3, fallback_color_argb=0xff02b415, filter=True)
        )
        
        self.assertEqual(len(ranked), 3)
        self.assertEqual(ranked[0], 0xfff51401)
        self.assertEqual(ranked[1], 0xff4a620d)
        self.assertEqual(ranked[2], 0xff2b8ebf)
    
    def test_generated_scenario_ten(self):
        argb_to_population: Dict[int, int] = {
            0xff8b1d99: 54,
            0xff27effe: 43,
            0xff6f558d: 2,
            0xff77fdf2: 78,
        }
        
        ranked = ranked_suggestions(
            argb_to_population,
            ScoreOptions(desired=4, fallback_color_argb=0xff5e7a10, filter=True)
        )
        
        self.assertEqual(len(ranked), 3)
        self.assertEqual(ranked[0], 0xff27effe)
        self.assertEqual(ranked[1], 0xff8b1d99)
        self.assertEqual(ranked[2], 0xff6f558d)

if __name__ == "__main__":
    unittest.main()
# hct_solver_test.py

import unittest
from PyMCUlib_cpp.cam.hct_solver import solve_to_int
from PyMCUlib_cpp.cam.cam import cam_from_int
from PyMCUlib_cpp.utils.utils import lstar_from_argb

class HctSolverTest(unittest.TestCase):
    
    def test_red(self):
        """Tests solving for red, given HCT."""
        # Compute HCT
        color = 0xFFFE0315
        cam = cam_from_int(color)
        tone = lstar_from_argb(color)
        
        # Compute input
        recovered = solve_to_int(cam.hue, cam.chroma, tone)
        self.assertEqual(recovered, color)
    
    def test_green(self):
        """Tests solving for green, given HCT."""
        # Compute HCT
        color = 0xFF15FE03
        cam = cam_from_int(color)
        tone = lstar_from_argb(color)
        
        # Compute input
        recovered = solve_to_int(cam.hue, cam.chroma, tone)
        self.assertEqual(recovered, color)
    
    def test_blue(self):
        """Tests solving for blue, given HCT."""
        # Compute HCT
        color = 0xFF0315FE
        cam = cam_from_int(color)
        tone = lstar_from_argb(color)
        
        # Compute input
        recovered = solve_to_int(cam.hue, cam.chroma, tone)
        self.assertEqual(recovered, color)
    
    def test_select_colors(self):
        """Tests solving for several key colors."""
        # Test a selection of colors rather than the exhaustive test in C++
        colors = [
            0xFF000000,  # Black
            0xFFFFFFFF,  # White
            0xFFFF0000,  # Red
            0xFF00FF00,  # Green
            0xFF0000FF,  # Blue
            0xFFFFFF00,  # Yellow
            0xFF00FFFF,  # Cyan
            0xFFFF00FF,  # Magenta
            0xFF123456,  # Some arbitrary color
            0xFFABCDEF   # Another arbitrary color
        ]
        
        for color in colors:
            cam = cam_from_int(color)
            tone = lstar_from_argb(color)
            recovered = solve_to_int(cam.hue, cam.chroma, tone)
            self.assertEqual(recovered, color)

if __name__ == '__main__':
    unittest.main()
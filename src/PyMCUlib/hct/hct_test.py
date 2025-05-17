# hct/hct_test.py

import unittest
from PyMCUlib.utils import color_utils
from PyMCUlib.hct.cam16 import Cam16
from PyMCUlib.hct.hct import Hct
from PyMCUlib.hct.viewing_conditions import ViewingConditions

# Define test color constants
RED = 0xffff0000
GREEN = 0xff00ff00
BLUE = 0xff0000ff
WHITE = 0xffffffff
BLACK = 0xff000000

class HctTest(unittest.TestCase):
    def test_cam_to_argb_red(self):
        """Test CAM16 conversion for red color."""
        cam = Cam16.from_int(RED)
        
        self.assertAlmostEqual(cam.hue, 27.408, places=3)
        self.assertAlmostEqual(cam.chroma, 113.358, places=3)
        self.assertAlmostEqual(cam.j, 46.445, places=3)
        self.assertAlmostEqual(cam.m, 89.494, places=3)
        self.assertAlmostEqual(cam.s, 91.890, places=3)
        self.assertAlmostEqual(cam.q, 105.989, places=3)
    
    def test_cam_to_argb_green(self):
        """Test CAM16 conversion for green color."""
        cam = Cam16.from_int(GREEN)
        
        self.assertAlmostEqual(cam.hue, 142.140, places=3)
        self.assertAlmostEqual(cam.chroma, 108.410, places=3)
        self.assertAlmostEqual(cam.j, 79.332, places=3)
        self.assertAlmostEqual(cam.m, 85.588, places=3)
        self.assertAlmostEqual(cam.s, 78.605, places=3)
        self.assertAlmostEqual(cam.q, 138.520, places=3)
    
    def test_cam_to_argb_blue(self):
        """Test CAM16 conversion for blue color."""
        cam = Cam16.from_int(BLUE)
        
        self.assertAlmostEqual(cam.hue, 282.788, places=3)
        self.assertAlmostEqual(cam.chroma, 87.231, places=3)
        self.assertAlmostEqual(cam.j, 25.466, places=3)
        self.assertAlmostEqual(cam.m, 68.867, places=3)
        self.assertAlmostEqual(cam.s, 93.675, places=3)
        self.assertAlmostEqual(cam.q, 78.481, places=3)
    
    def test_cam_to_argb_white(self):
        """Test CAM16 conversion for white color."""
        cam = Cam16.from_int(WHITE)
        
        self.assertAlmostEqual(cam.hue, 209.492, places=3)
        self.assertAlmostEqual(cam.chroma, 2.869, places=3)
        self.assertAlmostEqual(cam.j, 100.0, places=3)
        self.assertAlmostEqual(cam.m, 2.265, places=3)
        self.assertAlmostEqual(cam.s, 12.068, places=3)
        self.assertAlmostEqual(cam.q, 155.521, places=3)
    
    def test_cam_to_argb_black(self):
        """Test CAM16 conversion for black color."""
        cam = Cam16.from_int(BLACK)
        
        self.assertAlmostEqual(cam.hue, 0.0, places=3)
        self.assertAlmostEqual(cam.chroma, 0.0, places=3)
        self.assertAlmostEqual(cam.j, 0.0, places=3)
        self.assertAlmostEqual(cam.m, 0.0, places=3)
        self.assertAlmostEqual(cam.s, 0.0, places=3)
        self.assertAlmostEqual(cam.q, 0.0, places=3)
    
    def test_cam_to_argb_to_cam_red(self):
        """Test roundtrip conversion from CAM16 to ARGB back to CAM16 for red."""
        cam = Cam16.from_int(RED)
        argb = cam.to_int()
        self.assertEqual(argb, RED)
    
    def test_cam_to_argb_to_cam_green(self):
        """Test roundtrip conversion from CAM16 to ARGB back to CAM16 for green."""
        cam = Cam16.from_int(GREEN)
        argb = cam.to_int()
        self.assertEqual(argb, GREEN)
    
    def test_cam_to_argb_to_cam_blue(self):
        """Test roundtrip conversion from CAM16 to ARGB back to CAM16 for blue."""
        cam = Cam16.from_int(BLUE)
        argb = cam.to_int()
        self.assertEqual(argb, BLUE)
    
    def test_argb_to_hct_green(self):
        """Test ARGB to HCT conversion for green."""
        hct = Hct.from_int(GREEN)
        self.assertAlmostEqual(hct.hue, 142.139, places=2)
        self.assertAlmostEqual(hct.chroma, 108.410, places=2)
        self.assertAlmostEqual(hct.tone, 87.737, places=2)
    
    def test_argb_to_hct_blue(self):
        """Test ARGB to HCT conversion for blue."""
        hct = Hct.from_int(BLUE)
        self.assertAlmostEqual(hct.hue, 282.788, places=2)
        self.assertAlmostEqual(hct.chroma, 87.230, places=2)
        self.assertAlmostEqual(hct.tone, 32.302, places=2)
    
    def test_argb_to_hct_blue_tone90(self):
        """Test HCT creation with specified hue, chroma, tone."""
        hct = Hct.from_hct(282.788, 87.230, 90.0)
        self.assertAlmostEqual(hct.hue, 282.239, places=2)
        self.assertAlmostEqual(hct.chroma, 19.144, places=2)
        self.assertAlmostEqual(hct.tone, 90.035, places=2)
    
    def test_viewing_conditions_default(self):
        """Test default viewing conditions."""
        vc = ViewingConditions.DEFAULT
        self.assertAlmostEqual(vc.n, 0.184, places=3)
        self.assertAlmostEqual(vc.aw, 29.981, places=3)
        self.assertAlmostEqual(vc.nbb, 1.017, places=3)
        self.assertAlmostEqual(vc.ncb, 1.017, places=3)
        self.assertAlmostEqual(vc.c, 0.69, places=3)
        self.assertAlmostEqual(vc.nc, 1.0, places=3)
        self.assertAlmostEqual(vc.rgb_d[0], 1.021, places=3)
        self.assertAlmostEqual(vc.rgb_d[1], 0.986, places=3)
        self.assertAlmostEqual(vc.rgb_d[2], 0.934, places=3)
        self.assertAlmostEqual(vc.fl, 0.388, places=3)
        self.assertAlmostEqual(vc.fl_root, 0.789, places=3)
        self.assertAlmostEqual(vc.z, 1.909, places=3)

    def _color_is_on_boundary(self, argb):
        """Check if a color is on the RGB boundary (has a 0 or 255 component)."""
        return (color_utils.red_from_argb(argb) == 0 or
                color_utils.red_from_argb(argb) == 255 or
                color_utils.green_from_argb(argb) == 0 or
                color_utils.green_from_argb(argb) == 255 or
                color_utils.blue_from_argb(argb) == 0 or
                color_utils.blue_from_argb(argb) == 255)

    def test_cam_solver_returns_sufficiently_close_color(self):
        """Test that HctSolver returns colors with expected properties."""
        for hue in range(15, 360, 30):
            for chroma in range(0, 101, 10):
                for tone in range(20, 81, 10):
                    hct_color = Hct.from_hct(hue, chroma, tone)
                    
                    if chroma > 0:
                        self.assertLessEqual(abs(hct_color.hue - hue), 4.0)
                    
                    self.assertGreaterEqual(hct_color.chroma, 0)
                    self.assertLessEqual(hct_color.chroma, chroma + 2.5)
                    
                    if hct_color.chroma < chroma - 2.5:
                        self.assertTrue(self._color_is_on_boundary(hct_color.to_int()))
                    
                    self.assertLessEqual(abs(hct_color.tone - tone), 0.5)

if __name__ == '__main__':
    unittest.main()
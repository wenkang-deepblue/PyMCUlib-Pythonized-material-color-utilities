# cam_test.py

import unittest
from PyMCUlib.cam.cam import Cam, cam_from_int, int_from_cam
from PyMCUlib.utils.utils import hex_from_argb

class CamTest(unittest.TestCase):
    
    # Define constants for tests
    RED = 0xffff0000
    GREEN = 0xff00ff00
    BLUE = 0xff0000ff
    WHITE = 0xffffffff
    BLACK = 0xff000000
    
    def test_red(self):
        """Tests conversion of red to CAM16."""
        cam = cam_from_int(self.RED)
        
        self.assertAlmostEqual(cam.hue, 27.408, delta=0.001)
        self.assertAlmostEqual(cam.chroma, 113.357, delta=0.001)
        self.assertAlmostEqual(cam.j, 46.445, delta=0.001)
        self.assertAlmostEqual(cam.m, 89.494, delta=0.001)
        self.assertAlmostEqual(cam.s, 91.889, delta=0.001)
        self.assertAlmostEqual(cam.q, 105.988, delta=0.001)
    
    def test_green(self):
        """Tests conversion of green to CAM16."""
        cam = cam_from_int(self.GREEN)
        
        self.assertAlmostEqual(cam.hue, 142.139, delta=0.001)
        self.assertAlmostEqual(cam.chroma, 108.410, delta=0.001)
        self.assertAlmostEqual(cam.j, 79.331, delta=0.001)
        self.assertAlmostEqual(cam.m, 85.587, delta=0.001)
        self.assertAlmostEqual(cam.s, 78.604, delta=0.001)
        self.assertAlmostEqual(cam.q, 138.520, delta=0.001)
    
    def test_blue(self):
        """Tests conversion of blue to CAM16."""
        cam = cam_from_int(self.BLUE)
        
        self.assertAlmostEqual(cam.hue, 282.788, delta=0.001)
        self.assertAlmostEqual(cam.chroma, 87.230, delta=0.001)
        self.assertAlmostEqual(cam.j, 25.465, delta=0.001)
        self.assertAlmostEqual(cam.m, 68.867, delta=0.001)
        self.assertAlmostEqual(cam.s, 93.674, delta=0.001)
        self.assertAlmostEqual(cam.q, 78.481, delta=0.001)
    
    def test_white(self):
        """Tests conversion of white to CAM16."""
        cam = cam_from_int(self.WHITE)
        
        self.assertAlmostEqual(cam.hue, 209.492, delta=0.001)
        self.assertAlmostEqual(cam.chroma, 2.869, delta=0.001)
        self.assertAlmostEqual(cam.j, 100.0, delta=0.001)
        self.assertAlmostEqual(cam.m, 2.265, delta=0.001)
        self.assertAlmostEqual(cam.s, 12.068, delta=0.001)
        self.assertAlmostEqual(cam.q, 155.521, delta=0.001)
    
    def test_black(self):
        """Tests conversion of black to CAM16."""
        cam = cam_from_int(self.BLACK)
        
        self.assertAlmostEqual(cam.hue, 0.0, delta=0.001)
        self.assertAlmostEqual(cam.chroma, 0.0, delta=0.001)
        self.assertAlmostEqual(cam.j, 0.0, delta=0.001)
        self.assertAlmostEqual(cam.m, 0.0, delta=0.001)
        self.assertAlmostEqual(cam.s, 0.0, delta=0.001)
        self.assertAlmostEqual(cam.q, 0.0, delta=0.001)
    
    def test_red_round_trip(self):
        """Tests red does a round trip through CAM16."""
        cam = cam_from_int(self.RED)
        argb = int_from_cam(cam)
        self.assertEqual(argb, self.RED)
    
    def test_green_round_trip(self):
        """Tests green does a round trip through CAM16."""
        cam = cam_from_int(self.GREEN)
        argb = int_from_cam(cam)
        self.assertEqual(argb, self.GREEN)
    
    def test_blue_round_trip(self):
        """Tests blue does a round trip through CAM16."""
        cam = cam_from_int(self.BLUE)
        argb = int_from_cam(cam)
        self.assertEqual(argb, self.BLUE)

if __name__ == '__main__':
    unittest.main()
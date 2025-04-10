# temperature_test.py

import unittest
from PyMCUlib.cam.hct import Hct
from PyMCUlib.temperature.temperature_cache import TemperatureCache

class TemperatureCacheTest(unittest.TestCase):
    
    def test_raw_temperature(self):
        blue_hct = Hct.from_int(0xff0000ff)
        blue_temp = TemperatureCache.raw_temperature(blue_hct)
        self.assertAlmostEqual(-1.393, blue_temp, delta=0.001)
        
        red_hct = Hct.from_int(0xffff0000)
        red_temp = TemperatureCache.raw_temperature(red_hct)
        self.assertAlmostEqual(2.351, red_temp, delta=0.001)
        
        green_hct = Hct.from_int(0xff00ff00)
        green_temp = TemperatureCache.raw_temperature(green_hct)
        self.assertAlmostEqual(-0.267, green_temp, delta=0.001)
        
        white_hct = Hct.from_int(0xffffffff)
        white_temp = TemperatureCache.raw_temperature(white_hct)
        self.assertAlmostEqual(-0.5, white_temp, delta=0.001)
        
        black_hct = Hct.from_int(0xff000000)
        black_temp = TemperatureCache.raw_temperature(black_hct)
        self.assertAlmostEqual(-0.5, black_temp, delta=0.001)
    
    def test_complement(self):
        blue_complement = TemperatureCache(Hct.from_int(0xff0000ff)).get_complement().to_int()
        self.assertEqual(0xff9d0002, blue_complement)
        
        red_complement = TemperatureCache(Hct.from_int(0xffff0000)).get_complement().to_int()
        self.assertEqual(0xff007bfc, red_complement)
        
        green_complement = TemperatureCache(Hct.from_int(0xff00ff00)).get_complement().to_int()
        self.assertEqual(0xffffd2c9, green_complement)
        
        white_complement = TemperatureCache(Hct.from_int(0xffffffff)).get_complement().to_int()
        self.assertEqual(0xffffffff, white_complement)
        
        black_complement = TemperatureCache(Hct.from_int(0xff000000)).get_complement().to_int()
        self.assertEqual(0xff000000, black_complement)
    
    def test_analogous(self):
        blue_analogous = TemperatureCache(Hct.from_int(0xff0000ff)).get_analogous_colors()
        self.assertEqual(0xff00590c, blue_analogous[0].to_int())
        self.assertEqual(0xff00564e, blue_analogous[1].to_int())
        self.assertEqual(0xff0000ff, blue_analogous[2].to_int())
        self.assertEqual(0xff6700cc, blue_analogous[3].to_int())
        self.assertEqual(0xff81009f, blue_analogous[4].to_int())
        
        red_analogous = TemperatureCache(Hct.from_int(0xffff0000)).get_analogous_colors()
        self.assertEqual(0xfff60082, red_analogous[0].to_int())
        self.assertEqual(0xfffc004c, red_analogous[1].to_int())
        self.assertEqual(0xffff0000, red_analogous[2].to_int())
        self.assertEqual(0xffd95500, red_analogous[3].to_int())
        self.assertEqual(0xffaf7200, red_analogous[4].to_int())
        
        green_analogous = TemperatureCache(Hct.from_int(0xff00ff00)).get_analogous_colors()
        self.assertEqual(0xffcee900, green_analogous[0].to_int())
        self.assertEqual(0xff92f500, green_analogous[1].to_int())
        self.assertEqual(0xff00ff00, green_analogous[2].to_int())
        self.assertEqual(0xff00fd6f, green_analogous[3].to_int())
        self.assertEqual(0xff00fab3, green_analogous[4].to_int())
        
        black_analogous = TemperatureCache(Hct.from_int(0xff000000)).get_analogous_colors()
        self.assertEqual(0xff000000, black_analogous[0].to_int())
        self.assertEqual(0xff000000, black_analogous[1].to_int())
        self.assertEqual(0xff000000, black_analogous[2].to_int())
        self.assertEqual(0xff000000, black_analogous[3].to_int())
        self.assertEqual(0xff000000, black_analogous[4].to_int())
        
        white_analogous = TemperatureCache(Hct.from_int(0xffffffff)).get_analogous_colors()
        self.assertEqual(0xffffffff, white_analogous[0].to_int())
        self.assertEqual(0xffffffff, white_analogous[1].to_int())
        self.assertEqual(0xffffffff, white_analogous[2].to_int())
        self.assertEqual(0xffffffff, white_analogous[3].to_int())
        self.assertEqual(0xffffffff, white_analogous[4].to_int())

if __name__ == "__main__":
    unittest.main()
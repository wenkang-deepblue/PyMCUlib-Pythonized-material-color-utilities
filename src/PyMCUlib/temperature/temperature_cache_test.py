# temperature/temperature_cache_test.py

import unittest

from PyMCUlib.hct.hct import Hct
from PyMCUlib.temperature.temperature_cache import TemperatureCache


class TemperatureCacheTest(unittest.TestCase):
    """Tests for the TemperatureCache class."""

    def test_raw_temperature(self):
        """Tests that raw temperatures are computed correctly."""
        blue_temp = TemperatureCache.raw_temperature(Hct.from_int(0xff0000ff))
        self.assertAlmostEqual(blue_temp, -1.393, places=3)

        red_temp = TemperatureCache.raw_temperature(Hct.from_int(0xffff0000))
        self.assertAlmostEqual(red_temp, 2.351, places=3)

        green_temp = TemperatureCache.raw_temperature(Hct.from_int(0xff00ff00))
        self.assertAlmostEqual(green_temp, -0.267, places=3)

        white_temp = TemperatureCache.raw_temperature(Hct.from_int(0xffffffff))
        self.assertAlmostEqual(white_temp, -0.5, places=3)

        black_temp = TemperatureCache.raw_temperature(Hct.from_int(0xff000000))
        self.assertAlmostEqual(black_temp, -0.5, places=3)

    def test_relative_temperature(self):
        """Tests relative temperature calculations."""
        blue_temp = TemperatureCache(Hct.from_int(0xff0000ff)).input_relative_temperature
        self.assertAlmostEqual(blue_temp, 0.0, places=3)

        red_temp = TemperatureCache(Hct.from_int(0xffff0000)).input_relative_temperature
        self.assertAlmostEqual(red_temp, 1.0, places=3)

        green_temp = TemperatureCache(Hct.from_int(0xff00ff00)).input_relative_temperature
        self.assertAlmostEqual(green_temp, 0.467, places=3)

        white_temp = TemperatureCache(Hct.from_int(0xffffffff)).input_relative_temperature
        self.assertAlmostEqual(white_temp, 0.5, places=3)

        black_temp = TemperatureCache(Hct.from_int(0xff000000)).input_relative_temperature
        self.assertAlmostEqual(black_temp, 0.5, places=3)

    def test_complement(self):
        """Tests complement color generation."""
        blue_complement = TemperatureCache(Hct.from_int(0xff0000ff)).complement.to_int()
        self.assertEqual(blue_complement, 0xff9d0002)

        red_complement = TemperatureCache(Hct.from_int(0xffff0000)).complement.to_int()
        self.assertEqual(red_complement, 0xff007bfc)

        green_complement = TemperatureCache(Hct.from_int(0xff00ff00)).complement.to_int()
        self.assertEqual(green_complement, 0xffffd2c9)

        white_complement = TemperatureCache(Hct.from_int(0xffffffff)).complement.to_int()
        self.assertEqual(white_complement, 0xffffffff)

        black_complement = TemperatureCache(Hct.from_int(0xff000000)).complement.to_int()
        self.assertEqual(black_complement, 0xff000000)

    def test_analogous(self):
        """Tests analogous color generation."""
        blue_analogous = [
            color.to_int() for color in TemperatureCache(Hct.from_int(0xff0000ff)).analogous()
        ]
        self.assertEqual(blue_analogous[0], 0xff00590c)
        self.assertEqual(blue_analogous[1], 0xff00564e)
        self.assertEqual(blue_analogous[2], 0xff0000ff)
        self.assertEqual(blue_analogous[3], 0xff6700cc)
        self.assertEqual(blue_analogous[4], 0xff81009f)

        red_analogous = [
            color.to_int() for color in TemperatureCache(Hct.from_int(0xffff0000)).analogous()
        ]
        self.assertEqual(red_analogous[0], 0xfff60082)
        self.assertEqual(red_analogous[1], 0xfffc004c)
        self.assertEqual(red_analogous[2], 0xffff0000)
        self.assertEqual(red_analogous[3], 0xffd95500)
        self.assertEqual(red_analogous[4], 0xffaf7200)

        green_analogous = [
            color.to_int() for color in TemperatureCache(Hct.from_int(0xff00ff00)).analogous()
        ]
        self.assertEqual(green_analogous[0], 0xffcee900)
        self.assertEqual(green_analogous[1], 0xff92f500)
        self.assertEqual(green_analogous[2], 0xff00ff00)
        self.assertEqual(green_analogous[3], 0xff00fd6f)
        self.assertEqual(green_analogous[4], 0xff00fab3)

        black_analogous = [
            color.to_int() for color in TemperatureCache(Hct.from_int(0xff000000)).analogous()
        ]
        self.assertEqual(black_analogous[0], 0xff000000)
        self.assertEqual(black_analogous[1], 0xff000000)
        self.assertEqual(black_analogous[2], 0xff000000)
        self.assertEqual(black_analogous[3], 0xff000000)
        self.assertEqual(black_analogous[4], 0xff000000)

        white_analogous = [
            color.to_int() for color in TemperatureCache(Hct.from_int(0xffffffff)).analogous()
        ]
        self.assertEqual(white_analogous[0], 0xffffffff)
        self.assertEqual(white_analogous[1], 0xffffffff)
        self.assertEqual(white_analogous[2], 0xffffffff)
        self.assertEqual(white_analogous[3], 0xffffffff)
        self.assertEqual(white_analogous[4], 0xffffffff)


if __name__ == "__main__":
    unittest.main()
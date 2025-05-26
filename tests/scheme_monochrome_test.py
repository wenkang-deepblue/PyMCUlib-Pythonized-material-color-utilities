# test_scheme_monochrome.py

import unittest
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.scheme.monochrome import SchemeMonochrome
from PyMCUlib_cpp.dynamiccolor.material_dynamic_colors import MaterialDynamicColors

class TestSchemeMonochrome(unittest.TestCase):
    
    def test_dark_theme_monochrome_spec(self):
        """Test that dark theme monochrome scheme produces expected tone values."""
        scheme = SchemeMonochrome(Hct.from_int(0xff0000ff), True, 0.0)
        
        # Test primary colors
        self.assertAlmostEqual(MaterialDynamicColors.primary().get_hct(scheme).get_tone(), 100.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_primary().get_hct(scheme).get_tone(), 10.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.primary_container().get_hct(scheme).get_tone(), 85.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_primary_container().get_hct(scheme).get_tone(), 0.0, delta=1.0)
        
        # Test secondary colors
        self.assertAlmostEqual(MaterialDynamicColors.secondary().get_hct(scheme).get_tone(), 80.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_secondary().get_hct(scheme).get_tone(), 10.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.secondary_container().get_hct(scheme).get_tone(), 30.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_secondary_container().get_hct(scheme).get_tone(), 90.0, delta=1.0)
        
        # Test tertiary colors
        self.assertAlmostEqual(MaterialDynamicColors.tertiary().get_hct(scheme).get_tone(), 90.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_tertiary().get_hct(scheme).get_tone(), 10.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.tertiary_container().get_hct(scheme).get_tone(), 60.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_tertiary_container().get_hct(scheme).get_tone(), 0.0, delta=1.0)
    
    def test_light_theme_monochrome_spec(self):
        """Test that light theme monochrome scheme produces expected tone values."""
        scheme = SchemeMonochrome(Hct.from_int(0xff0000ff), False, 0.0)
        
        # Test primary colors
        self.assertAlmostEqual(MaterialDynamicColors.primary().get_hct(scheme).get_tone(), 0.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_primary().get_hct(scheme).get_tone(), 90.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.primary_container().get_hct(scheme).get_tone(), 25.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_primary_container().get_hct(scheme).get_tone(), 100.0, delta=1.0)
        
        # Test secondary colors
        self.assertAlmostEqual(MaterialDynamicColors.secondary().get_hct(scheme).get_tone(), 40.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_secondary().get_hct(scheme).get_tone(), 100.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.secondary_container().get_hct(scheme).get_tone(), 85.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_secondary_container().get_hct(scheme).get_tone(), 10.0, delta=1.0)
        
        # Test tertiary colors
        self.assertAlmostEqual(MaterialDynamicColors.tertiary().get_hct(scheme).get_tone(), 25.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_tertiary().get_hct(scheme).get_tone(), 90.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.tertiary_container().get_hct(scheme).get_tone(), 49.0, delta=1.0)
        self.assertAlmostEqual(MaterialDynamicColors.on_tertiary_container().get_hct(scheme).get_tone(), 100.0, delta=1.0)

if __name__ == "__main__":
    unittest.main()
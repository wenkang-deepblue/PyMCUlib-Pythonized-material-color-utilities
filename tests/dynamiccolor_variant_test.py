# test_variant.py

import unittest
from PyMCUlib_cpp.dynamiccolor.variant import Variant

class TestVariant(unittest.TestCase):
    
    def test_variant_enum_values(self):
        """Test that all variant enum values are defined correctly."""
        self.assertEqual(Variant.MONOCHROME.value, 0)
        self.assertEqual(Variant.NEUTRAL.value, 1)
        self.assertEqual(Variant.TONAL_SPOT.value, 2)
        self.assertEqual(Variant.VIBRANT.value, 3)
        self.assertEqual(Variant.EXPRESSIVE.value, 4)
        self.assertEqual(Variant.FIDELITY.value, 5)
        self.assertEqual(Variant.CONTENT.value, 6)
        self.assertEqual(Variant.RAINBOW.value, 7)
        self.assertEqual(Variant.FRUIT_SALAD.value, 8)
    
    def test_variant_enum_names(self):
        """Test that all variant enum names are defined correctly."""
        self.assertEqual(Variant.MONOCHROME.name, "MONOCHROME")
        self.assertEqual(Variant.NEUTRAL.name, "NEUTRAL")
        self.assertEqual(Variant.TONAL_SPOT.name, "TONAL_SPOT")
        self.assertEqual(Variant.VIBRANT.name, "VIBRANT")
        self.assertEqual(Variant.EXPRESSIVE.name, "EXPRESSIVE")
        self.assertEqual(Variant.FIDELITY.name, "FIDELITY")
        self.assertEqual(Variant.CONTENT.name, "CONTENT")
        self.assertEqual(Variant.RAINBOW.name, "RAINBOW")
        self.assertEqual(Variant.FRUIT_SALAD.name, "FRUIT_SALAD")

if __name__ == "__main__":
    unittest.main()
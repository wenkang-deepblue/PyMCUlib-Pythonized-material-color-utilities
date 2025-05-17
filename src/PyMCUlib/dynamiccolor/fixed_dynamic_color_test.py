# dynamiccolor/fixed_dynamic_color_test.py

import unittest

from PyMCUlib.hct.hct import Hct
from PyMCUlib.scheme.scheme_monochrome import SchemeMonochrome
from PyMCUlib.scheme.scheme_tonal_spot import SchemeTonalSpot
from PyMCUlib.dynamiccolor.material_dynamic_colors import MaterialDynamicColors


class FixedDynamicColorTest(unittest.TestCase):
    """Tests for fixed dynamic colors in different schemes."""

    def test_fixed_colors_in_non_monochrome_schemes(self):
        """Test fixed colors in non-monochrome schemes."""
        scheme = SchemeTonalSpot(
            Hct.from_int(0xFFFF0000),
            True,
            0.0,
        )

        # Check primary fixed colors
        self.assertAlmostEqual(
            MaterialDynamicColors.primary_fixed.get_hct(scheme).tone,
            90.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.primary_fixed_dim.get_hct(scheme).tone,
            80.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_primary_fixed.get_hct(scheme).tone,
            10.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_primary_fixed_variant.get_hct(scheme).tone,
            30.0, places=0)

        # Check secondary fixed colors
        self.assertAlmostEqual(
            MaterialDynamicColors.secondary_fixed.get_hct(scheme).tone,
            90.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.secondary_fixed_dim.get_hct(scheme).tone,
            80.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_secondary_fixed.get_hct(scheme).tone,
            10.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_secondary_fixed_variant.get_hct(scheme).tone,
            30.0, places=0)

        # Check tertiary fixed colors
        self.assertAlmostEqual(
            MaterialDynamicColors.tertiary_fixed.get_hct(scheme).tone,
            90.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.tertiary_fixed_dim.get_hct(scheme).tone,
            80.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_tertiary_fixed.get_hct(scheme).tone,
            10.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_tertiary_fixed_variant.get_hct(scheme).tone,
            30.0, places=0)

    def test_fixed_argb_colors_in_non_monochrome_schemes(self):
        """Test fixed ARGB colors in non-monochrome schemes."""
        scheme = SchemeTonalSpot(
            Hct.from_int(0xFFFF0000),
            True,
            0.0,
        )

        # Check primary fixed ARGB colors
        self.assertEqual(scheme.primary_fixed, 0xFFFFDAD4)
        self.assertEqual(scheme.primary_fixed_dim, 0xFFFFB4A8)
        self.assertEqual(scheme.on_primary_fixed, 0xFF3A0905)
        self.assertEqual(scheme.on_primary_fixed_variant, 0xFF73342A)

        # Check secondary fixed ARGB colors
        self.assertEqual(scheme.secondary_fixed, 0xFFFFDAD4)
        self.assertEqual(scheme.secondary_fixed_dim, 0xFFE7BDB6)
        self.assertEqual(scheme.on_secondary_fixed, 0xFF2C1512)
        self.assertEqual(scheme.on_secondary_fixed_variant, 0xFF5D3F3B)

        # Check tertiary fixed ARGB colors
        self.assertEqual(scheme.tertiary_fixed, 0xFFFBDFA6)
        self.assertEqual(scheme.tertiary_fixed_dim, 0xFFDEC48C)
        self.assertEqual(scheme.on_tertiary_fixed, 0xFF251A00)
        self.assertEqual(scheme.on_tertiary_fixed_variant, 0xFF564419)

    def test_fixed_colors_in_light_monochrome_schemes(self):
        """Test fixed colors in light monochrome schemes."""
        scheme = SchemeMonochrome(
            Hct.from_int(0xFFFF0000),
            False,
            0.0,
        )

        # Check primary fixed colors
        self.assertAlmostEqual(
            MaterialDynamicColors.primary_fixed.get_hct(scheme).tone,
            40.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.primary_fixed_dim.get_hct(scheme).tone,
            30.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_primary_fixed.get_hct(scheme).tone,
            100.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_primary_fixed_variant.get_hct(scheme).tone,
            90.0, places=0)

        # Check secondary fixed colors
        self.assertAlmostEqual(
            MaterialDynamicColors.secondary_fixed.get_hct(scheme).tone,
            80.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.secondary_fixed_dim.get_hct(scheme).tone,
            70.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_secondary_fixed.get_hct(scheme).tone,
            10.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_secondary_fixed_variant.get_hct(scheme).tone,
            25.0, places=0)

        # Check tertiary fixed colors
        self.assertAlmostEqual(
            MaterialDynamicColors.tertiary_fixed.get_hct(scheme).tone,
            40.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.tertiary_fixed_dim.get_hct(scheme).tone,
            30.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_tertiary_fixed.get_hct(scheme).tone,
            100.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_tertiary_fixed_variant.get_hct(scheme).tone,
            90.0, places=0)

    def test_fixed_colors_in_dark_monochrome_schemes(self):
        """Test fixed colors in dark monochrome schemes."""
        scheme = SchemeMonochrome(
            Hct.from_int(0xFFFF0000),
            True,
            0.0,
        )

        # Check primary fixed colors
        self.assertAlmostEqual(
            MaterialDynamicColors.primary_fixed.get_hct(scheme).tone,
            40.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.primary_fixed_dim.get_hct(scheme).tone,
            30.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_primary_fixed.get_hct(scheme).tone,
            100.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_primary_fixed_variant.get_hct(scheme).tone,
            90.0, places=0)

        # Check secondary fixed colors
        self.assertAlmostEqual(
            MaterialDynamicColors.secondary_fixed.get_hct(scheme).tone,
            80.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.secondary_fixed_dim.get_hct(scheme).tone,
            70.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_secondary_fixed.get_hct(scheme).tone,
            10.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_secondary_fixed_variant.get_hct(scheme).tone,
            25.0, places=0)

        # Check tertiary fixed colors
        self.assertAlmostEqual(
            MaterialDynamicColors.tertiary_fixed.get_hct(scheme).tone,
            40.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.tertiary_fixed_dim.get_hct(scheme).tone,
            30.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_tertiary_fixed.get_hct(scheme).tone,
            100.0, places=0)
        self.assertAlmostEqual(
            MaterialDynamicColors.on_tertiary_fixed_variant.get_hct(scheme).tone,
            90.0, places=0)


if __name__ == '__main__':
    unittest.main()
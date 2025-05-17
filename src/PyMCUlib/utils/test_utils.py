# utils/test_utils.py

import unittest
from PyMCUlib.utils import string_utils


class ColorTestCase(unittest.TestCase):
    """Custom test case with color-specific assertions."""
    
    def assertColorsEqual(self, actual: int, expected: int, msg: str = None):
        """
        Assert that two colors are equal, with readable hex output on failure.
        
        Args:
            actual: The actual color value
            expected: The expected color value
            msg: Optional message to include in the assertion error
        """
        if actual != expected:
            actual_hex = string_utils.hex_from_argb(actual)
            expected_hex = string_utils.hex_from_argb(expected)
            failure_msg = f"Colors do not match: {actual_hex} != {expected_hex}"
            
            if msg:
                failure_msg = f"{msg}: {failure_msg}"
                
            self.fail(failure_msg)

    def test_hex_from_argb(self):
           # test string_utils.hex_from_argb
           self.assertEqual(string_utils.hex_from_argb(0x00FF00), '#00ff00')

if __name__ == '__main__':
    unittest.main()
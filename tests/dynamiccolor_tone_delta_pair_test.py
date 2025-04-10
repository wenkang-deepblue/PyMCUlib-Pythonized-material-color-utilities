# test_tone_delta_pair.py

import unittest
from PyMCUlib.dynamiccolor.tone_delta_pair import TonePolarity, ToneDeltaPair

# Mock DynamicColor for testing
class MockDynamicColor:
    def __init__(self, name):
        self.name = name

class TestTonePolarity(unittest.TestCase):
    
    def test_tone_polarity_enum_values(self):
        """Test that TonePolarity enum values are defined correctly."""
        self.assertEqual(TonePolarity.DARKER.value, 0)
        self.assertEqual(TonePolarity.LIGHTER.value, 1)
        self.assertEqual(TonePolarity.NEARER.value, 2)
        self.assertEqual(TonePolarity.FARTHER.value, 3)

class TestToneDeltaPair(unittest.TestCase):
    
    def test_tone_delta_pair_initialization(self):
        """Test that ToneDeltaPair can be properly initialized."""
        role_a = MockDynamicColor("RoleA")
        role_b = MockDynamicColor("RoleB")
        delta = 15.0
        polarity = TonePolarity.DARKER
        stay_together = True
        
        pair = ToneDeltaPair(role_a, role_b, delta, polarity, stay_together)
        
        self.assertEqual(pair.role_a, role_a)
        self.assertEqual(pair.role_b, role_b)
        self.assertEqual(pair.delta, delta)
        self.assertEqual(pair.polarity, polarity)
        self.assertEqual(pair.stay_together, stay_together)

if __name__ == "__main__":
    unittest.main()
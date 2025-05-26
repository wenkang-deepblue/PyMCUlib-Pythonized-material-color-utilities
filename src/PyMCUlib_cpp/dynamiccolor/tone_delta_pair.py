# tone_delta_pair.py

from enum import Enum

class TonePolarity(Enum):
    """
    Describes the difference in tone between colors.
    """
    DARKER = 0
    LIGHTER = 1
    NEARER = 2
    FARTHER = 3

class ToneDeltaPair:
    """
    Documents a constraint between two DynamicColors, in which their tones must
    have a certain distance from each other.

    Prefer a DynamicColor with a background, this is for special cases when
    designers want tonal distance, literally contrast, between two colors that
    don't have a background / foreground relationship or a contrast guarantee.
    """
    
    def __init__(self, role_a, role_b, delta, polarity, stay_together):
        """
        Documents a constraint in tone distance between two DynamicColors.

        The polarity is an adjective that describes "A", compared to "B".

        For instance, ToneDeltaPair(A, B, 15, 'darker', stayTogether) states that
        A's tone should be at least 15 darker than B's.

        'nearer' and 'farther' describes closeness to the surface roles. For
        instance, ToneDeltaPair(A, B, 10, 'nearer', stayTogether) states that A
        should be 10 lighter than B in light mode, and 10 darker than B in dark
        mode.

        Args:
            role_a: The first role in a pair.
            role_b: The second role in a pair.
            delta: Required difference between tones. Absolute value, negative
                values have undefined behavior.
            polarity: The relative relation between tones of role_a and role_b,
                as described above.
            stay_together: Whether these two roles should stay on the same side of
                the "awkward zone" (T50-59). This is necessary for certain cases where
                one role has two backgrounds.
        """
        self.role_a = role_a
        self.role_b = role_b
        self.delta = delta
        self.polarity = polarity
        self.stay_together = stay_together
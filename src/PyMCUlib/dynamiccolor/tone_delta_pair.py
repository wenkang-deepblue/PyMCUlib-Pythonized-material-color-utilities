# dynamiccolor/tone_delta_pair.py

from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .dynamic_color import DynamicColor

# Describes the different in tone between colors.
# nearer and farther are deprecated. Use DeltaConstraint instead.
TonePolarity = Literal['darker', 'lighter', 'nearer', 'farther', 'relative_darker', 'relative_lighter']

# Describes how to fulfill a tone delta pair constraint.
DeltaConstraint = Literal['exact', 'nearer', 'farther']


class ToneDeltaPair:
    """
    Documents a constraint between two DynamicColors, in which their tones must
    have a certain distance from each other.

    Prefer a DynamicColor with a background, this is for special cases when
    designers want tonal distance, literally contrast, between two colors that
    don't have a background / foreground relationship or a contrast guarantee.
    """

    def __init__(
            self,
            role_a: 'DynamicColor',
            role_b: 'DynamicColor',
            delta: float,
            polarity: TonePolarity,
            stay_together: bool,
            constraint: Optional[DeltaConstraint] = None,
    ):
        """
        Documents a constraint in tone distance between two DynamicColors.

        The polarity is an adjective that describes "A", compared to "B".

        For instance, ToneDeltaPair(A, B, 15, 'darker', 'exact') states that
        A's tone should be exactly 15 darker than B's.

        'relative_darker' and 'relative_lighter' describes the tone adjustment
        relative to the surface color trend (white in light mode; black in dark
        mode). For instance, ToneDeltaPair(A, B, 10, 'relative_lighter',
        'farther') states that A should be at least 10 lighter than B in light
        mode, and at least 10 darker than B in dark mode.

        Args:
            role_a: The first role in a pair.
            role_b: The second role in a pair.
            delta: Required difference between tones. Absolute value, negative
                values have undefined behavior.
            polarity: The relative relation between tones of roleA and roleB,
                as described above.
            stay_together: Whether these two roles should stay on the same side
                of the "awkward zone" (T50-59). This is necessary for certain cases where
                one role has two backgrounds.
            constraint: How to fulfill the tone delta pair constraint.
        """
        self.role_a = role_a
        self.role_b = role_b
        self.delta = delta
        self.polarity = polarity
        self.stay_together = stay_together
        self.constraint = constraint if constraint is not None else 'exact'
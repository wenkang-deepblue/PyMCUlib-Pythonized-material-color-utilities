# temperature/temperature_cache.py

"""
Design utilities using color temperature theory.

Analogous colors, complementary color, and cache to efficiently, lazily,
generate data for calculations when needed.
"""

import math
from typing import List, Optional, Mapping

from PyMCUlib.hct.hct import Hct
from PyMCUlib.utils import color_utils
from PyMCUlib.utils import math_utils


class TemperatureCache:
    """
    Design utilities using color temperature theory.

    Analogous colors, complementary color, and cache to efficiently, lazily,
    generate data for calculations when needed.
    """

    def __init__(self, input_color: Hct):
        """
        Initialize with an input color.

        Args:
            input_color: The input color.
        """
        self.input = input_color
        self.hcts_by_temp_cache: List[Hct] = []
        self.hcts_by_hue_cache: List[Hct] = []
        self.temps_by_hct_cache: Mapping[Hct, float] = {}
        self.input_relative_temperature_cache: float = -1.0
        self.complement_cache: Optional[Hct] = None

    @property
    def hcts_by_temp(self) -> List[Hct]:
        """
        HCTs for all hues, with the same chroma/tone as the input,
        sorted by temperature.

        Returns:
            List of Hct colors, sorted by temperature.
        """
        if len(self.hcts_by_temp_cache) > 0:
            return self.hcts_by_temp_cache

        hcts = self.hcts_by_hue + [self.input]
        temperatures_by_hct = self.temps_by_hct
        hcts.sort(key=lambda hct: temperatures_by_hct[hct])
        self.hcts_by_temp_cache = hcts
        return hcts

    @property
    def warmest(self) -> Hct:
        """
        Returns the warmest color with the same chroma/tone as the input.

        Returns:
            The warmest color.
        """
        return self.hcts_by_temp[-1]

    @property
    def coldest(self) -> Hct:
        """
        Returns the coldest color with the same chroma/tone as the input.

        Returns:
            The coldest color.
        """
        return self.hcts_by_temp[0]

    def analogous(self, count: int = 5, divisions: int = 12) -> List[Hct]:
        """
        A set of colors with differing hues, equidistant in temperature.

        In art, this is usually described as a set of 5 colors on a color wheel
        divided into 12 sections. This method allows provision of either of those
        values.

        Behavior is undefined when count or divisions is 0.
        When divisions < count, colors repeat.

        Args:
            count: The number of colors to return, includes the input color.
            divisions: The number of divisions on the color wheel.

        Returns:
            A list of count colors analogous to the input color.
        """
        start_hue = round(self.input.hue)
        start_hct = self.hcts_by_hue[start_hue]
        last_temp = self.relative_temperature(start_hct)
        all_colors = [start_hct]

        absolute_total_temp_delta = 0.0
        for i in range(360):
            hue = math_utils.sanitize_degrees_int(start_hue + i)
            hct = self.hcts_by_hue[hue]
            temp = self.relative_temperature(hct)
            temp_delta = abs(temp - last_temp)
            last_temp = temp
            absolute_total_temp_delta += temp_delta

        hue_addend = 1
        temp_step = absolute_total_temp_delta / divisions
        total_temp_delta = 0.0
        last_temp = self.relative_temperature(start_hct)

        while len(all_colors) < divisions:
            hue = math_utils.sanitize_degrees_int(start_hue + hue_addend)
            hct = self.hcts_by_hue[hue]
            temp = self.relative_temperature(hct)
            temp_delta = abs(temp - last_temp)
            total_temp_delta += temp_delta

            desired_total_temp_delta_for_index = len(all_colors) * temp_step
            index_satisfied = total_temp_delta >= desired_total_temp_delta_for_index
            index_addend = 1
            # Keep adding this hue to the answers until its temperature is
            # insufficient. This ensures consistent behavior when there aren't
            # [divisions] discrete steps between 0 and 360 in hue with [tempStep]
            # delta in temperature between them.
            #
            # For example, white and black have no analogues: there are no other
            # colors at T100/T0. Therefore, they should just be added to the array
            # as answers.
            while index_satisfied and len(all_colors) < divisions:
                all_colors.append(hct)
                desired_total_temp_delta_for_index = (
                    (len(all_colors) + index_addend) * temp_step
                )
                index_satisfied = total_temp_delta >= desired_total_temp_delta_for_index
                index_addend += 1

            last_temp = temp
            hue_addend += 1
            if hue_addend > 360:
                while len(all_colors) < divisions:
                    all_colors.append(hct)
                break

        answers = [self.input]

        # First, generate analogues from rotating counter-clockwise.
        increase_hue_count = math.floor((count - 1) / 2.0)
        for i in range(1, increase_hue_count + 1):
            index = 0 - i
            while index < 0:
                index = len(all_colors) + index
            if index >= len(all_colors):
                index = index % len(all_colors)
            answers.insert(0, all_colors[index])

        # Second, generate analogues from rotating clockwise.
        decrease_hue_count = count - increase_hue_count - 1
        for i in range(1, decrease_hue_count + 1):
            index = i
            while index < 0:
                index = len(all_colors) + index
            if index >= len(all_colors):
                index = index % len(all_colors)
            answers.append(all_colors[index])

        return answers

    @property
    def complement(self) -> Hct:
        """
        A color that complements the input color aesthetically.

        In art, this is usually described as being across the color wheel.
        History of this shows intent as a color that is just as cool-warm as the
        input color is warm-cool.

        Returns:
            The complementary color.
        """
        if self.complement_cache is not None:
            return self.complement_cache

        coldest_hue = self.coldest.hue
        coldest_temp = self.temps_by_hct[self.coldest]

        warmest_hue = self.warmest.hue
        warmest_temp = self.temps_by_hct[self.warmest]
        range_val = warmest_temp - coldest_temp
        # If the coldest and warmest temperatures are the same, range_val is 0,
        # return the input color to avoid division by 0.
        if range_val == 0.0:
            self.complement_cache = self.input
            return self.input

        start_hue_is_coldest_to_warmest = TemperatureCache._is_between(
            self.input.hue, coldest_hue, warmest_hue
        )
        start_hue = warmest_hue if start_hue_is_coldest_to_warmest else coldest_hue
        end_hue = coldest_hue if start_hue_is_coldest_to_warmest else warmest_hue
        direction_of_rotation = 1.0
        smallest_error = 1000.0
        answer = self.hcts_by_hue[round(self.input.hue)]

        complement_relative_temp = 1.0 - self.input_relative_temperature
        # Find the color in the other section, closest to the inverse percentile
        # of the input color. This is the complement.
        for hue_addend in range(361):
            hue = math_utils.sanitize_degrees_double(
                start_hue + direction_of_rotation * hue_addend
            )
            if not TemperatureCache._is_between(hue, start_hue, end_hue):
                continue
            possible_answer = self.hcts_by_hue[round(hue)]
            relative_temp = (
                self.temps_by_hct[possible_answer] - coldest_temp
            ) / range_val
            error = abs(complement_relative_temp - relative_temp)
            if error < smallest_error:
                smallest_error = error
                answer = possible_answer

        self.complement_cache = answer
        return self.complement_cache

    def relative_temperature(self, hct: Hct) -> float:
        """
        Temperature relative to all colors with the same chroma and tone.
        Value on a scale from 0 to 1.

        Args:
            hct: The color to get the relative temperature of.

        Returns:
            The relative temperature of the color, from 0 to 1.
        """
        range_val = (
            self.temps_by_hct[self.warmest] - self.temps_by_hct[self.coldest]
        )
        difference_from_coldest = (
            self.temps_by_hct[hct] - self.temps_by_hct[self.coldest]
        )
        # Handle when there's no difference in temperature between warmest and
        # coldest: for example, at T100, only one color is available, white.
        if range_val == 0.0:
            return 0.5
        return difference_from_coldest / range_val

    @property
    def input_relative_temperature(self) -> float:
        """
        Relative temperature of the input color. See relativeTemperature.

        Returns:
            The relative temperature of the input color.
        """
        if self.input_relative_temperature_cache >= 0.0:
            return self.input_relative_temperature_cache

        self.input_relative_temperature_cache = self.relative_temperature(self.input)
        return self.input_relative_temperature_cache

    @property
    def temps_by_hct(self) -> Mapping[Hct, float]:
        """
        A Dict with keys of HCTs in hctsByTemp, values of raw temperature.

        Returns:
            A Dict mapping HCT colors to their raw temperature.
        """
        if len(self.temps_by_hct_cache) > 0:
            return self.temps_by_hct_cache

        all_hcts = self.hcts_by_hue + [self.input]
        temperatures_by_hct = {}
        for hct in all_hcts:
            temperatures_by_hct[hct] = TemperatureCache.raw_temperature(hct)
        self.temps_by_hct_cache = temperatures_by_hct
        return self.temps_by_hct_cache

    @property
    def hcts_by_hue(self) -> List[Hct]:
        """
        HCTs for all hues, with the same chroma/tone as the input.
        Sorted ascending, hue 0 to 360.

        Returns:
            List of Hct colors, sorted by hue.
        """
        if len(self.hcts_by_hue_cache) > 0:
            return self.hcts_by_hue_cache

        hcts = []
        for hue in range(361):
            color_at_hue = Hct.from_hct(hue, self.input.chroma, self.input.tone)
            hcts.append(color_at_hue)
        self.hcts_by_hue_cache = hcts
        return self.hcts_by_hue_cache

    @staticmethod
    def _is_between(angle: float, a: float, b: float) -> bool:
        """
        Determines if an angle is between two other angles, rotating clockwise.

        Args:
            angle: The angle to check.
            a: The first angle.
            b: The second angle.

        Returns:
            True if the angle is between the two angles, false otherwise.
        """
        if a < b:
            return a <= angle and angle <= b
        return a <= angle or angle <= b

    @staticmethod
    def raw_temperature(color: Hct) -> float:
        """
        Value representing cool-warm factor of a color.
        Values below 0 are considered cool, above, warm.

        Color science has researched emotion and harmony, which art uses to select
        colors. Warm-cool is the foundation of analogous and complementary colors.
        See:
        - Li-Chen Ou's Chapter 19 in Handbook of Color Psychology (2015).
        - Josef Albers' Interaction of Color chapters 19 and 21.

        Implementation of Ou, Woodcock and Wright's algorithm, which uses
        L*a*b* / LCH color space.
        Return value has these properties:
        - Values below 0 are cool, above 0 are warm.
        - Lower bound: -0.52 - (chroma ^ 1.07 / 20). L*a*b* chroma is infinite.
          Assuming max of 130 chroma, -9.66.
        - Upper bound: -0.52 + (chroma ^ 1.07 / 20). L*a*b* chroma is infinite.
          Assuming max of 130 chroma, 8.61.

        Args:
            color: The color to get the raw temperature of.

        Returns:
            The raw temperature of the color.
        """
        lab = color_utils.lab_from_argb(color.to_int())
        hue = math_utils.sanitize_degrees_double(
            math.atan2(lab[2], lab[1]) * 180.0 / math.pi
        )
        chroma = math.sqrt((lab[1] * lab[1]) + (lab[2] * lab[2]))
        temperature = (
            -0.5
            + 0.02
            * math.pow(chroma, 1.07)
            * math.cos(math_utils.sanitize_degrees_double(hue - 50.0) * math.pi / 180.0)
        )
        return temperature
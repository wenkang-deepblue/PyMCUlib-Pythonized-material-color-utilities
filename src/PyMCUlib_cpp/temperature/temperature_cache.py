# temperature_cache.py

from typing import List, Dict
import math
from PyMCUlib_cpp.utils.utils import sanitize_degrees_double, sanitize_degrees_int
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.quantize.lab import lab_from_int

class TemperatureCache:
    """
    Design utilities using color temperature theory.
    
    Analogous colors, complementary color, and cache to efficiently, lazily,
    generate data for calculations when needed.
    """
    
    def __init__(self, input_color: Hct):
        """
        Create a cache that allows calculation of ex. complementary and analogous
        colors.
        
        Args:
            input_color: Color to find complement/analogous colors of. Any colors will
                have the same tone, and chroma as the input color, modulo any restrictions
                due to the other hues having lower limits on chroma.
        """
        self.input = input_color
        self.precomputed_complement = None
        self.precomputed_hcts_by_temp = None
        self.precomputed_hcts_by_hue = None
        self.precomputed_temps_by_hct = None
        self._from_default = False
    
    def get_complement(self) -> Hct:
        """
        A color that complements the input color aesthetically.
        
        In art, this is usually described as being across the color wheel.
        History of this shows intent as a color that is just as cool-warm as the
        input color is warm-cool.
        
        Returns:
            A color that is complementary to the input color.
        """
        if self.precomputed_complement is not None:
            return self.precomputed_complement
        
        coldest_hue = self.get_coldest().get_hue()
        coldest_temp = self.get_temps_by_hct()[self.get_coldest()]
        
        warmest_hue = self.get_warmest().get_hue()
        warmest_temp = self.get_temps_by_hct()[self.get_warmest()]
        
        range_temp = warmest_temp - coldest_temp

        # Handle case when temperature range is zero
        # For colors like white or black, all hues have the same temperature
        if range_temp == 0:
            self.precomputed_complement = self.input
            return self.precomputed_complement
        
        start_hue_is_coldest_to_warmest = self._is_between(
            self.input.get_hue(), coldest_hue, warmest_hue)
        
        start_hue = warmest_hue if start_hue_is_coldest_to_warmest else coldest_hue
        end_hue = coldest_hue if start_hue_is_coldest_to_warmest else warmest_hue
        direction_of_rotation = 1.0
        
        smallest_error = 1000.0
        answer = self.get_hcts_by_hue()[round(self.input.get_hue())]
        
        complement_relative_temp = 1.0 - self.get_relative_temperature(self.input)
        # Find the color in the other section, closest to the inverse percentile
        # of the input color. This is the complement.
        for hue_addend in range(361):  # 0 to 360 inclusive
            hue = sanitize_degrees_double(start_hue + direction_of_rotation * hue_addend)
            if not self._is_between(hue, start_hue, end_hue):
                continue
                
            possible_answer = self.get_hcts_by_hue()[round(hue)]
            relative_temp = (self.get_temps_by_hct()[possible_answer] - coldest_temp) / range_temp
            error = abs(complement_relative_temp - relative_temp)
            
            if error < smallest_error:
                smallest_error = error
                answer = possible_answer
        
        self.precomputed_complement = answer
        return self.precomputed_complement
    
    def get_analogous_colors(self, count: int = 5, divisions: int = 12) -> List[Hct]:
        """
        A set of colors with differing hues, equidistant in temperature.
        
        In art, this is usually described as a set of 5 colors on a color wheel
        divided into 12 sections. This method allows provision of either of those
        values.
        
        Behavior is undefined when count or divisions is 0. When divisions 
        count, colors repeat.
        
        Args:
            count: The number of colors to return, includes the input color.
            divisions: The number of divisions on the color wheel.
            
        Returns:
            Analogous colors, ordered from coolest to warmest
        """
        if count == 5 and divisions == 12 and not self._from_default:
            self._from_default = True
            result = self.get_analogous_colors_default()
            self._from_default = False
            return result
        
        # The starting hue is the hue of the input color.
        start_hue = round(self.input.get_hue())
        start_hct = self.get_hcts_by_hue()[start_hue]
        last_temp = self.get_relative_temperature(start_hct)
        
        all_colors = [start_hct]
        
        absolute_total_temp_delta = 0.0
        for i in range(360):
            hue = sanitize_degrees_int(start_hue + i)
            hct = self.get_hcts_by_hue()[hue]
            temp = self.get_relative_temperature(hct)
            temp_delta = abs(temp - last_temp)
            last_temp = temp
            absolute_total_temp_delta += temp_delta
        
        hue_addend = 1
        temp_step = absolute_total_temp_delta / divisions
        total_temp_delta = 0.0
        last_temp = self.get_relative_temperature(start_hct)
        
        while len(all_colors) < divisions:
            hue = sanitize_degrees_int(start_hue + hue_addend)
            hct = self.get_hcts_by_hue()[hue]
            temp = self.get_relative_temperature(hct)
            temp_delta = abs(temp - last_temp)
            total_temp_delta += temp_delta
            
            desired_total_temp_delta_for_index = (len(all_colors) * temp_step)
            index_satisfied = total_temp_delta >= desired_total_temp_delta_for_index
            
            index_addend = 1
            # Keep adding this hue to the answers until its temperature is
            # insufficient. This ensures consistent behavior when there aren't
            # `divisions` discrete steps between 0 and 360 in hue with `temp_step`
            # delta in temperature between them.
            #
            # For example, white and black have no analogues: there are no other
            # colors at T100/T0. Therefore, they should just be added to the array
            # as answers.
            while index_satisfied and len(all_colors) < divisions:
                all_colors.append(hct)
                desired_total_temp_delta_for_index = ((len(all_colors) + index_addend) * temp_step)
                index_satisfied = total_temp_delta >= desired_total_temp_delta_for_index
                index_addend += 1
                
            last_temp = temp
            hue_addend += 1
            
            if hue_addend > 360:
                while len(all_colors) < divisions:
                    all_colors.append(hct)
                break
        
        answers = [self.input]
        
        ccw_count = math.floor((count - 1.0) / 2.0)
        for i in range(1, ccw_count + 1):
            index = 0 - i
            while index < 0:
                index = len(all_colors) + index
            if index >= len(all_colors):
                index = index % len(all_colors)
            answers.insert(0, all_colors[index])
        
        cw_count = count - ccw_count - 1
        for i in range(1, cw_count + 1):
            index = i
            while index < 0:
                index = len(all_colors) + index
            if index >= len(all_colors):
                index = index % len(all_colors)
            answers.append(all_colors[index])
        
        return answers
    
    def get_analogous_colors_default(self) -> List[Hct]:
        """
        5 colors that pair well with the input color.
        
        The colors are equidistant in temperature and adjacent in hue.
        
        Returns:
            Analogous colors, ordered from coolest to warmest.
        """
        return self.get_analogous_colors(5, 12)
    
    def get_relative_temperature(self, hct: Hct) -> float:
        """
        Temperature relative to all colors with the same chroma and tone.
        
        Args:
            hct: HCT to find the relative temperature of.
            
        Returns:
            Value on a scale from 0 to 1.
        """
        range_temp = (
            self.get_temps_by_hct()[self.get_warmest()] - 
            self.get_temps_by_hct()[self.get_coldest()]
        )
        
        difference_from_coldest = (
            self.get_temps_by_hct()[hct] - 
            self.get_temps_by_hct()[self.get_coldest()]
        )
        
        # Handle when there's no difference in temperature between warmest and
        # coldest: for example, at T100, only one color is available, white.
        if range_temp == 0.:
            return 0.5
            
        return difference_from_coldest / range_temp
    
    @staticmethod
    def raw_temperature(color: Hct) -> float:
        """
        Value representing cool-warm factor of a color. Values below 0 are
        considered cool, above, warm.
        
        Color science has researched emotion and harmony, which art uses to
        select colors. Warm-cool is the foundation of analogous and complementary
        colors. See: - Li-Chen Ou's Chapter 19 in Handbook of Color Psychology
        (2015). - Josef Albers' Interaction of Color chapters 19 and 21.
        
        Implementation of Ou, Woodcock and Wright's algorithm, which uses
        Lab/LCH color space. Return value has these properties:
        - Values below 0 are cool, above 0 are warm.
        - Lower bound: -9.66. Chroma is infinite. Assuming max of Lab chroma
        130.
        - Upper bound: 8.61. Chroma is infinite. Assuming max of Lab chroma 130.
        
        Args:
            color: HCT color to calculate raw temperature.
            
        Returns:
            Raw temperature of the color.
        """
        from math import pi, hypot, atan2, cos, pow
        
        lab = lab_from_int(color.to_int())
        hue = sanitize_degrees_double(atan2(lab.b, lab.a) * 180.0 / pi)
        chroma = hypot(lab.a, lab.b)
        
        return -0.5 + 0.02 * pow(chroma, 1.07) * cos(sanitize_degrees_double(hue - 50.) * pi / 180)
    
    def get_coldest(self) -> Hct:
        """
        Coldest color with same chroma and tone as input.
        
        Returns:
            The coldest color with the same chroma and tone as the input.
        """
        return self.get_hcts_by_temp()[0]
    
    def get_warmest(self) -> Hct:
        """
        Warmest color with same chroma and tone as input.
        
        Returns:
            The warmest color with the same chroma and tone as the input.
        """
        return self.get_hcts_by_temp()[-1]
    
    @staticmethod
    def _is_between(angle: float, a: float, b: float) -> bool:
        """
        Determines if an angle is between two other angles, rotating clockwise.
        
        Args:
            angle: The angle to check.
            a: First bounding angle.
            b: Second bounding angle.
            
        Returns:
            True if the angle is between the two bounding angles.
        """
        if a < b:
            return a <= angle and angle <= b
        return a <= angle or angle <= b
    
    def get_hcts_by_hue(self) -> List[Hct]:
        """
        HCTs for all colors with the same chroma/tone as the input.
        
        Sorted by hue, ex. index 0 is hue 0.
        
        Returns:
            HCTs for all colors with the same chroma/tone as the input.
        """
        if self.precomputed_hcts_by_hue is not None:
            return self.precomputed_hcts_by_hue
            
        hcts = []
        for hue in range(361):  # 0 to 360 inclusive
            color_at_hue = Hct.from_hct(hue, self.input.get_chroma(), self.input.get_tone())
            hcts.append(color_at_hue)
            
        self.precomputed_hcts_by_hue = hcts
        return self.precomputed_hcts_by_hue
    
    def get_hcts_by_temp(self) -> List[Hct]:
        """
        HCTs for all colors with the same chroma/tone as the input.
        
        Sorted from coldest first to warmest last.
        
        Returns:
            HCTs for all colors with the same chroma/tone as the input.
        """
        if self.precomputed_hcts_by_temp is not None:
            return self.precomputed_hcts_by_temp
            
        hcts = list(self.get_hcts_by_hue())
        hcts.append(self.input)
        
        temps_by_hct = self.get_temps_by_hct()
        
        # Sort HCTs by temperature
        hcts.sort(key=lambda a: temps_by_hct[a])
        
        self.precomputed_hcts_by_temp = hcts
        return self.precomputed_hcts_by_temp
    
    def get_temps_by_hct(self) -> Dict[Hct, float]:
        """
        Keys of HCTs in get_hcts_by_temp, values of raw temperature.
        
        Returns:
            Dictionary mapping HCTs to their raw temperature.
        """
        if self.precomputed_temps_by_hct is not None:
            return self.precomputed_temps_by_hct
            
        all_hcts = list(self.get_hcts_by_hue())
        all_hcts.append(self.input)
        
        temperatures_by_hct = {}
        for hct in all_hcts:
            temperatures_by_hct[hct] = self.raw_temperature(hct)
            
        self.precomputed_temps_by_hct = temperatures_by_hct
        return self.precomputed_temps_by_hct
# quantize/quantizer_wu.py

from typing import List
from PyMCUlib.utils import color_utils
from PyMCUlib.quantize.quantizer_map import QuantizerMap

# Constants
INDEX_BITS = 5
SIDE_LENGTH = 33  # ((1 << INDEX_INDEX_BITS) + 1)
TOTAL_SIZE = 35937  # SIDE_LENGTH * SIDE_LENGTH * SIDE_LENGTH

# Direction enum equivalent
class Direction:
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Box:
    """
    Keeps track of the state of each box created as the Wu quantization
    algorithm progresses through dividing the image's pixels as plotted in RGB.
    """
    def __init__(
        self,
        r0: int = 0,
        r1: int = 0,
        g0: int = 0,
        g1: int = 0,
        b0: int = 0,
        b1: int = 0,
        vol: int = 0
    ) -> None:
        self.r0 = r0
        self.r1 = r1
        self.g0 = g0
        self.g1 = g1
        self.b0 = b0
        self.b1 = b1
        self.vol = vol


class CreateBoxesResult:
    """
    Represents final result of Wu algorithm.
    """
    def __init__(self, requested_count: int, result_count: int) -> None:
        """
        Args:
            requested_count: how many colors the caller asked to be returned from
                quantization.
            result_count: the actual number of colors achieved from quantization.
                May be lower than the requested count.
        """
        self.requested_count = requested_count
        self.result_count = result_count


class MaximizeResult:
    """
    Represents the result of calculating where to cut an existing box in such
    a way to maximize variance between the two new boxes created by a cut.
    """
    def __init__(self, cut_location: int, maximum: float) -> None:
        self.cut_location = cut_location
        self.maximum = maximum


class QuantizerWu:
    """
    An image quantizer that divides the image's pixels into clusters by
    recursively cutting an RGB cube, based on the weight of pixels in each area
    of the cube.

    The algorithm was described by Xiaolin Wu in Graphic Gems II, published in
    1991.
    """
    
    def __init__(
        self,
        weights: List[int] = None,
        moments_r: List[int] = None,
        moments_g: List[int] = None,
        moments_b: List[int] = None,
        moments: List[float] = None,
        cubes: List[Box] = None
    ) -> None:
        self.weights = weights if weights is not None else []
        self.moments_r = moments_r if moments_r is not None else []
        self.moments_g = moments_g if moments_g is not None else []
        self.moments_b = moments_b if moments_b is not None else []
        self.moments = moments if moments is not None else []
        self.cubes = cubes if cubes is not None else []

    def quantize(self, pixels: List[int], max_colors: int) -> List[int]:
        """
        Args:
            pixels: Colors in ARGB format.
            max_colors: The number of colors to divide the image into. A lower
                number of colors may be returned.
        
        Returns:
            Colors in ARGB format.
        """
        self._construct_histogram(pixels)
        self._compute_moments()
        create_boxes_result = self._create_boxes(max_colors)
        results = self._create_result(create_boxes_result.result_count)
        return results

    def _construct_histogram(self, pixels: List[int]) -> None:
        """
        Constructs a histogram of the image's pixels.
        """
        self.weights = [0] * TOTAL_SIZE
        self.moments_r = [0] * TOTAL_SIZE
        self.moments_g = [0] * TOTAL_SIZE
        self.moments_b = [0] * TOTAL_SIZE
        self.moments = [0] * TOTAL_SIZE

        count_by_color = QuantizerMap.quantize(pixels)

        for pixel, count in count_by_color.items():
            red = color_utils.red_from_argb(pixel)
            green = color_utils.green_from_argb(pixel)
            blue = color_utils.blue_from_argb(pixel)

            bits_to_remove = 8 - INDEX_BITS
            i_r = (red >> bits_to_remove) + 1
            i_g = (green >> bits_to_remove) + 1
            i_b = (blue >> bits_to_remove) + 1
            index = self._get_index(i_r, i_g, i_b)

            self.weights[index] = self.weights[index] + count
            self.moments_r[index] += count * red
            self.moments_g[index] += count * green
            self.moments_b[index] += count * blue
            self.moments[index] += count * (red * red + green * green + blue * blue)

    def _compute_moments(self) -> None:
        """
        Computes moments for the histogram.
        """
        for r in range(1, SIDE_LENGTH):
            area = [0] * SIDE_LENGTH
            area_r = [0] * SIDE_LENGTH
            area_g = [0] * SIDE_LENGTH
            area_b = [0] * SIDE_LENGTH
            area2 = [0.0] * SIDE_LENGTH
            
            for g in range(1, SIDE_LENGTH):
                line = 0
                line_r = 0
                line_g = 0
                line_b = 0
                line2 = 0.0
                
                for b in range(1, SIDE_LENGTH):
                    index = self._get_index(r, g, b)
                    line += self.weights[index]
                    line_r += self.moments_r[index]
                    line_g += self.moments_g[index]
                    line_b += self.moments_b[index]
                    line2 += self.moments[index]

                    area[b] += line
                    area_r[b] += line_r
                    area_g[b] += line_g
                    area_b[b] += line_b
                    area2[b] += line2

                    previous_index = self._get_index(r - 1, g, b)
                    self.weights[index] = self.weights[previous_index] + area[b]
                    self.moments_r[index] = self.moments_r[previous_index] + area_r[b]
                    self.moments_g[index] = self.moments_g[previous_index] + area_g[b]
                    self.moments_b[index] = self.moments_b[previous_index] + area_b[b]
                    self.moments[index] = self.moments[previous_index] + area2[b]

    def _create_boxes(self, max_colors: int) -> CreateBoxesResult:
        """
        Creates boxes for the quantization process.
        """
        self.cubes = [Box() for _ in range(max_colors)]
        volume_variance = [0.0] * max_colors
        
        self.cubes[0].r0 = 0
        self.cubes[0].g0 = 0
        self.cubes[0].b0 = 0

        self.cubes[0].r1 = SIDE_LENGTH - 1
        self.cubes[0].g1 = SIDE_LENGTH - 1
        self.cubes[0].b1 = SIDE_LENGTH - 1

        generated_color_count = max_colors
        next_index = 0
        
        i = 1
        while i < max_colors:
            # Try to cut cube[next_index], result in cube[i]
            if self._cut(self.cubes[next_index], self.cubes[i]):
                # Success, calculate the variance of the two new cubes
                volume_variance[next_index] = (
                    self._variance(self.cubes[next_index])
                    if self.cubes[next_index].vol > 1 else 0.0
                )
                volume_variance[i] = (
                    self._variance(self.cubes[i])
                    if self.cubes[i].vol > 1 else 0.0
                )
                increment_i = True
            else:
                # Failed, reset the variance of the cube, and do not move the index to try again
                volume_variance[next_index] = 0.0
                increment_i = False

            # Select the cube with the largest variance from all the cubes created (0 to i) as the next cutting target
            next_index = 0
            temp = volume_variance[0]
            for j in range(1, i + 1):
                if volume_variance[j] > temp:
                    temp = volume_variance[j]
                    next_index = j

            # If no further cutting is possible, record the actual number of colors generated and exit
            if temp <= 0.0:
                generated_color_count = i + 1
                break

            # Only move to the next i when the cutting is successful
            if increment_i:
                i += 1
                
        return CreateBoxesResult(max_colors, generated_color_count)

    def _create_result(self, color_count: int) -> List[int]:
        """
        Creates the final result colors from the boxes.
        """
        colors = []
        for i in range(color_count):
            cube = self.cubes[i]
            weight = self._volume(cube, self.weights)
            if weight > 0:
                r = round(self._volume(cube, self.moments_r) / weight)
                g = round(self._volume(cube, self.moments_g) / weight)
                b = round(self._volume(cube, self.moments_b) / weight)
                color = (255 << 24) | ((r & 0x0ff) << 16) | ((g & 0x0ff) << 8) | (b & 0x0ff)
                colors.append(color)
        return colors

    def _variance(self, cube: Box) -> float:
        """
        Calculates the variance for a box.
        """
        dr = self._volume(cube, self.moments_r)
        dg = self._volume(cube, self.moments_g)
        db = self._volume(cube, self.moments_b)
        xx = (
            self.moments[self._get_index(cube.r1, cube.g1, cube.b1)]
            - self.moments[self._get_index(cube.r1, cube.g1, cube.b0)]
            - self.moments[self._get_index(cube.r1, cube.g0, cube.b1)]
            + self.moments[self._get_index(cube.r1, cube.g0, cube.b0)]
            - self.moments[self._get_index(cube.r0, cube.g1, cube.b1)]
            + self.moments[self._get_index(cube.r0, cube.g1, cube.b0)]
            + self.moments[self._get_index(cube.r0, cube.g0, cube.b1)]
            - self.moments[self._get_index(cube.r0, cube.g0, cube.b0)]
        )
        hypotenuse = dr * dr + dg * dg + db * db
        volume = self._volume(cube, self.weights)
        return xx - hypotenuse / volume

    def _cut(self, one: Box, two: Box) -> bool:
        """
        Cuts a box in two.
        """
        whole_r = self._volume(one, self.moments_r)
        whole_g = self._volume(one, self.moments_g)
        whole_b = self._volume(one, self.moments_b)
        whole_w = self._volume(one, self.weights)

        max_r_result = self._maximize(
            one, Direction.RED, one.r0 + 1, one.r1, whole_r, whole_g, whole_b, whole_w
        )
        max_g_result = self._maximize(
            one, Direction.GREEN, one.g0 + 1, one.g1, whole_r, whole_g, whole_b, whole_w
        )
        max_b_result = self._maximize(
            one, Direction.BLUE, one.b0 + 1, one.b1, whole_r, whole_g, whole_b, whole_w
        )

        max_r = max_r_result.maximum
        max_g = max_g_result.maximum
        max_b = max_b_result.maximum

        if max_r >= max_g and max_r >= max_b:
            if max_r_result.cut_location < 0:
                return False
            direction = Direction.RED
        elif max_g >= max_r and max_g >= max_b:
            direction = Direction.GREEN
        else:
            direction = Direction.BLUE

        two.r1 = one.r1
        two.g1 = one.g1
        two.b1 = one.b1

        if direction == Direction.RED:
            one.r1 = max_r_result.cut_location
            two.r0 = one.r1
            two.g0 = one.g0
            two.b0 = one.b0
        elif direction == Direction.GREEN:
            one.g1 = max_g_result.cut_location
            two.r0 = one.r0
            two.g0 = one.g1
            two.b0 = one.b0
        elif direction == Direction.BLUE:
            one.b1 = max_b_result.cut_location
            two.r0 = one.r0
            two.g0 = one.g0
            two.b0 = one.b1
        else:
            raise ValueError(f"unexpected direction {direction}")

        one.vol = (one.r1 - one.r0) * (one.g1 - one.g0) * (one.b1 - one.b0)
        two.vol = (two.r1 - two.r0) * (two.g1 - two.g0) * (two.b1 - two.b0)
        return True

    def _maximize(
        self,
        cube: Box,
        direction: str,
        first: int,
        last: int,
        whole_r: int,
        whole_g: int,
        whole_b: int,
        whole_w: int,
    ) -> MaximizeResult:
        """
        Finds where to cut a box to maximize variance.
        """
        bottom_r = self._bottom(cube, direction, self.moments_r)
        bottom_g = self._bottom(cube, direction, self.moments_g)
        bottom_b = self._bottom(cube, direction, self.moments_b)
        bottom_w = self._bottom(cube, direction, self.weights)

        max_val = 0.0
        cut = -1

        half_r = 0
        half_g = 0
        half_b = 0
        half_w = 0
        
        for i in range(first, last):
            half_r = bottom_r + self._top(cube, direction, i, self.moments_r)
            half_g = bottom_g + self._top(cube, direction, i, self.moments_g)
            half_b = bottom_b + self._top(cube, direction, i, self.moments_b)
            half_w = bottom_w + self._top(cube, direction, i, self.weights)
            
            if half_w == 0:
                continue

            temp_numerator = (half_r * half_r + half_g * half_g + half_b * half_b) * 1.0
            temp_denominator = half_w * 1.0
            temp = temp_numerator / temp_denominator

            half_r = whole_r - half_r
            half_g = whole_g - half_g
            half_b = whole_b - half_b
            half_w = whole_w - half_w
            
            if half_w == 0:
                continue

            temp_numerator = (half_r * half_r + half_g * half_g + half_b * half_b) * 1.0
            temp_denominator = half_w * 1.0
            temp += temp_numerator / temp_denominator

            if temp > max_val:
                max_val = temp
                cut = i
                
        return MaximizeResult(cut, max_val)

    def _volume(self, cube: Box, moment: List[float]) -> float:
        """
        Calculates the volume of a box.
        """
        return (
            moment[self._get_index(cube.r1, cube.g1, cube.b1)]
            - moment[self._get_index(cube.r1, cube.g1, cube.b0)]
            - moment[self._get_index(cube.r1, cube.g0, cube.b1)]
            + moment[self._get_index(cube.r1, cube.g0, cube.b0)]
            - moment[self._get_index(cube.r0, cube.g1, cube.b1)]
            + moment[self._get_index(cube.r0, cube.g1, cube.b0)]
            + moment[self._get_index(cube.r0, cube.g0, cube.b1)]
            - moment[self._get_index(cube.r0, cube.g0, cube.b0)]
        )

    def _bottom(self, cube: Box, direction: str, moment: List[float]) -> float:
        """
        Calculates the bottom of a box.
        """
        if direction == Direction.RED:
            return (
                -moment[self._get_index(cube.r0, cube.g1, cube.b1)]
                + moment[self._get_index(cube.r0, cube.g1, cube.b0)]
                + moment[self._get_index(cube.r0, cube.g0, cube.b1)]
                - moment[self._get_index(cube.r0, cube.g0, cube.b0)]
            )
        elif direction == Direction.GREEN:
            return (
                -moment[self._get_index(cube.r1, cube.g0, cube.b1)]
                + moment[self._get_index(cube.r1, cube.g0, cube.b0)]
                + moment[self._get_index(cube.r0, cube.g0, cube.b1)]
                - moment[self._get_index(cube.r0, cube.g0, cube.b0)]
            )
        elif direction == Direction.BLUE:
            return (
                -moment[self._get_index(cube.r1, cube.g1, cube.b0)]
                + moment[self._get_index(cube.r1, cube.g0, cube.b0)]
                + moment[self._get_index(cube.r0, cube.g1, cube.b0)]
                - moment[self._get_index(cube.r0, cube.g0, cube.b0)]
            )
        else:
            raise ValueError(f"unexpected direction {direction}")

    def _top(self, cube: Box, direction: str, position: int, moment: List[float]) -> float:
        """
        Calculates the top of a box.
        """
        if direction == Direction.RED:
            return (
                moment[self._get_index(position, cube.g1, cube.b1)]
                - moment[self._get_index(position, cube.g1, cube.b0)]
                - moment[self._get_index(position, cube.g0, cube.b1)]
                + moment[self._get_index(position, cube.g0, cube.b0)]
            )
        elif direction == Direction.GREEN:
            return (
                moment[self._get_index(cube.r1, position, cube.b1)]
                - moment[self._get_index(cube.r1, position, cube.b0)]
                - moment[self._get_index(cube.r0, position, cube.b1)]
                + moment[self._get_index(cube.r0, position, cube.b0)]
            )
        elif direction == Direction.BLUE:
            return (
                moment[self._get_index(cube.r1, cube.g1, position)]
                - moment[self._get_index(cube.r1, cube.g0, position)]
                - moment[self._get_index(cube.r0, cube.g1, position)]
                + moment[self._get_index(cube.r0, cube.g0, position)]
            )
        else:
            raise ValueError(f"unexpected direction {direction}")

    def _get_index(self, r: int, g: int, b: int) -> int:
        """
        Gets the index for a given r,g,b coordinate.
        """
        return (r << (INDEX_BITS * 2)) + (r << (INDEX_BITS + 1)) + r + (g << INDEX_BITS) + g + b
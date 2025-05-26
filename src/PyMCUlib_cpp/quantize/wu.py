# wu.py

from enum import Enum, auto
from typing import List, Tuple
from PyMCUlib_cpp.utils.utils import Argb, argb_from_rgb

# Constants
INDEX_BITS = 5
INDEX_COUNT = (1 << INDEX_BITS) + 1
TOTAL_SIZE = INDEX_COUNT * INDEX_COUNT * INDEX_COUNT
MAX_COLORS = 256

class Direction(Enum):
    """Direction enum for cutting boxes."""
    RED = auto()
    GREEN = auto()
    BLUE = auto()

class Box:
    """Represents a box (cube) in RGB color space."""
    def __init__(self):
        self.r0 = 0
        self.r1 = 0
        self.g0 = 0
        self.g1 = 0
        self.b0 = 0
        self.b1 = 0
        self.vol = 0

def _get_index(r: int, g: int, b: int) -> int:
    """
    Compute an index for a color in a 3D histogram.
    
    Args:
        r: Red component index.
        g: Green component index.
        b: Blue component index.
        
    Returns:
        An index in the 3D histogram.
    """
    return (r << (INDEX_BITS * 2)) + (r << (INDEX_BITS + 1)) + (g << INDEX_BITS) + r + g + b

def _construct_histogram(pixels: List[Argb], weights: List[int], m_r: List[int], 
                        m_g: List[int], m_b: List[int], moments: List[float]) -> None:
    """
    Construct a 3D histogram from a list of pixels.
    
    Args:
        pixels: List of pixels in ARGB format.
        weights: List to store the weight (frequency) of each color.
        m_r: List to store the red moment of each color.
        m_g: List to store the green moment of each color.
        m_b: List to store the blue moment of each color.
        moments: List to store the combined moments of each color.
    """
    for pixel in pixels:
        red = (pixel & 0x00ff0000) >> 16
        green = (pixel & 0x0000ff00) >> 8
        blue = (pixel & 0x000000ff)
        
        bits_to_remove = 8 - INDEX_BITS
        index_r = (red >> bits_to_remove) + 1
        index_g = (green >> bits_to_remove) + 1
        index_b = (blue >> bits_to_remove) + 1
        index = _get_index(index_r, index_g, index_b)
        
        weights[index] += 1
        m_r[index] += red
        m_g[index] += green
        m_b[index] += blue
        moments[index] += (red * red) + (green * green) + (blue * blue)

def _compute_moments(weights: List[int], m_r: List[int], m_g: List[int], 
                    m_b: List[int], moments: List[float]) -> None:
    """
    Compute statistical moments for a 3D histogram.
    
    Args:
        weights: List containing the weight (frequency) of each color.
        m_r: List containing the red moment of each color.
        m_g: List containing the green moment of each color.
        m_b: List containing the blue moment of each color.
        moments: List containing the combined moments of each color.
    """
    for r in range(1, INDEX_COUNT):
        area = [0] * INDEX_COUNT
        area_r = [0] * INDEX_COUNT
        area_g = [0] * INDEX_COUNT
        area_b = [0] * INDEX_COUNT
        area_2 = [0.0] * INDEX_COUNT
        
        for g in range(1, INDEX_COUNT):
            line = 0
            line_r = 0
            line_g = 0
            line_b = 0
            line_2 = 0.0
            
            for b in range(1, INDEX_COUNT):
                index = _get_index(r, g, b)
                line += weights[index]
                line_r += m_r[index]
                line_g += m_g[index]
                line_b += m_b[index]
                line_2 += moments[index]
                
                area[b] += line
                area_r[b] += line_r
                area_g[b] += line_g
                area_b[b] += line_b
                area_2[b] += line_2
                
                previous_index = _get_index(r - 1, g, b)
                
                weights[index] = weights[previous_index] + area[b]
                m_r[index] = m_r[previous_index] + area_r[b]
                m_g[index] = m_g[previous_index] + area_g[b]
                m_b[index] = m_b[previous_index] + area_b[b]
                moments[index] = moments[previous_index] + area_2[b]

def _top(cube: Box, direction: Direction, position: int, moment: List[int]) -> int:
    """
    Compute the top statistical moment for a box.
    
    Args:
        cube: The box to compute the moment for.
        direction: The direction to compute the moment (RED, GREEN, or BLUE).
        position: The position to compute the moment at.
        moment: The statistical moment.
        
    Returns:
        The top statistical moment for the box.
    """
    if direction == Direction.RED:
        return (moment[_get_index(position, cube.g1, cube.b1)] -
                moment[_get_index(position, cube.g1, cube.b0)] -
                moment[_get_index(position, cube.g0, cube.b1)] +
                moment[_get_index(position, cube.g0, cube.b0)])
    elif direction == Direction.GREEN:
        return (moment[_get_index(cube.r1, position, cube.b1)] -
                moment[_get_index(cube.r1, position, cube.b0)] -
                moment[_get_index(cube.r0, position, cube.b1)] +
                moment[_get_index(cube.r0, position, cube.b0)])
    else:  # direction == Direction.BLUE
        return (moment[_get_index(cube.r1, cube.g1, position)] -
                moment[_get_index(cube.r1, cube.g0, position)] -
                moment[_get_index(cube.r0, cube.g1, position)] +
                moment[_get_index(cube.r0, cube.g0, position)])

def _bottom(cube: Box, direction: Direction, moment: List[int]) -> int:
    """
    Compute the bottom statistical moment for a box.
    
    Args:
        cube: The box to compute the moment for.
        direction: The direction to compute the moment (RED, GREEN, or BLUE).
        moment: The statistical moment.
        
    Returns:
        The bottom statistical moment for the box.
    """
    if direction == Direction.RED:
        return (-moment[_get_index(cube.r0, cube.g1, cube.b1)] +
                moment[_get_index(cube.r0, cube.g1, cube.b0)] +
                moment[_get_index(cube.r0, cube.g0, cube.b1)] -
                moment[_get_index(cube.r0, cube.g0, cube.b0)])
    elif direction == Direction.GREEN:
        return (-moment[_get_index(cube.r1, cube.g0, cube.b1)] +
                moment[_get_index(cube.r1, cube.g0, cube.b0)] +
                moment[_get_index(cube.r0, cube.g0, cube.b1)] -
                moment[_get_index(cube.r0, cube.g0, cube.b0)])
    else:  # direction == Direction.BLUE
        return (-moment[_get_index(cube.r1, cube.g1, cube.b0)] +
                moment[_get_index(cube.r1, cube.g0, cube.b0)] +
                moment[_get_index(cube.r0, cube.g1, cube.b0)] -
                moment[_get_index(cube.r0, cube.g0, cube.b0)])

def _vol(cube: Box, moment: List[int]) -> int:
    """
    Compute the volume (weighted count) of a box.
    
    Args:
        cube: The box to compute the volume for.
        moment: The statistical moment.
        
    Returns:
        The volume of the box.
    """
    return (moment[_get_index(cube.r1, cube.g1, cube.b1)] -
            moment[_get_index(cube.r1, cube.g1, cube.b0)] -
            moment[_get_index(cube.r1, cube.g0, cube.b1)] +
            moment[_get_index(cube.r1, cube.g0, cube.b0)] -
            moment[_get_index(cube.r0, cube.g1, cube.b1)] +
            moment[_get_index(cube.r0, cube.g1, cube.b0)] +
            moment[_get_index(cube.r0, cube.g0, cube.b1)] -
            moment[_get_index(cube.r0, cube.g0, cube.b0)])

def _variance(cube: Box, weights: List[int], m_r: List[int], m_g: List[int], 
             m_b: List[int], moments: List[float]) -> float:
    """
    Compute the variance of the colors in a box.
    
    Args:
        cube: The box to compute the variance for.
        weights: The weight (frequency) of each color.
        m_r: The red moment of each color.
        m_g: The green moment of each color.
        m_b: The blue moment of each color.
        moments: The combined moments of each color.
        
    Returns:
        The variance of the colors in the box.
    """
    dr = _vol(cube, m_r)
    dg = _vol(cube, m_g)
    db = _vol(cube, m_b)
    xx = (moments[_get_index(cube.r1, cube.g1, cube.b1)] -
          moments[_get_index(cube.r1, cube.g1, cube.b0)] -
          moments[_get_index(cube.r1, cube.g0, cube.b1)] +
          moments[_get_index(cube.r1, cube.g0, cube.b0)] -
          moments[_get_index(cube.r0, cube.g1, cube.b1)] +
          moments[_get_index(cube.r0, cube.g1, cube.b0)] +
          moments[_get_index(cube.r0, cube.g0, cube.b1)] -
          moments[_get_index(cube.r0, cube.g0, cube.b0)])
    hypotenuse = dr * dr + dg * dg + db * db
    volume = _vol(cube, weights)
    return xx - hypotenuse / volume if volume > 0 else 0

def _maximize(cube: Box, direction: Direction, first: int, last: int, whole_w: int, 
             whole_r: int, whole_g: int, whole_b: int, weights: List[int], 
             m_r: List[int], m_g: List[int], m_b: List[int]) -> Tuple[float, int]:
    """
    Find the best place to cut a box into two boxes.
    
    Args:
        cube: The box to cut.
        direction: The direction to cut the box (RED, GREEN, or BLUE).
        first: The first position to consider for the cut.
        last: The last position to consider for the cut.
        whole_w: The total weight of the box.
        whole_r: The total red moment of the box.
        whole_g: The total green moment of the box.
        whole_b: The total blue moment of the box.
        weights: The weight (frequency) of each color.
        m_r: The red moment of each color.
        m_g: The green moment of each color.
        m_b: The blue moment of each color.
        
    Returns:
        A tuple containing the maximum variance improvement and the position to cut.
    """
    bottom_r = _bottom(cube, direction, m_r)
    bottom_g = _bottom(cube, direction, m_g)
    bottom_b = _bottom(cube, direction, m_b)
    bottom_w = _bottom(cube, direction, weights)
    
    max_val = 0.0
    cut = -1
    
    for i in range(first, last):
        half_r = bottom_r + _top(cube, direction, i, m_r)
        half_g = bottom_g + _top(cube, direction, i, m_g)
        half_b = bottom_b + _top(cube, direction, i, m_b)
        half_w = bottom_w + _top(cube, direction, i, weights)
        
        if half_w == 0:
            continue
            
        temp = (float(half_r) * half_r + float(half_g) * half_g + float(half_b) * half_b) / float(half_w)
        
        half_r = whole_r - half_r
        half_g = whole_g - half_g
        half_b = whole_b - half_b
        half_w = whole_w - half_w
        
        if half_w == 0:
            continue
            
        temp += (float(half_r) * half_r + float(half_g) * half_g + float(half_b) * half_b) / float(half_w)
        
        if temp > max_val:
            max_val = temp
            cut = i
            
    return max_val, cut

def _cut(box1: Box, box2: Box, weights: List[int], m_r: List[int], 
        m_g: List[int], m_b: List[int]) -> bool:
    """
    Cut a box into two boxes.
    
    Args:
        box1: The first box (will be modified to represent one half of the cut).
        box2: The second box (will be set to represent the other half of the cut).
        weights: The weight (frequency) of each color.
        m_r: The red moment of each color.
        m_g: The green moment of each color.
        m_b: The blue moment of each color.
        
    Returns:
        True if the box was successfully cut, False otherwise.
    """
    whole_r = _vol(box1, m_r)
    whole_g = _vol(box1, m_g)
    whole_b = _vol(box1, m_b)
    whole_w = _vol(box1, weights)
    
    max_r, cut_r = _maximize(box1, Direction.RED, box1.r0 + 1, box1.r1, whole_w, 
                             whole_r, whole_g, whole_b, weights, m_r, m_g, m_b)
    max_g, cut_g = _maximize(box1, Direction.GREEN, box1.g0 + 1, box1.g1, whole_w, 
                             whole_r, whole_g, whole_b, weights, m_r, m_g, m_b)
    max_b, cut_b = _maximize(box1, Direction.BLUE, box1.b0 + 1, box1.b1, whole_w, 
                             whole_r, whole_g, whole_b, weights, m_r, m_g, m_b)
    
    if max_r >= max_g and max_r >= max_b:
        direction = Direction.RED
        if cut_r < 0:
            return False
    elif max_g >= max_r and max_g >= max_b:
        direction = Direction.GREEN
    else:
        direction = Direction.BLUE
        
    box2.r1 = box1.r1
    box2.g1 = box1.g1
    box2.b1 = box1.b1
    
    if direction == Direction.RED:
        box2.r0 = box1.r1 = cut_r
        box2.g0 = box1.g0
        box2.b0 = box1.b0
    elif direction == Direction.GREEN:
        box2.r0 = box1.r0
        box2.g0 = box1.g1 = cut_g
        box2.b0 = box1.b0
    else:  # direction == Direction.BLUE
        box2.r0 = box1.r0
        box2.g0 = box1.g0
        box2.b0 = box1.b1 = cut_b
        
    box1.vol = (box1.r1 - box1.r0) * (box1.g1 - box1.g0) * (box1.b1 - box1.b0)
    box2.vol = (box2.r1 - box2.r0) * (box2.g1 - box2.g0) * (box2.b1 - box2.b0)
    
    return True

def quantize_wu(pixels: List[Argb], max_colors: int) -> List[Argb]:
    """
    Quantize colors using Wu's algorithm.
    
    Args:
        pixels: A list of pixels in ARGB format.
        max_colors: The maximum number of colors to return.
        
    Returns:
        A list of quantized colors in ARGB format.
    """
    if max_colors <= 0 or max_colors > 256 or not pixels:
        return []
        
    weights = [0] * TOTAL_SIZE
    moments_red = [0] * TOTAL_SIZE
    moments_green = [0] * TOTAL_SIZE
    moments_blue = [0] * TOTAL_SIZE
    moments = [0.0] * TOTAL_SIZE
    
    _construct_histogram(pixels, weights, moments_red, moments_green, moments_blue, moments)
    _compute_moments(weights, moments_red, moments_green, moments_blue, moments)
    
    cubes = [Box() for _ in range(MAX_COLORS)]
    cubes[0].r0 = cubes[0].g0 = cubes[0].b0 = 0
    cubes[0].r1 = cubes[0].g1 = cubes[0].b1 = INDEX_COUNT - 1
    
    volume_variance = [0.0] * MAX_COLORS
    next_cube = 0
    
    for i in range(1, max_colors):
        if _cut(cubes[next_cube], cubes[i], weights, moments_red, moments_green, moments_blue):
            volume_variance[next_cube] = (
                _variance(cubes[next_cube], weights, moments_red, moments_green, moments_blue, moments) 
                if cubes[next_cube].vol > 1 else 0.0
            )
            volume_variance[i] = (
                _variance(cubes[i], weights, moments_red, moments_green, moments_blue, moments) 
                if cubes[i].vol > 1 else 0.0
            )
        else:
            volume_variance[next_cube] = 0.0
            i -= 1
            
        next_cube = 0
        temp = volume_variance[0]
        for j in range(1, i + 1):
            if volume_variance[j] > temp:
                temp = volume_variance[j]
                next_cube = j
                
        if temp <= 0.0:
            max_colors = i + 1
            break
            
    out_colors = []
    for i in range(max_colors):
        weight = _vol(cubes[i], weights)
        if weight > 0:
            red = _vol(cubes[i], moments_red) // weight
            green = _vol(cubes[i], moments_green) // weight
            blue = _vol(cubes[i], moments_blue) // weight
            argb = argb_from_rgb(red, green, blue)
            out_colors.append(argb)
            
    return out_colors
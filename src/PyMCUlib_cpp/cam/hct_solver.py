# hct_solver.py

import math
from typing import Tuple
from PyMCUlib_cpp.utils.utils import (
    Argb, Vec3, PI, y_from_lstar,
    signum, matrix_multiply, argb_from_linrgb
)
from PyMCUlib_cpp.cam.viewing_conditions import DEFAULT_VIEWING_CONDITIONS

# Constants
SCALED_DISCOUNT_FROM_LINRGB = [
    [0.001200833568784504, 0.002389694492170889, 0.0002795742885861124],
    [0.0005891086651375999, 0.0029785502573438758, 0.0003270666104008398],
    [0.00010146692491640572, 0.0005364214359186694, 0.0032979401770712076]
]

LINRGB_FROM_SCALED_DISCOUNT = [
    [1373.2198709594231, -1100.4251190754821, -7.278681089101213],
    [-271.815969077903, 559.6580465940733, -32.46047482791194],
    [1.9622899599665666, -57.173814538844006, 308.7233197812385]
]

Y_FROM_LINRGB = [0.2126, 0.7152, 0.0722]

CRITICAL_PLANES = [
    0.015176349177441876, 0.045529047532325624, 0.07588174588720938,
    0.10623444424209313, 0.13658714259697685, 0.16693984095186062,
    0.19729253930674434, 0.2276452376616281, 0.2579979360165119,
    0.28835063437139563, 0.3188300904430532, 0.350925934958123,
    0.3848314933096426, 0.42057480301049466, 0.458183274052838,
    0.4976837250274023, 0.5391024159806381, 0.5824650784040898,
    0.6277969426914107, 0.6751227633498623, 0.7244668422128921,
    0.775853049866786, 0.829304845476233, 0.8848452951698498,
    0.942497089126609, 1.0022825574869039, 1.0642236851973577,
    1.1283421258858297, 1.1946592148522128, 1.2631959812511864,
    1.3339731595349034, 1.407011200216447, 1.4823302800086415,
    1.5599503113873272, 1.6398909516233677, 1.7221716113234105,
    1.8068114625156377, 1.8938294463134073, 1.9832442801866852,
    2.075074464868551, 2.1693382909216234, 2.2660538449872063,
    2.36523901573795, 2.4669114995532007, 2.5710888059345764,
    2.6777882626779785, 2.7870270208169257, 2.898822059350997,
    3.0131901897720907, 3.1301480604002863, 3.2497121605402226,
    3.3718988244681087, 3.4967242352587946, 3.624204428461639,
    3.754355295633311, 3.887192587735158, 4.022731918402185,
    4.160988767090289, 4.301978482107941, 4.445716283538092,
    4.592217266055746, 4.741496401646282, 4.893568542229298,
    5.048448422192488, 5.20615066083972, 5.3666897647573375,
    5.5300801301023865, 5.696336044816294, 5.865471690767354,
    6.037501145825082, 6.212438385869475, 6.390297286737924,
    6.571091626112461, 6.7548350853498045, 6.941541251256611,
    7.131223617812143, 7.323895587840543, 7.5195704746346665,
    7.7182615035334345, 7.919981813454504, 8.124744458384042,
    8.332562408825165, 8.543448553206703, 8.757415699253682,
    8.974476575321063, 9.194643831691977, 9.417930041841839,
    9.644347703669503, 9.873909240696694, 10.106627003236781,
    10.342513269534024, 10.58158024687427, 10.8238400726681,
    11.069304815507364, 11.317986476196008, 11.569896988756009,
    11.825048221409341, 12.083451977536606, 12.345119996613247,
    12.610063955123938, 12.878295467455942, 13.149826086772048,
    13.42466730586372, 13.702830557985108, 13.984327217668513,
    14.269168601521828, 14.55736596900856, 14.848930523210871,
    15.143873411576273, 15.44220572664832, 15.743938506781891,
    16.04908273684337, 16.35764934889634, 16.66964922287304,
    16.985093187232053, 17.30399201960269, 17.62635644741625,
    17.95219714852476, 18.281524751807332, 18.614349837764564,
    18.95068293910138, 19.290534541298456, 19.633915083172692,
    19.98083495742689, 20.331304511189067, 20.685334046541502,
    21.042933821039977, 21.404114048223256, 21.76888489811322,
    22.137256497705877, 22.50923893145328, 22.884842241736916,
    23.264076429332462, 23.6469514538663, 24.033477234264016,
    24.42366364919083, 24.817520537484558, 25.21505769858089,
    25.61628489293138, 26.021211842414342, 26.429848230738664,
    26.842203703840827, 27.258287870275353, 27.678110301598522,
    28.10168053274597, 28.529008062403893, 28.96010235337422,
    29.39497283293396, 29.83362889318845, 30.276079891419332,
    30.722335150426627, 31.172403958865512, 31.62629557157785,
    32.08401920991837, 32.54558406207592, 33.010999283389665,
    33.4802739966603, 33.953417292456834, 34.430438229418264,
    34.911345834551085, 35.39614910352207, 35.88485700094671,
    36.37747846067349, 36.87402238606382, 37.37449765026789,
    37.87891309649659, 38.38727753828926, 38.89959975977785,
    39.41588851594697, 39.93615253289054, 40.460400508064545,
    40.98864111053629, 41.520882981230194, 42.05713473317016,
    42.597404951718396, 43.141702194811224, 43.6900349931913,
    44.24241185063697, 44.798841244188324, 45.35933162437017,
    45.92389141541209, 46.49252901546552, 47.065252796817916,
    47.64207110610409, 48.22299226451468, 48.808024568002054,
    49.3971762874833, 49.9904556690408, 50.587870934119984,
    51.189430279724725, 51.79514187861014, 52.40501387947288,
    53.0190544071392, 53.637271562750364, 54.259673423945976,
    54.88626804504493, 55.517063457223934, 56.15206766869424,
    56.79128866487574, 57.43473440856916, 58.08241284012621,
    58.734331877617365, 59.39049941699807, 60.05092333227251,
    60.715611475655585, 61.38457167773311, 62.057811747619894,
    62.7353394731159, 63.417162620860914, 64.10328893648692,
    64.79372614476921, 65.48848194977529, 66.18756403501224,
    66.89098006357258, 67.59873767827808, 68.31084450182222,
    69.02730813691093, 69.74813616640164, 70.47333615344107,
    71.20291564160104, 71.93688215501312, 72.67524319850172,
    73.41800625771542, 74.16517879925733, 74.9167682708136,
    75.67278210128072, 76.43322770089146, 77.1981124613393,
    77.96744375590167, 78.74122893956174, 79.51947534912904,
    80.30219030335869, 81.08938110306934, 81.88105503125999,
    82.67721935322541, 83.4778813166706, 84.28304815182372,
    85.09272707154808, 85.90692527145302, 86.72564993000343,
    87.54890820862819, 88.3767072518277, 89.2090541872801,
    90.04595612594655, 90.88742016217518, 91.73345337380438,
    92.58406282226491, 93.43925555268066, 94.29903859396902,
    95.16341895893969, 96.03240364439274, 96.9059996312159,
    97.78421388448044, 98.6670533535366, 99.55452497210776
]

def sanitize_radians(angle: float) -> float:
    """
    Sanitizes a small enough angle in radians.
    
    Args:
        angle: An angle in radians; must not deviate too much from 0.
        
    Returns:
        A coterminal angle between 0 and 2pi.
    """
    return math.fmod(angle + PI * 8, PI * 2)

def true_delinearized(rgb_component: float) -> float:
    """
    Delinearizes an RGB component, returning a floating-point number.
    
    Args:
        rgb_component: 0.0 <= rgb_component <= 100.0, represents linear R/G/B channel
        
    Returns:
        0.0 <= output <= 255.0, color channel converted to regular RGB space
    """
    normalized = rgb_component / 100.0
    if normalized <= 0.0031308:
        delinearized_value = normalized * 12.92
    else:
        delinearized_value = 1.055 * pow(normalized, 1.0 / 2.4) - 0.055
    return delinearized_value * 255.0

def chromatic_adaptation(component: float) -> float:
    """
    Chromatic adaptation function.
    """
    af = pow(abs(component), 0.42)
    return signum(component) * 400.0 * af / (af + 27.13)

def hue_of(linrgb: Vec3) -> float:
    """
    Returns the hue of a linear RGB color in CAM16.
    
    Args:
        linrgb: The linear RGB coordinates of a color.
        
    Returns:
        The hue of the color in CAM16, in radians.
    """
    scaled_discount = matrix_multiply(linrgb, SCALED_DISCOUNT_FROM_LINRGB)
    r_a = chromatic_adaptation(scaled_discount.a)
    g_a = chromatic_adaptation(scaled_discount.b)
    b_a = chromatic_adaptation(scaled_discount.c)
    # redness-greenness
    a = (11.0 * r_a + -12.0 * g_a + b_a) / 11.0
    # yellowness-blueness
    b = (r_a + g_a - 2.0 * b_a) / 9.0
    return math.atan2(b, a)

def are_in_cyclic_order(a: float, b: float, c: float) -> bool:
    """
    Determines if three angles are in cyclic order.
    """
    delta_a_b = sanitize_radians(b - a)
    delta_a_c = sanitize_radians(c - a)
    return delta_a_b < delta_a_c

def intercept(source: float, mid: float, target: float) -> float:
    """
    Solves the lerp equation.
    
    Args:
        source: The starting number.
        mid: The number in the middle.
        target: The ending number.
        
    Returns:
        A number t such that lerp(source, target, t) = mid.
    """
    return (mid - source) / (target - source)

def lerp_point(source: Vec3, t: float, target: Vec3) -> Vec3:
    """
    Linear interpolation between two points.
    """
    return Vec3(
        source.a + (target.a - source.a) * t,
        source.b + (target.b - source.b) * t,
        source.c + (target.c - source.c) * t
    )

def get_axis(vector: Vec3, axis: int) -> float:
    """
    Gets a specific axis value from a vector.
    """
    if axis == 0:
        return vector.a
    elif axis == 1:
        return vector.b
    elif axis == 2:
        return vector.c
    else:
        return -1.0

def set_coordinate(source: Vec3, coordinate: float, target: Vec3, axis: int) -> Vec3:
    """
    Intersects a segment with a plane.
    
    Args:
        source: The coordinates of point A.
        coordinate: The R-, G-, or B-coordinate of the plane.
        target: The coordinates of point B.
        axis: The axis the plane is perpendicular with. (0: R, 1: G, 2: B)
        
    Returns:
        The intersection point of the segment AB with the plane R=coordinate,
        G=coordinate, or B=coordinate
    """
    t = intercept(get_axis(source, axis), coordinate, get_axis(target, axis))
    return lerp_point(source, t, target)

def is_bounded(x: float) -> bool:
    """
    Determines if a value is within bounds.
    """
    return 0.0 <= x <= 100.0

def nth_vertex(y: float, n: int) -> Vec3:
    """
    Returns the nth possible vertex of the polygonal intersection.
    
    Args:
        y: The Y value of the plane.
        n: The zero-based index of the point. 0 <= n <= 11.
        
    Returns:
        The nth possible vertex of the polygonal intersection of the y plane
        and the RGB cube, in linear RGB coordinates, if it exists. If this possible
        vertex lies outside of the cube,
        [-1.0, -1.0, -1.0] is returned.
    """
    k_r = Y_FROM_LINRGB[0]
    k_g = Y_FROM_LINRGB[1]
    k_b = Y_FROM_LINRGB[2]
    coord_a = 0.0 if n % 4 <= 1 else 100.0
    coord_b = 0.0 if n % 2 == 0 else 100.0
    
    if n < 4:
        g = coord_a
        b = coord_b
        r = (y - g * k_g - b * k_b) / k_r
        if is_bounded(r):
            return Vec3(r, g, b)
        else:
            return Vec3(-1.0, -1.0, -1.0)
    elif n < 8:
        b = coord_a
        r = coord_b
        g = (y - r * k_r - b * k_b) / k_g
        if is_bounded(g):
            return Vec3(r, g, b)
        else:
            return Vec3(-1.0, -1.0, -1.0)
    else:
        r = coord_a
        g = coord_b
        b = (y - r * k_r - g * k_g) / k_b
        if is_bounded(b):
            return Vec3(r, g, b)
        else:
            return Vec3(-1.0, -1.0, -1.0)

def bisect_to_segment(y: float, target_hue: float) -> Tuple[Vec3, Vec3]:
    """
    Finds the segment containing the desired color.
    
    Args:
        y: The Y value of the color.
        target_hue: The hue of the color.
        
    Returns:
        A list of two sets of linear RGB coordinates, each corresponding to
        an endpoint of the segment containing the desired color.
    """
    left = Vec3(-1.0, -1.0, -1.0)
    right = left
    left_hue = 0.0
    right_hue = 0.0
    initialized = False
    uncut = True
    
    for n in range(12):
        mid = nth_vertex(y, n)
        if mid.a < 0:
            continue
            
        mid_hue = hue_of(mid)
        if not initialized:
            left = mid
            right = mid
            left_hue = mid_hue
            right_hue = mid_hue
            initialized = True
            continue
            
        if uncut or are_in_cyclic_order(left_hue, mid_hue, right_hue):
            uncut = False
            if are_in_cyclic_order(left_hue, target_hue, mid_hue):
                right = mid
                right_hue = mid_hue
            else:
                left = mid
                left_hue = mid_hue
    
    return left, right

def midpoint(a: Vec3, b: Vec3) -> Vec3:
    """
    Calculates the midpoint of two points.
    """
    return Vec3(
        (a.a + b.a) / 2,
        (a.b + b.b) / 2,
        (a.c + b.c) / 2
    )

def critical_plane_below(x: float) -> int:
    """
    Critical plane index below x.
    """
    return math.floor(x - 0.5)

def critical_plane_above(x: float) -> int:
    """
    Critical plane index above x.
    """
    return math.ceil(x - 0.5)

def bisect_to_limit(y: float, target_hue: float) -> Vec3:
    """
    Finds a color with the given Y and hue on the boundary of the cube.
    
    Args:
        y: The Y value of the color.
        target_hue: The hue of the color.
        
    Returns:
        The desired color, in linear RGB coordinates.
    """
    segment = bisect_to_segment(y, target_hue)
    left = segment[0]
    left_hue = hue_of(left)
    right = segment[1]
    
    for axis in range(3):
        if get_axis(left, axis) != get_axis(right, axis):
            l_plane = -1
            r_plane = 255
            
            if get_axis(left, axis) < get_axis(right, axis):
                l_plane = critical_plane_below(true_delinearized(get_axis(left, axis)))
                r_plane = critical_plane_above(true_delinearized(get_axis(right, axis)))
            else:
                l_plane = critical_plane_above(true_delinearized(get_axis(left, axis)))
                r_plane = critical_plane_below(true_delinearized(get_axis(right, axis)))
            
            for i in range(8):
                if abs(r_plane - l_plane) <= 1:
                    break
                else:
                    m_plane = math.floor((l_plane + r_plane) / 2.0)
                    mid_plane_coordinate = CRITICAL_PLANES[m_plane]
                    mid = set_coordinate(left, mid_plane_coordinate, right, axis)
                    mid_hue = hue_of(mid)
                    
                    if are_in_cyclic_order(left_hue, target_hue, mid_hue):
                        right = mid
                        r_plane = m_plane
                    else:
                        left = mid
                        left_hue = mid_hue
                        l_plane = m_plane
    
    return midpoint(left, right)

def inverse_chromatic_adaptation(adapted: float) -> float:
    """
    Inverse chromatic adaptation function.
    """
    adapted_abs = abs(adapted)
    base = max(0, 27.13 * adapted_abs / (400.0 - adapted_abs))
    return signum(adapted) * pow(base, 1.0 / 0.42)

def find_result_by_j(hue_radians: float, chroma: float, y: float) -> Argb:
    """
    Finds a color with the given hue, chroma, and Y.
    
    Args:
        hue_radians: The desired hue in radians.
        chroma: The desired chroma.
        y: The desired Y.
        
    Returns:
        The desired color as a hexadecimal integer, if found; 0 otherwise.
    """
    # Initial estimate of j.
    j = math.sqrt(y) * 11.0

    # Operations inlined from Cam16 to avoid repeated calculation
    # Using default viewing conditions referenced in the original C++ code
    viewing_conditions = DEFAULT_VIEWING_CONDITIONS
    t_inner_coeff = 1 / pow(1.64 - pow(0.29, viewing_conditions.background_y_to_white_point_y), 0.73)
    e_hue = 0.25 * (math.cos(hue_radians + 2.0) + 3.8)
    p1 = e_hue * (50000.0 / 13.0) * viewing_conditions.n_c * viewing_conditions.ncb
    h_sin = math.sin(hue_radians)
    h_cos = math.cos(hue_radians)
    
    for iteration_round in range(5):
        # Operations inlined from Cam16 to avoid repeated calculation
        j_normalized = j / 100.0
        alpha = 0.0 if chroma == 0.0 or j == 0.0 else chroma / math.sqrt(j_normalized)
        t = pow(alpha * t_inner_coeff, 1.0 / 0.9)
        ac = viewing_conditions.aw * pow(j_normalized, 1.0 / viewing_conditions.c / viewing_conditions.z)
        p2 = ac / viewing_conditions.nbb
        gamma = 23.0 * (p2 + 0.305) * t / (23.0 * p1 + 11 * t * h_cos + 108.0 * t * h_sin)
        a = gamma * h_cos
        b = gamma * h_sin
        r_a = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0
        g_a = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0
        b_a = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0
        r_c_scaled = inverse_chromatic_adaptation(r_a)
        g_c_scaled = inverse_chromatic_adaptation(g_a)
        b_c_scaled = inverse_chromatic_adaptation(b_a)
        scaled = Vec3(r_c_scaled, g_c_scaled, b_c_scaled)
        linrgb = matrix_multiply(scaled, LINRGB_FROM_SCALED_DISCOUNT)
        
        # Operations inlined from Cam16 to avoid repeated calculation
        if linrgb.a < 0 or linrgb.b < 0 or linrgb.c < 0:
            return 0
            
        k_r = Y_FROM_LINRGB[0]
        k_g = Y_FROM_LINRGB[1]
        k_b = Y_FROM_LINRGB[2]
        fnj = k_r * linrgb.a + k_g * linrgb.b + k_b * linrgb.c
        
        if fnj <= 0:
            return 0
            
        if iteration_round == 4 or abs(fnj - y) < 0.002:
            if linrgb.a > 100.01 or linrgb.b > 100.01 or linrgb.c > 100.01:
                return 0
                
            return argb_from_linrgb(linrgb)
            
        # Newton method iteration,
        # Using 2 * fn(j) / j as the approximation of fn'(j)
        j = j - (fnj - y) * j / (2 * fnj)
    
    return 0

def solve_to_int(hue_degrees: float, chroma: float, lstar: float) -> Argb:
    """
    Finds an sRGB color with the given hue, chroma, and L*, if possible.
    
    Args:
        hue_degrees: The desired hue, in degrees.
        chroma: The desired chroma.
        lstar: The desired L*.
        
    Returns:
        A hexadecimal representing the sRGB color. The color has sufficiently
        close hue, chroma, and L* to the desired values, if possible; otherwise,
        the hue and L* will be sufficiently close, and chroma will be maximized.
    """
    if chroma < 0.0001 or lstar < 0.0001 or lstar > 99.9999:
        from PyMCUlib_cpp.utils import int_from_lstar
        return int_from_lstar(lstar)
    
    from PyMCUlib_cpp.utils import sanitize_degrees_double
    hue_degrees = sanitize_degrees_double(hue_degrees)
    hue_radians = hue_degrees / 180 * PI
    y = y_from_lstar(lstar)
    exact_answer = find_result_by_j(hue_radians, chroma, y)
    
    if exact_answer != 0:
        return exact_answer
    
    linrgb = bisect_to_limit(y, hue_radians)
    return argb_from_linrgb(linrgb)

def solve_to_cam(hue_degrees: float, chroma: float, lstar: float):
    """
    Finds an sRGB color with the given hue, chroma, and L*, if possible.
    
    Args:
        hue_degrees: The desired hue, in degrees.
        chroma: The desired chroma.
        lstar: The desired L*.
        
    Returns:
        An CAM16 object representing the sRGB color. The color has
        sufficiently close hue, chroma, and L* to the desired values, if possible;
        otherwise, the hue and L* will be sufficiently close, and chroma will be
        maximized.
    """
    from PyMCUlib_cpp.cam.cam import cam_from_int
    return cam_from_int(solve_to_int(hue_degrees, chroma, lstar))
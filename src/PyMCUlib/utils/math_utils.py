# utils/math_utils.py

from typing import List


def signum(num: float) -> int:
    """
    The signum function.

    Args:
        num: The input number

    Returns:
        1 if num > 0, -1 if num < 0, and 0 if num = 0
    """
    if num < 0:
        return -1
    elif num == 0:
        return 0
    else:
        return 1


def lerp(start: float, stop: float, amount: float) -> float:
    """
    The linear interpolation function.

    Args:
        start: The start value
        stop: The end value
        amount: The interpolation factor (0.0 to 1.0)

    Returns:
        start if amount = 0 and stop if amount = 1
    """
    return (1.0 - amount) * start + amount * stop


def clamp_int(min_val: int, max_val: int, input_val: int) -> int:
    """
    Clamps an integer between two integers.

    Args:
        min_val: The lower bound
        max_val: The upper bound
        input_val: The input value

    Returns:
        input_val when min_val <= input_val <= max_val, and either min_val or max_val
        otherwise.
    """
    if input_val < min_val:
        return min_val
    elif input_val > max_val:
        return max_val

    return input_val


def clamp_double(min_val: float, max_val: float, input_val: float) -> float:
    """
    Clamps a floating-point number between two floating-point numbers.

    Args:
        min_val: The lower bound
        max_val: The upper bound
        input_val: The input value

    Returns:
        input_val when min_val <= input_val <= max_val, and either min_val or max_val
        otherwise.
    """
    if input_val < min_val:
        return min_val
    elif input_val > max_val:
        return max_val

    return input_val


def sanitize_degrees_int(degrees: int) -> int:
    """
    Sanitizes a degree measure as an integer.

    Args:
        degrees: The input angle in degrees

    Returns:
        A degree measure between 0 (inclusive) and 360 (exclusive).
    """
    degrees = degrees % 360
    if degrees < 0:
        degrees = degrees + 360
    return degrees


def sanitize_degrees_double(degrees: float) -> float:
    """
    Sanitizes a degree measure as a floating-point number.

    Args:
        degrees: The input angle in degrees

    Returns:
        A degree measure between 0.0 (inclusive) and 360.0 (exclusive).
    """
    degrees = degrees % 360.0
    if degrees < 0:
        degrees = degrees + 360.0
    return degrees


def rotation_direction(from_val: float, to_val: float) -> float:
    """
    Sign of direction change needed to travel from one angle to another.

    For angles that are 180 degrees apart from each other, both
    directions have the same travel distance, so either direction is
    shortest. The value 1.0 is returned in this case.

    Args:
        from_val: The angle travel starts from, in degrees.
        to_val: The angle travel ends at, in degrees.

    Returns:
        -1 if decreasing from_val leads to the shortest travel
        distance, 1 if increasing from_val leads to the shortest travel
        distance.
    """
    increasing_difference = sanitize_degrees_double(to_val - from_val)
    return 1.0 if increasing_difference <= 180.0 else -1.0


def difference_degrees(a: float, b: float) -> float:
    """
    Distance of two points on a circle, represented using degrees.

    Args:
        a: First angle in degrees
        b: Second angle in degrees

    Returns:
        The shortest angular distance between the two angles
    """
    return 180.0 - abs(abs(a - b) - 180.0)


def matrix_multiply(row: List[float], matrix: List[List[float]]) -> List[float]:
    """
    Multiplies a 1x3 row vector with a 3x3 matrix.

    Args:
        row: A 1x3 row vector
        matrix: A 3x3 matrix

    Returns:
        The resulting 1x3 row vector after multiplication
    """
    a = row[0] * matrix[0][0] + row[1] * matrix[0][1] + row[2] * matrix[0][2]
    b = row[0] * matrix[1][0] + row[1] * matrix[1][1] + row[2] * matrix[1][2]
    c = row[0] * matrix[2][0] + row[1] * matrix[2][1] + row[2] * matrix[2][2]
    return [a, b, c]
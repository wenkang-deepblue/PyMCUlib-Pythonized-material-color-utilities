# utils/string_utils.py

from PyMCUlib.utils import color_utils


def hex_from_argb(argb: int) -> str:
    """
    Converts an ARGB color to its hex string representation.
    
    Args:
        argb: ARGB representation of a color.
    
    Returns:
        Hex string representing color, ex. #ff0000 for red.
    """
    r = color_utils.red_from_argb(argb)
    g = color_utils.green_from_argb(argb)
    b = color_utils.blue_from_argb(argb)
    out_parts = [format(r, '02x'), format(g, '02x'), format(b, '02x')]
    
    return '#' + ''.join(out_parts)


def argb_from_hex(hex_str: str) -> int:
    """
    Converts a hex string to its ARGB representation.
    
    Args:
        hex_str: String representing color as hex code. Accepts strings with or
                without leading #, and string representing the color using 3, 6, or 8
                hex characters.
    
    Returns:
        ARGB representation of color.
    
    Raises:
        ValueError: If the hex string has an unexpected format.
    """
    hex_str = hex_str.replace('#', '')
    is_three = len(hex_str) == 3
    is_six = len(hex_str) == 6
    is_eight = len(hex_str) == 8
    
    if not is_three and not is_six and not is_eight:
        raise ValueError(f'unexpected hex {hex_str}')
    
    r = 0
    g = 0
    b = 0
    
    if is_three:
        r = _parse_int_hex(hex_str[0] * 2)
        g = _parse_int_hex(hex_str[1] * 2)
        b = _parse_int_hex(hex_str[2] * 2)
    elif is_six:
        r = _parse_int_hex(hex_str[0:2])
        g = _parse_int_hex(hex_str[2:4])
        b = _parse_int_hex(hex_str[4:6])
    elif is_eight:
        r = _parse_int_hex(hex_str[2:4])
        g = _parse_int_hex(hex_str[4:6])
        b = _parse_int_hex(hex_str[6:8])
    
    return (255 << 24 | (r & 0xff) << 16 | (g & 0xff) << 8 | (b & 0xff)) & 0xFFFFFFFF


def _parse_int_hex(value: str) -> int:
    """
    Parse a hexadecimal string to an integer.
    
    Args:
        value: The hexadecimal string
        
    Returns:
        The integer value
    """
    return int(value, 16)
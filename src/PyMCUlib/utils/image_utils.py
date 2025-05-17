# utils/image_utils.py

from typing import List, Union, Optional, Tuple
import numpy as np
from PIL import Image
import io
from PyMCUlib.utils import color_utils


def source_color_from_image(image_data: Union[str, bytes, Image.Image],
                            area: Optional[Tuple[int, int, int, int]] = None) -> int:
    """
    Get the source color from an image.

    Args:
        image_data: The image data, can be a file path, bytes, or PIL Image object
        area: Optional crop area as (left, top, width, height)

    Returns:
        Source color - the color most suitable for creating a UI theme
    """
    # Convert to PIL Image if not already
    if isinstance(image_data, str):
        # Assume it's a file path
        img = Image.open(image_data)
    elif isinstance(image_data, bytes):
        # Bytes data
        img = Image.open(io.BytesIO(image_data))
    elif isinstance(image_data, Image.Image):
        # Already a PIL Image
        img = image_data
    else:
        raise ValueError("Unsupported image data type")
    
    # Determine crop rectangle
    if area is not None:
        sx, sy, sw, sh = area
        rect = (sx, sy, sx + sw, sy + sh)
    else:
        rect = (0, 0, img.width, img.height)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Get image data
    cropped_img = img.crop(rect)
    img_array = np.array(cropped_img)
    
    # Convert to flattened bytes
    image_bytes = img_array.flatten()
    
    return source_color_from_image_bytes(image_bytes)


def source_color_from_image_bytes(image_bytes: np.ndarray) -> int:
    """
    Get the source color from image bytes.

    Args:
        image_bytes: The image bytes as a numpy array

    Returns:
        Source color - the color most suitable for creating a UI theme
    """
    # Convert Image data to Pixel Array
    pixels: List[int] = []
    
    # Handle the data in RGBA format (R,G,B,A sequence)
    for i in range(0, len(image_bytes), 4):
        if i + 3 >= len(image_bytes):
            break
            
        r = int(image_bytes[i])
        g = int(image_bytes[i + 1])
        b = int(image_bytes[i + 2])
        a = int(image_bytes[i + 3])
        
        if a < 255:
            continue
            
        argb = color_utils.argb_from_rgb(r, g, b)
        pixels.append(argb)
    
    # Convert Pixels to Material Colors
    from PyMCUlib.quantize.quantizer_celebi import QuantizerCelebi
    result = QuantizerCelebi.quantize(pixels, 128)
    from PyMCUlib.score.score import Score
    ranked = Score.score(result)
    top = ranked[0]
    return top

def source_color_from_file(file_path: str,
                            area: Optional[Tuple[int, int, int, int]] = None) -> int:
    """
    Get the source color from an image file.

    Args:
        file_path: Path to the image file
        area: Optional crop area as (left, top, width, height)

    Returns:
        Source color - the color most suitable for creating a UI theme

    Raises:
        FileNotFoundError: If the file does not exist
    """
    image = Image.open(file_path)
    return source_color_from_image(image, area)
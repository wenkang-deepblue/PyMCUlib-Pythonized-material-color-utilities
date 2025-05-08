# image_utils.py

import numpy as np
from PIL import Image
from io import BytesIO
from typing import Any, Optional, Tuple

# Import required modules
from .utils import argb_from_rgb
from ..quantize.celebi import quantize_celebi
from ..score.score import ranked_suggestions

def source_color_from_image(image: Any, area: Optional[Tuple[int, int, int, int]] = None) -> int:
    """
    Get the source color from an image.
    
    Args:
        image: The image object (PIL Image or compatible)
        area: Optional area to crop the image before processing (x, y, width, height)
              Format: (left, top, width, height)
    
    Returns:
        Source color - the color most suitable for creating a UI theme
        
    Raises:
        ValueError: If the image cannot be processed or no valid color can be extracted
    """
    # Convert Image to PIL Image if it's not already
    if not isinstance(image, Image.Image):
        try:
            image = Image.open(image)
        except Exception as e:
            raise ValueError(f"Could not convert input to PIL Image: {e}")
    
    # Convert image to RGBA mode
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Handle area parameter (equivalent to dataset['area'] in TypeScript version)
    if area:
        try:
            sx, sy, sw, sh = area
            image = image.crop((sx, sy, sx + sw, sy + sh))
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid area specification: {e}")
    
    # Extract image data from the specified area
    rgba_data = np.array(image)
    
    # Flatten the image data
    image_bytes = rgba_data.reshape(-1)
    
    return source_color_from_image_bytes(image_bytes)

def source_color_from_image_bytes(image_bytes: np.ndarray) -> int:
    """
    Get the source color from image bytes.
    
    Args:
        image_bytes: Flattened image data as a numpy array in RGBA format
    
    Returns:
        Source color - the color most suitable for creating a UI theme
        
    Raises:
        ValueError: If no valid pixels can be found or colors cannot be scored
    """
    # Convert Image data to Pixel Array
    pixels = []
    for i in range(0, len(image_bytes), 4):
        if i + 3 < len(image_bytes):  # Ensure not out of bounds
            r = int(image_bytes[i])
            g = int(image_bytes[i + 1])
            b = int(image_bytes[i + 2])
            a = int(image_bytes[i + 3])
            
            if a < 255:
                continue
            
            argb = argb_from_rgb(r, g, b)
            pixels.append(argb)
    
    if not pixels:
        raise ValueError("No valid pixels found in the image")
    
    # Convert Pixels to Material Colors
    result = quantize_celebi(pixels, 128)
    ranked = ranked_suggestions(result.color_to_count)
    
    if not ranked:
        raise ValueError("Could not score any colors from the image")
    
    top = ranked[0]
    return top

def source_color_from_file(file_path: str, area: Optional[Tuple[int, int, int, int]] = None) -> int:
    """
    Get the source color from an image file.
    
    Args:
        file_path: Path to the image file
        area: Optional area to crop the image before processing (x, y, width, height)
    
    Returns:
        Source color - the color most suitable for creating a UI theme
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the image cannot be processed
    """
    try:
        image = Image.open(file_path)
        return source_color_from_image(image, area)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise ValueError(f"Error processing image file: {e}")


def source_color_from_bytes(raw_bytes: bytes) -> int:
    """
    Get the source color from raw image bytes.
    
    Args:
        raw_bytes: Raw image bytes (e.g., from a file read or network request)
    
    Returns:
        Source color - the color most suitable for creating a UI theme
        
    Raises:
        ValueError: If the image bytes cannot be processed
    """
    try:
        image = Image.open(BytesIO(raw_bytes))
        return source_color_from_image(image)
    except Exception as e:
        raise ValueError(f"Error processing image bytes: {e}")
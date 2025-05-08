# Image Utils Module

The `image_utils` module provides functionality to extract the source color from images. The source color is the color most suitable for creating a UI theme based on the image.

## Overview

This module allows you to extract a dominant and visually appealing color from an image, which can then be used to generate a complete theme using other Material Color Utilities components. It utilizes the `quantize_celebi` for color quantization and the `score` module for ranking extracted colors.

## Functions

### `source_color_from_image(image, area=None)`

Extracts the source color from a PIL Image.

**Parameters:**
- `image`: A PIL Image object or compatible image source
- `area` (optional): A tuple of (left, top, width, height) specifying the area to crop before processing

**Returns:**
- An integer representing the source color in ARGB format (0xAARRGGBB)

**Example:**
```python
from PIL import Image
from PyMCUlib.utils.image_utils import source_color_from_image

# Open an image
img = Image.open("my_image.jpg")

# Extract the source color
source_color = source_color_from_image(img)

# Print the color in hex format
print(f"Source color: #{source_color & 0xFFFFFF:06x}")

# Extract from a specific area of the image
area = (100, 100, 200, 200)  # x, y, width, height
source_color = source_color_from_image(img, area)
```

### `source_color_from_image_bytes(image_bytes)`

Extracts the source color from image bytes.

**Parameters:**
- `image_bytes`: Flattened image data as a numpy array in RGBA format

**Returns:**
- An integer representing the source color in ARGB format (0xAARRGGBB)

**Example:**
```python
import numpy as np
from PIL import Image
from PyMCUlib.utils.image_utils import source_color_from_image_bytes

# Get image bytes from a PIL Image
img = Image.open("my_image.jpg").convert("RGBA")
rgba_data = np.array(img)
image_bytes = rgba_data.flatten()

# Extract the source color
source_color = source_color_from_image_bytes(image_bytes)
```

### `source_color_from_file(file_path, area=None)`

Extracts the source color from an image file.

**Parameters:**
`file_path`: Path to the image file
`area` (optional): A tuple of (left, top, width, height) specifying the area to crop before processing

**Returns:**
- An integer representing the source color in ARGB format (0xAARRGGBB)

**Example:**
```python
from PyMCUlib.utils.image_utils import source_color_from_file

# Extract the source color from a file
source_color = source_color_from_file("my_image.jpg")

# Extract from a specific area
area = (100, 100, 200, 200)  # x, y, width, height
source_color = source_color_from_file("my_image.jpg", area)
```

### `source_color_from_bytes(raw_bytes)`
Extracts the source color from raw image bytes.

**Parameters:**
`raw_bytes`: Raw image bytes (e.g., from a file read or network request)

**Returns:**
- An integer representing the source color in ARGB format (0xAARRGGBB)

**Example:**
```python
from PyMCUlib.utils.image_utils import source_color_from_bytes

# Read image bytes from a file
with open("my_image.jpg", "rb") as f:
    raw_bytes = f.read()

# Extract the source color
source_color = source_color_from_bytes(raw_bytes)
```

## Error Handling
All functions in this module may raise:

- `ValueError`: If the image cannot be processed or no valid colors can be extracted
- `FileNotFoundError`: If an image file doesn't exist
- Other exceptions related to image processing

## Usage Notes
- Only pixels with full opacity (alpha = 255) are considered for color extraction
- The resulting color is chosen based on a scoring algorithm that considers various factors like vibrance, contrast, and neutrality
- For best results, provide images with clear, distinct colors
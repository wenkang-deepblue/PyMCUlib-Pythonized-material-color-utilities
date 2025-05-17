# Blend Module Documentation

## Overview

The Blend module provides functions for blending colors in different color spaces, particularly in HCT (Hue, Chroma, Tone) and CAM16 color spaces. These functions allow for color harmonization and interpolation that respect human color perception.

## Key Features

- Harmonization of colors by blending hues while preserving recognizability
- Blending of hues between colors while maintaining chroma and tone
- Full color blending in the CAM16-UCS color space

## Main Function Categories

### Harmonization

The `harmonize` function shifts a design color's hue towards a source color's hue in a way that creates harmony while keeping the original color recognizable.

### Hue Blending

The `hct_hue` function blends the hue from one color into another while maintaining the original color's chroma and tone.

### Color Space Blending

The `cam16_ucs` function performs blending in the perceptually uniform CAM16-UCS color space.

## Usage Examples

### Harmonizing Colors

```python
from PyMCUlib.blend.blend import Blend

# Define colors in ARGB format (0xAARRGGBB)
design_color = 0xffff0000  # Red
source_color = 0xff0000ff  # Blue

# Harmonize design color towards source color
harmonized_color = Blend.harmonize(design_color, source_color)
```

### Blending Hues

```python
from PyMCUlib.blend.blend import Blend

# Define colors in ARGB format
from_color = 0xffff0000  # Red
to_color = 0xff0000ff    # Blue

# Blend 50% of to_color's hue into from_color
blended_color = Blend.hct_hue(from_color, to_color, 0.5)
```

### Blending in CAM16-UCS Space

```python
from PyMCUlib.blend.blend import Blend

# Define colors in ARGB format
from_color = 0xffff0000  # Red
to_color = 0xff0000ff    # Blue

# Blend 25% of to_color into from_color
blended_color = Blend.cam16_ucs(from_color, to_color, 0.25)
```

## API Reference

### `Blend` Class

A utility class containing static methods for color blending operations.

#### `harmonize(design_color, source_color)`

Blends the design color's HCT hue towards the source color's HCT hue, creating a harmonious variant that remains recognizable as the original color.

- **Parameters:**
  - `design_color`: ARGB integer representation of an arbitrary color
  - `source_color`: ARGB integer representation of the main theme color
- **Returns:** ARGB integer representation of the harmonized color
- **Example:**
  ```python
  # Harmonize red towards blue
  result = Blend.harmonize(0xffff0000, 0xff0000ff)  # Returns 0xffFB0057
  ```

#### `hct_hue(from_color, to_color, amount)`

Blends the hue from one color into another while maintaining the original chroma and tone.

- **Parameters:**
  - `from_color`: ARGB integer representation of the starting color
  - `to_color`: ARGB integer representation of the target color
  - `amount`: Float between 0.0 and 1.0 indicating how much blending to perform
- **Returns:** ARGB integer representation of the blended color
- **Example:**
  ```python
  # Blend 30% of blue's hue into red
  result = Blend.hct_hue(0xffff0000, 0xff0000ff, 0.3)
  ```

#### `cam16_ucs(from_color, to_color, amount)`

Blends colors in the perceptually uniform CAM16-UCS color space.

- **Parameters:**
  - `from_color`: ARGB integer representation of the starting color
  - `to_color`: ARGB integer representation of the target color
  - `amount`: Float between 0.0 and 1.0 indicating how much blending to perform
- **Returns:** ARGB integer representation of the blended color
- **Example:**
  ```python
  # Blend 40% of blue into red in CAM16-UCS space
  result = Blend.cam16_ucs(0xffff0000, 0xff0000ff, 0.4)
  ```

## Implementation Notes
- All colors are represented as ARGB integers in the format 0xAARRGGBB
- The implementation relies on the HCT and CAM16 color spaces for perceptually accurate color manipulation
- The `harmonize` function uses a maximum rotation of 15 degrees or half the difference between hues, whichever is smaller
- Outputs are always opaque (alpha = 0xFF); current implementation does not preserve original alpha channel
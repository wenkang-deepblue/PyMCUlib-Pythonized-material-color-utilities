# <center> Dislike Component Documentation </center>

## Overview

The dislike component provides functions to check for and fix universally disliked colors. According to color science studies of color preference, dark yellow-greens are universally disliked due to their correlation with biological waste and rotting food.

This component is based on research by Palmer and Schloss (2010) and Schloss and Palmer's Chapter 21 in Handbook of Color Psychology (2015).

## Import Guide

To use the dislike component, use the following import statements:

```python
# Import dislike component functions
from PyMCUlib_cpp.dislike import is_disliked, fix_if_disliked

# Import HCT color system
from PyMCUlib_cpp.cam.hct import Hct

# For utility functions like hex_from_argb
from PyMCUlib_cpp.utils import hex_from_argb
```

## Main Features

The dislike component contains two main functions:

- `is_disliked`: Checks if a color is disliked
- `fix_if_disliked`: Fixes a disliked color by lightening it

## Function Details

### is_disliked

```python
def is_disliked(hct: Hct) -> bool
```

### Determines whether a color is disliked.
Disliked is defined as a dark yellow-green that is not neutral, specifically:
* Hue between 90° and 111°
* Chroma greater than 16
* Tone less than 65

### Parameters:
* `hct`: The color to be tested, as an Hct object

### Returns:
* `bool`: Whether the color is disliked

### Example:
```python
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dislike import is_disliked

# Create an HCT color (yellow-green, potentially disliked)
color = Hct.from_int(0xff95884B)

# Check if it's disliked
if is_disliked(color):
    print("This color is disliked")
```

### fix_if_disliked
```python
def fix_if_disliked(hct: Hct) -> Hct
```

If a color is disliked, lightens it to make it likable.
The original color is not modified. If the color is disliked, the function returns a new Hct object with the same hue and chroma but with a tone of 70.0. If the color is not disliked, the function returns the original color.

### Parameters:
* `hct`: The color to be tested (and fixed, if needed), as an Hct object

### Returns:
* `Hct`: The original color if it is not disliked; otherwise, a fixed version of the color

### Example:
```python
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.dislike import fix_if_disliked
from PyMCUlib_cpp.utils import hex_from_argb

# Create a potentially disliked yellow-green color
color = Hct.from_int(0xff95884B)

# Fix it if it's disliked
fixed_color = fix_if_disliked(color)

# Display the result
print(f"Original color: {hex_from_argb(color.to_int())}")
print(f"Fixed color: {hex_from_argb(fixed_color.to_int())}")
```

## Dependencies

The dislike component depends on the following modules:
* `PyMCUlib_cpp.cam.hct`: For the HCT color system
* `PyMCUlib_cpp.utils`: For utility functions

## Usage Notes
* The dislike component works with Hct objects, which can be created from ARGB colors using `Hct.from_int()` or from hue, chroma, and tone using `Hct.from_hct()`
* Disliked colors are fixed by setting their tone to 70.0, which makes them lighter but preserves their hue and chroma
* This component is based on color science research and aims to improve user experience by avoiding colors that tend to be universally disliked

## Decision Flow

```
Input Color (Hct)
    |
    v
Is color disliked?
(90° ≤ hue ≤ 111°) AND (chroma > 16) AND (tone < 65)
    |
    +---Yes---> Return fixed color with tone = 70.0
    |
    +---No----> Return original color
```

## Complete Example
```python
from PyMCUlib_cpp.dislike import is_disliked, fix_if_disliked
from PyMCUlib_cpp.cam.hct import Hct
from PyMCUlib_cpp.utils import hex_from_argb

# Example colors
liked_color = Hct.from_int(0xfff6ede4)    # Monk skin tone (liked)
disliked_color = Hct.from_int(0xff95884B)  # Bile color (disliked)

# Check if colors are disliked
print(f"Is skin tone disliked? {is_disliked(liked_color)}")
print(f"Is bile color disliked? {is_disliked(disliked_color)}")

# Fix disliked color
fixed_color = fix_if_disliked(disliked_color)
print(f"Original disliked color: {hex_from_argb(disliked_color.to_int())}")
print(f"Fixed color: {hex_from_argb(fixed_color.to_int())}")
print(f"Is fixed color still disliked? {is_disliked(fixed_color)}")
```
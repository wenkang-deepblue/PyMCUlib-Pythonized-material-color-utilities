# <center> Blend Component Documentation </center>

## Overview
The blend component provides a set of utility functions for blending colors. These functions allow for smooth blending and harmonization of colors in different color spaces, creating harmonious color schemes.

## Main Features
The blend component contains three main functions:
1. `blend_harmonize`: Harmonizes two colors
2. `blend_hct_hue`: Blends hue in the HCT color space
3. `blend_cam16_ucs`: Blends colors in the CAM16-UCS color space

## Function Details
### blend_harmonize
```python
def blend_harmonize(design_color: Argb, key_color: Argb) -> Argb
```
Harmonizes one color (design_color) to another (key_color). This is achieved by rotating the source color's hue toward the target color's hue, making the two colors more harmonious.

Parameters:
* `design_color`: Color to harmonize, in ARGB format
* `key_color`: Color providing the direction to move, in ARGB format

Returns:
* Harmonized color, in ARGB format

Example:
```python
from PyMCUlib.blend import blend_harmonize

harmonized_color = blend_harmonize(0xff1a6fb0, 0xffe4a789)
```
### blend_hct_hue
```python
def blend_hct_hue(from_color: Argb, to_color: Argb, amount: float) -> Argb
```
Blends hue from two colors in the HCT color space, maintaining the source color's chroma and tone.

Parameters:
* `from_color`: Source color, in ARGB format
* `to_color`: Destination color, in ARGB format
* `amount`: Blend amount, ranging from 0.0 (source color) to 1.0 (destination color)

Returns:
* Blended color, in ARGB format

Example:
```python
from PyMCUlib.blend import blend_hct_hue

# 80% blend from red to blue
mixed_color = blend_hct_hue(0xffff0000, 0xff0000ff, 0.8)  # Result: 0xff905eff
```
### blend_cam16_ucs
```python
def blend_cam16_ucs(from_color: Argb, to_color: Argb, amount: float) -> Argb
```
Linearly blends two colors in the CAM16-UCS color space. CAM16-UCS is a perceptually uniform color space, ideal for color interpolation.

Parameters:
* `from_color`: Source color, in ARGB format
* `to_color`: Destination color, in ARGB format
* `amount`: Blend amount, ranging from 0.0 (source color) to 1.0 (destination color)

Returns:
* Blended color, in ARGB format

Example:
```python
from PyMCUlib.blend import blend_cam16_ucs

# 50% blend from green to purple
mixed_color = blend_cam16_ucs(0xff00ff00, 0xff800080, 0.5)
```
### Usage Notes
* All functions use ARGB format to represent colors (integers, typically represented in hexadecimal, like 0xffrrggbb)
* The `amount` parameter should be between 0.0 and 1.0, representing the degree of blending
* `blend_harmonize` rotates the source color toward the target color, but at most 15 degrees, to maintain certain characteristics of the source color
* These functions depend on the utils, cam, and hct modules for underlying functionality

## Complete Example
```python
from PyMCUlib.blend import blend_harmonize, blend_hct_hue, blend_cam16_ucs
from PyMCUlib.utils import hex_from_argb

# Color definitions
red = 0xffff0000
blue = 0xff0000ff
green = 0xff00ff00
purple = 0xff800080

# Test different blending methods
harmonized = blend_harmonize(red, green)
print(f"Harmonized red with green: {hex_from_argb(harmonized)}")

hct_mixed = blend_hct_hue(red, blue, 0.8)
print(f"80% HCT hue mix of red to blue: {hex_from_argb(hct_mixed)}")

ucs_mixed = blend_cam16_ucs(green, purple, 0.5)
print(f"50% CAM16-UCS mix of green to purple: {hex_from_argb(ucs_mixed)}")
```
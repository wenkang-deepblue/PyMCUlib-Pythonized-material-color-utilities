# Contrast Module Documentation

## Overview

The Contrast module provides utility methods for calculating contrast given two colors, or calculating a color given one color and a contrast ratio.

Contrast ratio is calculated using XYZ's Y. When linearized to match human perception, Y becomes HCT's tone and L*a*b*'s L*. Informally, this is the lightness of a color.

Methods in this module primarily refer to tone (T) in the HCT color space. Tone is equivalent to L* in the L*a*b* color space, or L in the LCH color space.

## Key Features

- Calculate contrast ratio between two tones (lightness values)
- Find colors with specific contrast ratios relative to a given color
- Handle edge cases with "safe" and "unsafe" methods

## Main Functions

### ratio_of_tones(tone_a, tone_b)

Returns a contrast ratio between two tones, which ranges from 1 to 21.

**Parameters:**
- `tone_a`: Tone between 0 and 100. Values outside will be clamped.
- `tone_b`: Tone between 0 and 100. Values outside will be clamped.

**Returns:**
- Contrast ratio between the two tones

### ratio_of_ys(y1, y2)

Calculates the contrast ratio between two luminance values (Y in XYZ color space).

**Parameters:**
- `y1`: First luminance value
- `y2`: Second luminance value

**Returns:**
- Contrast ratio between the two luminance values (ranges from 1 to 21)

### lighter(tone, ratio)

Returns a tone ≥ given tone that ensures the specified contrast ratio.

**Parameters:**
- `tone`: Tone return value must contrast with. Range is 0 to 100. Invalid values will result in -1 being returned.
- `ratio`: Contrast ratio of return value and tone. Range is 1 to 21.

**Returns:**
- Tone value (0-100) that achieves the desired contrast ratio
- -1 if the ratio cannot be achieved with the given tone

### darker(tone, ratio)

Returns a tone ≤ given tone that ensures the specified contrast ratio.

**Parameters:**
- `tone`: Tone return value must contrast with. Range is 0 to 100. Invalid values will result in -1 being returned.
- `ratio`: Contrast ratio of return value and tone. Range is 1 to 21.

**Returns:**
- Tone value (0-100) that achieves the desired contrast ratio
- -1 if the ratio cannot be achieved with the given tone

### lighter_unsafe(tone, ratio)

Similar to `lighter()`, but returns 100 instead of -1 if the ratio cannot be achieved.

**Parameters:**
- `tone`: Tone return value must contrast with. Range is 0 to 100.
- `ratio`: Desired contrast ratio. Range is 1 to 21.

**Returns:**
- Tone value (0-100) that achieves the desired contrast ratio, or 100 if not possible

### darker_unsafe(tone, ratio)

Similar to `darker()`, but returns 0 instead of -1 if the ratio cannot be achieved.

**Parameters:**
- `tone`: Tone return value must contrast with. Range is 0 to 100.
- `ratio`: Desired contrast ratio. Range is 1 to 21.

**Returns:**
- Tone value (0-100) that achieves the desired contrast ratio, or 0 if not possible

## Usage Examples

### Calculate Contrast Ratio Between Two Tones

```python
from PyMCUlib.contrast.contrast import Contrast

# Calculate contrast ratio between two tones
ratio = Contrast.ratio_of_tones(20.0, 80.0)
print(f"Contrast ratio: {ratio}")  # Will be approximately 7.7
```
### Find a Lighter Tone with Required Contrast
```python
from PyMCUlib.contrast.contrast import Contrast

# Find a tone that is lighter than tone 30 with contrast ratio of 4.5
lighter_tone = Contrast.lighter(30.0, 4.5)
if lighter_tone >= 0:
    print(f"Lighter tone: {lighter_tone}")
else:
    print("Cannot achieve requested contrast ratio")
```
### Find a Darker Tone with Required Contrast
```python
from PyMCUlib.contrast.contrast import Contrast

# Find a tone that is darker than tone 70 with contrast ratio of 3.0
darker_tone = Contrast.darker(70.0, 3.0)
if darker_tone >= 0:
    print(f"Darker tone: {darker_tone}")
else:
    print("Cannot achieve requested contrast ratio")
```
### Using Unsafe Methods for Guaranteed Bounds
```python
from PyMCUlib.contrast.contrast import Contrast

# Always returns a value between 0-100, even if contrast ratio can't be achieved
safer_lighter_tone = Contrast.lighter_unsafe(95.0, 10.0)  # Returns 100 if not achievable
safer_darker_tone = Contrast.darker_unsafe(5.0, 10.0)     # Returns 0 if not achievable
```
## Implementation Notes
- All contrast calculations are based on the WCAG (Web Content Accessibility Guidelines) contrast formula
- The methods handle out-of-bounds input gracefully
- "Unsafe" methods guarantee that the return value is within the valid tone range (0-100), but may not achieve the requested contrast ratio
- A slight adjustment (±0.4) is added to ensure that gamut mapping will still result in the correct ratio

## Related Modules
- `color_utils`: Provides color space conversion functions used by the contrast module
- `math_utils`: Provides mathematical utilities like clamping values
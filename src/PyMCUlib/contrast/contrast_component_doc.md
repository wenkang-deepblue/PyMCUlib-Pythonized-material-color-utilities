# <center> Contrast Component Documentation </center>

## Overview

The contrast component provides utility methods for calculating contrast given two colors, or calculating a color given one color and a contrast ratio.

Contrast ratio is calculated using XYZ's Y. When linearized to match human perception, Y becomes HCT's tone and L*a*b*'s L*. Informally, this is the lightness of a color.

The methods in this component refer to tone, which is T in the HCT color space. Tone is equivalent to L* in the L*a*b* color space, or L in the LCH color space.

## Main Features

The contrast component contains the following main functions:

- `ratio_of_ys`: Calculate contrast ratio between two Y values
- `ratio_of_tones`: Calculate contrast ratio between two tones
- `lighter`: Find a tone that is lighter than input and achieves target contrast ratio
- `darker`: Find a tone that is darker than input and achieves target contrast ratio
- `lighter_unsafe`: Always returns a valid tone value (may not achieve target contrast)
- `darker_unsafe`: Always returns a valid tone value (may not achieve target contrast)

## Constants

The contrast component uses the following constants to handle perceptual accuracy:

- `CONTRAST_RATIO_EPSILON = 0.04`: Threshold for acceptable difference between desired and actual contrast ratio. When the difference exceeds this value, safe methods will return an error.

- `LUMINANCE_GAMUT_MAP_TOLERANCE = 0.4`: Compensates for inaccuracies when mapping between perceptual color spaces and display color spaces. Ensures that even with gamut mapping, the desired contrast ratio will still be achieved.

## Function Details

### ratio_of_ys

```python
def ratio_of_ys(y1: float, y2: float) -> float
```

Calculates the contrast ratio between two Y values from the XYZ color space.

### Parameters:
* `y1`: First Y value
* `y2`: Second Y value

### Returns:
* Contrast ratio between y1 and y2 (ranges from 1 to 21)

### Example:
```python
from PyMCUlib.contrast import ratio_of_ys
from PyMCUlib.utils import y_from_lstar

# Calculate contrast between Y values corresponding to tones 20 and 80
y1 = y_from_lstar(20.0)
y2 = y_from_lstar(80.0)
contrast = ratio_of_ys(y1, y2)
print(f"Contrast ratio: {contrast:.2f}")
```

### ratio_of_tones

```python
def ratio_of_tones(tone_a: float, tone_b: float) -> float
```
Returns a contrast ratio, which ranges from 1 to 21.

### Parameters:
* `tone_a`: Tone between 0 and 100. Values outside will be clamped.
* `tone_b`: Tone between 0 and 100. Values outside will be clamped.

### Returns:
* Contrast ratio between tone_a and tone_b

### Example:
```python
from PyMCUlib.contrast import ratio_of_tones

# Calculate contrast between a dark tone (20) and a light tone (80)
contrast = ratio_of_tones(20.0, 80.0)
print(f"Contrast ratio: {contrast:.2f}")  # Output: Contrast ratio: 9.69
```

### lighter

```python
def lighter(tone: float, ratio: float) -> float
```
Returns a tone >= input tone that ensures the target contrast ratio.
Return value is between 0 and 100, or -1 if the ratio cannot be achieved with the input tone.

### Parameters:
* `tone`: Tone return value must contrast with (0 to 100).
* `ratio`: Contrast ratio of return value and tone (1 to 21).

### Returns:
* A tone value that contrasts with input, or -1 if not possible.

### Example:
```python
from PyMCUlib.contrast import lighter

# Find a tone that is lighter than 30 and has a contrast ratio of at least 4.5
lighter_tone = lighter(30.0, 4.5)
print(f"Lighter tone: {lighter_tone:.2f}")  # Example output: Lighter tone: 72.38
```

### darker

```python
def darker(tone: float, ratio: float) -> float
```
Returns a tone <= input tone that ensures the target contrast ratio.
Return value is between 0 and 100, or -1 if the ratio cannot be achieved with the input tone.

### Parameters:
* `tone`: Tone return value must contrast with (0 to 100).
* `ratio`: Contrast ratio of return value and tone (1 to 21).

### Returns:
* A tone value that contrasts with input, or -1 if not possible.

### Example:
```python
from PyMCUlib.contrast import darker

# Find a tone that is darker than 80 and has a contrast ratio of at least 3.0
darker_tone = darker(80.0, 3.0)
print(f"Darker tone: {darker_tone:.2f}")  # Example output: Darker tone: 36.65
```

### lighter_unsafe

```python
def lighter_unsafe(tone: float, ratio: float) -> float
```
Returns a tone >= input tone that ensures the target contrast ratio.
This method is "unsafe" because it always returns a value between 0 and 100, even if the target contrast ratio cannot be achieved.

### Parameters:
* `tone`: Tone return value must contrast with (0 to 100).
* `ratio`: Desired contrast ratio (1 to 21).

### Returns:
* A tone value between 0 and 100 (returns 100 if ratio cannot be achieved).

### Example:
```python
from PyMCUlib.contrast import lighter_unsafe

# Find a tone that is lighter than 90, aiming for a contrast ratio of 10
# (which may not be achievable)
lighter_tone = lighter_unsafe(90.0, 10.0)
print(f"Lighter tone (unsafe): {lighter_tone:.2f}")  # Output: Lighter tone (unsafe): 100.00
```

### darker_unsafe

```python
def darker_unsafe(tone: float, ratio: float) -> float
```
Returns a tone <= input tone that ensures the target contrast ratio.
This method is "unsafe" because it always returns a value between 0 and 100, even if the target contrast ratio cannot be achieved.

### Parameters:
* `tone`: Tone return value must contrast with (0 to 100).
* `ratio`: Desired contrast ratio (1 to 21).

### Returns:
* A tone value between 0 and 100 (returns 0 if ratio cannot be achieved).

### Example:
```python
from PyMCUlib.contrast import darker_unsafe

# Find a tone that is darker than 10, aiming for a contrast ratio of 15
# (which may not be achievable)
darker_tone = darker_unsafe(10.0, 15.0)
print(f"Darker tone (unsafe): {darker_tone:.2f}")  # Output: Darker tone (unsafe): 0.00
```

## Implementation Details

### Perceptual Color Spaces vs. Display Color Spaces

The contrast component deals with the inherent challenges of mapping between perceptually accurate color spaces and display color spaces:

- **Perceptual color spaces** (like L*a*b*, XYZ, HCT) measure luminance accurately according to human perception
- **Display color spaces** (like RGB/HSL/HSV) have defined limits on available colors

When mapping between these spaces (gamut mapping), some accuracy must be sacrificed. The implementation prioritizes:
1. Maintaining lightness (preserving contrast/accessibility)
2. Maintaining hue (preserving aesthetic intent)
3. Reducing chroma until the color is in gamut

The constants `CONTRAST_RATIO_EPSILON` and `LUMINANCE_GAMUT_MAP_TOLERANCE` help compensate for these mapping inaccuracies.

## Usage Notes

* All tone values are between 0 and 100, representing the lightness of a color.
* Contrast ratios range from 1.0 (no contrast) to 21.0 (maximum contrast).
* For accessibility, common minimum contrast ratios are:
    * 3.0 for large text (18pt+)
    * 4.5 for normal text
    * 7.0 for enhanced contrast

## Dependencies

This component relies on the following utilities:
- `y_from_lstar`: Converts L* (tone) to Y
- `lstar_from_y`: Converts Y to L* (tone)

These functions are imported from the `PyMCUlib.utils` module.

## Complete Example

```python
from PyMCUlib.contrast import ratio_of_tones, lighter, darker, lighter_unsafe, darker_unsafe
from PyMCUlib.utils import y_from_lstar, lstar_from_y, int_from_lstar, hex_from_argb

# Define some tone values
dark_tone = 30.0
light_tone = 80.0

# Calculate contrast ratio
ratio = ratio_of_tones(dark_tone, light_tone)
print(f"Contrast ratio between tones {dark_tone} and {light_tone}: {ratio:.2f}")

# Find a lighter tone that has a contrast ratio of 4.5 with dark_tone
accessibility_tone = lighter(dark_tone, 4.5)
print(f"Tone with 4.5 contrast to {dark_tone}: {accessibility_tone:.2f}")

# Convert tones to colors for visualization
dark_color = int_from_lstar(dark_tone)
light_color = int_from_lstar(light_tone)
accessible_color = int_from_lstar(accessibility_tone)

# Display as hex
print(f"Dark color: {hex_from_argb(dark_color)}")
print(f"Light color: {hex_from_argb(light_color)}")
print(f"Accessible color: {hex_from_argb(accessible_color)}")
```
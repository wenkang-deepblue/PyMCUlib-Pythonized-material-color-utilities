# Temperature Module Documentation
## Overview
The Temperature module provides design utilities for working with color temperature theory. It helps generate harmonious color combinations using temperature relationships between colors, which can enhance the aesthetic appeal of design systems.

Temperature in this context refers to the perceptual warmth or coolness of a color, which is distinct from its hue or chroma. This module enables developers to create color palettes based on well-established color harmony principles.

## Key Features
- Calculate color temperature values (raw and relative)
- Generate complementary colors
- Create analogous color palettes
- Efficiently cache color temperature calculations for performance

## Core Classes
### TemperatureCache
The main class that provides color temperature utilities with lazy calculation and caching mechanisms.

#### Key Methods and Properties:
- `raw_temperature(color)`: Static method that calculates the cool-warm factor of a color
- `complement`: Property that returns a color that aesthetically complements the input color
- `analogous(count, divisions)`: Method that generates a set of analogous colors
- `warmest`/`coldest`: Properties that return the warmest and coldest colors with same chroma/tone as input
- `relative_temperature(hct)`: Method that calculates temperature relative to all colors with same chroma/tone

## Usage Examples
### Calculating Color Temperature

```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.temperature.temperature_cache import TemperatureCache

# Create colors in HCT format
blue = Hct.from_int(0xff0000ff)  # Blue color in ARGB format
red = Hct.from_int(0xffff0000)   # Red color in ARGB format

# Calculate raw temperature values
blue_temp = TemperatureCache.raw_temperature(blue)  # Approx -1.393
red_temp = TemperatureCache.raw_temperature(red)    # Approx 2.351

# Calculate relative temperature
blue_cache = TemperatureCache(blue)
red_cache = TemperatureCache(red)

blue_relative = blue_cache.input_relative_temperature  # 0.0 (coolest)
red_relative = red_cache.input_relative_temperature    # 1.0 (warmest)
```

### Generating Complementary Colors
```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.temperature.temperature_cache import TemperatureCache

# Create a color
blue = Hct.from_int(0xff0000ff)  # Blue color

# Find its complement
temp_cache = TemperatureCache(blue)
complement = temp_cache.complement  # Returns a reddish color (ARGB: 0xff9d0002)

# Print information about the complement
print(f"Original color: {hex(blue.to_int())}")
print(f"Complement color: {hex(complement.to_int())}")
```
### Creating Analogous Color Palettes
```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.temperature.temperature_cache import TemperatureCache

# Create a color
hct_color = Hct.from_int(0xff0000ff)  # Blue color

# Get analogous colors (default is 5 colors)
temp_cache = TemperatureCache(hct_color)
analogous_colors = temp_cache.analogous()  # Returns 5 colors including the input

# Get more analogous colors
more_analogous = temp_cache.analogous(count=7)  # Returns 7 colors

# Get analogous colors with more color wheel divisions
fine_analogous = temp_cache.analogous(count=5, divisions=24)  # More precise divisions

# Print the color codes
for i, color in enumerate(analogous_colors):
    print(f"Color {i+1}: {hex(color.to_int())}")
```
### Warmest/Coldest:
```python
cache = TemperatureCache(blue)
print("Coldest:", hex(cache.coldest.to_int()))
print("Warmest:", hex(cache.warmest.to_int()))
```

## Implementation Notes

- The temperature calculations are based on color science research by Ou, Woodcock, and Wright
- Raw temperature values typically range from -9.66 to 8.61, with negative values considered "cool" and positive values "warm"
- The module uses efficient caching mechanisms to avoid redundant calculations
- Temperature is calculated using the Lab* / LCH color space for perceptual accuracy
- The module automatically handles edge cases like white and black colors, which have no temperature differences across hues

## Related Components
- `hct`: HCT color space representation used by this module
- `utils.color_utils`: Color utility functions
- `utils.math_utils`: Mathematical utility functions

## References
- Li-Chen Ou's Chapter 19 in Handbook of Color Psychology (2015)
- Josef Albers' Interaction of Color chapters 19 and 21
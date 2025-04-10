# <center> Temperature Component Documentation </center>

## Overview

The temperature component provides design utilities using color temperature theory. It allows the creation of color palettes that are harmonious and aesthetically pleasing by calculating complementary and analogous colors based on temperature.

Color temperature in this context refers to the warm-cool factor of a color. Warm colors typically have hues in the red-yellow-orange spectrum, while cool colors have hues in the blue-green-purple spectrum.

## Main Features

The temperature component provides the following main features:

- Calculate complementary colors that balance the warm-cool factor of a base color
- Generate analogous color schemes with colors that are equidistant in temperature
- Calculate the relative temperature of a color
- Determine raw temperature values for colors
- Efficient caching mechanism for repeated color calculations

## Classes

### TemperatureCache

The `TemperatureCache` class manages calculations related to color temperature theory and caches results for efficiency.

#### Constructor

```python
def __init__(input_color: Hct)
```
Creates a cache that allows calculation of complementary and analogous colors.

#### Parameters:
* `input_color`: Color to find complement/analogous colors of. Any generated colors will have the same tone and chroma as the input color, modulo any restrictions due to the other hues having lower limits on chroma.

#### Methods

##### get_complement
```python
def get_complement() -> Hct
```
Returns a color that complements the input color aesthetically.

In art, this is usually described as being across the color wheel. The intent is to find a color that is just as cool-warm as the input color is warm-cool.

#### Returns:

* A color that is complementary to the input color.

#### Example:
```python
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.cam.hct import Hct
from PyMCUlib.utils.utils import hex_from_argb

# Create a temperature cache with a blue color
blue = Hct.from_int(0xff0000ff)
temp_cache = TemperatureCache(blue)

# Get the complementary color
complement = temp_cache.get_complement()
print(f"Complement of blue: {hex_from_argb(complement.to_int())}")  # Output: 9d0002
```

##### get_analogous_colors
```python
def get_analogous_colors(count: int = 5, divisions: int = 12) -> List[Hct]
```
Returns a set of colors with differing hues, equidistant in temperature.

In art, this is usually described as a set of 5 colors on a color wheel divided into 12 sections. This method allows provision of either of those values.

#### Parameters:
* `count`: The number of colors to return, includes the input color.
* `divisions`: The number of divisions on the color wheel.

#### Returns:
Analogous colors, ordered from coolest to warmest.

#### Example:
```python
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.cam.hct import Hct
from PyMCUlib.utils.utils import hex_from_argb

# Create a temperature cache with a red color
red = Hct.from_int(0xffff0000)
temp_cache = TemperatureCache(red)

# Get the analogous colors
analogous = temp_cache.get_analogous_colors()
for i, color in enumerate(analogous):
    print(f"Analogous color {i}: {hex_from_argb(color.to_int())}")
```

##### get_analogous_colors_default
```python
def get_analogous_colors_default() -> List[Hct]
```
Returns 5 colors that pair well with the input color. The colors are equidistant in temperature and adjacent in hue.

This is a convenience method that calls `get_analogous_colors(5, 12)`.

#### Returns:
Analogous colors, ordered from coolest to warmest.

#### Example:
```python
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.cam.hct import Hct
from PyMCUlib.utils.utils import hex_from_argb

# Create a temperature cache with a red color
red = Hct.from_int(0xffff0000)
temp_cache = TemperatureCache(red)

# Get the default analogous colors (5 colors)
analogous = temp_cache.get_analogous_colors_default()
for i, color in enumerate(analogous):
    print(f"Analogous color {i}: {hex_from_argb(color.to_int())}")
```

##### get_relative_temperature
```python
def get_relative_temperature(hct: Hct) -> float
```
Calculates temperature relative to all colors with the same chroma and tone.

#### Parameters:
* `hct`: HCT to find the relative temperature of.

#### Returns:
* Value on a scale from 0 to 1.

#### Example:
```python
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.cam.hct import Hct

# Create a temperature cache
blue = Hct.from_int(0xff0000ff)
temp_cache = TemperatureCache(blue)

# Get the relative temperature
red = Hct.from_int(0xffff0000)
rel_temp = temp_cache.get_relative_temperature(red)
print(f"Relative temperature of red: {rel_temp}")
```

##### raw_temperature (static)
```python
@staticmethod
def raw_temperature(color: Hct) -> float
```
Calculates a value representing the cool-warm factor of a color. Values below 0 are considered cool, above 0 are warm.

This is an implementation of Ou, Woodcock and Wright's algorithm, which uses Lab/LCH color space.

#### Parameters:
* `color`: HCT color to calculate raw temperature.

#### Returns:
* Raw temperature of the color. Values have these properties:
  * Values below 0 are cool, above 0 are warm
  * Lower bound: -9.66 (assuming max Lab chroma of 130)
  * Upper bound: 8.61 (assuming max Lab chroma of 130)

#### Example:
```python
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.cam.hct import Hct

# Calculate raw temperature of different colors
blue = Hct.from_int(0xff0000ff)
blue_temp = TemperatureCache.raw_temperature(blue)
print(f"Raw temperature of blue: {blue_temp}")  # Negative value (cool)

red = Hct.from_int(0xffff0000)
red_temp = TemperatureCache.raw_temperature(red)
print(f"Raw temperature of red: {red_temp}")  # Positive value (warm)
```

##### get_coldest
```python
def get_coldest() -> Hct
```
Returns the coldest color with the same chroma and tone as the input color.

#### Returns:
* The coldest color with the same chroma and tone as the input.

#### Example:
```python
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.cam.hct import Hct
from PyMCUlib.utils.utils import hex_from_argb

# Create a temperature cache
color = Hct.from_int(0xff9c27b0)  # Purple
temp_cache = TemperatureCache(color)

# Get the coldest color
coldest = temp_cache.get_coldest()
print(f"Coldest color: {hex_from_argb(coldest.to_int())}")
```

##### get_warmest
```python
def get_warmest() -> Hct
```
Returns the warmest color with the same chroma and tone as the input color.

#### Returns:
* The warmest color with the same chroma and tone as the input.

#### Example:
```python
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.cam.hct import Hct
from PyMCUlib.utils.utils import hex_from_argb

# Create a temperature cache
color = Hct.from_int(0xff9c27b0)  # Purple
temp_cache = TemperatureCache(color)

# Get the warmest color
warmest = temp_cache.get_warmest()
print(f"Warmest color: {hex_from_argb(warmest.to_int())}")
```

##### get_hcts_by_hue
```python
def get_hcts_by_hue() -> List[Hct]
```
Returns HCTs for all colors with the same chroma/tone as the input, sorted by hue.

#### Returns:
* A list of HCT colors sorted by hue (index 0 is hue 0).

##### get_hcts_by_temp
```python
def get_hcts_by_temp() -> List[Hct]
```
Returns HCTs for all colors with the same chroma/tone as the input, sorted from coldest to warmest.

#### Returns:
* A list of HCT colors sorted by temperature from coldest to warmest.

##### get_temps_by_hct
```python
def get_temps_by_hct() -> Dict[Hct, float]
```
Returns a dictionary mapping HCTs to their raw temperature values.

#### Returns:
* A dictionary with HCT objects as keys and raw temperature values as values.

## Complete Example
```python
from PyMCUlib.temperature.temperature_cache import TemperatureCache
from PyMCUlib.cam.hct import Hct
from PyMCUlib.utils.utils import hex_from_argb

# Create colors
blue = Hct.from_int(0xff0000ff)
red = Hct.from_int(0xffff0000)
green = Hct.from_int(0xff00ff00)

# Calculate raw temperatures
blue_temp = TemperatureCache.raw_temperature(blue)
red_temp = TemperatureCache.raw_temperature(red)
green_temp = TemperatureCache.raw_temperature(green)

print(f"Raw temperatures:")
print(f"Blue: {blue_temp:.3f}")  # Cool (negative)
print(f"Red: {red_temp:.3f}")   # Warm (positive)
print(f"Green: {green_temp:.3f}")  # Slightly cool (negative)

# Create a temperature cache for blue
temp_cache = TemperatureCache(blue)

# Get complementary color
complement = temp_cache.get_complement()
print(f"\nComplement of blue: {hex_from_argb(complement.to_int())}")

# Get analogous colors
analogous = temp_cache.get_analogous_colors()
print("\nAnalogous colors to blue:")
for i, color in enumerate(analogous):
    print(f"Color {i}: {hex_from_argb(color.to_int())}")

# Get relative temperature
rel_temp = temp_cache.get_relative_temperature(red)
print(f"\nRelative temperature of red: {rel_temp:.3f}")

# Get coldest and warmest colors with same chroma/tone
coldest = temp_cache.get_coldest()
warmest = temp_cache.get_warmest()
print(f"\nColdest color: {hex_from_argb(coldest.to_int())}")
print(f"Warmest color: {hex_from_argb(warmest.to_int())}")
```

## Implementation Details

### Caching Mechanism

The `TemperatureCache` class uses lazy initialization for various calculations:

- All calculations are performed only when needed and then cached
- The cache includes:
  - `precomputed_complement`: The complementary color
  - `precomputed_hcts_by_temp`: HCT colors sorted by temperature
  - `precomputed_hcts_by_hue`: HCT colors sorted by hue
  - `precomputed_temps_by_hct`: Dictionary mapping HCT colors to temperatures

This caching mechanism makes repeated operations efficient, particularly when generating multiple color schemes from the same base color.

### Optimization for Default Analogous Colors

The class uses an internal flag `_from_default` to optimize performance when calling the default analogous colors method. This prevents redundant calculations when `get_analogous_colors_default()` calls `get_analogous_colors(5, 12)`.

## Usage Notes

* The component makes extensive use of the HCT color space, which is a perceptually accurate color system
* When generating analogous colors, the input color is always included as one of the returned colors
* Raw temperature is an absolute measure, while relative temperature is normalized to a 0-1 scale
* The complementary color is found by looking for a color with the inverse relative temperature of the input color
* Special cases are handled for colors with no temperature variation (like white or black)
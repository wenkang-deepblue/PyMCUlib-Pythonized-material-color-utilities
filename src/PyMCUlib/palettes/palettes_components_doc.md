# <center> Palettes Component Documentation </center>

## Overview

The Palettes component provides functionality for creating and working with color palettes based on the Material Design color system. It includes tools to create palettes of colors that vary in tone while maintaining consistent hue and chroma.

## Main Features

The Palettes component contains:

1. **TonalPalette** - A class that represents a palette of colors with the same hue and chroma but different tones
2. **KeyColor** - A helper class to find a key color that represents the hue and chroma of a tonal palette
3. **CorePalettes** - A structure that contains five tonal palettes that are used as the foundation for a color scheme

## Class Details

### CorePalettes

```python
@dataclass
class CorePalettes:
    """
    Comprises foundational palettes to build a color scheme. Generated from a
    source color, these palettes will then be part of a [DynamicScheme] together
    with appearance preferences.
    """
    primary: TonalPalette
    secondary: TonalPalette
    tertiary: TonalPalette
    neutral: TonalPalette
    neutral_variant: TonalPalette
```
A dataclass that comprises foundational palettes to build a color scheme. Generated from a source color, these palettes will then be part of a DynamicScheme together with appearance preferences.

### TonalPalette
```python
class TonalPalette:
    """
    A convenience class for retrieving colors that are constant in hue and chroma, but vary in tone.
    """
    
    def __init__(self, arg1, arg2=None, arg3=None):
        """
        Initialize a TonalPalette from various inputs:
        1. TonalPalette(argb) - from ARGB color
        2. TonalPalette(hct) - from HCT color
        3. TonalPalette(hue, chroma) - from hue and chroma values
        4. TonalPalette(hue, chroma, key_color) - from hue, chroma and key color
        """
```
A convenience class for retrieving colors that are constant in hue and chroma, but vary in tone.

#### Constructor Patterns
1. `TonalPalette(argb)` - Create from an ARGB color integer
2. `TonalPalette(hct)` - Create from an HCT color object
3. `TonalPalette(hue, chroma)` - Create from hue and chroma values
4. `TonalPalette(hue, chroma, key_color)` - Create from hue, chroma, and a key color

#### Methods
get
```python
def get(self, tone: float) -> Argb:
    """
    Returns the color for a given tone in this palette.
    
    Args:
        tone: 0.0 <= tone <= 100.0
        
    Returns:
        a color as an integer, in ARGB format.
    """
```
Parameters:
* `tone`: A tone value between 0.0 and 100.0
Returns:
* A color as an integer in ARGB format
get_hue
```python
def get_hue(self) -> float:
    # Returns the hue of this palette
```
Returns:
* The hue value of this palette (0.0 to 360.0)

get_chroma
```python
def get_chroma(self) -> float:
    # Returns the chroma of this palette
```
Returns:
* The chroma value of this palette

get_key_color
```python
def get_key_color(self) -> Hct:
    """Returns the key color of this palette."""
```
Returns:
* The key color of this palette as an Hct object
### KeyColor
```python
class KeyColor:
    """
    Key color is a color that represents the hue and chroma of a tonal palette
    """
    def __init__(self, hue: float, requested_chroma: float):
        """
        Initialize a KeyColor with hue and requested chroma.
        
        Args:
            hue: The hue value (0.0 to 360.0)
            requested_chroma: The requested chroma value
        """
```
A helper class that finds a key color representing the hue and chroma of a tonal palette. Internally, it uses a binary search algorithm and caching mechanism to efficiently find the closest possible tone that can provide the requested chroma.

#### Internal Properties

* `_hue`: The hue value
* `_requested_chroma`: The target chroma value
* `_max_chroma_value`: Maximum possible chroma value (200.0)
* `_chroma_cache`: A dictionary to cache maximum achievable chroma for each tone

#### Methods
create
```python
def create(self) -> Hct:
    # Creates a key color from a hue and a chroma
```
Returns:
* The key color in Hct format
max_chroma
```python
def max_chroma(self, tone: float) -> float:
    """
    Calculates the maximum achievable chroma for a given tone.
    
    Args:
        tone: The tone value
        
    Returns:
        Maximum achievable chroma
    """
```

Parameters:
* `tone`: The tone value (0.0 to 100.0)

Returns:
* Maximum achievable chroma for the given tone

```python
def create(self) -> Hct:
    """
    Creates a key color from a [hue] and a [chroma].
    The key color is the first tone, starting from T50, matching the given hue
    and chroma.
    
    Returns:
        Key color in Hct.
    """
```

Returns:
* The key color as an Hct object

The `create()` method uses a binary search algorithm pivoting around T50 (which typically has the most chroma available) to find the tone that can provide a chroma closest to the requested chroma.

## Usage Examples
### Creating and Using a Tonal Palette
```python
from PyMCUlib.palettes import TonalPalette
from PyMCUlib.utils.utils import hex_from_argb

# Create a tonal palette from a blue color
blue_color = 0xff0000ff
palette = TonalPalette(blue_color)

# Get colors at different tones
light_blue = palette.get(90)  # Lighter shade, tone 90
medium_blue = palette.get(50)  # Medium shade, tone 50
dark_blue = palette.get(10)   # Darker shade, tone 10

print(f"Light blue: {hex_from_argb(light_blue)}")
print(f"Medium blue: {hex_from_argb(medium_blue)}")
print(f"Dark blue: {hex_from_argb(dark_blue)}")
```
### Creating a Tonal Palette from Hue and Chroma
```python
from PyMCUlib.palettes import TonalPalette
from PyMCUlib.utils.utils import hex_from_argb

# Create a tonal palette with hue 120 (green) and chroma 50
green_palette = TonalPalette(120.0, 50.0)

# Print a few colors from the palette
for tone in [20, 40, 60, 80]:
    color = green_palette.get(tone)
    print(f"Tone {tone}: {hex_from_argb(color)}")
```

### Using CorePalettes

```python
from PyMCUlib.palettes import TonalPalette, CorePalettes
from PyMCUlib.utils.utils import hex_from_argb

# Create a TonalPalette from a primary color
primary_color = 0xff6750a4  # Purple

# Create a primary palette
primary_palette = TonalPalette(primary_color)

# Create a CorePalettes instance with custom palettes
core_palettes = CorePalettes(
    primary=primary_palette,
    secondary=TonalPalette(primary_palette.get_hue() + 60, 30.0),
    tertiary=TonalPalette(primary_palette.get_hue() + 120, 40.0),
    neutral=TonalPalette(primary_palette.get_hue(), 10.0),
    neutral_variant=TonalPalette(primary_palette.get_hue(), 15.0)
)

# Access colors from different palettes
primary_50 = core_palettes.primary.get(50)
secondary_60 = core_palettes.secondary.get(60)
tertiary_70 = core_palettes.tertiary.get(70)

print(f"Primary 50: {hex_from_argb(primary_50)}")
print(f"Secondary 60: {hex_from_argb(secondary_60)}")
print(f"Tertiary 70: {hex_from_argb(tertiary_70)}")
```
## Notes and Implementation Details

* All color values are represented in ARGB format as integers
* Tone values range from 0.0 (black) to 100.0 (white)
* Hue values range from 0.0 to 360.0 (degrees on a color wheel)
* Chroma values represent color purity/intensity (higher values are more vivid)

### KeyColor Binary Search Implementation

The `KeyColor.create()` method uses a binary search algorithm to find the optimal tone that can provide a chroma closest to the requested chroma:

1. It pivots around T50 (tone 50) because T50 typically has the most chroma available
2. It uses an epsilon value (0.01) to accept values slightly higher than the requested chroma
3. It searches within the tone range [0, 100] to find the optimal tone
4. For each iteration, it checks if the mid-tone has sufficient chroma
5. If sufficient chroma is found, it continues searching in the range closer to the pivot tone
6. If not, it follows the direction to the chroma peak

## Dependencies

This component depends on the following PyMCUlib modules:
* `PyMCUlib.utils.utils` - For ARGB color manipulation utilities
* `PyMCUlib.cam.cam` - For color appearance model functions
* `PyMCUlib.cam.hct` - For the HCT color space representation
# DynamicColor Module Documentation

## Overview

The DynamicColor module is a core component of Material Color Utilities (MCU) that enables theme colors to adjust dynamically based on context parameters such as light/dark mode, contrast levels, and theme style variants. This module powers the adaptive color system in Material Design, allowing colors to maintain appropriate contrast and aesthetic properties across different environments and accessibility requirements.

The module consists of several interconnected components that work together to calculate and provide dynamic colors that respond to various parameters defined in a DynamicScheme.

## Module Architecture

The DynamicColor module is organized into several files with carefully managed dependencies:

```
dynamiccolor/
├── color_spec_delegate.py     # Abstract base class defining delegate interfaces
├── color_spec.py              # Global spec instances and helper functions
├── color_spec_2021.py         # 2021 spec implementation 
├── color_spec_2025.py         # 2025 spec implementation (extends 2021 spec)
├── contrast_curve.py          # Contrast ratio calculations based on scheme contrast level
├── dynamic_color.py           # Core class for dynamic color calculations
├── dynamic_scheme.py          # Defines context parameters for dynamic colors
├── material_dynamic_colors.py # Material design's system of dynamic colors
├── tone_delta_pair.py         # Manages tone relationships between color pairs
└── variant.py                 # Enumeration of theme variants
```

### Dependency Management

**Important Note**: The original TypeScript implementation contained circular dependencies between files. These have been resolved in the Python implementation as follows:

1. The `ColorSpecDelegate` interface was extracted from `color_spec.py` into a separate file `color_spec_delegate.py`, which is imported by the other color spec files.

2. Circular dependencies between `dynamic_color.py` and `dynamic_scheme.py` were resolved using Python's `from __future__ import annotations` and strategic use of string-based type annotations.

## Key Components

### ColorSpecDelegate

The `ColorSpecDelegate` is an abstract base class that defines the interface for dynamic color specifications. It provides methods to calculate colors based on different criteria and contexts.

```python
class ColorSpecDelegate(ABC):
    """
    A delegate that provides the dynamic color constraints for
    MaterialDynamicColors.
    
    This is used to allow for different color constraints for different spec
    versions.
    """
    
    # Methods for main palette colors
    @abstractmethod
    def primary_palette_key_color(self) -> 'DynamicColor':
        pass
    
    # ... (many other abstract methods)
```

### ColorSpec (2021 and 2025 specs)

The module supports two specification versions: 2021 and 2025. The 2025 spec extends the 2021 spec with additional refinements and platform-specific behavior.

```python
# Get a specific spec implementation
def get_spec(spec_version: Literal['2021', '2025']) -> ColorSpecDelegate:
    """
    Returns the ColorSpecDelegate for the given spec version.
    """
    if spec_version == '2021':
        return spec_2021
    elif spec_version == '2025':
        return spec_2025
    else:
        raise ValueError(f"Unsupported spec version: {spec_version}")
```

### ContrastCurve

The `ContrastCurve` class represents a value that varies with the contrast level of a scheme, typically used to specify contrast requirements against a background. The four parameters correspond to contrast levels -1.0 (lowest), 0.0 (normal), 0.5 (medium), and 1.0 (highest), and its `get` method returns an interpolated value:

```python
class ContrastCurve:
    def __init__(self, low: float, normal: float, medium: float, high: float):
        """
        Initializes a ContrastCurve.

        Args:
            low: Value at contrast level -1.0.
            normal: Value at contrast level 0.0.
            medium: Value at contrast level 0.5.
            high: Value at contrast level 1.0.
        """
        self.low = low
        self.normal = normal
        self.medium = medium
        self.high = high

    def get(self, contrast_level: float) -> float:
        """
        Returns the value corresponding to the given contrast level.

        Args:
            contrast_level: A float in [-1.0, 1.0]. Values <= -1.0 return `low`,
                            values >= 1.0 return `high`, and intermediate
                            values are linearly interpolated.

        Returns:
            A float, typically in the range [1.0, 21.0] when representing
            WCAG contrast ratios.
        """
        if contrast_level <= -1.0:
            return self.low
        elif contrast_level < 0.0:
            return math_utils.lerp(self.low, self.normal, (contrast_level + 1.0) / 1.0)
        elif contrast_level < 0.5:
            return math_utils.lerp(self.normal, self.medium, contrast_level / 0.5)
        elif contrast_level < 1.0:
            return math_utils.lerp(self.medium, self.high, (contrast_level - 0.5) / 0.5)
        else:
            return self.high
```

### DynamicColor

Update the description to reflect that only the `from_palette` static constructor is currently supported in Python (there are no hex-code or hue/chroma constructors at this time):

```python
class DynamicColor:
    """
    A color that adjusts itself based on UI state provided by DynamicScheme.

    Colors without backgrounds keep a fixed tone regardless of contrast changes.
    Colors with backgrounds adjust their tone closer to the background at lower
    contrast levels and further at higher contrast levels.

    Static constructors:
      - from_palette: the only supported constructor in this Python port.
    """

    @staticmethod
    def from_palette(args: FromPaletteOptions) -> DynamicColor:
        """
        Create a DynamicColor defined by a TonalPalette and tone function.

        Args:
            args:
                name: Optional name of the color.
                palette: Function (scheme) -> TonalPalette.
                tone: Function (scheme) -> float tone value.
                is_background: Boolean indicating if this color is a background.
                background: Optional function (scheme) -> DynamicColor.
                second_background: Optional function (scheme) -> DynamicColor.
                chroma_multiplier: Optional function (scheme) -> float multiplier.
                contrast_curve: Optional function (scheme) -> ContrastCurve.
                tone_delta_pair: Optional function (scheme) -> ToneDeltaPair.

        Returns:
            A new DynamicColor instance.
        """
        # ...
```

### DynamicScheme

Provides context for a set of dynamic colors, including parameters like light/dark mode, contrast level, and theme variant:

```python
class DynamicScheme:
    """
    Constructed by a set of values representing the current UI state (such as
    whether or not its dark theme, what the theme style is, etc.), and
    provides a set of TonalPalettes that can create colors that fit in
    with the theme style. Used by DynamicColor to resolve into a color.
    """
    
    def __init__(self, args: DynamicSchemeOptions):
        """
        Initialize a dynamic scheme.
        """
        # ...
```

### MaterialDynamicColors

Provides a comprehensive set of dynamic colors used in Material Design:

```python
class MaterialDynamicColors:
    """
    DynamicColors for the colors in the Material Design system.
    """
    
    # Methods for accessing different Material Design colors
    def primary(self) -> DynamicColor:
        """
        Returns the primary color.
        """
        return MaterialDynamicColors._color_spec.primary()
    
    # ... (many other methods for different colors)
```

### ToneDeltaPair

Defines tone relationships between pairs of colors:

```python
class ToneDeltaPair:
    """
    Documents a constraint between two DynamicColors, in which their tones must
    have a certain distance from each other.

    Prefer a DynamicColor with a background, this is for special cases when
    designers want tonal distance, literally contrast, between two colors that
    don't have a background / foreground relationship or a contrast guarantee.
    """
    
    def __init__(
            self,
            role_a: 'DynamicColor',
            role_b: 'DynamicColor',
            delta: float,
            polarity: TonePolarity,
            stay_together: bool,
            constraint: Optional[DeltaConstraint] = None,
    ):
        # ...
```

### Variant

An enumeration of the theme variants supported by the system:

```python
class Variant(IntEnum):
    """
    Set of themes supported by Dynamic Color.
    Instantiate the corresponding subclass, ex. SchemeTonalSpot, to create
    colors corresponding to the theme.
    """
    MONOCHROME = 0
    NEUTRAL = 1
    TONAL_SPOT = 2
    VIBRANT = 3
    EXPRESSIVE = 4
    FIDELITY = 5
    CONTENT = 6
    RAINBOW = 7
    FRUIT_SALAD = 8
```

## Usage Examples

### Creating a DynamicScheme

```python
from PyMCUlib.hct.hct import Hct
from PyMCUlib.dynamiccolor.dynamic_scheme import DynamicScheme
from PyMCUlib.dynamiccolor.variant import Variant

# Create a source color using HCT
source_color = Hct.from_int(0xFF0000FF)  # Red in ARGB

# Create a dynamic scheme
scheme = DynamicScheme({
    'source_color_hct': source_color,
    'variant': Variant.TONAL_SPOT,  # Use the Tonal Spot theme style
    'contrast_level': 0.0,          # Standard contrast
    'is_dark': False,               # Light mode
    'platform': 'phone',            # Platform-specific adjustments
    'spec_version': '2025',         # Use 2025 spec
})
```

### Accessing Material Design Colors

```python
# Get the primary color as an ARGB integer
primary_color = scheme.primary

# Get the on-primary color as an ARGB integer
on_primary_color = scheme.on_primary

# Get the surface color
surface_color = scheme.surface
```

### Creating a Custom Dynamic Color

```python
from PyMCUlib.dynamiccolor.dynamic_color import DynamicColor
from PyMCUlib.dynamiccolor.contrast_curve import ContrastCurve

# Create a custom dynamic color based on the primary palette
custom_color = DynamicColor.from_palette({
    'name': 'custom_accent',
    'palette': lambda s: s.primary_palette,
    'tone': lambda s: 70 if s.is_dark else 30,
    'is_background': True,
    'background': lambda s: s.colors.surface_container(),
    'contrast_curve': lambda s: ContrastCurve(3, 4.5, 7, 11),
})

# Get the resulting color for the given scheme
custom_color_argb = custom_color.get_argb(scheme)
```

### Working with Tone Delta Pairs

```python
from PyMCUlib.dynamiccolor.tone_delta_pair import ToneDeltaPair

# Create two dynamic colors with a tone relationship
background = DynamicColor.from_palette({
    'name': 'background',
    'palette': lambda s: s.neutral_palette,
    'tone': lambda s: 90 if s.is_dark else 30,
    'is_background': True,
})

foreground = DynamicColor.from_palette({
    'name': 'foreground',
    'palette': lambda s: s.neutral_palette,
    'tone': lambda s: 20 if s.is_dark else 80,
    'is_background': False,
    'tone_delta_pair': lambda s: ToneDeltaPair(
        foreground, background, 15, 'lighter', True, 'exact'),
})
```

### Using Different Spec Versions

```python
from PyMCUlib.dynamiccolor.color_spec import get_spec

# Get a 2021 spec delegate
spec_2021 = get_spec('2021')

# Get a 2025 spec delegate
spec_2025 = get_spec('2025')

# Create a color using the 2025 spec
primary_2025 = spec_2025.primary()
```

## Advanced Topics

### Dynamic Color Calculation Process

The process of calculating a dynamic color involves several steps:

1. The `DynamicScheme` provides context parameters like theme variant, contrast level, and light/dark mode.
2. The appropriate `ColorSpecDelegate` is selected based on the spec version.
3. The delegate calculates the TonalPalette for each color role based on the scheme.
4. Each `DynamicColor` calculates its final tone by applying constraints like:
   - Contrast against background
   - Tone delta pairs with other colors
   - Adjustments based on contrast level
5. The final ARGB color is computed using the HCT color space.

### Dynamic Color Constraints

Dynamic colors can have several types of constraints:

1. **Background Contrast**: A color must maintain a certain contrast ratio with its background.
2. **Tone Delta Pairs**: Two colors must maintain a specific tonal distance from each other.
3. **Adjustments for Light/Dark**: Colors behave differently in light mode vs. dark mode.
4. **Platform-Specific Behavior**: Different platforms (phone, watch) may have different color behavior.
5. **Contrast Level Adjustments**: As contrast level changes, colors adjust to maintain readability.

## Implementation Notes

- Colors are represented internally using the HCT (Hue, Chroma, Tone) color space.
- All dynamic colors have an associated TonalPalette that preserves their hue and chroma.
- Tone values range from 0-100 (0 = black, 100 = white).
- Contrast ratios are calculated according to WCAG standards.
- The 2021 spec is the baseline, while the 2025 spec adds refinements.
- Material Design uses a specific set of dynamic colors with carefully calibrated relationships.

## Special Handling for Circular Dependencies

This module contains several circular dependencies that required special handling in the Python implementation:

1. **Color Spec Files**:
   - In TypeScript, `color_spec.ts`, `color_spec_2021.ts`, and `color_spec_2025.ts` had circular references.
   - In Python, we extracted the `ColorSpecDelegate` abstract base class into a separate file `color_spec_delegate.py`.
   - This allows all other files to import from the base delegate without creating cycles.

2. **DynamicColor and DynamicScheme**:
   - In TypeScript, these classes referenced each other.
   - In the Python implementation, we use `from __future__ import annotations` and string-based type hints.
   - For example: `def background(self) -> 'DynamicColor'` instead of `def background(self) -> DynamicColor`.

These approaches allow the Python code to maintain the same structure and relationships as the original TypeScript code without causing import errors.
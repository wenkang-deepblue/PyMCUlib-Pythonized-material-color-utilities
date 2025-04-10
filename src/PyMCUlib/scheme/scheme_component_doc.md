# <center> Scheme Component Documentation</center>

## Overview

The Scheme component is a central part of the Material Color Utilities library that provides various color scheme generators for Material Design 3. Each scheme transforms a source color into a comprehensive color palette suitable for user interfaces, following different aesthetic approaches.

Schemes serve as a bridge between raw colors and dynamic UI colors. They generate multiple coordinated tonal palettes that Material Dynamic Colors use to create specific UI colors (like primary, secondary, surface, etc.) with proper contrast ratios.

## Available Schemes

The Scheme component offers multiple scheme types, each with unique characteristics:

1. **SchemeMonochrome**: A monochromatic theme with a single hue at zero chroma (grayscale)
2. **SchemeNeutral**: A neutral theme with a single hue at very low chroma
3. **SchemeTonalSpot**: The standard Material You theme with complementary accent colors
4. **SchemeVibrant**: A theme with highly saturated colors for vibrant designs
5. **SchemeExpressive**: A theme with unconventional color choices for expressive designs
6. **SchemeFidelity**: A theme that preserves the source color exactly
7. **SchemeContent**: A theme that stays close to the source color
8. **SchemeRainbow**: A playful theme with high colorfulness
9. **SchemeFruitSalad**: A playful theme that uses colors unrelated to the source color

## Common Usage Pattern
All scheme classes follow the same basic usage pattern:

```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.monochrome import SchemeMonochrome
# Import other schemes as needed

# Create a source color in HCT format
source_color = Hct.from_int(0xff0000ff)  # Blue in ARGB format

# Create a scheme (light or dark variant)
light_scheme = SchemeMonochrome(source_color, is_dark=False)
dark_scheme = SchemeMonochrome(source_color, is_dark=True)

# Optionally specify contrast level (0.0 to 1.0)
high_contrast_scheme = SchemeMonochrome(source_color, is_dark=True, contrast_level=0.5)

# Access colors from the scheme (returns ARGB integer values)
primary_color = light_scheme.get_primary()  # returns int
on_primary_color = light_scheme.get_on_primary()  # returns int
primary_container = light_scheme.get_primary_container()  # returns int
```

## Class Relationships

```
                        ┌─────────────────┐
                        │   DynamicScheme │
                        └────────┬────────┘
                                 │
                                 │ extends
                                 ▼
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│  │ SchemeMonochrome│  │ SchemeVibrant   │  │ SchemeFidelity │ │
│  └─────────────────┘  └─────────────────┘  └────────────────┘ │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│  │ SchemeNeutral   │  │ SchemeExpressive│  │ SchemeContent  │ │
│  └─────────────────┘  └─────────────────┘  └────────────────┘ │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│  │ SchemeTonalSpot │  │ SchemeRainbow   │  │SchemeFruitSalad│ │
│  └─────────────────┘  └─────────────────┘  └────────────────┘ │
│                                                               │
└───────────────────────────────────────────────────────────────┘

    ┌─────────────┐    ┌───────────────┐    ┌─────────────────┐
    │     Hct     │    │  TonalPalette │    │TemperatureCache │
    └─────────────┘    └───────────────┘    └─────────────────┘
          ▲                   ▲                     ▲
          │                   │                     │
          └───────uses────────┴────────uses─────────┘
```

## Scheme Base Class
All schemes inherit from the `DynamicScheme` class, which provides:

* Access to tonal palettes
* Methods to access all dynamic colors (returning ARGB int values)
* Contrast level handling
* Light/dark theme variants

## Constructor Parameters
All scheme classes accept the following parameters:

* `source_color_hct`: A color in HCT format that serves as the basis for the scheme
* `is_dark`: A boolean indicating whether to generate a dark theme (true) or light theme (false)
* `contrast_level`: A float from 0.0 to 1.0 specifying the desired contrast level (default: 0.0)

## Tonal Palettes
Each scheme creates five tonal palettes with specific hue and chroma values:

1. __Primary Palette__: Used for primary UI elements
2. __Secondary Palette__: Used for secondary UI elements
3. __Tertiary Palette__: Used for accent elements
4. __Neutral Palette__: Used for backgrounds and surfaces
5. __Neutral Variant Palette__: Used for surface variants

These palettes are then accessed by Material Dynamic Colors to create the final UI colors.

## Available Colors
Through the `DynamicScheme` base class, all schemes provide the following color categories:

### Primary Colors
* `get_primary() -> int`: The primary color
* `get_on_primary() -> int`: Color for content on the primary color
* `get_primary_container() -> int`: Container color derived from primary
* `get_on_primary_container() -> int`: Color for content on primary container
* `get_inverse_primary() -> int`: Opposite of the primary color

### Secondary Colors
* `get_secondary() -> int`: The secondary color
* `get_on_secondary() -> int`: Color for content on the secondary color
* `get_secondary_container() -> int`: Container color derived from secondary
* `get_on_secondary_container() -> int`: Color for content on secondary container

### Tertiary Colors
* `get_tertiary() -> int`: The tertiary color
* `get_on_tertiary() -> int`: Color for content on the tertiary color
* `get_tertiary_container() -> int`: Container color derived from tertiary
* `get_on_tertiary_container() -> int`: Color for content on tertiary container

### Surface Colors
* `get_surface() -> int`: The main surface color
* `get_on_surface() -> int`: Color for content on the surface
* `get_surface_variant() -> int`: An alternative surface color
* `get_on_surface_variant() -> int`: Color for content on surface variant
* `get_surface_bright() -> int`: A brighter surface color
* `get_surface_dim() -> int`: A dimmer surface color
* `get_surface_container_lowest() -> int`: Lowest container surface
* `get_surface_container_low() -> int`: Low container surface
* `get_surface_container() -> int`: Standard container surface
* `get_surface_container_high() -> int`: High container surface
* `get_surface_container_highest() -> int`: Highest container surface

### Other Colors
* `get_outline() -> int`: Color for UI outlines
* `get_outline_variant() -> int`: Variant color for UI outlines
* `get_shadow() -> int`: Color for shadows
* `get_scrim() -> int`: Color for scrims
* `get_inverse_surface() -> int`: Opposite of the surface color
* `get_inverse_on_surface() -> int`: Color for content on inverse surface
* `get_surface_tint() -> int`: Tint color for surfaces

### Error Colors
* `get_error() -> int`: The error color
* `get_on_error() -> int`: Color for content on the error color
* `get_error_container() -> int`: Container color derived from error
* `get_on_error_container() -> int`: Color for content on error container

### Fixed Colors
* `get_primary_fixed() -> int`: Fixed primary color
* `get_primary_fixed_dim() -> int`: Dimmed fixed primary color
* `get_on_primary_fixed() -> int`: Color for content on fixed primary
* `get_on_primary_fixed_variant() -> int`: Variant for content on fixed primary
* `get_secondary_fixed() -> int`: Fixed secondary color
* `get_secondary_fixed_dim() -> int`: Dimmed fixed secondary color
* `get_on_secondary_fixed() -> int`: Color for content on fixed secondary
* `get_on_secondary_fixed_variant() -> int`: Variant for content on fixed secondary
* `get_tertiary_fixed() -> int`: Fixed tertiary color
* `get_tertiary_fixed_dim() -> int`: Dimmed fixed tertiary color
* `get_on_tertiary_fixed() -> int`: Color for content on fixed tertiary
* `get_on_tertiary_fixed_variant() -> int`: Variant for content on fixed tertiary

## Scheme Comparison
| Scheme | Primary | Secondary | Tertiary | Distinctive Feature | Best Used For |
| ------ | ------- | --------- | -------- | ------------------ | ------------ |
| Monochrome | Source hue, 0.0 chroma | Source hue, 0.0 chroma | Source hue, 0.0 chroma | Single hue, grayscale | Minimalist designs, photo editing apps, text-focused applications |
| Neutral | Source hue, 12.0 chroma | Source hue, 8.0 chroma | Source hue, 16.0 chroma | Single hue, low chroma | Professional applications, document editors, reading apps |
| TonalSpot | Source hue, 36.0 chroma | Source hue, 16.0 chroma | Source hue + 60°, 24.0 chroma | Standard Material You | Most applications, balanced designs, consumer apps |
| Vibrant | Source hue, 200.0 chroma | Rotated hue, 24.0 chroma | Different rotated hue, 32.0 chroma | Highly saturated colors | Entertainment apps, games, social media, youth-oriented applications |
| Expressive | Source hue + 240°, 40.0 chroma | Rotated hue, 24.0 chroma | Different rotated hue, 32.0 chroma | Unconventional colors | Creative applications, art platforms, unconventional brands |
| Fidelity | Source hue & chroma | Source hue, reduced chroma | Complementary color | Preserves source color exactly | Brand-focused applications, color-critical workflows |
| Content | Source hue & chroma | Source hue, reduced chroma | Analogous color | Close to source color | Content-focused apps, news platforms, information displays |
| Rainbow | Source hue, 48.0 chroma | Source hue, 16.0 chroma | Source hue + 60°, 24.0 chroma | High colorfulness | Kids applications, educational software, playful designs |
| FruitSalad | Source hue - 50°, 48.0 chroma | Source hue - 50°, 36.0 chroma | Source hue, 36.0 chroma | Unrelated to source color | Playful applications, celebrations, distinctly creative contexts |

## Complete Example
```python
from PyMCUlib.cam.hct import Hct
from PyMCUlib.scheme.tonal_spot import SchemeTonalSpot
from PyMCUlib.scheme.vibrant import SchemeVibrant
from PyMCUlib.scheme.monochrome import SchemeMonochrome

# Create a source color
source_color = Hct.from_int(0xff4285F4)  # Google Blue

# Create different schemes from the same source color
standard_scheme = SchemeTonalSpot(source_color, is_dark=False)
vibrant_scheme = SchemeVibrant(source_color, is_dark=False)
mono_scheme = SchemeMonochrome(source_color, is_dark=False)

# Create a simple UI with different colors
def create_ui(scheme):
    return {
        'background': scheme.get_background(),  # Returns ARGB int
        'surface': scheme.get_surface(),  # Returns ARGB int
        'primary_button': {
            'background': scheme.get_primary(),  # Returns ARGB int
            'text': scheme.get_on_primary(),  # Returns ARGB int
        },
        'secondary_button': {
            'background': scheme.get_secondary_container(),  # Returns ARGB int
            'text': scheme.get_on_secondary_container(),  # Returns ARGB int
        },
        'card': {
            'background': scheme.get_surface_container(),  # Returns ARGB int
            'title': scheme.get_on_surface(),  # Returns ARGB int
            'body': scheme.get_on_surface_variant(),  # Returns ARGB int
            'outline': scheme.get_outline(),  # Returns ARGB int
        },
        'accent': scheme.get_tertiary(),  # Returns ARGB int
    }

# Get UI colors for different schemes
standard_ui = create_ui(standard_scheme)
vibrant_ui = create_ui(vibrant_scheme)
mono_ui = create_ui(mono_scheme)
```

## Detailed Scheme Documentation

### SchemeMonochrome
A monochromatic theme with a single hue at zero chroma (grayscale).

**Characteristics:**
- All palettes use the source color's hue with 0.0 chroma
- Creates a true monochromatic (grayscale) palette
- Variations come only from tone differences

**Best For:**
- Minimalist interfaces
- Photo editing applications
- Text-heavy applications
- When color might be distracting

### SchemeNeutral
A neutral theme with a single hue at very low chroma.

**Characteristics:**
- Primary palette: source hue, 12.0 chroma
- Secondary palette: source hue, 8.0 chroma
- Tertiary palette: source hue, 16.0 chroma
- Neutral and neutral variant palettes: source hue, 2.0 chroma

**Best For:**
- Professional applications
- Document editors
- Reading applications
- Subtle, sophisticated designs

### SchemeTonalSpot
The standard Material You theme with complementary accent colors.

**Characteristics:**
- Primary palette: source hue, 36.0 chroma
- Secondary palette: source hue, 16.0 chroma
- Tertiary palette: source hue + 60°, 24.0 chroma
- Neutral palette: source hue, 6.0 chroma
- Neutral variant palette: source hue, 8.0 chroma

**Best For:**
- Most general applications
- Balanced designs
- When following standard Material Design 3 guidelines
- Consumer applications

### SchemeVibrant
A theme with highly saturated colors for vibrant designs.

**Characteristics:**
- Primary palette: source hue, 200.0 chroma (extremely vibrant)
- Secondary palette: rotated hue, 24.0 chroma
- Tertiary palette: different rotated hue, 32.0 chroma
- Uses hue rotation algorithms for secondary and tertiary colors

**Best For:**
- Entertainment applications
- Games
- Social media platforms
- Youth-oriented applications
- Brands wanting to appear energetic

### SchemeExpressive
A theme with unconventional color choices for expressive designs.

**Characteristics:**
- Primary palette: source hue + 240°, 40.0 chroma
- Secondary palette: rotated hue, 24.0 chroma
- Tertiary palette: different rotated hue, 32.0 chroma
- Dramatically shifts the primary color's hue by 240 degrees

**Best For:**
- Creative applications
- Art platforms
- Unconventional brands
- Expressive, artistic interfaces
- When breaking design norms is desired

### SchemeFidelity
A theme that preserves the source color exactly.

**Characteristics:**
- Primary palette: exact source hue and chroma
- Secondary palette: source hue, reduced chroma
- Tertiary palette: complementary color
- Uses TemperatureCache to find complementary colors

**Best For:**
- Brand-focused applications
- Color-critical workflows
- When maintaining exact color fidelity is essential
- When the source color must be preserved precisely

### SchemeContent
A theme that stays close to the source color.

**Characteristics:**
- Primary palette: exact source hue and chroma
- Secondary palette: source hue, reduced chroma
- Tertiary palette: analogous color
- Uses TemperatureCache to find analogous colors

**Best For:**
- Content-focused applications
- News platforms
- Information displays
- When source color should be prominent but not isolated

### SchemeRainbow
A playful theme with high colorfulness.

**Characteristics:**
- Primary palette: source hue, 48.0 chroma
- Secondary palette: source hue, 16.0 chroma
- Tertiary palette: source hue + 60°, 24.0 chroma
- High chroma values create vibrant, colorful designs

**Best For:**
- Kids applications
- Educational software
- Playful designs
- Celebratory interfaces
- Applications targeting creative or young audiences

### SchemeFruitSalad
A playful theme that uses colors unrelated to the source color.

**Characteristics:**
- Primary palette: source hue - 50°, 48.0 chroma
- Secondary palette: source hue - 50°, 36.0 chroma
- Tertiary palette: source hue, 36.0 chroma
- Significant hue shifts create diverse, unrelated colors

**Best For:**
- Playful applications
- Celebrations
- Distinctly creative contexts
- When color diversity is more important than harmony
- Applications for children or creative exploration

## Related Components

* **Hct**: Color representation using Hue, Chroma, and Tone
* **DynamicScheme**: Base class for all schemes
* **TonalPalette**: Creates colors of different tones from a fixed hue and chroma
* **MaterialDynamicColors**: Uses schemes to generate UI colors with proper contrast
* **TemperatureCache**: Used by some schemes to find complementary and analogous colors
* **Dislike**: Used to avoid unpleasant colors (yellow-greens) in some schemes
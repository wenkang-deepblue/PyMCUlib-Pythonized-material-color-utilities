# scheme/__init__.py

# --- scheme ---
from PyMCUlib.scheme.scheme import Scheme

# --- scheme_android ---
from PyMCUlib.scheme.scheme_android import SchemeAndroid

# --- scheme_neutral ---
from PyMCUlib.scheme.scheme_neutral import SchemeNeutral

# --- scheme_expressive ---
from PyMCUlib.scheme.scheme_expressive import SchemeExpressive

# --- scheme_tonal_spot ---
from PyMCUlib.scheme.scheme_tonal_spot import SchemeTonalSpot

# --- scheme_rainbow ---
from PyMCUlib.scheme.scheme_rainbow import SchemeRainbow

# --- scheme_content ---
from PyMCUlib.scheme.scheme_content import SchemeContent

# --- scheme_fidelity ---
from PyMCUlib.scheme.scheme_fidelity import SchemeFidelity

# --- scheme_vibrant ---
from PyMCUlib.scheme.scheme_vibrant import SchemeVibrant

# --- scheme_monochrome ---
from PyMCUlib.scheme.scheme_monochrome import SchemeMonochrome

# --- scheme_fruit_salad ---
from PyMCUlib.scheme.scheme_fruit_salad import SchemeFruitSalad

__all__ = [
    # scheme
    "Scheme",
    # scheme_android
    "SchemeAndroid",
    # scheme_neutral
    "SchemeNeutral",
    # scheme_expressive
    "SchemeExpressive",
    # scheme_tonal_spot
    "SchemeTonalSpot",
    # scheme_rainbow
    "SchemeRainbow",
    # scheme_content
    "SchemeContent",
    # scheme_fidelity
    "SchemeFidelity",
    # scheme_vibrant
    "SchemeVibrant",
    # scheme_monochrome
    "SchemeMonochrome",
    # scheme_fruit_salad
    "SchemeFruitSalad",
]
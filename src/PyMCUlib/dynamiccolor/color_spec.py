# dynamiccolor/color_spec.py

from typing import Literal

from PyMCUlib.dynamiccolor.color_spec_delegate import ColorSpecDelegate
from PyMCUlib.dynamiccolor.color_spec_2021 import ColorSpecDelegateImpl2021
from PyMCUlib.dynamiccolor.color_spec_2025 import ColorSpecDelegateImpl2025

# Instantiate delegates for each spec version
spec_2021 = ColorSpecDelegateImpl2021()
spec_2025 = ColorSpecDelegateImpl2025()

def get_spec(spec_version: Literal['2021', '2025']) -> ColorSpecDelegate:
    """
    Returns the ColorSpecDelegate for the given spec version.
    
    Args:
        spec_version: The specification version, either '2021' or '2025'
        
    Returns:
        The appropriate ColorSpecDelegate implementation
    """
    if spec_version == '2021':
        return spec_2021
    if spec_version == '2025':
        return spec_2025
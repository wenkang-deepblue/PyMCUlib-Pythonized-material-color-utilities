"""
mcu_python library

This package allows importing mcu_python modules directly from the src directory.
This is a forwarding import, exposing all public APIs from the mcu_python package to users.
"""

# Import all public APIs from the mcu_python package
from PyMCUlib_cpp import *

# The version number should match the subpackage
from PyMCUlib_cpp import __version__

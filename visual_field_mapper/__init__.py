# -*- coding: utf-8 -*-

from .point import Point
from .visual_field import VisualField


"""Top-level package for napari-aicsimageio."""

__author__ = "Erik Jönsson"
__email__ = "efjonsson@gmail.com"
__version__ = "0.0.1"


def get_module_version() -> str:
    return __version__

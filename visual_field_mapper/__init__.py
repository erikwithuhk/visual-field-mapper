# -*- coding: utf-8 -*-

from enum import Enum
from typing import NamedTuple

__author__ = "Erik Jönsson"
__email__ = "efjonsson@gmail.com"
__version__ = "0.0.1"


class Colors(Enum):
    black = "#000"
    gray = "#ddd"
    blue = "#386cb0"
    green = "#7fc97f"
    orange = "#fdc086"
    pink = "#f0027f"
    purple = "#beaed4"
    red = "#be1e2d"
    white = "#fff"
    yellow = "#ffff99"


class Dimensions(NamedTuple):
    width: int
    height: int


class Position(NamedTuple):
    x: int
    y: int


def get_module_version() -> str:
    return __version__

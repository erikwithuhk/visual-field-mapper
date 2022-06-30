# -*- coding: utf-8 -*-

from enum import Enum
from pathlib import Path
from typing import NamedTuple, Union

__author__ = "Erik Jönsson"
__email__ = "efjonsson@gmail.com"
__version__ = "0.0.1"


BASE_DIR = Path(__file__).parent.parent.resolve()
ASSETS_DIR = BASE_DIR.joinpath("assets")
DATA_DIR = BASE_DIR.joinpath("data")
OUT_DIR = BASE_DIR.joinpath("out")
IMAGE_DIR = OUT_DIR.joinpath("images")
SVG_DIR = IMAGE_DIR.joinpath("SVG")
PNG_DIR = IMAGE_DIR.joinpath("PNG")
ARCHETYPE_DIR = IMAGE_DIR.joinpath("archetypes")

NORMAL_DATA_FILEPATH = DATA_DIR.joinpath("normal.csv")
STUDY_DATA_FILEPATH = DATA_DIR.joinpath("study.csv")
ARCHETYPE_DATA_FILEPATH = DATA_DIR.joinpath("archetypal_analysis.csv")

NORMAL_MEAN_TD_BY_SECTOR_FILEPATH = OUT_DIR.joinpath("normal_mean_td_by_sector.csv")
NORMAL_AGGREGATE_STATS_FILEPATH = OUT_DIR.joinpath("normal_aggregate_stats.csv")
ARCHETYPE_FILL_COLORS_FILEPATH = OUT_DIR.joinpath("archetype_fill_colors.csv")


class Colors(Enum):
    black = "#333"
    gray = "#bebebe"
    blue = "#386cb0"
    green = "#7fc97f"
    orange = "#fdc086"
    pink = "#f0027f"
    purple = "#beaed4"
    red = "#ff1a09"
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

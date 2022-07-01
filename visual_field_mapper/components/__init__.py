from typing import Union

from visual_field_mapper import Dimensions

BASE_FONT_SIZE = 16.0
CELL_DIMENSIONS = Dimensions(50, 50)


def rem(num: Union[float, int]) -> float:
    return num * BASE_FONT_SIZE

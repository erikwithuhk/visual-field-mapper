from typing import Union

BASE_FONT_SIZE = 16.0


def rem(num: Union[float, int]) -> float:
    return num * BASE_FONT_SIZE

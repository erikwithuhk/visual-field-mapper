from typing import Union

from .. import Dimensions, Position


def is_numeric(x):
    return type(x) == float or type(x) == int


class BaseComponent:
    def __init__(
        self,
        width: Union[float, int] = 0,
        height: Union[float, int] = 0,
        margin: Union[float, int] = 0,
        margin_top: Union[float, int] = 0,
        margin_bottom: Union[float, int] = 0,
        margin_left: Union[float, int] = 0,
        margin_right: Union[float, int] = 0,
        position: Position = Position(0, 0),
    ):
        self.width = width
        self.height = height
        self.margin_top = margin or margin_top
        self.margin_bottom = margin or margin_bottom
        self.margin_left = margin or margin_left
        self.margin_right = margin or margin_right
        self.position = position
        self.size = Dimensions(
            self.margin_left + self.width + self.margin_right,
            self.margin_top + self.height + self.margin_bottom,
        )

    def get_position(self):
        x = self.position.x
        y = self.position.y

        if is_numeric(x):
            x = x + self.margin_left

        if is_numeric(y):
            y = y + self.margin_top

        return Position(x, y)

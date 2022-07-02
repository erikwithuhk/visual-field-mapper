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
        self.initial_position = self.get_position()
        self.size = Dimensions(
            self.margin_left + self.width + self.margin_right,
            self.margin_top + self.height + self.margin_bottom,
        )
        self.x = self.initial_position.x
        self.y = self.initial_position.y
        self.children = []

    def reset_x(self):
        self.width = max(self.width, self.x)
        self.x = self.initial_position.x

    def reset_y(self):
        self.height = max(self.height, self.y)
        self.y = self.initial_position.y

    def add_height(self, height):
        self.y += height

    def add_child(self, component):
        self.children.append(component)
        self.x += component.size.width

    def get_position(self):
        x = self.position.x or 0
        y = self.position.y or 0

        if is_numeric(x):
            x = x + self.margin_left

        if is_numeric(y):
            y = y + self.margin_top

        return Position(x, y)

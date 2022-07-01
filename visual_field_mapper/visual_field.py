from enum import Enum
from pprint import pformat
from typing import List, NamedTuple

import drawSvg as draw

from visual_field_mapper import Colors, Dimensions, Position


class Eye(Enum):
    od = "od"
    os = "os"


class Fill(NamedTuple):
    color: str
    opacity: float


class Point:
    lower_limit = -35
    upper_limit = 10
    range = abs(upper_limit - lower_limit)

    def __init__(self, position: int, total_deviation: int = None, color: str = None):
        if position < 1 or position > 54:
            raise ValueError(
                f"Point position must be between 1 and 54, received <{position}>."
            )

        self.position = position
        self.total_deviation = total_deviation
        self.fill = Fill(color, 1.0) if color else self.__get_fill()

    def __repr__(self) -> str:
        return pformat(vars(self))

    def is_blind_spot(self) -> bool:
        return self.total_deviation == None

    def __get_fill(self) -> Fill:
        if self.is_blind_spot():
            return Fill(Colors.black.value, 1.0)
        if self.total_deviation <= Point.upper_limit:
            return Fill(
                Colors.red.value,
                1 - round((self.total_deviation + 35) / Point.range, 2),
            )
        else:
            return Fill(Colors.white.value, 0.0)

    def draw(self, dimensions: Dimensions, position: Position) -> draw.Group:
        rect = draw.Rectangle(
            position.x,
            position.y,
            dimensions.width,
            dimensions.height,
            fill=self.fill.color,
            fill_opacity=self.fill.opacity,
        )

        dot = draw.Circle(
            position.x + dimensions.width / 2,
            position.y + dimensions.height / 2,
            3,
            fill=Colors.black.value,
        )
        return draw.Group([rect, dot])


class VisualField:
    def __init__(self, eye: Eye, points: List[Point]):
        self.eye = eye
        self.points = points

    def __repr__(self) -> str:
        return pformat(vars(self))

    def __create_row(self, points: List[Point]) -> List[Point]:
        row = []

        if len(points) == 4:
            row.extend([None, None, None])
            row.extend(points)
            row.extend([None, None])
        elif len(points) == 6:
            row.extend([None, None])
            row.extend(points)
            row.extend([None])
        elif len(points) == 8:
            row.append(None)
            row.extend(points)
        elif len(points) == 9:
            row = points
        else:
            raise Exception(f"No rule for points length <{len(points)}>.")

        return row

    def to_matrix(self) -> List[List[Point]]:
        rows = [
            self.__create_row(points)
            for points in [
                self.points[0:4],
                self.points[4:10],
                self.points[10:18],
                self.points[18:27],
                self.points[27:36],
                self.points[36:44],
                self.points[44:50],
                self.points[50:],
            ]
        ]

        return rows

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

    def draw_outline(
        self, cell_dimensions: Dimensions, position: Position = None
    ) -> draw.Lines:
        fill_opacity = 0
        stroke = Colors.black.value
        stroke_width = 4
        transform = f"translate({position.x},{position.y})" if position else None

        return draw.Lines(
            3 * cell_dimensions.width,
            0 * -cell_dimensions.height,
            7 * cell_dimensions.width,
            0 * -cell_dimensions.height,
            7 * cell_dimensions.width,
            1 * -cell_dimensions.height,
            8 * cell_dimensions.width,
            1 * -cell_dimensions.height,
            8 * cell_dimensions.width,
            2 * -cell_dimensions.height,
            9 * cell_dimensions.width,
            2 * -cell_dimensions.height,
            9 * cell_dimensions.width,
            6 * -cell_dimensions.height,
            8 * cell_dimensions.width,
            6 * -cell_dimensions.height,
            8 * cell_dimensions.width,
            7 * -cell_dimensions.height,
            7 * cell_dimensions.width,
            7 * -cell_dimensions.height,
            7 * cell_dimensions.width,
            8 * -cell_dimensions.height,
            3 * cell_dimensions.width,
            8 * -cell_dimensions.height,
            3 * cell_dimensions.width,
            7 * -cell_dimensions.height,
            2 * cell_dimensions.width,
            7 * -cell_dimensions.height,
            2 * cell_dimensions.width,
            6 * -cell_dimensions.height,
            1 * cell_dimensions.width,
            6 * -cell_dimensions.height,
            1 * cell_dimensions.width,
            5 * -cell_dimensions.height,
            0 * cell_dimensions.width,
            5 * -cell_dimensions.height,
            0 * cell_dimensions.width,
            3 * -cell_dimensions.height,
            1 * cell_dimensions.width,
            3 * -cell_dimensions.height,
            1 * cell_dimensions.width,
            2 * -cell_dimensions.height,
            2 * cell_dimensions.width,
            2 * -cell_dimensions.height,
            2 * cell_dimensions.width,
            1 * -cell_dimensions.height,
            3 * cell_dimensions.width,
            1 * -cell_dimensions.height,
            3 * cell_dimensions.width,
            0 * -cell_dimensions.height,
            fill_opacity=fill_opacity,
            stroke=stroke,
            stroke_width=stroke_width,
            transform=transform,
        )

    def __draw_row(
        self, points: List[Point], cell_dimensions: Dimensions, position: Position
    ) -> draw.Group:
        return draw.Group(
            [
                point.draw(
                    cell_dimensions,
                    Position(i * cell_dimensions.width, -cell_dimensions.height),
                )
                for i, point in enumerate(points)
                if point
            ],
            transform=f"translate({position.x},{position.y})" if position else None,
        )

    def draw(
        self, cell_dimensions: Dimensions, position: Position = None
    ) -> draw.Group:
        matrix = self.to_matrix()
        rows = [
            self.__draw_row(
                row, cell_dimensions, Position(0, i * cell_dimensions.height)
            )
            for i, row in enumerate(matrix)
        ]
        outline = self.draw_outline(cell_dimensions)
        rows.append(outline)
        return draw.Group(
            rows,
            transform=f"translate({position.x},{position.y})" if position else None,
        )

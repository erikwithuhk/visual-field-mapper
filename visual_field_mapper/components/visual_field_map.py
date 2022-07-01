from enum import Enum
from pprint import pformat
from typing import List, NamedTuple

import drawSvg as draw

from .. import Colors, Dimensions, Position
from ..visual_field import Point, VisualField
from . import CELL_DIMENSIONS, rem
from .base_component import BaseComponent


class Eye(Enum):
    od = "od"
    os = "os"


class Fill(NamedTuple):
    color: str
    opacity: float


class VisualFieldMap(BaseComponent):
    def __init__(self, visual_field: VisualField, *args, **kwargs):
        self.visual_field = visual_field
        width = CELL_DIMENSIONS.width * 9
        height = CELL_DIMENSIONS.height * 8
        super().__init__(width, height, *args, margin=rem(2), **kwargs)

    def __repr__(self) -> str:
        return pformat(vars(self))

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

    def render(self) -> draw.Group:
        matrix = self.visual_field.to_matrix()
        rows = [
            self.__draw_row(
                row, CELL_DIMENSIONS, Position(0, i * CELL_DIMENSIONS.height)
            )
            for i, row in enumerate(matrix)
        ]
        outline = self.draw_outline(CELL_DIMENSIONS)
        rows.append(outline)
        position = self.get_position()

        return draw.Group(
            rows,
            x=position.x,
            y=position.y,
            transform=f"translate({position.x},{position.y})",
        )

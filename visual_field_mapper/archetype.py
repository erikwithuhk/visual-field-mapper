from pprint import pformat
from typing import List

import drawSvg as draw

from visual_field_mapper import Dimensions, Position

from .visual_field import Point, VisualField


class Archetype:
    @classmethod
    def parse(self, id: int, fill_colors: List[str]):
        points = [Point(i + 1, color=color) for i, color in enumerate(fill_colors)]
        visual_field = VisualField(None, points)
        return Archetype(id, visual_field)

    def __init__(self, id, visual_field: VisualField):
        self.id = id
        self.visual_field = visual_field

    def __repr__(self) -> str:
        return pformat(vars(self))

    def render(self):
        cell_dimensions = Dimensions(50, 50)
        width = cell_dimensions.width * 9
        height = cell_dimensions.height * 8

        svg = draw.Drawing(
            width,
            height,
            origin=(0, -height),
            displayInline=False,
        )
        svg.append(self.visual_field.draw(cell_dimensions, Position(0, 0)))
        return svg

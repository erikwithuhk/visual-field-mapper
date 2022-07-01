from pprint import pformat
from typing import List

import drawSvg as draw

from visual_field_mapper.components.visual_field_map import VisualFieldMap
from visual_field_mapper.components.base_component import BaseComponent

from .visual_field import Point, VisualField


class Archetype(BaseComponent):
    @classmethod
    def parse(self, id: int, fill_colors: List[str]):
        self.colors = fill_colors
        points = [Point(i + 1, color=color) for i, color in enumerate(fill_colors)]
        visual_field = VisualField(None, points)
        return Archetype(id, visual_field)

    def __init__(self, id, visual_field: VisualField, *args, **kwargs):
        self.id = id
        self.visual_field = visual_field
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return pformat(vars(self))

    def render(self):

        visual_field_map = VisualFieldMap(self.visual_field)

        height = visual_field_map.size.height
        svg = draw.Drawing(
            visual_field_map.size.width,
            height,
            origin=(0, -height),
            displayInline=False,
        )

        svg.append(visual_field_map.render())
        return svg

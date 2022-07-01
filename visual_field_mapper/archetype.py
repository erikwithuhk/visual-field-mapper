from pprint import pformat
from typing import List

from .visual_field import Point, VisualField


class Archetype:
    @classmethod
    def parse(self, id: int, fill_colors: List[str]):
        self.colors = fill_colors
        points = [
            Point(i + 1, color=color if type(color) == str else None)
            for i, color in enumerate(fill_colors)
        ]
        visual_field = VisualField(None, points)
        return Archetype(id, visual_field)

    def __init__(self, id, visual_field: VisualField):
        self.id = id
        self.visual_field = visual_field

    def __repr__(self) -> str:
        return pformat(vars(self))

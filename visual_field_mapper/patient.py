from pprint import pformat
from typing import Dict, List

import drawSvg as draw

from . import Colors, Dimensions, Position
from .archetype import Archetype
from .components import rem
from .components.garway_heath_view import GarwayHeathView
from .components.table import Table
from .components.typography import H1
from .components.visual_field_map import VisualFieldMap
from .garway_heath import GarwayHeathSectorization
from .visual_field import Point, VisualField


class Patient:
    def _parse_archetype_id():
        pass

    @classmethod
    def parse(self, id, row, archetypes_by_id: Dict[int, Archetype]):
        points = []

        for i in range(1, 55):
            if i == 26 or i == 35:
                points.append(Point(i, None))
            else:
                points.append(Point(i, int(row.loc[f"td{i}"])))

        visual_field = VisualField(row.Eye, points)
        matching_archetypes = [
            archetypes_by_id[archetype_id] for archetype_id in row.matching_archetypes
        ]
        patient = Patient(id, visual_field, matching_archetypes)
        return patient

    def __init__(
        self, id: int, visual_field: VisualField, matching_archetypes: List[Archetype]
    ):
        self.id = id
        self.visual_field = visual_field
        self.matching_archetypes = matching_archetypes

    def render(self, limits_by_sector):
        self.margin = rem(6)
        self.x = self.margin
        self.y = self.margin

        def reset_row():
            self.x = self.margin

        def add_height(height):
            self.y += height

        children = []

        def add_child(component):
            children.append(component)
            self.x += component.size.width

        title = H1(f"Patient #{self.id}", position=Position("50%", self.y))
        add_child(title)

        reset_row()
        add_height(title.size.height)

        visual_field_map = VisualFieldMap(
            self.visual_field, position=Position(self.x, self.y)
        )
        add_child(visual_field_map)

        garway_heath = GarwayHeathSectorization(self.visual_field)
        garway_heath_view = GarwayHeathView(
            garway_heath, limits_by_sector, position=Position(self.x, self.y)
        )
        add_child(garway_heath_view)

        means_by_sector = garway_heath.get_means_by_sector()
        table = Table(
            [
                list(means_by_sector.keys()),
                list(means_by_sector.values()),
            ],
            headers=["Sector", "Average TD"],
            col_widths=[75, 115],
            position=Position(self.x, self.y + rem(8)),
        )
        add_child(table)

        add_height(max(visual_field_map.size.height, garway_heath_view.size.height))

        svg_dimensions = Dimensions(
            self.x + self.margin,
            self.y + self.margin,
        )

        svg = draw.Drawing(
            svg_dimensions.width,
            svg_dimensions.height,
            origin=(0, -svg_dimensions.height),
            displayInline=False,
        )

        background = draw.Rectangle(
            0,
            -svg_dimensions.height,
            svg_dimensions.width,
            svg_dimensions.height,
            fill=Colors.white.value,
            stroke=Colors.black.value,
            stroke_width=2,
        )

        svg.append(background)
        [svg.append(child.render()) for child in children]
        return svg

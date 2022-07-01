import logging
from pprint import pformat
from typing import Dict, List

import drawSvg as draw

from visual_field_mapper import Colors, Dimensions, Position
from visual_field_mapper.components import rem
from visual_field_mapper.components.typography import H1

from .archetype import Archetype
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
        margin = rem(6)

        children = []

        title = H1(f"Patient #{self.id}", position=Position("50%", margin))
        children.append(title)

        ###

        cell_dimensions = Dimensions(50, 50)
        drawing_dimensions = Dimensions(
            9 * cell_dimensions.width, 8 * cell_dimensions.height
        )

        table_width = 200
        svg_dimensions = Dimensions(
            drawing_dimensions.width * 2 + table_width + margin * 4,
            title.size.height + drawing_dimensions.height + margin * 3,
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
        # svg.append(title.render())

        position_y = title.size.height + margin * 2

        visual_field_position = Position(margin, position_y)
        visual_field_map = self.visual_field.draw(
            cell_dimensions, visual_field_position
        )
        svg.append(visual_field_map)

        garway_heath = GarwayHeathSectorization(self.visual_field)
        garway_heath_position = Position(
            visual_field_position.x + drawing_dimensions.width + margin,
            position_y,
        )
        garway_heath_map = garway_heath.draw(
            limits_by_sector, cell_dimensions, garway_heath_position
        )
        svg.append(garway_heath_map)

        garway_heath_table = garway_heath.draw_table(
            table_width,
            Position(
                garway_heath_position.x + drawing_dimensions.width + margin,
                position_y + drawing_dimensions.height / 2 - 24 * 3.5,
            ),
        )
        svg.append(
            garway_heath_table,
        )

        return svg

import logging
from pprint import pformat

import drawSvg as draw

from visual_field_mapper import Colors, Dimensions, Position

from .garway_heath import GarwayHeathSectorization
from .visual_field import Point, VisualField


class Patient:
    @classmethod
    def parse(self, id, row):
        points = []

        for i in range(1, 55):
            if i == 26 or i == 35:
                points.append(Point(i, None))
            else:
                points.append(Point(i, int(row.loc[f"td{i}"])))

        visual_field = VisualField(row.loc["Eye"], points)

        patient = Patient(id, visual_field)
        return patient

    def __init__(self, id: int, visual_field: VisualField):
        self.id = id
        self.visual_field = visual_field

    def render(self, limits_by_sector):
        cell_dimensions = Dimensions(50, 50)
        drawing_dimensions = Dimensions(
            9 * cell_dimensions.width, 8 * cell_dimensions.height
        )
        margin = cell_dimensions.height
        title_height = cell_dimensions.height / 2

        table_width = 200
        svg_dimensions = Dimensions(
            drawing_dimensions.width * 2 + table_width + margin * 4,
            title_height + drawing_dimensions.height + margin * 3,
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
        )
        svg.append(background)

        title = draw.Text(
            f"Patient #{self.id}",
            16 * 2,
            x="50%",
            y=-margin,
            height=title_height,
            font_family="Arial,Helvetica",
            center=True,
            font_weight="bold",
        )
        svg.append(title)

        position_y = title_height + margin * 2

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

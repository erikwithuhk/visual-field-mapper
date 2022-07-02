import drawSvg as draw

from .. import Colors, Dimensions, Position
from ..patient import Patient
from . import rem
from .archetype_view import ArchetypeView
from .base_component import BaseComponent
from .garway_heath_view import GarwayHeathView
from .table import Table
from .typography import H1, H3
from .visual_field_map import VisualFieldMap


class PatientView(BaseComponent):
    def __init__(self, patient: Patient, limits_by_sector):
        self.patient = patient
        self.limits_by_sector = limits_by_sector
        width = 0
        height = 0
        margin = rem(6)
        super().__init__(
            width,
            height,
            margin_left=margin,
            margin_right=margin,
            margin_top=margin,
            margin_bottom=margin,
        )

    def render(self):
        title = H1(f"Patient #{self.patient.id}", position=Position(self.x, self.y))
        self.add_child(title)

        self.add_height(title.size.height)
        self.reset_x()

        visual_field_map = VisualFieldMap(
            self.patient.visual_field,
            label="Visual Field",
            position=Position(self.x, self.y),
        )
        self.add_child(visual_field_map)

        garway_heath_view = GarwayHeathView(
            self.patient.garway_heath,
            self.limits_by_sector,
            position=Position(self.x, self.y),
        )
        self.add_child(garway_heath_view)

        means_by_sector = self.patient.garway_heath.get_means_by_sector()
        table = Table(
            [
                list(means_by_sector.keys()),
                list(means_by_sector.values()),
            ],
            headers=["Sector", "Average TD"],
            col_widths=[75, 115],
            position=Position(self.x, self.y + rem(8)),
        )
        self.add_child(table)

        self.add_height(
            max(
                visual_field_map.size.height,
                garway_heath_view.size.height,
                table.size.height,
            )
        )
        self.reset_x()

        if len(self.patient.matching_archetypes):
            self.add_height(rem(2))

            matching_archetypes_header = H3(
                "Matching Archetypes (≥ 7%)", position=Position(self.x, self.y)
            )
            self.add_child(matching_archetypes_header)
            self.add_height(matching_archetypes_header.size.height)
            self.reset_x()

            view_height = 0

            for archetype in self.patient.matching_archetypes:
                view = ArchetypeView(archetype, position=Position(self.x, self.y))
                view_height = max(view_height, view.size.height)
                self.add_child(view)

            self.add_height(view_height)

            self.reset_x()

        svg_dimensions = Dimensions(
            self.width + self.margin_right,
            self.y + +self.margin_bottom,
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
        [svg.append(child.render()) for child in self.children]
        return svg

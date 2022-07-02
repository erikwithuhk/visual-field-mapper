from typing import Dict

import drawSvg as draw

from .. import Colors, Dimensions, Position
from ..archetype import Archetype
from ..patient import Patient
from . import rem
from .archetype_view import ArchetypeView
from .base_component import BaseComponent
from .garway_heath_view import GarwayHeathView
from .table import Table
from .typography import H1, H3
from .visual_field_map import VisualFieldMap

ARCHETYPE_MATCH_THRESHOLD = 0.07


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

    def render(self, archetypes_by_id: Dict[int, Archetype]):
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

        matching_archetypes = [
            {
                id: archetype_id,
                "match": match,
                "archetype": archetypes_by_id[archetype_id],
            }
            for archetype_id, match in self.patient.match_by_archetype.items()
            if match >= ARCHETYPE_MATCH_THRESHOLD
        ]
        matching_archetypes.sort(reverse=True, key=lambda x: x["match"])

        if len(matching_archetypes):
            self.add_height(rem(2))

            matching_archetypes_header = H3(
                f"Matching Archetypes (≥ {round(ARCHETYPE_MATCH_THRESHOLD * 100)}%)",
                position=Position(self.x, self.y),
            )
            self.add_child(matching_archetypes_header)
            self.add_height(matching_archetypes_header.size.height)
            self.reset_x()

            view_height = 0

            for archetype_data in matching_archetypes:
                view = ArchetypeView(
                    archetype_data.get("archetype"),
                    archetype_data.get("match"),
                    position=Position(self.x, self.y),
                )
                view_height = max(view_height, view.size.height)
                self.add_child(view)

            self.add_height(view_height)

            self.reset_x()

        return draw.Group(super().render())

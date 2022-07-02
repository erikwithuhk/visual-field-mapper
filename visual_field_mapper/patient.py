from typing import Dict, List

from .archetype import Archetype
from .garway_heath import GarwayHeathSectorization
from .visual_field import Point, VisualField


class Patient:
    def _parse_archetype_id():
        pass

    @classmethod
    def parse(self, id, row):
        points = []

        for i in range(1, 55):
            if i == 26 or i == 35:
                points.append(Point(i, None))
            else:
                points.append(Point(i, int(row.loc[f"td{i}"])))

        visual_field = VisualField(row.Eye, points)
        garway_heath = GarwayHeathSectorization(visual_field)
        match_by_archetype = {
            archetype_id: row.loc[f"AT{archetype_id}"] for archetype_id in range(1, 17)
        }
        # matching_archetypes = [
        #     archetypes_by_id[archetype_id] for archetype_id in row.matching_archetypes
        # ]
        patient = Patient(id, visual_field, garway_heath, match_by_archetype)
        return patient

    def __init__(
        self,
        id: int,
        visual_field: VisualField,
        garway_heath: GarwayHeathSectorization,
        match_by_archetype: Dict[int, float],
    ):
        self.id = id
        self.visual_field = visual_field
        self.garway_heath = garway_heath
        self.match_by_archetype = match_by_archetype

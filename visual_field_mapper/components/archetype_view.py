from ..archetype import Archetype
from . import CELL_DIMENSIONS, rem
from .base_component import BaseComponent
from .visual_field_map import VisualFieldMap


class ArchetypeView(BaseComponent):
    def __init__(self, archtype: Archetype, *args, **kwargs):
        self.archtype = archtype
        width = CELL_DIMENSIONS.width * 9
        height = CELL_DIMENSIONS.width * 8
        super().__init__(width, height, *args, margin=rem(2), **kwargs)

    def render(self):
        position = self.get_position()
        return VisualFieldMap(
            self.archtype.visual_field, label=f"{self.archtype.id}", position=position
        ).render()

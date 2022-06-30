from svgwrite.container import SVG
from svgwrite.shapes import Rect
from visual_field_mapper import Colors


class BaseComponent:
    def __init__(
        self,
        width=0,
        height=0,
        margin_top=0,
        margin_bottom=0,
        margin_left=0,
        margin_right=0,
    ):
        self.width = width
        self.height = height
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.total_width = width + self.margin_left + self.margin_right
        self.total_height = height + self.margin_top + self.margin_bottom

    def render(self, children, insert=(0, 0), debug: bool = False):
        svg = SVG(insert=insert)

        if debug:
            background = Rect(size=("100%", "100%"))
            background.fill(Colors.black.value, opacity=0.1)
            background.stroke(Colors.red.value, 2)
            svg.add(background)

        for i, child in enumerate(children):
            if issubclass(child.__class__, BaseComponent):
                children[i] = child.render(insert=(self.margin_left, self.margin_top))
            else:
                child.translate(self.margin_left, self.margin_top)

        [svg.add(child) for child in children]
        return svg

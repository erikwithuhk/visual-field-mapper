from svgwrite.container import SVG


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
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.width = width + self.margin_left + self.margin_right
        self.height = height + self.margin_top + self.margin_bottom

    def render(self, children):
        svg = SVG(
            insert=(self.margin_left, self.margin_top), size=(self.width, self.height)
        )
        [svg.add(child) for child in children]
        return svg

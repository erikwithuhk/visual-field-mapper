from svgwrite.container import SVG
from svgwrite.text import Text as SVGText

from . import BASE_FONT_SIZE, rem
from .base_component import BaseComponent


class Text(BaseComponent):
    def __init__(
        self,
        text,
        font_size: int = BASE_FONT_SIZE,
        line_height: int = rem(1.5),
        *args,
        **kwargs
    ):
        self.text = text
        self.font_size = font_size
        self.line_height = line_height
        width = round(len(self.text) * (font_size / 1.75), 1)
        height = line_height
        super().__init__(width, height, *args, **kwargs)

    def render(self):
        text = SVGText(
            self.text,
            insert=("50%", 0),
            font_size=self.font_size,
            alignment_baseline="hanging",
            text_anchor="middle",
            font_family="Arial,Helvetica",
            font_weight="bold",
        )
        return super().render([text])


class H1(Text):
    def __init__(self, text):
        super().__init__(
            text,
            font_size=rem(4.25),  # 68px
            line_height=rem(4.5),  # 72px
            margin_top=rem(1.5),  # 24px
            margin_bottom=rem(3.0),  # 48px
        )


H1_EXAMPLE = H1("Lorem Ipsum")


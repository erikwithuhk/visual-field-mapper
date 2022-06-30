from svgwrite.shapes import Rect
from svgwrite.text import Text as SVGText
from visual_field_mapper import Colors

from . import BASE_FONT_SIZE, rem
from .base_component import BaseComponent


class Text(BaseComponent):
    def __init__(
        self,
        text,
        font_size: int = BASE_FONT_SIZE,
        font_weight: str = "normal",
        line_height: int = rem(1.5),
        *args,
        **kwargs
    ):
        self.text = text
        self.font_size = font_size
        self.line_height = line_height
        self.font_weight = font_weight
        width = round(len(self.text) * (font_size / 1.75), 1)
        height = line_height
        super().__init__(width, height, *args, **kwargs)

    def render(self, debug: bool = False, *args, **kwargs):
        text = SVGText(
            self.text,
            insert=("50%", (self.line_height - self.font_size) / 2),
            font_size=self.font_size,
            alignment_baseline="hanging",
            text_anchor="middle",
            font_family="Arial,Helvetica",
            font_weight=self.font_weight,
        )
        children = [text]

        if debug:
            background = Rect(size=(self.width, self.height))
            background.fill(Colors.white.value)
            background.stroke(Colors.red.value, 1)
            new_children = [background]
            new_children.extend(children)
            children = new_children

        return super().render(children, debug=debug, *args, **kwargs)


TEXT_EXAMPLE = Text("Lorem Ipsum")


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


class H2(Text):
    def __init__(self, text):
        super().__init__(
            text,
            font_size=rem(2.625),  # 42px
            line_height=rem(3),  # 48px
            margin_top=rem(1.5),  # 24px
            margin_bottom=rem(1.5),  # 24px
        )


H2_EXAMPLE = H2("Lorem Ipsum")


class H3(Text):
    def __init__(self, text):
        super().__init__(
            text,
            font_size=rem(1.625),  # 26px
            line_height=rem(3),  # 48px
            margin_top=rem(1.5),  # 24px
        )


H3_EXAMPLE = H3("Lorem Ipsum")


class H4(Text):
    def __init__(self, text):
        super().__init__(
            text,
            font_size=rem(1),  # 16px
            line_height=rem(1.5),  # 24px
            margin_top=rem(1.5),  # 24px
        )


H4_EXAMPLE = H4("Lorem Ipsum")

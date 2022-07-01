import drawSvg as draw

from .. import Colors, Position
from . import BASE_FONT_SIZE, rem
from .base_component import BaseComponent

DEFAULT_POSITION = Position(0, 0)


class Text(BaseComponent):
    def __init__(
        self,
        text,
        font_size: int = BASE_FONT_SIZE,
        font_weight: str = "normal",
        line_height: int = rem(1.5),
        *args,
        **kwargs,
    ):
        self.text = text
        self.font_size = font_size
        self.line_height = line_height
        self.font_weight = font_weight
        width = round(len(self.text) * (font_size / 1.75), 1)
        height = line_height
        super().__init__(width, height, *args, **kwargs)

    def render(self):
        position = self.get_position()

        return draw.Text(
            self.text,
            self.font_size,
            x=position.x,
            y=position.y * -1,
            color=Colors.black.value,
            font_family="Arial,Helvetica",
            font_weight=self.font_weight,
            alignment_baseline="hanging",
            text_anchor="middle",
        )


TEXT_EXAMPLE = Text("Lorem Ipsum")


class Heading(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            font_weight="bold",
            **kwargs,
        )


class H1(Heading):
    def __init__(self, text, *args, **kwargs):
        super().__init__(
            text,
            font_size=rem(4.25),  # 68px
            line_height=rem(4.5),  # 72px
            margin_top=rem(1.5),  # 24px
            margin_bottom=rem(3.0),  # 48px
            *args,
            **kwargs,
        )


H1_EXAMPLE = H1("Lorem Ipsum")


class H2(Heading):
    def __init__(self, text, *args, **kwargs):
        super().__init__(
            text,
            font_size=rem(2.625),  # 42px
            line_height=rem(3),  # 48px
            margin_top=rem(1.5),  # 24px
            margin_bottom=rem(1.5),  # 24px
            *args,
            **kwargs,
        )


H2_EXAMPLE = H2("Lorem Ipsum")


class H3(Heading):
    def __init__(self, text, *args, **kwargs):
        super().__init__(
            text,
            font_size=rem(1.625),  # 26px
            line_height=rem(3),  # 48px
            margin_top=rem(1.5),  # 24px
            *args,
            **kwargs,
        )


H3_EXAMPLE = H3("Lorem Ipsum")


class H4(Heading):
    def __init__(self, text, *args, **kwargs):
        super().__init__(
            text,
            font_size=rem(1),  # 16px
            line_height=rem(1.5),  # 24px
            margin_top=rem(1.5),  # 24px
            *args,
            **kwargs,
        )


H4_EXAMPLE = H4("Lorem Ipsum")

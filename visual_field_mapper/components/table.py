import drawSvg as draw

from .. import Colors, Position
from . import rem
from .base_component import BaseComponent
from .typography import Text


class Cell(BaseComponent):
    def __init__(self, content):
        self.content = content
        super().__init__()

    def render(self, debug: bool = False, *args, **kwargs):
        text = Text(f"{self.content}")
        return super().render([text], debug=debug, *args, **kwargs)


class Table(BaseComponent):
    def __init__(self, data, *args, headers=None, col_widths=None, **kwargs):
        self.data = data
        self.headers = headers
        self.col_widths = col_widths or [100, 100]
        width = self.col_widths[0] + self.col_widths[1]
        super().__init__(width, *args, margin=rem(2), **kwargs)

    def render(
        self,
    ):
        position = self.get_position()

        font_size = rem(1)

        text_formatting = {
            "font_family": "Arial,Helvetica",
            "valign": "middle",
            "text_anchor": "middle",
        }

        row_height = 24
        col_1_width = self.col_widths[0]
        col_2_width = self.col_widths[1]
        margin = 10

        col_2_start = col_1_width + margin

        col_1_text_x = margin + col_1_width / 2
        col_2_text_x = col_2_start + col_2_width / 2

        def draw_row(sector_name: str, mean: float, position: Position):
            sector_text = draw.Text(
                sector_name, font_size, col_1_text_x, 0, **text_formatting
            )
            mean_text = draw.Text(
                "{:.2f}".format(round(mean, 2)),
                font_size,
                col_2_text_x,
                0,
                **text_formatting,
            )

            return draw.Group(
                [sector_text, mean_text], transform=f"translate(0,{position.y})"
            )

        sector_header = draw.Text(
            self.headers[0],
            font_size,
            col_1_text_x,
            0,
            **text_formatting,
            font_weight="bold",
        )
        mean_header = draw.Text(
            self.headers[1],
            font_size,
            col_2_text_x,
            0,
            **text_formatting,
            font_weight="bold",
        )
        children = [sector_header, mean_header]
        divider_x = col_1_width + margin
        children.append(
            draw.Line(
                divider_x,
                row_height * 0.5,
                divider_x,
                row_height * -6.5,
                stroke=Colors.black.value,
                stroke_width=2,
            )
        )
        children.append(
            draw.Line(
                0,
                -12,
                col_2_start + col_2_width,
                -12,
                stroke=Colors.black.value,
                stroke_width=2,
            )
        )
        children.extend(
            [
                draw_row(
                    self.data[0][i], self.data[1][i], Position(0, row_height * (i + 1))
                )
                for i in range(0, len(self.data[0]))
            ]
        )

        return draw.Group(
            children,
            transform=f"translate({position.x},{position.y})" if position else None,
        )


TABLE_EXAMPLE = Table(
    [["IN", -14.29], ["IT", -11.43]], headers=["Sector", "Average TD"]
)

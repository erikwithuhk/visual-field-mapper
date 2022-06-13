from statistics import mean
from typing import List, NamedTuple

import drawSvg as draw
from colorama import Back, Style

from visual_field_mapper import Dimensions, Position

from .visual_field import Colors, Point, VisualField


class Sector(NamedTuple):
    name: str
    abbreviation: str
    color: str
    print_color: str


SECTORS = {
    "IN": Sector("Inferonasal", "IN", Colors.green, Style.BRIGHT + Back.GREEN),
    "IT": Sector("Inferotemporal", "IT", Colors.purple, Back.BLUE),
    "T": Sector("Temporal", "T", Colors.orange, Style.DIM + Back.YELLOW),
    "N": Sector("Nasal", "N", Colors.yellow, Style.BRIGHT + Back.YELLOW),
    "ST": Sector("Superotemporal", "ST", Colors.blue, Style.DIM + Back.GREEN),
    "SN": Sector("Superonasal", "SN", Colors.pink, Back.RED),
    "BS": Sector("Blind spot", "BS", Colors.black, Back.BLACK),
}


def get_sector(point: Point):
    def is_between(start: int, end: int):
        return point.position >= start and point.position <= end

    if is_between(1, 5) or point.position in [10, 17]:
        return SECTORS["IN"]

    if is_between(6, 9) or is_between(11, 16) or is_between(19, 22):
        return SECTORS["IT"]

    if point.position in [18, 27, 36, 44]:
        return SECTORS["N"]

    if is_between(23, 25) or is_between(32, 34):
        return SECTORS["T"]

    if is_between(29, 31) or is_between(38, 42) or is_between(47, 48):
        return SECTORS["ST"]

    if point.position in [28, 37, 43] or is_between(45, 46) or is_between(49, 54):
        return SECTORS["SN"]

    if point.position in [26, 35]:
        return SECTORS["BS"]

    return None


class GarwayHeathSectorization:
    def __init__(self, visual_field: VisualField):
        self.__limits_by_sector = {
            sector: 0 for sector in SECTORS.keys() if sector != "BS"
        }
        self.visual_field = visual_field

    def get_means_by_sector(self):
        tds_by_sector = {sector.abbreviation: [] for sector in SECTORS.values()}

        for point in self.visual_field.points:
            sector_name = get_sector(point).abbreviation
            tds_by_sector[sector_name].append(point.total_deviation)

        return {
            sector: mean(points)
            for sector, points in tds_by_sector.items()
            if sector != "BS"
        }

    def __format_point(self, point: Point):
        sector = None
        total_deviation = "   "

        if point:
            sector = get_sector(point)

            total_deviation = str(point.total_deviation)

            if point.total_deviation == None:
                total_deviation = "   "
            elif point.total_deviation >= 0 and point.total_deviation < 10:
                total_deviation = f"  {total_deviation}"
            elif point.total_deviation > -10:
                total_deviation = f" {total_deviation}"

        return f"{sector.print_color if sector else ''} {total_deviation} {Back.RESET}{Style.RESET_ALL}"

    def __format_row(self, points: List[Point]):
        return "".join([self.__format_point(point) for point in points])

    def __repr__(self):
        matrix = self.to_matrix()

        return "\n".join([self.__format_row(row) for row in matrix])

    def __draw_point(self, dimensions: Dimensions, position: Position) -> draw.Circle:
        return draw.Circle(
            position.x + dimensions.width / 2,
            position.y + dimensions.height / 2,
            3,
            fill=Colors.black.value,
        )

    def __get_fill_opacity(self, sector):
        fill_opacity = 0.0

        sector_limit = self.__limits_by_sector[sector.abbreviation]
        sector_mean = self.get_means_by_sector()[sector.abbreviation]
        if sector_mean < sector_limit:
            fill_opacity = sector_mean / (-35 - sector_limit)

        return fill_opacity

    def __draw_sectors(
        self, cell_dimensions: Dimensions, position: Position
    ) -> draw.Group:
        fill = Colors.red.value
        stroke = Colors.gray.value
        stroke_width = 5

        in_sector = draw.Lines(
            0,
            0,
            2 * cell_dimensions.width,
            2 * cell_dimensions.height,
            6 * cell_dimensions.width,
            2 * cell_dimensions.height,
            7 * cell_dimensions.width,
            1 * cell_dimensions.height,
            7 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            6 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            6 * cell_dimensions.width,
            1 * cell_dimensions.height,
            2 * cell_dimensions.width,
            1 * cell_dimensions.height,
            2 * cell_dimensions.width,
            0 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["IN"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate({1 * cell_dimensions.width},{2 * cell_dimensions.height})",
        )

        it_sector = draw.Lines(
            0,
            0,
            0 * cell_dimensions.width,
            1 * cell_dimensions.height,
            1 * cell_dimensions.width,
            2 * cell_dimensions.height,
            3 * cell_dimensions.width,
            2 * cell_dimensions.height,
            3 * cell_dimensions.width,
            3 * cell_dimensions.height,
            7 * cell_dimensions.width,
            3 * cell_dimensions.height,
            7 * cell_dimensions.width,
            1 * cell_dimensions.height,
            4 * cell_dimensions.width,
            1 * cell_dimensions.height,
            4 * cell_dimensions.width,
            0 * cell_dimensions.height,
            0 * cell_dimensions.width,
            0 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["IT"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate(0,{4 * cell_dimensions.height})",
        )

        t_sector = draw.Rectangle(
            4 * cell_dimensions.width,
            5 * -cell_dimensions.height,
            3 * cell_dimensions.width,
            2 * cell_dimensions.height,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["T"]),
            stroke=stroke,
            stroke_width=stroke_width,
        )

        n_sector = draw.Lines(
            0,
            0,
            0 * cell_dimensions.width,
            6 * cell_dimensions.height,
            1 * cell_dimensions.width,
            5 * cell_dimensions.height,
            1 * cell_dimensions.width,
            1 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["N"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate({8 * cell_dimensions.width},{7 * cell_dimensions.height})",
        )

        st_sector = draw.Lines(
            0,
            0,
            0 * cell_dimensions.width,
            1 * cell_dimensions.height,
            3 * cell_dimensions.width,
            1 * cell_dimensions.height,
            3 * cell_dimensions.width,
            0 * cell_dimensions.height,
            6 * cell_dimensions.width,
            0 * cell_dimensions.height,
            6 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            5 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            5 * cell_dimensions.width,
            -2 * cell_dimensions.height,
            3 * cell_dimensions.width,
            -2 * cell_dimensions.height,
            3 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            1 * cell_dimensions.width,
            -1 * cell_dimensions.height,
            1 * cell_dimensions.width,
            0 * cell_dimensions.height,
            0 * cell_dimensions.width,
            0 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["ST"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate({1 * cell_dimensions.width},{5 * cell_dimensions.height})",
        )

        sn_sector = draw.Lines(
            0,
            0,
            -3 * cell_dimensions.width,
            3 * cell_dimensions.height,
            -3 * cell_dimensions.width,
            4 * cell_dimensions.height,
            -2 * cell_dimensions.width,
            4 * cell_dimensions.height,
            -2 * cell_dimensions.width,
            3 * cell_dimensions.height,
            -1 * cell_dimensions.width,
            3 * cell_dimensions.height,
            -1 * cell_dimensions.width,
            2 * cell_dimensions.height,
            1 * cell_dimensions.width,
            2 * cell_dimensions.height,
            1 * cell_dimensions.width,
            1 * cell_dimensions.height,
            3 * cell_dimensions.width,
            1 * cell_dimensions.height,
            3 * cell_dimensions.width,
            2 * cell_dimensions.height,
            4 * cell_dimensions.width,
            2 * cell_dimensions.height,
            4 * cell_dimensions.width,
            3 * cell_dimensions.height,
            5 * cell_dimensions.width,
            3 * cell_dimensions.height,
            5 * cell_dimensions.width,
            1 * cell_dimensions.height,
            4 * cell_dimensions.width,
            0 * cell_dimensions.height,
            close=True,
            fill=fill,
            fill_opacity=self.__get_fill_opacity(SECTORS["SN"]),
            stroke=stroke,
            stroke_width=stroke_width,
            transform=f"translate({3 * cell_dimensions.width},{8 * cell_dimensions.height})",
        )

        blind_spot = draw.Rectangle(
            7 * cell_dimensions.width,
            5 * -cell_dimensions.height,
            1 * cell_dimensions.width,
            2 * cell_dimensions.height,
            fill=Colors.black.value,
            stroke=stroke,
            stroke_width=stroke_width,
        )
        return draw.Group(
            [in_sector, it_sector, t_sector, n_sector, st_sector, sn_sector, blind_spot]
        )

    def __draw_row(
        self,
        points: List[Point],
        cell_dimensions: Dimensions,
        position: Position = None,
    ) -> draw.Group:
        return draw.Group(
            [
                self.__draw_point(
                    cell_dimensions,
                    Position(i * cell_dimensions.width, -cell_dimensions.height),
                )
                for i, point in enumerate(points)
                if point
            ],
            transform=f"translate({position.x},{position.y})" if position else None,
        )

    def __draw_outline(
        self, cell_dimensions: Dimensions, position: Position = None
    ) -> draw.Lines:
        return draw.Lines(
            0,
            0,
            3 * cell_dimensions.width,
            3 * cell_dimensions.height,
            7 * cell_dimensions.width,
            3 * cell_dimensions.height,
            9 * cell_dimensions.width,
            1 * cell_dimensions.height,
            9 * cell_dimensions.width,
            -3 * cell_dimensions.height,
            7 * cell_dimensions.width,
            -5 * cell_dimensions.height,
            3 * cell_dimensions.width,
            -5 * cell_dimensions.height,
            0 * cell_dimensions.width,
            -2 * cell_dimensions.height,
            close=True,
            fill_opacity=0.0,
            stroke=Colors.black.value,
            stroke_width=4,
            transform=f"translate({position.x},{position.y})" if position else None,
        )

    def draw_table(self, table_width: int, position: Position = None):

        font_size = 16

        text_formatting = {
            "font_family": "Arial,Helvetica",
            "valign": "middle",
            "text_anchor": "middle",
        }

        row_height = 24
        col_1_width = 75
        col_2_width = 115
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
            "Sector", font_size, col_1_text_x, 0, **text_formatting, font_weight="bold"
        )
        mean_header = draw.Text(
            "Average TD",
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
        means_by_sector = self.get_means_by_sector()
        children.extend(
            [
                draw_row(sector, mean, Position(0, row_height * (i + 1)))
                for i, (sector, mean) in enumerate(means_by_sector.items())
            ]
        )

        return draw.Group(
            children,
            transform=f"translate({position.x},{position.y})" if position else None,
        )

    def draw(
        self, limits_by_sector, cell_dimensions: Dimensions, position: Position = None
    ) -> draw.Group:
        self.__limits_by_sector = limits_by_sector
        matrix = self.visual_field.to_matrix()
        children = []
        children.append(self.__draw_sectors(cell_dimensions, position))
        children.extend(
            [
                self.__draw_row(
                    row, cell_dimensions, Position(0, i * cell_dimensions.height)
                )
                for i, row in enumerate(matrix)
            ]
        )
        outline = self.__draw_outline(
            cell_dimensions, Position(0, 3 * cell_dimensions.height)
        )
        children.append(outline)
        return draw.Group(
            children,
            transform=f"translate({position.x},{position.y})" if position else None,
        )

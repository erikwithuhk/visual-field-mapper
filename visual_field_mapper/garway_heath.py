from statistics import mean
from typing import Dict, List, NamedTuple

import drawSvg
from colorama import Back, Style

from .visual_field import Point, VisualField


class Sector(NamedTuple):
    name: str
    abbreviation: str
    print_color: str


SECTORS = {
    "IN": Sector("Inferonasal", "IN", Style.BRIGHT + Back.GREEN),
    "IT": Sector("Inferotemporal", "IT", Back.BLUE),
    "T": Sector("Temporal", "T", Style.DIM + Back.YELLOW),
    "N": Sector("Nasal", "N", Style.BRIGHT + Back.YELLOW),
    "ST": Sector("Superotemporal", "ST", Style.DIM + Back.GREEN),
    "SN": Sector("Superonasal", "SN", Back.RED),
    "BS": Sector("Blind spot", "BS", Back.BLACK),
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
        self.visual_field = visual_field

    def get_averages_by_sector(self):
        tds_by_sector = {sector.abbreviation: [] for sector in SECTORS.values()}

        for point in self.visual_field.points:
            sector_name = get_sector(point).abbreviation
            tds_by_sector[sector_name].append(point.total_deviation)

        return {
            sector: mean(points)
            for sector, points in tds_by_sector.items()
            if sector != "BS"
        }

    def create_row(self, points: List[Point]):
        row = []

        if len(points) == 4:
            row.extend([None, None, None])
            row.extend(points)
            row.extend([None, None])
        elif len(points) == 6:
            row.extend([None, None])
            row.extend(points)
            row.extend([None])
        elif len(points) == 8:
            row.append(None)
            row.extend(points)
        elif len(points) == 9:
            row = points
        else:
            raise Exception(f"No rule for points length <{len(points)}>.")

        return row

    def to_matrix(self):
        rows = [
            self.create_row(points)
            for points in [
                self.visual_field.points[0:4],
                self.visual_field.points[4:10],
                self.visual_field.points[10:18],
                self.visual_field.points[18:27],
                self.visual_field.points[27:36],
                self.visual_field.points[36:44],
                self.visual_field.points[44:50],
                self.visual_field.points[50:],
            ]
        ]
        return rows

    def draw_heat_map(self, means_by_sector: Dict[str, float]) -> drawSvg.Drawing:
        matrix = self.to_matrix()
        rect_size = 100
        width = 11 * rect_size
        height = 10 * rect_size
        svg = drawSvg.Drawing(width, height, origin=(0, -height), displayInline=False)

        starting_x = 1 * rect_size
        starting_y = -2 * rect_size

        x = starting_x
        y = starting_y

        def draw_cell(point: Point):
            nonlocal x
            nonlocal y

            if point:
                sector = get_sector(point)

                fill = "black"
                fill_opacity = 1.0

                if sector.abbreviation != "BS":
                    fill = "white"
                    fill_opacity = 1.0

                    mean = means_by_sector[sector.abbreviation]

                    if point.total_deviation < mean:
                        fill = "red"
                        fill_opacity = (point.total_deviation - mean) / (-35 - mean)

                rect = drawSvg.Rectangle(
                    x,
                    y,
                    rect_size,
                    rect_size,
                    fill=fill,
                    fill_opacity=fill_opacity,
                )
                svg.append(rect)

            x += rect_size

        def draw_row(points):
            nonlocal x
            nonlocal y
            x = starting_x
            row = [draw_cell(point) for point in points]
            y -= rect_size
            return row

        [draw_row(row) for row in matrix]
        outline = drawSvg.Lines(
            starting_x + 3 * rect_size,
            starting_y + 1 * rect_size,
            starting_x + 7 * rect_size,
            starting_y + 1 * rect_size,
            starting_x + 7 * rect_size,
            starting_y + 1 * rect_size,
            starting_x + 7 * rect_size,
            starting_y + 0 * rect_size,
            starting_x + 8 * rect_size,
            starting_y + 0 * rect_size,
            starting_x + 8 * rect_size,
            starting_y + -1 * rect_size,
            starting_x + 9 * rect_size,
            starting_y + -1 * rect_size,
            starting_x + 9 * rect_size,
            starting_y + -5 * rect_size,
            starting_x + 8 * rect_size,
            starting_y + -5 * rect_size,
            starting_x + 8 * rect_size,
            starting_y + -6 * rect_size,
            starting_x + 7 * rect_size,
            starting_y + -6 * rect_size,
            starting_x + 7 * rect_size,
            starting_y + -7 * rect_size,
            starting_x + 3 * rect_size,
            starting_y + -7 * rect_size,
            starting_x + 3 * rect_size,
            starting_y + -6 * rect_size,
            starting_x + 2 * rect_size,
            starting_y + -6 * rect_size,
            starting_x + 2 * rect_size,
            starting_y + -5 * rect_size,
            starting_x + 1 * rect_size,
            starting_y + -5 * rect_size,
            starting_x + 1 * rect_size,
            starting_y + -4 * rect_size,
            starting_x + 0 * rect_size,
            starting_y + -4 * rect_size,
            starting_x + 0 * rect_size,
            starting_y + -2 * rect_size,
            starting_x + 1 * rect_size,
            starting_y + -2 * rect_size,
            starting_x + 1 * rect_size,
            starting_y + -1 * rect_size,
            starting_x + 2 * rect_size,
            starting_y + -1 * rect_size,
            starting_x + 2 * rect_size,
            starting_y + 0 * rect_size,
            starting_x + 3 * rect_size,
            starting_y + 0 * rect_size,
            starting_x + 3 * rect_size,
            starting_y + 1 * rect_size,
            fill_opacity=0,
            stroke="black",
            stroke_width=4,
        )
        svg.append(outline)
        t = drawSvg.Text(str(self.visual_field.patient_id), 16, x=0, y=y)
        svg.append(t)
        return svg

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

import enum
from typing import NamedTuple

from colorama import Back, Style

from .visual_field import Point, VisualField


class Sector(NamedTuple):
    name: str
    abbreviation: str
    print_color: str


class Sectors(enum.Enum):
    ST = Sector("Superotemporal", "ST", Style.DIM + Back.GREEN)
    T = Sector("Temporal", "T", Style.DIM + Back.YELLOW)
    IT = Sector("Inferotemporal", "IT", Back.BLUE)
    IN = Sector("Inferonasal", "IN", Style.BRIGHT + Back.GREEN)
    N = Sector("Nasal", "N", Style.BRIGHT + Back.YELLOW)
    SN = Sector("Superonasal", "SN", Back.RED)
    BS = Sector("Blind spot", "BS", Back.BLACK)


def get_sector(point: Point):
    def is_between(start: int, end: int):
        return point.position >= start and point.position <= end

    if is_between(1, 5) or point.position in [10, 17]:
        return Sectors.IN

    if is_between(6, 9) or is_between(11, 16) or is_between(19, 22):
        return Sectors.IT

    if point.position in [18, 27, 36, 44]:
        return Sectors.N

    if is_between(23, 25) or is_between(32, 34):
        return Sectors.T

    if is_between(29, 31) or is_between(38, 42) or is_between(47, 48):
        return Sectors.ST

    if point.position in [28, 37, 43] or is_between(45, 46) or is_between(49, 54):
        return Sectors.SN

    if point.position in [26, 35]:
        return Sectors.BS

    return None


class GarwayHeathSectorization:
    def __init__(self, visual_field: VisualField):
        self.visual_field = visual_field

    def __format_point(self, point: Point):
        sector = get_sector(point)

        total_deviation = str(point.total_deviation)

        if point.total_deviation == None:
            total_deviation = "   "
        elif point.total_deviation >= 0 and point.total_deviation < 10:
            total_deviation = f"  {total_deviation}"
        elif point.total_deviation > -10:
            total_deviation = f" {total_deviation}"

        return f"{sector.value.print_color if sector.value else ''} {total_deviation} {Back.RESET}{Style.RESET_ALL}"

    def __format_line(self, points: list[Point]):
        empty = "     "

        formatted_line = []
        formatted_points = [self.__format_point(point) for point in points]

        if len(points) == 4:
            formatted_line.extend([empty, empty, empty])
            formatted_line.extend(formatted_points)
            formatted_line.extend([empty, empty])
        elif len(points) == 6:
            formatted_line.extend([empty, empty])
            formatted_line.extend(formatted_points)
            formatted_line.extend([empty])
        elif len(points) == 8:
            formatted_line.append(empty)
            formatted_line.extend(formatted_points)
        elif len(points) == 9:
            formatted_line = formatted_points
        else:
            raise Exception(f"No formatting rule for line length <{len(points)}>.")

        return "".join(formatted_line)

    def __repr__(self):
        def format_line(points):
            return self.__format_line(points)

        line_1 = format_line(self.visual_field.points[0:4])
        line_2 = format_line(self.visual_field.points[4:10])
        line_3 = format_line(self.visual_field.points[10:18])
        line_4 = format_line(self.visual_field.points[18:27])
        line_5 = format_line(self.visual_field.points[27:36])
        line_6 = format_line(self.visual_field.points[36:44])
        line_7 = format_line(self.visual_field.points[44:50])
        line_8 = format_line(self.visual_field.points[50:])

        return "\n".join(
            [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8]
        )

from statistics import mean
from typing import Dict, List, NamedTuple

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

    def draw_heat_map(self, means_by_sector: Dict[str, float]):
        pass

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

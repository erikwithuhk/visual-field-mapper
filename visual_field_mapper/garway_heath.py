from pprint import pformat
from statistics import mean
from typing import NamedTuple

from colorama import Back, Style

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

    def __repr__(self):
        return pformat(vars(self))

from colorama import Back, Style

from .point import Point
from .visual_field import VisualField


class Printer:
    __CENTRAL_PERIPHERAL_COLORS = {
        "central": Back.BLUE,
        "peripheral": Back.YELLOW,
    }

    __GARWAY_HEATH_COLORS = {
        "SN": Back.RED,
        "N": Style.BRIGHT + Back.YELLOW,
        "IN": Style.BRIGHT + Back.GREEN,
        "IT": Back.BLUE,
        "N": Style.BRIGHT + Back.YELLOW,
        "T": Style.DIM + Back.YELLOW,
        "ST": Style.DIM + Back.GREEN,
    }

    def __format_line(
        self,
        points: list[Point],
        flip: bool = False,
        has_blind_spot: bool = False,
        type: str = None,
    ):
        empty = "    "

        formatted_line = []
        formatted_points = [self.__format_point(point, type) for point in points]

        if len(points) == 4:
            formatted_line.extend([empty, empty])
            formatted_line.extend(formatted_points)
            formatted_line.extend([empty, empty, empty])
        elif len(points) == 6:
            formatted_line.extend([empty])
            formatted_line.extend(formatted_points)
            formatted_line.extend([empty, empty])
        elif len(points) == 8 and has_blind_spot:
            formatted_line.append(formatted_points[0])
            formatted_line.append(empty)
            formatted_line.extend(formatted_points[1:])
        elif len(points) == 8:
            formatted_line = formatted_points
            formatted_line.append(empty)
        else:
            raise Exception(
                f"No formatting rule for line length <{len(points)}> and has_blind_spot <{has_blind_spot}>"
            )

        if flip:
            formatted_line.reverse()

        return "".join(formatted_line)

    def __get_color(self, point: Point, type: str):
        if (
            type == "central_peripheral"
            and point.central_peripheral_sector in self.__CENTRAL_PERIPHERAL_COLORS
        ):
            return self.__CENTRAL_PERIPHERAL_COLORS[point.central_peripheral_sector]

        if (
            type == "garway_heath"
            and point.garway_heath_sector in self.__GARWAY_HEATH_COLORS
        ):
            return self.__GARWAY_HEATH_COLORS[point.garway_heath_sector]

        return ""

    def __format_point(self, point: Point, type: str = None):
        color = ""

        if type:
            color = self.__get_color(point, type)

        value = str(point.value)

        if point.value < 10:
            value = f" {value}"

        return f"{color} {value} {Back.RESET}{Style.RESET_ALL}"

    def print(self, visual_field: VisualField, flip: bool = False, type: str = None):
        def format_line(points, **kwargs):
            return self.__format_line(points, flip=flip, type=type, **kwargs)

        line_1 = format_line(visual_field.points[0:4])
        line_2 = format_line(visual_field.points[4:10])
        line_3 = format_line(visual_field.points[10:18])
        line_4 = format_line(visual_field.points[18:26], has_blind_spot=True)
        line_5 = format_line(visual_field.points[26:34], has_blind_spot=True)
        line_6 = format_line(visual_field.points[34:42])
        line_7 = format_line(visual_field.points[42:48])
        line_8 = format_line(visual_field.points[48:])

        [
            print(line)
            for line in [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8]
        ]

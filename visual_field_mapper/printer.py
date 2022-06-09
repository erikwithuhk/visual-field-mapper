from .point import Point
from .visual_field import VisualField


class Printer:
    def __format_line(self, points: list[Point], has_blind_spot=False):
        empty = "  "
        blind_spot = " X"

        formatted_line = []
        formatted_points = [self.__format_point(point) for point in points]

        if len(points) == 4:
            formatted_line.extend([empty, empty])
            formatted_line.extend(formatted_points)
        elif len(points) == 6:
            formatted_line.append(empty)
            formatted_line.extend(formatted_points)
        elif len(points) == 8 and has_blind_spot:
            formatted_line.append(formatted_points[0])
            formatted_line.append(blind_spot)
            formatted_line.extend(formatted_points[1:])
        elif len(points) == 8:
            formatted_line = formatted_points
        else:
            raise Exception(
                f"No formatting rule for line length <{len(points)}> and has_blind_spot <{has_blind_spot}>"
            )

        return "  ".join(formatted_line)

    def __format_point(self, point: Point):
        if point.value < 10:
            return f" {str(point.value)}"

        return str(point.value)

    def print(self, visual_field: VisualField):
        line_1 = self.__format_line(visual_field.points[0:4])
        line_2 = self.__format_line(visual_field.points[4:10])
        line_3 = self.__format_line(visual_field.points[10:18])
        line_4 = self.__format_line(visual_field.points[18:26], has_blind_spot=True)
        line_5 = self.__format_line(visual_field.points[26:34], has_blind_spot=True)
        line_6 = self.__format_line(visual_field.points[34:42])
        line_7 = self.__format_line(visual_field.points[42:48])
        line_8 = self.__format_line(visual_field.points[48:])

        [
            print(line, "\n")
            for line in [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8]
        ]

from .point import Point


class VisualField:
    __DEFAULT_VALUES = [
        1,
        1,
        0,
        1,
        2,
        3,
        1,
        0,
        1,
        0,
        2,
        2,
        4,
        1,
        2,
        1,
        1,
        2,
        5,
        5,
        6,
        3,
        3,
        3,
        3,
        5,
        19,
        21,
        20,
        22,
        21,
        22,
        21,
        22,
        20,
        22,
        22,
        22,
        22,
        22,
        22,
        23,
        22,
        22,
        22,
        22,
        23,
        22,
        22,
        22,
        22,
        22,
    ]

    def __init__(self, values: list[int] = __DEFAULT_VALUES):
        self.points = self.__create_points(values)

    def __repr__(self):
        from pprint import pformat

        return "VisualField: " + pformat(vars(self), indent=2)

    def __create_points(self, values: list[int]):
        values_length = 52
        points = []

        if len(values) != values_length:
            raise Exception(
                f"VisualField must have {values_length} values, and received only {len(values)}"
            )

        for i, value in enumerate(values):
            position = i + 1
            points.append(Point(position, value))

        return points

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

    # TODO: Move to Printer class
    def print(self):
        line_1 = self.__format_line(self.points[0:4])
        line_2 = self.__format_line(self.points[4:10])
        line_3 = self.__format_line(self.points[10:18])
        line_4 = self.__format_line(self.points[18:26], has_blind_spot=True)
        line_5 = self.__format_line(self.points[26:34], has_blind_spot=True)
        line_6 = self.__format_line(self.points[34:42])
        line_7 = self.__format_line(self.points[42:48])
        line_8 = self.__format_line(self.points[48:])

        [
            print(line, "\n")
            for line in [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8]
        ]

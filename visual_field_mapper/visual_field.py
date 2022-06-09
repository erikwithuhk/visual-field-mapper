from .point import Point


class VisualField:
    def __init__(self, values: list[int]):
        self.points = self.__create_points(values)

    def __repr__(self):
        from pprint import pformat

        return "VisualField: " + pformat(vars(self))

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

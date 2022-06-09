from .point import Point


class VisualField:
    def __init__(self):
        self.points = self.__create_points()

    def __repr__(self):
        from pprint import pformat

        return "VisualField: " + pformat(vars(self), indent=2)

    def __create_points(self):
        points = []

        for position in range(1, 53):
            points.append(Point(position))

        return points

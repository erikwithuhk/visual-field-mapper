class Point:
    def __init__(self, position: int, total_deviation: int):
        if position < 1 or position > 54:
            raise ValueError(
                f"Point position must be between 1 and 54, received <{position}>."
            )

        self.position = position
        self.total_deviation = total_deviation

    def __repr__(self) -> str:
        from pprint import pformat

        return "Point: " + pformat(vars(self))


class VisualField:
    def __init__(self, points: list[Point]):
        self.points = points

    def __repr__(self) -> str:
        from pprint import pformat

        return "VisualField: " + pformat(vars(self))

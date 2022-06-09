class Point:
    def __init__(self, position):
        self.position = position

    def __repr__(self):
        from pprint import pformat

        return "Point: " + pformat(vars(self), indent=2)

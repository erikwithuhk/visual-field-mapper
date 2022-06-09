class Point:
    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __repr__(self):
        from pprint import pformat

        return "Point: " + pformat(vars(self), indent=2)

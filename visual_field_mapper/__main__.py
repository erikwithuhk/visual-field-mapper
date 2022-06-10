import argparse

from .printer import Printer
from .visual_field import VisualField


def main(flip: bool = False, type: str = None):
    values = [
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

    visual_field = VisualField(values)
    printer = Printer()
    printer.print(visual_field, flip=flip, type=type)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="visual_field_mapper")
    parser.add_argument("--flip", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("-t", "--type", help='"central_peripheral" or "garway_heath"')
    args = parser.parse_args()
    main(flip=args.flip, type=args.type)

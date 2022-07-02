import argparse
import os
from enum import Enum

from svgwrite import Drawing

from .. import OUT_DIR
from .table import TABLE_EXAMPLE
from .typography import H1_EXAMPLE, H2_EXAMPLE, H3_EXAMPLE, H4_EXAMPLE, TEXT_EXAMPLE

__COMPONENTS = [
    TEXT_EXAMPLE,
    H1_EXAMPLE,
    H2_EXAMPLE,
    H3_EXAMPLE,
    H4_EXAMPLE,
    TABLE_EXAMPLE,
]


BUILD_DIR = OUT_DIR.joinpath("components")


def build():
    os.makedirs(BUILD_DIR, exist_ok=True)

    def build_component(component):
        name = type(component).__name__
        drawing = Drawing(
            BUILD_DIR.joinpath(f"{name}.svg"),
            size=(component.total_width, component.total_height),
        )
        drawing.viewbox(0, 0, component.total_width, component.total_height)
        drawing.add(component.render(debug=True))
        drawing.save(pretty=True)

    [build_component(component) for component in __COMPONENTS]


class Commands(Enum):
    build = "build"


def main(command):
    if command == Commands.build.value:
        build()
    else:
        raise Exception("Unknown command: %s".format(command))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("visual_field_mapper.components")
    subparser = parser.add_subparsers(dest="command")

    build_parser = subparser.add_parser(Commands.build.value)

    args = parser.parse_args()

    main(args.command)

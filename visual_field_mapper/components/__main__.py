import argparse
import os
from enum import Enum


from svgwrite import Drawing
from svgwrite.shapes import Rect
from visual_field_mapper import OUT_DIR, Colors

from . import rem
from .typography import H1_EXAMPLE

__COMPONENTS = [H1_EXAMPLE]


BUILD_DIR = OUT_DIR.joinpath("components")


def build():
    os.makedirs(BUILD_DIR, exist_ok=True)

    margin = rem(2)

    def build_component(component):
        name = type(component).__name__
        drawing = Drawing(
            BUILD_DIR.joinpath(f"{name}.svg"), size=("100%", component.height)
        )
        drawing.viewbox(0, 0, component.width, component.height)
        background = Rect(size=(component.width, component.height))
        background.fill(None, opacity=0)
        drawing.add(background)
        drawing.add(component.render())
        drawing.save(pretty=True)

    [build_component(component) for component in __COMPONENTS]


class Commands(Enum):
    build = "build"


def main(command):
    if command == Commands.build.value:
        build()
    else:
        raise Exception("Unknown command: %s".format(command))


# COMMANDS = {"BUILD_LIBRARY": "build-library"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser("visual_field_mapper.components")
    subparser = parser.add_subparsers(dest="command")

    build_parser = subparser.add_parser(Commands.build.value)
    # build_parser.add_argument("inputfile", type=str)

    args = parser.parse_args()

    main(args.command)

import argparse
import os

from .file_reader import FileReader
from .garway_heath import GarwayHeathSectorization

from .visual_field import Point, VisualField

root_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(root_dir, "data")
file_reader = FileReader()


def main():
    scans = file_reader.read_csv(os.path.join(data_dir, "normal.csv"))

    for scan in scans:
        points = []
        for i in range(1, 55):
            if i == 26 or i == 35:
                points.append(Point(i, None))
            else:
                points.append(Point(i, int(scan[f"td{i}"])))

        visual_field = VisualField(points)
        garway_heath = GarwayHeathSectorization(visual_field)
        print(garway_heath, "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="visual_field_mapper")
    args = parser.parse_args()
    main()

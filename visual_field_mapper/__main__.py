import argparse
import csv
import math

import pandas as pd

from .file_reader import FileReader
from .garway_heath import GarwayHeathSectorization, Sectors
from .visual_field import Point, VisualField

file_reader = FileReader()


def get_average_by_sector(input_filepath: str, output_filepath: str):
    scans = file_reader.read_csv(input_filepath)
    averages = []

    for scan in scans:
        patient_id = scan["PtID"]
        test_date = scan["TestDt"]
        eye = scan["EYE"]

        points = []
        for i in range(1, 55):
            if i == 26 or i == 35:
                points.append(Point(i, None))
            else:
                points.append(Point(i, int(scan[f"td{i}"])))

        visual_field = VisualField(points)
        garway_heath = GarwayHeathSectorization(visual_field)
        averages_by_sector = garway_heath.get_averages_by_sector()
        averages.append(
            {
                "patient_id": patient_id,
                "test_date": test_date,
                "eye": eye,
                **averages_by_sector,
            }
        )

    fieldnames = list(averages[0].keys())
    with open(output_filepath, "w", encoding="UTF8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(averages)


def get_all_averages_by_sector(input_filepath: str, output_filepath: str):
    df = pd.read_csv(input_filepath)

    result = []

    for sector in Sectors:
        if sector.value.abbreviation != "BS":
            result.append(
                {
                    "sector": sector.value.abbreviation,
                    "mean": df[sector.value.abbreviation].mean(),
                    "std_dev": df[sector.value.abbreviation].std(),
                }
            )

    fieldnames = list(result[0].keys())
    with open(output_filepath, "w", encoding="UTF8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result)


def get_max_min(input_filepath: str):
    scans = file_reader.read_csv(input_filepath)

    keys = []

    for i in range(1, 55):
        if i == 26 or i == 35:
            pass
        else:
            keys.append(f"td{i}")

    max_td = -math.inf
    min_td = math.inf

    for scan in scans:
        for key in keys:
            max_td = max(max_td, int(scan[key]))
            min_td = min(min_td, int(scan[key]))

    print(f"Max: {max_td}, Min: {min_td}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("visual_field_mapper")
    subparser = parser.add_subparsers(dest="command")

    average_by_sector = subparser.add_parser("average-by-sector")
    average_by_sector.add_argument("inputfile", type=str)
    average_by_sector.add_argument("outputfile", type=str)

    all_averages_by_sector = subparser.add_parser("all-averages")
    all_averages_by_sector.add_argument("inputfile", type=str)
    all_averages_by_sector.add_argument("outputfile", type=str)

    max_min = subparser.add_parser("max-min")
    max_min.add_argument("inputfile", type=str)

    args = parser.parse_args()

    if args.command == "average-by-sector":
        get_average_by_sector(args.inputfile, args.outputfile)

    if args.command == "all-averages":
        get_all_averages_by_sector(args.inputfile, args.outputfile)

    if args.command == "max-min":
        get_max_min(args.inputfile)

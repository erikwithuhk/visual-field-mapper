import argparse
import csv
import math
from pathlib import Path

import numpy as np
import pandas as pd

from .file_reader import FileReader
from .garway_heath import GarwayHeathSectorization, SECTORS
from .visual_field import Point, VisualField

BASE_DIR = Path(__file__).parent.parent.resolve()
DATA_DIR = BASE_DIR.joinpath("data")
OUT_DIR = BASE_DIR.joinpath("out")
IMAGE_DIR = OUT_DIR.joinpath("images")

# TODO: Set as env var
NORMAL_DATA_FILEPATH = DATA_DIR.joinpath("normal.csv")
STUDY_DATA_FILEPATH = DATA_DIR.joinpath("study.csv")

NORMAL_MEAN_TD_BY_SECTOR_FILEPATH = OUT_DIR.joinpath("normal_mean_td_by_sector.csv")
NORMAL_AGGREGATE_STATS_FILEPATH = OUT_DIR.joinpath("normal_aggregate_stats.csv")

file_reader = FileReader()


def get_average_by_sector():
    averages = []

    scans = file_reader.read_csv(NORMAL_DATA_FILEPATH)
    for scan in scans:
        patient_id = scan["PtID"]

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
                **averages_by_sector,
            }
        )

    fieldnames = list(averages[0].keys())
    with open(NORMAL_MEAN_TD_BY_SECTOR_FILEPATH, "w", encoding="UTF8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(averages)


def get_stats(sector: str, series: pd.Series, percentile: int = 5):
    return {
        "sector": sector,
        "mean": series.mean(),
        "std_dev": series.std(),
        f"percentile-{percentile}": np.percentile(series, percentile),
    }


def get_all_averages_by_sector():
    df = pd.read_csv(NORMAL_MEAN_TD_BY_SECTOR_FILEPATH)

    all_averages = [
        get_stats(sector.abbreviation, df[sector.abbreviation])
        for sector in SECTORS.values()
        if sector.abbreviation != "BS"
    ]

    fieldnames = list(all_averages[0].keys())
    with open(NORMAL_AGGREGATE_STATS_FILEPATH, "w", encoding="UTF8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_averages)


def get_max_min():
    scans = file_reader.read_csv(NORMAL_DATA_FILEPATH)

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


def draw_heat_map():
    df = pd.read_csv(NORMAL_AGGREGATE_STATS_FILEPATH)
    means_by_sector = {row["sector"]: row["mean"] for _, row in df.iterrows()}

    df = pd.read_csv(STUDY_DATA_FILEPATH)
    for i, row in df.iterrows():
        patient_id = row["PtID"]

        points = []
        for i in range(1, 55):
            if i == 26 or i == 35:
                points.append(Point(i, None))
            else:
                points.append(Point(i, int(row[f"td{i}"])))

        visual_field = VisualField(patient_id, points)
        garway_heath = GarwayHeathSectorization(visual_field)
        heat_map = garway_heath.draw_heat_map(means_by_sector)
        heat_map.saveSvg(f"{IMAGE_DIR}/{patient_id}.svg")
        # heat_map.savePng(IMAGE_DIR.joinpath(f"{patient_id}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("visual_field_mapper")
    subparser = parser.add_subparsers(dest="command")

    average_by_sector = subparser.add_parser("average-by-sector")
    all_averages_by_sector = subparser.add_parser("all-averages")
    max_min = subparser.add_parser("max-min")
    draw_heat_map_parser = subparser.add_parser("draw-heat-map")

    args = parser.parse_args()

    if args.command == "average-by-sector":
        get_average_by_sector()

    if args.command == "all-averages":
        get_all_averages_by_sector()

    if args.command == "max-min":
        get_max_min()

    if args.command == "draw-heat-map":
        draw_heat_map()

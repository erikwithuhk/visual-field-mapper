import argparse
import csv
import logging
import math
import os
from pathlib import Path
from pprint import pformat

import numpy as np
import pandas as pd

from .file_reader import FileReader
from .garway_heath import SECTORS, GarwayHeathSectorization
from .patient import Patient
from .visual_field import Point, VisualField

BASE_DIR = Path(__file__).parent.parent.resolve()
DATA_DIR = BASE_DIR.joinpath("data")
OUT_DIR = BASE_DIR.joinpath("out")
IMAGE_DIR = OUT_DIR.joinpath("images")
SVG_DIR = IMAGE_DIR.joinpath("SVG")
PNG_DIR = IMAGE_DIR.joinpath("PNG")

NORMAL_DATA_FILEPATH = DATA_DIR.joinpath("normal.csv")
STUDY_DATA_FILEPATH = DATA_DIR.joinpath("study.csv")
ARCHETYPE_DATA_FILEPATH = DATA_DIR.joinpath("archetypal_analysis.csv")

NORMAL_MEAN_TD_BY_SECTOR_FILEPATH = OUT_DIR.joinpath("normal_mean_td_by_sector.csv")
NORMAL_AGGREGATE_STATS_FILEPATH = OUT_DIR.joinpath("normal_aggregate_stats.csv")

file_reader = FileReader()


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)


def get_average_by_sector(input_file: str, output_file: str):
    os.makedirs(Path(output_file).parent, exist_ok=True)

    averages = []

    scans = file_reader.read_csv(input_file)
    for scan in scans:
        patient_id = int(scan["PtID"])
        eye = scan["Eye"]

        points = []
        for i in range(1, 55):
            if i == 26 or i == 35:
                points.append(Point(i, None))
            else:
                points.append(Point(i, int(scan[f"td{i}"])))

        visual_field = VisualField(eye, points)
        garway_heath = GarwayHeathSectorization(visual_field)
        averages_by_sector = garway_heath.get_means_by_sector()
        averages.append(
            {
                "patient_id": patient_id,
                **averages_by_sector,
            }
        )

    fieldnames = list(averages[0].keys())
    with open(output_file, "w", encoding="UTF8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(averages)


def get_stats(sector: str, series: pd.Series, percentile: int = 5):
    return {
        "sector": sector,
        "mean": series.mean(),
        "std_dev": series.std(),
        f"percentile_{percentile}": np.percentile(series, percentile),
    }


def get_all_averages_by_sector():
    os.makedirs(Path(NORMAL_AGGREGATE_STATS_FILEPATH).parent, exist_ok=True)

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


def __get_patient_data():
    patient_id_column = "PtID"
    matching_archetypes_column = "matching_archetypes"

    tds_df = pd.read_csv(STUDY_DATA_FILEPATH)
    tds_df.set_index(patient_id_column, inplace=True)

    selected_rows = ["Eye"]
    # Select TD rows
    selected_rows.extend([f"td{i}" for i in range(1, 55)])
    # Select sector averages
    selected_rows.extend([sector for sector in SECTORS if sector != "BS"])
    tds_df = tds_df[selected_rows]

    archetypes_df = pd.read_csv(ARCHETYPE_DATA_FILEPATH)
    archetypes_df.set_index(patient_id_column, inplace=True)

    # Select the columns needed to find matching archetypes
    archetypes_df = archetypes_df[[f"AT{i}" for i in range(1, 17)]]

    # Get matching archetypes
    archetypes_df[matching_archetypes_column] = archetypes_df.apply(
        lambda row: row[pd.to_numeric(row, errors="coerce") >= 0.07].index.to_list(),
        axis=1,
    )

    # Only keep matching archetypes column
    archetypes_df = archetypes_df[[matching_archetypes_column]]

    merge_df = pd.merge(tds_df, archetypes_df, on=patient_id_column, indicator=True)

    missing = merge_df.loc[merge_df["_merge"] != "both"]

    if len(missing) > 0:
        raise Exception("Missing patient data")

    return merge_df


def __save_images(id, row, limits_by_sector):
    logger = logging.getLogger("__save_images")
    patient = Patient.parse(id, row)

    def log(s):
        return logger.info(f"{s} >> %s", pformat({"patient_id": patient.id}))

    log("Rendering SVG")
    svg = patient.render(limits_by_sector)

    log("Saving SVG")
    svg.saveSvg(f"{IMAGE_DIR}/SVG/{patient.id}.svg")

    log("Saving PNG")
    svg.savePng(f"{IMAGE_DIR}/PNG/{patient.id}.png")


def draw_visual_field():
    os.makedirs(SVG_DIR, exist_ok=True)
    os.makedirs(PNG_DIR, exist_ok=True)

    logger = logging.getLogger("draw_visual_field")

    normal_aggregate_df = pd.read_csv(NORMAL_AGGREGATE_STATS_FILEPATH)
    limits_by_sector = {
        row["sector"]: row["percentile_5"] for _, row in normal_aggregate_df.iterrows()
    }

    logger.info("Reading patient data")
    patient_data = __get_patient_data()

    logger.info("Saving images")
    [__save_images(id, row, limits_by_sector) for id, row in patient_data.iterrows()]

    logger.info("All visual fields drawn >> %s", pformat({"total": len(patient_data)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("visual_field_mapper")
    subparser = parser.add_subparsers(dest="command")

    average_by_sector_parser = subparser.add_parser("average-by-sector")
    average_by_sector_parser.add_argument("inputfile", type=str)
    average_by_sector_parser.add_argument("outputfile", type=str)

    all_averages_by_sector_parser = subparser.add_parser("all-averages")
    max_min_parser = subparser.add_parser("max-min")
    draw_parser = subparser.add_parser("draw")

    args = parser.parse_args()

    if args.command == "average-by-sector":
        get_average_by_sector(args.inputfile, args.outputfile)

    if args.command == "all-averages":
        get_all_averages_by_sector()

    if args.command == "max-min":
        get_max_min()

    if args.command == "draw":
        draw_visual_field()

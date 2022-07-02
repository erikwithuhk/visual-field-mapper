import argparse
import csv
import logging
import math
import os
from pathlib import Path
from pprint import pformat
from typing import List
from xml.dom import minidom

import drawSvg as draw
import numpy as np
import pandas as pd

from . import (
    ARCHETYPE_DATA_FILEPATH,
    ARCHETYPE_FILL_COLORS_FILEPATH,
    ASSETS_DIR,
    IMAGE_DIR,
    NORMAL_AGGREGATE_STATS_FILEPATH,
    NORMAL_DATA_FILEPATH,
    NORMAL_MEAN_TD_BY_SECTOR_FILEPATH,
    PNG_DIR,
    STUDY_DATA_FILEPATH,
    SVG_DIR,
    Colors,
    Dimensions,
)
from .archetype import Archetype
from .components.patient_view import PatientView
from .file_reader import FileReader
from .garway_heath import SECTORS, GarwayHeathSectorization
from .patient import Patient
from .visual_field import Point, VisualField

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

    def find_matching_archetype_ids(row) -> List[int]:
        matching_archetypes_cols = row[
            pd.to_numeric(row, errors="coerce") >= 0.07
        ].index.to_list()
        return [int(col.replace("AT", "")) for col in matching_archetypes_cols]

    # Get matching archetypes
    archetypes_df[matching_archetypes_column] = archetypes_df.apply(
        find_matching_archetype_ids,
        axis=1,
    )

    # Only keep matching archetypes column
    archetypes_df = archetypes_df[[matching_archetypes_column]]

    merge_df = pd.merge(tds_df, archetypes_df, on=patient_id_column, indicator=True)

    missing = merge_df.loc[merge_df["_merge"] != "both"]

    if len(missing) > 0:
        raise Exception("Missing patient data")

    return merge_df


def __save_images(id, row, limits_by_sector, fill_colors_by_archetype):
    logger = logging.getLogger("__save_images")

    logger.info("Saving matching_archetype SVGs")
    all_archetypes = [
        Archetype.parse(id, fill_colors)
        for id, fill_colors in fill_colors_by_archetype.iterrows()
    ]
    archetypes_by_id = {archetype.id: archetype for archetype in all_archetypes}

    patient = Patient.parse(id, row, archetypes_by_id)

    def log(s):
        return logger.info(f"{s} >> %s", pformat({"patient_id": patient.id}))

    log("Rendering SVG")
    patient_view = PatientView(patient, limits_by_sector)
    rendered_patient_view = patient_view.render()

    svg_dimensions = patient_view.get_size()

    svg = draw.Drawing(
        svg_dimensions.width,
        svg_dimensions.height,
        origin=(0, -svg_dimensions.height),
        displayInline=False,
    )

    background = draw.Rectangle(
        0,
        -svg_dimensions.height,
        svg_dimensions.width,
        svg_dimensions.height,
        fill=Colors.white.value,
        stroke=Colors.black.value,
        stroke_width=2,
    )

    svg.append(background)
    svg.append(rendered_patient_view)

    log("Saving SVG")
    svg.saveSvg(f"{IMAGE_DIR}/SVG/patient_{patient.id}.svg")

    log("Saving PNG")
    svg.savePng(f"{IMAGE_DIR}/PNG/patient_{patient.id}.png")


def draw_visual_field(test: bool = False):
    os.makedirs(SVG_DIR, exist_ok=True)
    os.makedirs(PNG_DIR, exist_ok=True)

    logger = logging.getLogger("draw_visual_field")

    logger.info("Getting limits by sector")
    normal_aggregate_df = pd.read_csv(NORMAL_AGGREGATE_STATS_FILEPATH)
    limits_by_sector = {
        row["sector"]: row["percentile_5"] for _, row in normal_aggregate_df.iterrows()
    }

    logger.info("Getting fills by archetype")
    fill_colors_by_archetype = pd.read_csv(ARCHETYPE_FILL_COLORS_FILEPATH)
    fill_colors_by_archetype = fill_colors_by_archetype.set_index("id")

    logger.info("Reading patient data")
    patient_data = __get_patient_data()

    logger.info("Saving images")
    if test:
        patient_data = patient_data[:10]

    [
        __save_images(id, row, limits_by_sector, fill_colors_by_archetype)
        for id, row in patient_data.iterrows()
    ]

    logger.info("All visual fields drawn >> %s", pformat({"total": len(patient_data)}))


def __get_coordinates(x: float, y: float):
    width = 17.42
    height = 14.56
    row = y / height
    column = x / width
    return (round(row), round(column))


COL_OFFSETS = [3, 2, 1, 0, 0, 1, 2, 3]
TOTAL_COLUMNS = 9
ROW_LENGTHS = [4, 6, 8, 9, 9, 8, 6, 4]
ROW_STARTS = [1, 5, 11, 19, 28, 37, 45, 51]


def __get_position(coordinates) -> int:
    row = coordinates[0]
    col = coordinates[1]
    return ROW_STARTS[row] + col - COL_OFFSETS[row] - 1


def __extract_fills(svg):
    rects = svg.getElementsByTagName("rect")
    fills = [None] * 54
    for rect in rects:
        x = rect.getAttribute("x") or 0
        y = rect.getAttribute("y") or 0
        coordinates = __get_coordinates(float(x), float(y))
        position = __get_position(coordinates)

        fill = rect.getAttribute("fill")

        if fill == "none" or fill == "#bfbebe":
            fill = None

        if fill:
            fills[position] = fill
    return fills


def __parse_archetype_fill(id: int):
    filepath = str(ASSETS_DIR.joinpath(f"{id}.svg"))
    svg = minidom.parse(filepath)
    return __extract_fills(svg)


def get_archetype_fills():
    fills = {f"{id}": __parse_archetype_fill(id) for id in range(1, 17)}
    df = pd.DataFrame(fills).transpose()
    df.index.name = "id"
    df.to_csv(ARCHETYPE_FILL_COLORS_FILEPATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("visual_field_mapper")
    subparser = parser.add_subparsers(dest="command")

    average_by_sector_parser = subparser.add_parser("average-by-sector")
    average_by_sector_parser.add_argument("inputfile", type=str)
    average_by_sector_parser.add_argument("outputfile", type=str)

    all_averages_by_sector_parser = subparser.add_parser("all-averages")
    max_min_parser = subparser.add_parser("max-min")

    draw_parser = subparser.add_parser("draw")
    draw_parser.add_argument("--test", action=argparse.BooleanOptionalAction)

    get_archetype_fills_parser = subparser.add_parser("get-archetype-fills")

    args = parser.parse_args()

    if args.command == "average-by-sector":
        get_average_by_sector(args.inputfile, args.outputfile)

    if args.command == "all-averages":
        get_all_averages_by_sector()

    if args.command == "max-min":
        get_max_min()

    if args.command == "draw":
        draw_visual_field(test=args.test)

    if args.command == "get-archetype-fills":
        get_archetype_fills()

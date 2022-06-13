import argparse
import csv
import math
from pathlib import Path

import drawSvg as draw
import numpy as np
import pandas as pd

from visual_field_mapper import Colors, Dimensions, Position

from .file_reader import FileReader
from .garway_heath import SECTORS, GarwayHeathSectorization
from .visual_field import Point, VisualField

BASE_DIR = Path(__file__).parent.parent.resolve()
DATA_DIR = BASE_DIR.joinpath("data")
OUT_DIR = BASE_DIR.joinpath("out")
IMAGE_DIR = OUT_DIR.joinpath("images")

NORMAL_DATA_FILEPATH = DATA_DIR.joinpath("normal.csv")
STUDY_DATA_FILEPATH = DATA_DIR.joinpath("study.csv")

NORMAL_MEAN_TD_BY_SECTOR_FILEPATH = OUT_DIR.joinpath("normal_mean_td_by_sector.csv")
NORMAL_AGGREGATE_STATS_FILEPATH = OUT_DIR.joinpath("normal_aggregate_stats.csv")

file_reader = FileReader()


def get_average_by_sector(input_file: str, output_file: str):
    averages = []

    scans = file_reader.read_csv(input_file)
    for scan in scans:
        patient_id = int(scan["PtID"])
        eye = None
        try:
            eye = scan["Affected_Eye"]
        except:
            eye = scan["EYE"]

        points = []
        for i in range(1, 55):
            if i == 26 or i == 35:
                points.append(Point(i, None))
            else:
                points.append(Point(i, int(scan[f"td{i}"])))

        visual_field = VisualField(patient_id, eye, points)
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


def draw_visual_field():
    df = pd.read_csv(NORMAL_AGGREGATE_STATS_FILEPATH)
    percentiles_5_by_sector = {
        row["sector"]: row["percentile_5"] for _, row in df.iterrows()
    }

    cell_dimensions = Dimensions(75, 50)
    drawing_dimensions = Dimensions(
        9 * cell_dimensions.width, 8 * cell_dimensions.height
    )
    margin = cell_dimensions.height
    title_height = cell_dimensions.height / 2

    df = pd.read_csv(STUDY_DATA_FILEPATH)
    for i, row in df.iterrows():
        patient_id = row["PtID"]
        affected_eye = row["Affected_Eye"]

        points = []
        for i in range(1, 55):
            if i == 26 or i == 35:
                points.append(Point(i, None))
            else:
                points.append(Point(i, int(row[f"td{i}"])))

        svg_dimensions = Dimensions(
            drawing_dimensions.width * 2 + margin * 3,
            title_height + drawing_dimensions.height + margin * 3,
        )
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
        )
        svg.append(background)

        title = draw.Text(
            f"Patient #{patient_id}",
            16 * 2,
            x="50%",
            y=-margin,
            height=title_height,
            font_family="Arial",
            center=True,
        )
        svg.append(title)

        position_y = title_height + margin * 2

        visual_field = VisualField(patient_id, affected_eye, points)
        visual_field_position = Position(margin, position_y)
        visual_field_map = visual_field.draw(cell_dimensions, visual_field_position)
        svg.append(visual_field_map)

        garway_heath = GarwayHeathSectorization(visual_field)
        garway_heath_position = Position(
            visual_field_position.x + drawing_dimensions.width + margin,
            position_y,
        )
        garway_heath_map = garway_heath.draw(
            percentiles_5_by_sector, cell_dimensions, garway_heath_position
        )
        svg.append(garway_heath_map)

        svg.saveSvg(f"{IMAGE_DIR}/SVG/{patient_id}.svg")
        svg.savePng(f"{IMAGE_DIR}/PNG/{patient_id}.png")


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

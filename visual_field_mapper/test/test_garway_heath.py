import pytest
from visual_field_mapper.garway_heath import (
    GarwayHeathSectorization,
    Sector,
    Sectors,
    get_sector,
)
from visual_field_mapper.visual_field import Point, VisualField

from visual_field_mapper.test.test_visual_field import points, total_deviations


@pytest.fixture
def sector():
    return Sector("name", "NN", "")


def test_add_point(points, sector):
    sector.add_point(points[0])
    sector.add_point(points[1])
    sector.add_point(points[2])

    sector_points = sector.get_points()
    assert sector_points[0] == points[0]
    assert sector_points[1] == points[1]
    assert sector_points[2] == points[2]


def test_get_average_total_deviation(sector):
    sector.add_point(Point(1, 0))
    assert sector.get_average_total_deviation() == 0
    sector.add_point(Point(2, 1))
    assert sector.get_average_total_deviation() == 0.5
    sector.add_point(Point(3, 2))
    assert sector.get_average_total_deviation() == 1
    sector.add_point(Point(4, 4))
    assert sector.get_average_total_deviation() == 1.75


@pytest.mark.parametrize(
    "position, expected_sector",
    [
        (1, Sectors.IN),
        (2, Sectors.IN),
        (3, Sectors.IN),
        (4, Sectors.IN),
        (5, Sectors.IN),
        (6, Sectors.IT),
        (7, Sectors.IT),
        (8, Sectors.IT),
        (9, Sectors.IT),
        (10, Sectors.IN),
        (11, Sectors.IT),
        (12, Sectors.IT),
        (13, Sectors.IT),
        (14, Sectors.IT),
        (15, Sectors.IT),
        (16, Sectors.IT),
        (17, Sectors.IN),
        (18, Sectors.N),
        (19, Sectors.IT),
        (20, Sectors.IT),
        (21, Sectors.IT),
        (22, Sectors.IT),
        (23, Sectors.T),
        (24, Sectors.T),
        (25, Sectors.T),
        (26, Sectors.BS),
        (27, Sectors.N),
        (28, Sectors.SN),
        (29, Sectors.ST),
        (30, Sectors.ST),
        (31, Sectors.ST),
        (32, Sectors.T),
        (33, Sectors.T),
        (34, Sectors.T),
        (35, Sectors.BS),
        (36, Sectors.N),
        (37, Sectors.SN),
        (38, Sectors.ST),
        (39, Sectors.ST),
        (40, Sectors.ST),
        (41, Sectors.ST),
        (42, Sectors.ST),
        (43, Sectors.SN),
        (44, Sectors.N),
        (45, Sectors.SN),
        (46, Sectors.SN),
        (47, Sectors.ST),
        (48, Sectors.ST),
        (49, Sectors.SN),
        (50, Sectors.SN),
        (51, Sectors.SN),
        (52, Sectors.SN),
        (53, Sectors.SN),
        (54, Sectors.SN),
    ],
)
def test_get_sector(position, expected_sector):
    point = Point(position, 0)
    assert get_sector(point) == expected_sector


@pytest.mark.parametrize(
    "tds, expected",
    [
        (
            [
                -2,
                -2,
                -2,
                -4,
                -2,
                -4,
                -2,
                -1,
                -1,
                -5,
                -2,
                -3,
                -1,
                -6,
                -2,
                -3,
                -5,
                -6,
                -1,
                -6,
                -1,
                -3,
                -7,
                -3,
                -3,
                None,
                -4,
                -2,
                -3,
                0,
                -2,
                -2,
                -1,
                -2,
                None,
                -3,
                2,
                -2,
                0,
                0,
                -3,
                -2,
                -2,
                -5,
                -1,
                -1,
                -2,
                -3,
                -3,
                -3,
                0,
                1,
                -3,
                -3,
            ],
            {
                "SN": -1.363636364,
                "N": -4.5,
                "IN": -3.142857143,
                "IT": -2.571428571,
                "T": -3,
                "ST": -1.7,
            },
        ),
        (
            [
                -2,
                -2,
                -3,
                -1,
                -5,
                -4,
                -3,
                -7,
                -2,
                -1,
                -1,
                0,
                -2,
                -6,
                -3,
                -1,
                -2,
                -3,
                -4,
                -4,
                -4,
                -4,
                -1,
                -3,
                -1,
                None,
                0,
                1,
                -3,
                -1,
                -1,
                -2,
                -1,
                -3,
                None,
                -2,
                -1,
                -2,
                2,
                -1,
                -2,
                -2,
                -2,
                -2,
                -1,
                -1,
                -3,
                -2,
                -1,
                -2,
                -2,
                0,
                -1,
                -3,
            ],
            {
                "SN": -1.181818182,
                "N": -1.75,
                "IN": -2.285714286,
                "IT": -3.214285714,
                "T": -1.833333333,
                "ST": -1.5,
            },
        ),
        (
            [
                -12,
                -14,
                -23,
                -29,
                -12,
                -8,
                -6,
                -5,
                -6,
                -1,
                -6,
                -2,
                -4,
                -2,
                -3,
                -5,
                -5,
                -5,
                -4,
                -8,
                -2,
                -6,
                -3,
                -6,
                -1,
                None,
                -6,
                -7,
                -5,
                -3,
                -3,
                -2,
                -3,
                -2,
                None,
                -1,
                1,
                -6,
                0,
                -5,
                -2,
                -6,
                -4,
                -1,
                -1,
                -7,
                0,
                -5,
                -1,
                -2,
                0,
                -2,
                -3,
                -3,
            ],
            {
                "SN": -2.636363636,
                "N": -3.25,
                "IN": -13.71428571,
                "IT": -4.785714286,
                "T": -2.833333333,
                "ST": -3.5,
            },
        ),
    ],
)
def test_get_averages_by_sector(tds, expected):
    points = [Point(i + 1, td) for i, td in enumerate(tds)]
    visual_field = VisualField(points)
    garway_heath = GarwayHeathSectorization(visual_field)
    actual = garway_heath.get_averages_by_sector()
    assert round(actual["SN"], 4) == round(expected["SN"], 4)
    assert round(actual["N"], 4) == round(expected["N"], 4)
    assert round(actual["IN"], 4) == round(expected["IN"], 4)
    assert round(actual["IT"], 4) == round(expected["IT"], 4)
    assert round(actual["T"], 4) == round(expected["T"], 4)
    assert round(actual["ST"], 4) == round(expected["ST"], 4)

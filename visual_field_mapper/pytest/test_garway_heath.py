import pytest
from visual_field_mapper.garway_heath import (
    GarwayHeathSectorization,
    Sector,
    get_sector,
)
from visual_field_mapper.visual_field import Point, VisualField


@pytest.fixture
def sector():
    return Sector("name", "NN", "")


@pytest.mark.parametrize(
    "position, expected_sector",
    [
        (1, "IN"),
        (2, "IN"),
        (3, "IN"),
        (4, "IN"),
        (5, "IN"),
        (6, "IT"),
        (7, "IT"),
        (8, "IT"),
        (9, "IT"),
        (10, "IN"),
        (11, "IT"),
        (12, "IT"),
        (13, "IT"),
        (14, "IT"),
        (15, "IT"),
        (16, "IT"),
        (17, "IN"),
        (18, "N"),
        (19, "IT"),
        (20, "IT"),
        (21, "IT"),
        (22, "IT"),
        (23, "T"),
        (24, "T"),
        (25, "T"),
        (26, "BS"),
        (27, "N"),
        (28, "SN"),
        (29, "ST"),
        (30, "ST"),
        (31, "ST"),
        (32, "T"),
        (33, "T"),
        (34, "T"),
        (35, "BS"),
        (36, "N"),
        (37, "SN"),
        (38, "ST"),
        (39, "ST"),
        (40, "ST"),
        (41, "ST"),
        (42, "ST"),
        (43, "SN"),
        (44, "N"),
        (45, "SN"),
        (46, "SN"),
        (47, "ST"),
        (48, "ST"),
        (49, "SN"),
        (50, "SN"),
        (51, "SN"),
        (52, "SN"),
        (53, "SN"),
        (54, "SN"),
    ],
)
def test_get_sector(position, expected_sector):
    point = Point(position, 0)
    sector = get_sector(point)
    assert sector.abbreviation == expected_sector


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
                "IN": -3.142857143,
                "IT": -2.571428571,
                "T": -3,
                "N": -4.5,
                "ST": -1.7,
                "SN": -1.363636364,
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
                "IN": -2.285714286,
                "IT": -3.214285714,
                "T": -1.833333333,
                "N": -1.75,
                "ST": -1.5,
                "SN": -1.181818182,
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
                "IN": -13.71428571,
                "IT": -4.785714286,
                "T": -2.833333333,
                "N": -3.25,
                "ST": -3.5,
                "SN": -2.636363636,
            },
        ),
        (
            [
                -1,
                -1,
                0,
                0,
                0,
                -1,
                1,
                2,
                1,
                -6,
                1,
                -1,
                3,
                -3,
                -2,
                -4,
                -1,
                0,
                1,
                -1,
                -1,
                -1,
                0,
                -2,
                -2,
                None,
                1,
                0,
                2,
                2,
                0,
                3,
                0,
                0,
                None,
                3,
                -2,
                2,
                -6,
                -2,
                -3,
                -5,
                -1,
                -1,
                0,
                0,
                0,
                -3,
                0,
                3,
                -2,
                -1,
                -2,
                2,
            ],
            {
                "IN": -1.285714286,
                "IT": -0.3571428571,
                "T": -0.1666666667,
                "N": 0.75,
                "ST": -1.3,
                "SN": -0.2727272727,
            },
        ),
    ],
)
def test_get_means_by_sector(tds, expected):
    points = [Point(i + 1, td) for i, td in enumerate(tds)]
    visual_field = VisualField("OD", points)
    garway_heath = GarwayHeathSectorization(visual_field)
    actual = garway_heath.get_means_by_sector()
    assert round(actual["IN"], 4) == round(expected["IN"], 4)
    assert round(actual["IT"], 4) == round(expected["IT"], 4)
    assert round(actual["T"], 4) == round(expected["T"], 4)
    assert round(actual["N"], 4) == round(expected["N"], 4)
    assert round(actual["ST"], 4) == round(expected["ST"], 4)
    assert round(actual["SN"], 4) == round(expected["SN"], 4)

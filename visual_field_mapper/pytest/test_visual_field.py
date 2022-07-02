import pytest
from visual_field_mapper import Colors
from visual_field_mapper.visual_field import Point, VisualField


def test_point_constructor(total_deviations):
    for i, total_deviation in enumerate(total_deviations):
        position = i + 1
        point = Point(position, total_deviation)
        assert point.position == position
        assert point.total_deviation == total_deviation


def test_point_constructor_accepts_fill():
    color = "#fff"
    point = Point(1, 0, color)
    assert point.fill.color == color
    assert point.fill.opacity == 1.0


@pytest.mark.parametrize(
    "td, expected_color, expected_opacity",
    [
        (None, Colors.black, 1.0),
        (35, Colors.white, 0.0),
        (11, Colors.white, 0.0),
        (10, Colors.red, 0.0),
        (-12.5, Colors.red, 0.5),
        (-35, Colors.red, 1.0),
    ],
)
def test_point_constructor_generates_fill(td, expected_color, expected_opacity):
    point = Point(1, td)
    assert point.fill.color == expected_color.value
    assert point.fill.opacity == expected_opacity


def test_visual_field_construtctor(points):
    eye = "OD"
    visual_field = VisualField(eye, points)
    assert visual_field.eye == eye
    assert visual_field.points == points

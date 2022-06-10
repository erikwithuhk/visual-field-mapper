import pytest
from visual_field_mapper.visual_field import Point, VisualField


@pytest.fixture
def total_deviations(faker):
    return [faker.random_int(min=-35, max=35) for _ in range(0, 54)]


@pytest.fixture
def points(total_deviations):
    return [Point(i + 1, td) for i, td in enumerate(total_deviations)]


def test_point_constructor(total_deviations):
    for i, total_deviation in enumerate(total_deviations):
        position = i + 1
        point = Point(position, total_deviation)
        assert point.position == position
        assert point.total_deviation == total_deviation


def test_visual_field_construtctor(points):
    visual_field = VisualField(points)
    assert visual_field.points == points

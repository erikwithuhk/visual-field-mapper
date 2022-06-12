import pytest

from visual_field_mapper.visual_field import Point


@pytest.fixture
def total_deviations(faker):
    return [faker.random_int(min=-35, max=35) for _ in range(0, 54)]


@pytest.fixture
def points(total_deviations):
    return [Point(i + 1, td) for i, td in enumerate(total_deviations)]

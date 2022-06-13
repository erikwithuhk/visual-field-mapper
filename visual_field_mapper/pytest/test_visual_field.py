import pytest
from visual_field_mapper.visual_field import Point, VisualField


def test_point_constructor(total_deviations):
    for i, total_deviation in enumerate(total_deviations):
        position = i + 1
        point = Point(position, total_deviation)
        assert point.position == position
        assert point.total_deviation == total_deviation


def test_visual_field_construtctor(points):
    patient_id = "patient_id"
    eye = "OD"
    visual_field = VisualField(patient_id, eye, points)
    assert visual_field.patient_id == patient_id
    assert visual_field.eye == eye
    assert visual_field.points == points

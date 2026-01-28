import pytest
from hw00b import classify_triangle


def test_equilateral():
    assert classify_triangle(3, 3, 3) == "equilateral"


def test_scalene_right():
    assert classify_triangle(3, 4, 5) == "scalene right triangle"


def test_isosceles():
    assert classify_triangle(5, 5, 8) == "isosceles"


def test_invalid_triangle():
    assert classify_triangle(1, 2, 3) == "Not a valid triangle"

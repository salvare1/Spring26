import pytest
"""Utility functions to handle test cases"""
from hw00b import classify_triangle


def test_equilateral():
    """
    Docstring for test_equilateral
    """
    assert classify_triangle(3, 3, 3) == "equilateral"


def test_scalene_right():
    """
    Docstring for test_scalene_right
    """
    assert classify_triangle(3, 4, 5) == "scalene right triangle"


def test_isosceles():
    """
    Docstring for test_isosceles
    """
    assert classify_triangle(5, 5, 8) == "isosceles"


def test_invalid_triangle():
    """
    Docstring for test_invalid_triangle
    """
    assert classify_triangle(1, 2, 3) == "Not a valid triangle"

def test_scalene_not_right():
    """
    Docstring for test_scalene_not_right
    """
    assert classify_triangle(2, 3, 4) == "scalene"

def test_invalid_zero_side():
    """
    Docstring for test_invalid_zero_side
    """
    assert classify_triangle(0, 3, 4) == "Not a valid triangle"


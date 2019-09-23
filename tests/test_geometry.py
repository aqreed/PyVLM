"""
    Unit tests of the Geometry methods

"""

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from vlm.geometry import (cross_prod, vect_dot, norm_dir_vect,
                            dist_point2line, area_4points)


def test_cross_prod():
    A = np.array([0, 0])
    B = np.array([1, 1])

    calculated_vector = cross_prod(A, B)
    expected_vector = 0.0*1.0 - 0.0*1.0

    assert_almost_equal(calculated_vector, expected_vector)


def test_vect_dot():
    A = np.array([0, 0])
    B = np.array([1, 1])

    calculated_vector = vect_dot(A, B)
    expected_vector = 0.0*1.0 + 0.0*1.0

    assert_almost_equal(calculated_vector, expected_vector)


def test_norm_dir_vect():
    A = np.array([0, 0])
    B = np.array([1, 1])

    calculated_vector = norm_dir_vect(A, B)
    expected_vector = np.sqrt(2)/2 * np.array([1, 1])

    assert_almost_equal(calculated_vector, expected_vector)


def test_dist_point2line():
    P = np.array([0, 1])
    A = np.array([0, 0])
    B = np.array([1, 0])

    calculated_dist = dist_point2line(P, A, B)
    expected_dist = 1.0

    assert_almost_equal(calculated_dist, expected_dist)


def test_area_4points():
    A = np.array([0, 0])
    B = np.array([1, 0])
    C = np.array([1, 1])
    D = np.array([0, 1])

    calculated_area = area_4points(A, B, C, D)
    expected_area = 1.0

    assert_almost_equal(calculated_area, expected_area)

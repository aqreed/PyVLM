"""
    Unit tests of the Mesh class and its methods

"""

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from vlm.vlm import PyVLM


def test_add_wing():
    test_wing = PyVLM()

    A = np.array([0, 0])
    B = np.array([0, 1])

    leading_edges_position = [A, B]
    chord_length = [1, 1]

    n, m = 1, 2
    test_wing.add_wing(leading_edges_position, chord_length, n, m)

    calculated_points = test_wing.Points
    expected_points = [np.array([0, 0]), np.array([0, .5]), np.array([0, 1]),
                       np.array([1, 0]), np.array([1, .5]), np.array([1, 1]),
                       np.array([0, -1]), np.array([0, -.5]), np.array([0, 0]),
                       np.array([1, -1]), np.array([1, -.5]), np.array([1, 0])]

    assert_almost_equal(calculated_points, expected_points)


def test_vlm():
    test_vlm = PyVLM()

    A = np.array([0, 0])
    B = np.array([0, 1])

    leading_edges_position = [A, B]
    chord_length = [1, 1]

    n, m = 1, 1
    test_vlm.add_wing(leading_edges_position, chord_length, n, m)

    alpha = np.deg2rad(0)

    test_vlm.vlm(alpha, False)

    calculated_AIC = test_vlm.AIC
    expected_AIC = np.array([[-0.768468, 0.1634183],
                             [0.1634183, -0.768468]])

    assert_almost_equal(calculated_AIC, expected_AIC)

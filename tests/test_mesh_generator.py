"""
    Unit tests of the Mesh class and its methods

"""

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from vlm.mesh_generator import Mesh


def test_mesh_points():
    A, B = np.array([0, 0]), np.array([0, 1])

    leading_edges_coord = [A, B]
    chord_lengths = [1, 1]

    mesh = Mesh(leading_edges_coord, chord_lengths, 1, 2)

    calculated_points = mesh.points()
    expected_points = [np.array([0, 0]), np.array([0, 0.5]),
                       np.array([0, 1]), np.array([1, 0]),
                       np.array([1, 0.5]), np.array([1, 1])]

    assert_almost_equal(calculated_points, expected_points)


def test_mesh_panels():
    A, B = np.array([0, 0]), np.array([0, 1])

    leading_edges_coord = [A, B]
    chord_lengths = [1, 1]

    mesh = Mesh(leading_edges_coord, chord_lengths, 1, 2)
    mesh.points()

    panels = mesh.panels()
    calculated_panel = [panels[0].P1, panels[0].P2,
                        panels[0].P3, panels[0].P4]
    expected_panel = [np.array([1, 0]), np.array([0, 0]),
                      np.array([0, .5]), np.array([1, 0.5])]

    assert_almost_equal(calculated_panel, expected_panel)

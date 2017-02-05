"""
    Unit tests of the Mesh class and its methods

"""

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from pyvlm.mesh_generator import Mesh


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

    calculated_panels = mesh.panels()
    expected_panels = [[np.array([1, 0]), np.array([0, 0]),
                        np.array([0, .5]), np.array([1, 0.5])],
                       [np.array([1, 0.5]), np.array([0, 0.5]),
                        np.array([0, 1]), np.array([1, 1])]]

    assert_almost_equal(calculated_panels, expected_panels)


def test_mesh_chordwise_panel_pos():
    A, B = np.array([0, 0]), np.array([0, 1])

    leading_edges_coord = [A, B]
    chord_lengths = [1, 1]

    mesh = Mesh(leading_edges_coord, chord_lengths, 1, 2)
    mesh.points()
    mesh.panels()

    calculated_chordwise_panel_pos = mesh.panel_chord_positions()
    expected_chordwise_panel_pos = np.array([.5, .5])

    assert_almost_equal(calculated_chordwise_panel_pos,
                        expected_chordwise_panel_pos)


def test_mesh_panels_span():
    A, B = np.array([0, 0]), np.array([0, 1])

    leading_edges_coord = [A, B]
    chord_lengths = [1, 1]

    mesh = Mesh(leading_edges_coord, chord_lengths, 1, 2)
    mesh.points()
    mesh.panels()

    calculated_panels_span = mesh.panels_span()
    expected_panels_span = np.array([.5, .5])

    assert_almost_equal(calculated_panels_span, expected_panels_span)

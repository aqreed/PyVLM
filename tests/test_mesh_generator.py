"""
    Unit tests of the Mesh class and its methods

"""

import pytest
from numpy import array
from numpy.testing import assert_almost_equal

from vlm.mesh_generator import Mesh


def test_mesh_points():
    A, B = array([0, 0]), array([0, 1])

    leading_edges_coord = [A, B]
    chord_lengths = [1, 1]
    n, m = 1, 2
    mesh = Mesh(leading_edges_coord, chord_lengths, n, m)

    calculated_points = mesh.points()
    expected_points = [array([0, 0]), array([0, 0.5]),
                       array([0, 1]), array([1, 0]),
                       array([1, 0.5]), array([1, 1])]

    assert_almost_equal(calculated_points, expected_points)


def test_mesh_points_BS():
    """
    Based on example 7.2 of Bertin & Smith "Aerodynamics for
    Engineers" with b = 1
    """
    A, B = array([0, 0]), array([0.5, 0.5])

    leading_edges_coord = [A, B]
    chord_lengths = [.2, .2]
    n, m = 1, 4
    mesh = Mesh(leading_edges_coord, chord_lengths, n, m)

    calculated_points = mesh.points()
    expected_points = [array([0, 0]), array([0.125, 0.125]),
                       array([0.25, 0.25]), array([0.375, 0.375]),
                       array([0.5, 0.5]), array([0.2, 0.0]),
                       array([0.325, 0.125]), array([0.45, 0.25]),
                       array([0.575, 0.375]), array([0.7, 0.5])]

    assert_almost_equal(calculated_points, expected_points)


def test_mesh_panels():
    A, B = array([0, 0]), array([0, 1])

    leading_edges_coord = [A, B]
    chord_lengths = [1, 1]
    n, m = 1, 2
    mesh = Mesh(leading_edges_coord, chord_lengths, n, m)
    mesh.points()

    panels = mesh.panels()
    calculated_panel = [panels[0].P1, panels[0].P2,
                        panels[0].P3, panels[0].P4]
    expected_panel = [array([1, 0]), array([0, 0]),
                      array([0, .5]), array([1, 0.5])]

    assert_almost_equal(calculated_panel, expected_panel)


def test_mesh_panels_BS():
    """
    Based on example 7.2 of Bertin & Smith "Aerodynamics for
    Engineers" with b = 1
    """
    A, B = array([0, 0]), array([0.5, 0.5])

    leading_edges_coord = [A, B]
    chord_lengths = [.2, .2]
    n, m = 1, 4
    mesh = Mesh(leading_edges_coord, chord_lengths, n, m)
    mesh.points()

    panels = mesh.panels()
    calculated_bound_vortices = [panels[0].A, panels[0].B,
                                 panels[1].A, panels[1].B,
                                 panels[2].A, panels[2].B,
                                 panels[3].A, panels[3].B]
    expected_bound_vortices = [array([0.05, 0]), array([0.175, 0.125]),
                               array([0.175, 0.125]), array([0.3, 0.25]),
                               array([0.3, 0.25]), array([0.425, 0.375]),
                               array([0.425, 0.375]), array([0.55, 0.5])]

    assert_almost_equal(calculated_bound_vortices, expected_bound_vortices)

    calculated_control_point = [panels[0].CP, panels[1].CP,
                                panels[2].CP, panels[3].CP]
    expected_control_point = [array([0.2125, 0.0625]),
                              array([0.3375, 0.1875]),
                              array([0.4625, 0.3125]),
                              array([0.5875, 0.4375])]

    assert_almost_equal(calculated_control_point, expected_control_point)

"""
    This tests aims to validate the Panel class

"""

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from pyvlm.panel import Panel


def test_area():
    # Grid generator
    b, c = 1, 1  # size of the panel (span, chord)
    P1, P2 = np.array([c/2, -b/2]), np.array([-c/2, -b/2])
    P3, P4 = np.array([-c/2, b/2]), np.array([c/2, b/2])

    # Creating the panel from the points of the grid
    panel = Panel(P1, P2, P3, P4)

    calculated_area = panel.area()
    expected_area = 1.0

    assert_almost_equal(calculated_area, expected_area)


def test_span():
    # Grid generator
    b, c = 1, 1  # size of the panel (span, chord)
    P1, P2 = np.array([c/2, -b/2]), np.array([-c/2, -b/2])
    P3, P4 = np.array([-c/2, b/2]), np.array([c/2, b/2])

    # Creating the panel from the points of the grid
    panel = Panel(P1, P2, P3, P4)

    calculated_span = panel.span()
    expected_span = 1.0

    assert_almost_equal(calculated_span, expected_span)


def test__vortex_position():
    # Grid generator
    b, c = 1, 1  # size of the panel (span, chord)
    P1, P2 = np.array([c/2, -b/2]), np.array([-c/2, -b/2])
    P3, P4 = np.array([-c/2, b/2]), np.array([c/2, b/2])

    # Creating the panel from the points of the grid
    panel = Panel(P1, P2, P3, P4)

    calculated_position = panel._vortex_position()
    expected_position = [np.array([0.25, 0]), np.array([0.25, -0.5]),
                         np.array([-0.25, -0.5]), np.array([-0.25, 0.5]),
                         np.array([0.25, 0.5])]

    assert_almost_equal(calculated_position, expected_position)


def test_cp_position():
    # Grid generator
    b, c = 1, 1  # size of the panel (span, chord)
    P1, P2 = np.array([c/2, -b/2]), np.array([-c/2, -b/2])
    P3, P4 = np.array([-c/2, b/2]), np.array([c/2, b/2])

    # Creating the panel from the points of the grid
    panel = Panel(P1, P2, P3, P4)

    calculated_position = panel.control_point()
    expected_position = np.array([0.25, 0])

    assert_almost_equal(calculated_position, expected_position)


def test_v_induced():
    # Grid generator
    b, c = 1, 1  # size of the panel (span, chord)
    P1, P2 = np.array([c/2, -b/2]), np.array([-c/2, -b/2])
    P3, P4 = np.array([-c/2, b/2]), np.array([c/2, b/2])

    # Creating the panel from the points of the grid
    panel = Panel(P1, P2, P3, P4)
    CP = panel.control_point()

    calculated_velocity = panel.induced_velocity(CP)
    expected_velocity = -0.76846804

    assert_almost_equal(calculated_velocity, expected_velocity)

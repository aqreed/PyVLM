"""
    Unit tests of the Panel class and its methods

"""

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from vlm.panel import Panel


def test_area():
    P1, P2 = np.array([1, 0]), np.array([0, 0])
    P3, P4 = np.array([0, 1]), np.array([1, 1])

    panel = Panel(P1, P2, P3, P4)

    calculated_area = panel.area
    expected_area = 1.0

    assert_almost_equal(calculated_area, expected_area)


def test_span():
    P1, P2 = np.array([1, 0]), np.array([0, 0])
    P3, P4 = np.array([0, 1]), np.array([1, 1])

    panel = Panel(P1, P2, P3, P4)

    calculated_span = panel.span
    expected_span = 1.0

    assert_almost_equal(calculated_span, expected_span)


def test_vortex_position():
    P1, P2 = np.array([1, 0]), np.array([0, 0])
    P3, P4 = np.array([0, 1]), np.array([1, 1])

    panel = Panel(P1, P2, P3, P4)

    calculated_vortex_position = [panel.CP, panel.A, panel.B]
    expected_vortex_position = [np.array([0.75, 0.5]),
                                np.array([0.25, 0]),
                                np.array([0.25, 1])]

    assert_almost_equal(calculated_vortex_position,
                        expected_vortex_position)


def test_control_point():
    P1, P2 = np.array([1, 0]), np.array([0, 0])
    P3, P4 = np.array([0, 1]), np.array([1, 1])

    panel = Panel(P1, P2, P3, P4)

    calculated_control_point = panel.CP
    expected_control_point = np.array([0.75, 0.5])

    assert_almost_equal(calculated_control_point,
                        expected_control_point)


def test_induced_velocity():
    P1, P2 = np.array([1, 0]), np.array([0, 0])
    P3, P4 = np.array([0, 1]), np.array([1, 1])

    panel = Panel(P1, P2, P3, P4)
    CP = panel.CP

    calculated_induced_velocity = panel.induced_velocity(CP)
    expected_induced_velocity = -0.7684680, -0.543389

    assert_almost_equal(calculated_induced_velocity,
                        expected_induced_velocity)

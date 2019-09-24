"""
    Unit tests of the Vortices methods

"""

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from vlm.vortices import (vortex_position_in_panel,
                          v_induced_by_horseshoe_vortex,
                          v_induced_by_finite_vortex_line)


def test_vortex_position_in_panel():
    P1 = np.array([1, 0])
    P2 = np.array([0, 0])
    P3 = np.array([0, 1])
    P4 = np.array([0.5, 1])

    calculated_points = vortex_position_in_panel(P1, P2, P3, P4)
    expected_points = [np.array([0.5625, 0.5]),
                       np.array([0.25, 0]),
                       np.array([0.125, 1])]

    assert_almost_equal(calculated_points, expected_points)


def test_v_induced_by_horseshoe_vortex():
    P = np.array([1, 0.5])
    P1 = np.array([0, 0])
    P2 = np.array([0, 1])

    calculated_vel = v_induced_by_horseshoe_vortex(P, P1, P2)
    expected_vel = -0.674191156, -0.6030149

    assert_almost_equal(calculated_vel, expected_vel)

    # point P in between P1 and P2: vtotal == vtrail
    P = np.array([0, 0.5])
    P1 = np.array([0, 0])
    P2 = np.array([0, 1])

    vtotal = v_induced_by_horseshoe_vortex(P, P1, P2)[0]
    vtrail = v_induced_by_horseshoe_vortex(P, P1, P2)[1]

    assert_almost_equal(vtotal, vtrail)

    # point P = P1: vbound = vtrail1 = 0, vtotal = vtrail = vtrail2
    P = np.array([0, 0])
    P1 = np.array([0, 0])
    P2 = np.array([0, 1])

    vtotal = v_induced_by_horseshoe_vortex(P, P1, P2)[0]
    vtrail = v_induced_by_horseshoe_vortex(P, P1, P2)[1]

    assert_almost_equal(vtotal, vtrail)

    # point P = P2: vbound = vtrail2 = 0, vtotal = vtrail = vtrail1
    P = np.array([0, 1])
    P1 = np.array([0, 0])
    P2 = np.array([0, 1])

    vtotal = v_induced_by_horseshoe_vortex(P, P1, P2)[0]
    vtrail = v_induced_by_horseshoe_vortex(P, P1, P2)[1]

    assert_almost_equal(vtotal, vtrail)


def test_v_induced_by_finite_vortex_line():
    P = np.array([1, 0])
    A = np.array([0, 0])
    B = np.array([0, 1])

    calculated_vel = v_induced_by_finite_vortex_line(P, A, B)
    expected_vel = -0.056269769

    assert_almost_equal(calculated_vel, expected_vel)

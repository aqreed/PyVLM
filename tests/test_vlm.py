"""
    Unit tests of the PyVLM class and its methods

"""

import pytest
import unittest as ut
import numpy as np
from numpy.testing import assert_almost_equal

from vlm import PyVLM


class test_PyVLM(ut.TestCase):
    """
    Tests for the PyVLM class
    """
    def test_add_surface(self):
        plane = PyVLM()

        A = np.array([0, 0])
        B = np.array([0, 1])
        leading_edges_position = [A, B]
        chord_length = [1, 1]
        n, m = 1, 2
        plane.add_surface(leading_edges_position, chord_length, n, m)

        calculated_points = plane.Points
        expected_points = [np.array([0, 0]), np.array([0, .5]),
                           np.array([0, 1]), np.array([1, 0]),
                           np.array([1, .5]), np.array([1, 1]),
                           np.array([0, -1]), np.array([0, -.5]),
                           np.array([0, 0]), np.array([1, -1]),
                           np.array([1, -.5]), np.array([1, 0])]
        plane.reset()
        assert_almost_equal(calculated_points, expected_points)

    def test_add_surface_exceptions(self):
        plane = PyVLM()
        le_pos = [np.array([0, 0])]
        chrd_len = [1, 1]
        n, m = 3, 4
        self.assertRaises(ValueError, plane.add_surface,
                          le_pos, chrd_len, n, m)

        plane = PyVLM()
        A = np.array([0, 0])
        B = np.array([0, 1])
        C = np.array([0, 1])
        le_pos = [A, B, C]
        chrd_len = [1, 1, 1]
        self.assertRaises(ValueError, plane.add_surface,
                          le_pos, chrd_len, n, m)

    def test_show_mesh(self):
        plane = PyVLM()
        A = np.array([0, 0])
        B = np.array([0, 1])
        le_pos = [A, B]
        chrd_len = [1, 1]
        n, m = 2, 2
        plane.add_surface(le_pos, chrd_len, n, m)
        plane.show_mesh(print_mesh=True, plot_mesh=True)

    def test_vlm(self):
        plane = PyVLM()

        A = np.array([0, 0])
        B = np.array([0, 1])
        leading_edges_position = [A, B]
        chord_length = [1, 1]
        n, m = 1, 1
        plane.add_surface(leading_edges_position, chord_length, n, m)

        alpha = np.deg2rad(0)
        plane.vlm(alpha, True)
        calculated_AIC = plane.AIC
        expected_AIC = np.array([[-0.768468, 0.1634183],
                                 [0.1634183, -0.768468]])

        assert_almost_equal(calculated_AIC, expected_AIC)

    def test_aerodyn_forces_coeff(self):
        plane = PyVLM()

        A = np.array([0, 0])
        B = np.array([0, 1])
        leading_edges_position = [A, B]
        chord_length = [1, 1]
        n, m = 1, 1
        alpha = 0
        plane.add_surface(leading_edges_position, chord_length, n, m)
        plane.vlm(alpha, True)
        plane.aerodyn_forces_coeff()
        # TODO: improve this test with real-life values

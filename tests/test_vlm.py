"""
    Unit tests of the PyVLM class and its methods

"""

import pytest
import unittest as ut
from numpy import array, deg2rad, pi
from numpy.testing import assert_almost_equal

from vlm import PyVLM


class test_PyVLM(ut.TestCase):
    """
    Tests for the PyVLM class
    """
    def test_add_surface(self):
        plane = PyVLM()

        A = array([0, 0])
        B = array([0, 1])
        leading_edges_position = [A, B]
        chord_length = [1, 1]
        n, m = 1, 2
        plane.add_surface(leading_edges_position, chord_length, n, m)

        calculated_points = plane.Points
        expected_points = [array([0, 0]), array([0, .5]),
                           array([0, 1]), array([1, 0]),
                           array([1, .5]), array([1, 1]),
                           array([0, -1]), array([0, -.5]),
                           array([0, 0]), array([1, -1]),
                           array([1, -.5]), array([1, 0])]
        plane.reset()
        assert_almost_equal(calculated_points, expected_points)

    def test_add_surface_exceptions(self):
        # nº chords =! nº leading edge coordinates
        plane = PyVLM()
        le_pos = [array([0, 0])]
        chrd_len = [1, 1]
        n, m = 3, 4
        self.assertRaises(ValueError, plane.add_surface,
                          le_pos, chrd_len, n, m)

        # two leading edge coordinates are the same
        plane = PyVLM()
        A = array([0, 0])
        B = array([0, 1])
        C = array([0, 1])
        le_pos = [A, B, C]
        chrd_len = [1, 1, 1]
        self.assertRaises(ValueError, plane.add_surface,
                          le_pos, chrd_len, n, m)

    def test_show_mesh(self):
        plane = PyVLM()
        A = array([0, 0])
        B = array([0, 1])
        le_pos = [A, B]
        chrd_len = [1, 1]
        n, m = 2, 2
        plane.add_surface(le_pos, chrd_len, n, m)
        plane.show_mesh(print_mesh=True, plot_mesh=True)

    def test_vlm(self):
        plane = PyVLM()

        A = array([0, 0])
        B = array([0, 1])
        leading_edges_position = [A, B]
        chord_length = [1, 1]
        n, m = 1, 1
        plane.add_surface(leading_edges_position, chord_length, n, m)

        alpha = deg2rad(0)
        plane.vlm(alpha, True)
        calculated_AIC = plane.AIC
        expected_AIC = array([[-0.768468, 0.1634183],
                             [0.1634183, -0.768468]])

        assert_almost_equal(calculated_AIC, expected_AIC)

    def test_aerodyn_forces_coeff(self):
        plane = PyVLM()

        A = array([0, 0])
        B = array([0, 1])
        leading_edges_position = [A, B]
        chord_length = [1, 1]
        n, m = 1, 1
        alpha = 0
        plane.add_surface(leading_edges_position, chord_length, n, m)
        plane.vlm(alpha, True)
        plane.aerodyn_forces_coeff()
        # TODO: improve this test with real-life values


class test_BertinSmith(ut.TestCase):
    """
    Tests for the PyVLM class based on example 7.2 from Bertin, J.J. and
    Smith, M.L.,"Aerodynamics for Engineers" (1998) with b = 1
    """
    def test_add_surface(self):
        plane = PyVLM()

        A = array([0, 0])
        B = array([0.5, 0.5])
        leading_edges_position = [A, B]
        chord_length = [.2, .2]
        n, m = 1, 4
        plane.add_surface(leading_edges_position, chord_length,
                          n, m, mirror=False)

        calculated_points = plane.Points
        expected_points = [array([0, 0]), array([0.125, 0.125]),
                           array([0.25, 0.25]), array([0.375, 0.375]),
                           array([0.5, 0.5]), array([0.2, 0.0]),
                           array([0.325, 0.125]), array([0.45, 0.25]),
                           array([0.575, 0.375]), array([0.7, 0.5])]
        assert_almost_equal(calculated_points, expected_points)

    def test_vlm(self):
        plane = PyVLM()

        A = array([0, 0])
        B = array([0.5, 0.5])
        leading_edges_position = [A, B]
        chord_length = [.2, .2]
        n, m = 1, 4
        plane.add_surface(leading_edges_position, chord_length, n, m)

        alpha = 1  # rad
        plane.vlm(alpha, True)
        calculated_AIC = plane.AIC
        expected_AIC = array([[-71.5187, 11.2933, 1.0757, 0.3775,
                               0.2659, 0.5887, 2.0504, 18.515],
                             [20.2174, -71.5187, 11.2933, 1.0757,
                              0.2503, 0.4903, 1.1742, 3.6144],
                             [3.8792, 20.2174, -71.5187, 11.2933,
                              0.2179, 0.3776, 0.7227, 1.548],
                             [1.6334, 3.8792,  20.2174, -71.5187,
                              0.1836, 0.2895, 0.4834, 0.8609],
                             [0.8609, 0.4834, 0.2895, 0.1836,
                              -71.5187, 20.2174, 3.8792, 1.6334],
                             [1.548, 0.7227, 0.3776, 0.2179,
                              11.2933, -71.5187, 20.2174, 3.8792],
                             [3.6144, 1.1742, 0.4903, 0.2503,
                              1.0757, 11.2933, -71.5187, 20.2174],
                             [18.515, 2.0504, 0.5887, 0.2659,
                              0.3775, 1.0757, 11.2933, -71.5187]])

        assert_almost_equal(calculated_AIC*4*pi, expected_AIC, decimal=4)

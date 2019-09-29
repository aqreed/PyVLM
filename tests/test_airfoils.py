"""
    Unit tests of the airfoil classes and its methods

"""

import pytest
import unittest as ut
import numpy as np
from numpy.testing import assert_almost_equal

from vlm.airfoils import flat_plate, NACA4


class test_flat_plate(ut.TestCase):
    """
    Tests for the flat plate airfoil class
    """
    def test_camber_line(self):
        airfoil = flat_plate()
        x = 0.1

        calculated_value = airfoil.camber_line(x)
        expected_value = 0.0
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_camber_slope(self):
        airfoil = flat_plate()
        x = 0.76

        calculated_value = airfoil.camber_slope(x)
        expected_value = 0.0
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_thickness(self):
        airfoil = flat_plate()
        x = 0.5

        calculated_value = airfoil.thickness(x)
        expected_value = 0.0
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_upper_surface(self):
        airfoil = flat_plate()
        x = 0.34

        calculated_value = airfoil.upper_surface(x)
        expected_value = x, 0.0
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_lower_surface(self):
        airfoil = flat_plate()
        x = 0.34

        calculated_value = airfoil.lower_surface(x)
        expected_value = x, 0.0
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_flat_plate_exceptiona(self):
        airfoil = flat_plate()
        self.assertRaises(ValueError, airfoil.camber_line, 1.1)
        self.assertRaises(ValueError, airfoil.camber_line, -0.1)
        self.assertRaises(ValueError, airfoil.camber_slope, 1.1)
        self.assertRaises(ValueError, airfoil.camber_slope, -0.1)
        self.assertRaises(ValueError, airfoil.thickness, 1.1)
        self.assertRaises(ValueError, airfoil.thickness, -0.1)
        self.assertRaises(ValueError, airfoil.upper_surface, 1.1)
        self.assertRaises(ValueError, airfoil.upper_surface, -0.1)
        self.assertRaises(ValueError, airfoil.lower_surface, 1.1)
        self.assertRaises(ValueError, airfoil.lower_surface, -0.1)


class test_NACA4(ut.TestCase):
    """
    Tests for the NACA4 airfoil class
    """
    def test_camber_line(self):
        airfoil = NACA4()

        x = 0.5
        calculated_value = airfoil.camber_line(x)
        expected_value = 0.0194444
        assert_almost_equal(calculated_value, expected_value, 6)

        x = 0.3
        calculated_value = airfoil.camber_line(x)
        expected_value = 0.01875
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_camber_slope(self):
        airfoil = NACA4()
        x = 0.5

        calculated_value = airfoil.camber_slope(x)
        expected_value = -0.0111111
        assert_almost_equal(calculated_value, expected_value, 6)

        x = 0.3
        calculated_value = airfoil.camber_slope(x)
        expected_value = 0.025
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_thickness(self):
        airfoil = NACA4()
        x = 0.5

        calculated_value = airfoil.thickness(x)
        expected_value = 0.052940252
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_upper_surface(self):
        airfoil = NACA4()
        x = 0.5

        calculated_value = airfoil.upper_surface(x)
        expected_value = 0.500588188, 0.07238143
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_lower_surface(self):
        airfoil = NACA4()
        x = 0.5

        calculated_value = airfoil.lower_surface(x)
        expected_value = 0.499411811, -0.033492539
        assert_almost_equal(calculated_value, expected_value, 6)

    def test_flat_plate_exceptiona(self):
        self.assertRaises(ValueError, NACA4, -1, 4, 12)
        self.assertRaises(ValueError, NACA4, 9.6, 4, 12)
        self.assertRaises(ValueError, NACA4, 2, -1, 12)
        self.assertRaises(ValueError, NACA4, 2, 9.1, 12)
        self.assertRaises(ValueError, NACA4, 2, 4, -1)
        self.assertRaises(ValueError, NACA4, 2, 4, 41)

        airfoil = NACA4()
        self.assertRaises(ValueError, airfoil.camber_line, 1.1)
        self.assertRaises(ValueError, airfoil.camber_line, -0.1)
        self.assertRaises(ValueError, airfoil.camber_slope, 1.1)
        self.assertRaises(ValueError, airfoil.camber_slope, -0.1)
        self.assertRaises(ValueError, airfoil.thickness, 1.1)
        self.assertRaises(ValueError, airfoil.thickness, -0.1)
        self.assertRaises(ValueError, airfoil.upper_surface, 1.1)
        self.assertRaises(ValueError, airfoil.upper_surface, -0.1)
        self.assertRaises(ValueError, airfoil.lower_surface, 1.1)
        self.assertRaises(ValueError, airfoil.lower_surface, -0.1)

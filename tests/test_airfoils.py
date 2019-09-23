"""
    Unit tests of the airfoil classes and its methods

"""

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from vlm.airfoils import NACA4


def test_camber_line():
    airfoil = NACA4()
    x = 0.5

    calculated_camber_line = airfoil.camber_line(x)
    expected_camber_line = 0.0194444

    assert_almost_equal(calculated_camber_line, expected_camber_line)


def test_camber_gradient():
    airfoil = NACA4()
    x = 0.5

    calculated_camber_grad = airfoil.camber_gradient(x)
    expected_camber_grad = -0.0111111

    assert_almost_equal(calculated_camber_grad, expected_camber_grad)


def test_thickness():
    airfoil = NACA4()
    x = 0.5

    calculated_thickness = airfoil.thickness(x)
    expected_thickness = 0.052940252

    assert_almost_equal(calculated_thickness, expected_thickness)


def test_upper_surface():
    airfoil = NACA4()
    x = 0.5

    calculated_upper = airfoil.upper_surface(x)
    expected_upper = 0.500588188, 0.07238143

    assert_almost_equal(calculated_upper, expected_upper)


def test_lower_surface():
    airfoil = NACA4()
    x = 0.5

    calculated_lower = airfoil.lower_surface(x)
    expected_lower = 0.499411811, -0.033492539

    assert_almost_equal(calculated_lower, expected_lower)

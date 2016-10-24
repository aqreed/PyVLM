import numpy as np
import matplotlib.pyplot as plt


def camber_gradient_NACA4(x, M=2, P=4):
    """
    Camber line gradient (dz/dx) for 4-digit NACA airfoils.
    Default values for NACA 2412

    Reference:
    [1] http://airfoiltools.com/airfoil/naca4digit

    Parameters
    ----------
    x : float
        Chord position, from 0 to 1
    M, P : integer
           First and second digit on the NACA designation
           M - maximum camber (divided by 100)
           P - maximum camber position (divided by 10)

    Returns
    -------
    dz : float
         Camber gradient
    """
    M /= 100
    P /= 10
    if x < P:
        # z = (M/P**2) * (2*P*x - x**2)
        dz = (2*M/P**2) * (P - x)
    else:
        # z = (M / (1 - P)**2) * (1 - 2*P + 2*P*x - x**2)
        dz = (2*M / (1 - P)**2) * (P - x)
    return dz


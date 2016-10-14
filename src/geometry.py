import numpy as np


def norm_direction_vector(A, B):
    """
    Normalized direction vector from point A to point B

    Parameters
    ----------
    A, B : array_like
           Points in space

    Returns
    -------
    a : array_like
    """
    if (A == B).all():
        raise ValueError("Can't calculate vector, same points")

    a = (B - A) / np.linalg.norm(B - A)
    return a


def vect_perpendicular(a):
    """
    Normal vector to vector a, so cross_product(a, b) < 0
    in a 2D euclidean space.

    Parameters
    ----------
    a : array_like
        Vector in a 2D-euclidean space

    Returns
    -------
    b : array_like
    """
    if (a == np.zeros_like(a)).all():
        raise ValueError("Can't calculate, null vector")

    b = np.empty_like(a)
    b[0] = a[1]
    b[1] = - a[0]
    return b


def dist_point2line(P, A, B):
    """
    Distance from a point P to a straight line
    in a 2D euclidean space defined by A and B

    Parameters
    ----------
    P, A, B : array_like
              P - point of reference
              A,B - points that define the line

    Returns
    -------
    d : float
    """
    a = (B - A) / np.linalg.norm(B - A)
    b = vect_perpendicular(a)

    if np.cross((B - P), a) == 0:
        raise ValueError('Point P belongs to the line AB')

    d = abs(np.vdot((B - P), b))
    return d


def area_4points(A, B, C, D):
    """

  y	^   C +-+ D     Area of the polygon defined by 4 points,
    |    /   \		previously ordered in a clockwise
    | B +-----+ A   (or counterclockwise) manner in a 2D
    +----->			euclidean space.
           x

    Parameters
    ----------
    A, B, C, D : array_like
                 points of the polygon

    Returns
    -------
    S : float
    """
    AB = B - A
    AC = C - A
    AD = D - A

    if np.sign(np.cross(AB, AC)) != np.sign(np.cross(AC, AD)):
        raise ValueError('Points not in a clockwise/counterclockwise fashion')

    S = np.cross(A, B) + np.cross(B, C) + np.cross(C, D) + np.cross(D, A)

    S *= 1/2
    return abs(S)

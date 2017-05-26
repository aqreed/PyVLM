import numpy as np


def cross_prod(a, b):

    x = a[0]*b[1] - a[1]*b[0]

    return x


def vect_dot(a, b):

    x = a[0]*b[0] + a[1]*b[1]

    return x


def norm_dir_vect(A, B):
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
        msg = "Can't calculate vector, same points"
        raise ValueError(msg)

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
        msg = "Can't calculate, null vector"
        raise ValueError(msg)

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

    AB = B - A
    PB = B - P

    a = AB / np.linalg.norm(AB)
    b = vect_perpendicular(a)

    if cross_prod((PB), a) == 0:
        d = 0
    else:
        d = abs(vect_dot((PB), b))

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

    if np.sign(cross_prod(AB, AC)) != np.sign(cross_prod(AC, AD)):
        msg = 'Points not in a clockwise/counterclockwise fashion'
        raise ValueError(msg)

    S = cross_prod(A, B) + cross_prod(B, C) + \
        cross_prod(C, D) + cross_prod(D, A)

    S *= 1/2

    return abs(S)

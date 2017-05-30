import numpy as np


def cross_prod(a, b):
    """
    Simplified cross product of two 2D vectors.

    Parameters
    ----------
    a, b : array_like
           Vectors in a 2D-euclidean space

    Returns
    -------
    x : float
    """

    x = a[0]*b[1] - a[1]*b[0]

    return x


def vect_dot(a, b):
    """
    Simplified dot product of two 2D vectors.

    Parameters
    ----------
    a, b : array_like
           Vectors in a 2D-euclidean space

    Returns
    -------
    x : float
    """

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

    S = cross_prod(A, B) + cross_prod(B, C) + \
        cross_prod(C, D) + cross_prod(D, A)

    S *= 1/2

    return abs(S)

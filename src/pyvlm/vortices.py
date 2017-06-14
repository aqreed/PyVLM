import numpy as np

from .geometry import (norm_dir_vect, dist_point2line)


def vortex_position_in_panel(P1, P2, P3, P4):
    """
    For a given panel defined by points P1, P2, P3 and P4
    returns the position of the horseshoe vortex defined
    by points A, B, C and D and its control point P.

            ^
          y |                Points defining the panel are
            |                named clockwise.
     P3--C--|--D--P4         Points defining the horseshoe
      |  |  |  |  |          are named clockwise as well.
      |  |  |  |  |
      |  |  +--P--|---->
      |  |     |  |     x
      |  |     |  |
     P2--B-----A--P1

    Parameters
    ----------
    P1, P2, P3, P4 : array_like
                     Points that define the panel

    Returns
    -------
    results : dict
        P - control point where the boundary condition V*n = 0
            is applied according to the Vortice Lattice Method.
        A, B, C, D - points that define the horseshoe position
    """

    P1P2 = P2 - P1
    P3P4 = P4 - P3
    P1P4 = P4 - P1

    A = P1 + P1P2 / 4
    B = A + P1P2 / 2
    C = P3 + P3P4 / 4
    D = C + P3P4 / 2

    AD = D - A
    P = A + AD / 2

    results = [P, A, B, C, D]

    return results


def v_induced_by_horseshoe_vortex(P, A, B, C, D, gamma=1):
    """
    Induced velocity at point P due to a horseshoe vortex
    spatially positioned by points A, B, C and D, extended
    to x_Inf(+) in a 2D euclidean space. Circulation
    direction: x_Inf(+) -> A -> B -> C -> D -> x_Inf(+)

                ^
              y |                Points defining the horseshoe
    V_inf       | i_3            are named clockwise.
    ->     C----|->--D  ...>...  A direction vector is
    ->     |    |    |           calculated for each vortex.
    -> i_2 ^    +----|------>
    ->	   |         |       x
    ->	   B----<----A  ...<...
                i_1

    Parameters
    ----------
    P, A, B, C, D : array_like
                    P - point of reference
                    A, B, C, D - points of the horseshoe vortex
    gamma : circulation

    Returns
    -------
    v : float
    """

    pi = np.pi

    a = P[0] - B[0]
    b = P[1] - B[1]
    c = P[0] - C[0]
    d = P[1] - C[1]
    e = (a**2 + b**2)**0.5
    f = (c**2 + d**2)**0.5
    g = C[0] - B[0]
    h = C[1] - B[1]

    div = a*d - c*b
    if (div == 0):
        v_bounded = 0
    else:
        v_bounded = (1/div) * (((g*a + h*b)/e) - ((g*c + h*d)/f))
        v_bounded /= 4*pi  # Induced velocity in P due to bounded vortex

    if (b == 0):
        v_trail1 = 0
    else:
        v_trail1 = -(a + e)/(b*e)

    if (d == 0):
        v_trail2 = 0
    else:
        v_trail2 = (c + f)/(d*f)

    v_trail = v_trail1 + v_trail2
    v_trail /= 4*pi  # Induced velocity in P due to trailing vortices

    v_total = v_trail + v_bounded  # Total induced velocity in P

    return v_total, v_trail


def v_induced_by_finite_vortex_line(P, A, B, gamma=1):
    """

    Y^						Induced velocity at point P due
     |	  + P(x,y)			to a finite straight line vortex
     |						defined by points A and B.
     +=======+--------> X	Circulation from A --> B.
     A		 B

    Parameters
    ----------
    P, A, B : array_like
              P - point of reference
              A, B - points of the vortex
    gamma : circulation

    Returns
    -------
    v : float
    """

    pi = np.pi
    i = norm_dir_vect(A, B)  # vortex_2 direction vector

    i_PA = norm_dir_vect(P, A)  # PB direction vector
    i_PB = norm_dir_vect(P, B)  # PC direction vector

    h = dist_point2line(P, A, B)  # distance to vortex_2
    sign = np.sign(np.cross(i_PA, i))

    cos_1 = np.dot(-i_PA, i)
    cos_2 = np.dot(-i_PB, i)
    v = sign * (gamma/(4 * pi * h)) * (cos_1 - cos_2)

    return v

import numpy as np
import matplotlib.pyplot as plt


def mesh(A, B, C, D, n, m):
    """
    A +......> y     Given a trapezoid defined by vertices ABDC
      | \            representing a wing segment that complies
      |  \           with the VLM theory, returns the points
      |   + C        and panels of the mesh.
      |   |          Points are presented as an array of 2xNp
    B +---+ D        elements, being Np the sum of points of
      |              the mesh. Panels are given as a list of
     x               NP rows of 4 points, where NP is the sum
                     of panels of the mesh. The corner points
    x - chordwise    of each panel are already arranged in a
        direction    clockwise fashion following this order:
    y - spanwise             P3 +-----+ P4
        direction               |
                                |
                             P2 +-----+ P1

    Parameters
    ----------
    A, B, C, D : array_like
                 Corner points in a 2D euclidean space
    n, m : integer
           n - nº of chordwise panels
           m - nº of spanwise panels
    Returns
    -------
    mesh_points : array_like
                  Mesh points
    mesh_panels : list
                  Mesh panels defined by 4 points
    """
    AB = B - A
    CD = D - C

    if np.cross(AB, CD) != 0:
        msg = 'Invalid panel, AB and CD not parallel'
        raise ValueError(msg)

    N_points = (n + 1) * (m + 1)
    N_panels = n * m

    mesh_points = np.zeros(shape=(N_points, 2))
    Pi = A
    Pf = C
    k = 0
    for i in range(0, n + 1):
        PiPf = Pf - Pi
        P = Pi
        for j in range(0, m + 1):
            mesh_points[k] = P
            P = P + PiPf / m
            k += 1
        Pi = Pi + AB / n
        Pf = Pf + CD / n

    mesh_panels = []
    for i in range(0, N_panels):
        k = int(i / m)
        mesh_panels.append([])
        mesh_panels[i].append(mesh_points[i + k + m + 1])  # P1
        mesh_panels[i].append(mesh_points[i + k])  # P2
        mesh_panels[i].append(mesh_points[i + k + 1])  # P3
        mesh_panels[i].append(mesh_points[i + k + m + 2])  # P4

    return mesh_points, mesh_panels

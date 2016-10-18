import numpy as np
import matplotlib.pyplot as plt


def mesh(A, B, C, D, n, m):
    """
    A +......> y     Given a trapezoid defined by vertices
      | \            ABDC representing a wing segment that
      |  \           complies with the VLM theory, returns
      |   + C        the points and panels of the mesh.
      |   |          Points are presented as an array of
    B +---+ D        2xNp elements, being Np the sum of
      |              points of the mesh. Panels are given
     x               as a list of NP rows of 4 points,
                     where NP is the sum of panels of the
    x - chordwise    mesh. The corner points of each panel
        direction    are already arranged in a clockwise
    y - spanwise     fashion following this order:
        direction        P3 +-----+ P4
                            |
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

A = np.array([0, 0])
B = np.array([1, 0])
C = np.array([0.5, 1])
D = np.array([1, 1])

n = 10
m = 10

Points, Panels = mesh(A, B, C, D, n, m)

for row in Panels:
    for column in row:
        print(column, end="")
    print(end="\n")

plt.style.use('ggplot')
plt.plot(Points[:, 0], Points[:, 1], 'ro')
plt.show()

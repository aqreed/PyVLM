import numpy as np


class Mesh(object):
    """
   Pi +......> y     Given a trapezoid defined by vertices Pi
      | \            and Pf and chords 1 and 2 representing a
chord1|  \ Pf        wing segment that complies with VLM theory,
      |   +          returns the points and panels of the mesh.
      |   |chord2    Points are presented as an array of 2xNp
      +---+          elements, being Np the sum of points of
      |              the mesh. Panels are given as a list of
     x               NP rows of 4 points, where NP is the sum
                     of panels of the mesh. The corner points
    x - chordwise    of each panel are already arranged in a
        direction    clockwise fashion following this order:
    y - spanwise
        direction            P2 +---+ P3...> y
                                |   |
                             P1 +   + P4
                                |
    Parameters                 x
    ----------
    leading_edges : list (containing arrays)
                    Coordinates of the leading edge points as
                    arrays in a 2D euclidean space
    chords : list
             Chord lenghts
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

    def __init__(self, leading_edges, chords, n, m):
        self.leading_edges = leading_edges
        self.chords = chords
        self.n = n
        self.m = m

    def points_panels(self):
        Pi = self.leading_edges[0]
        Pf = self.leading_edges[1]
        chord_1 = np.array([self.chords[0], 0])
        chord_2 = np.array([self.chords[1], 0])
        n = self.n
        m = self.m

        N_points = (n + 1) * (m + 1)
        mesh_points = np.zeros(shape=(N_points, 2))
        k = 0
        for i in range(0, n + 1):
            PiPf = Pf - Pi
            P = Pi
            for j in range(0, m + 1):
                mesh_points[k] = P
                P = P + PiPf / m
                k += 1
            Pi = Pi + chord_1 / n
            Pf = Pf + chord_2 / n

        N_panels = n * m
        mesh_panels = []
        for i in range(0, N_panels):
            k = int(i / m)
            mesh_panels.append([])
            mesh_panels[i].append(mesh_points[i + k + m + 1])  # P1
            mesh_panels[i].append(mesh_points[i + k])  # P2
            mesh_panels[i].append(mesh_points[i + k + 1])  # P3
            mesh_panels[i].append(mesh_points[i + k + m + 2])  # P4

        return mesh_points, mesh_panels

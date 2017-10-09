import numpy as np

from .panel import Panel


class Mesh(object):
    """
   Pi +......> y     Given a trapezoid defined by vertices Pi and Pf
      | \            and chords 1 and 2 representing a wing segment
      |  \           that complies with the VLM theory, returns the
      |   + Pf       points and panels of the mesh:
chord1|   |
      |   |             - Points are given as a list of Np elements,
      |   |chord2         being Np the number of points of the mesh.
      +---+
      |                 - Panels are given as a list of list of NP
     x 				      elements, each element composed of 4 points,
                          where NP is the number of panels of the mesh.
    x - chordwise
        direction    The corner points of each panel are arranged in a
    y - spanwise     clockwise fashion following this order:
        direction
                             P2 +---+ P3...> y
                                |   |
                             P1 +   + P4
                                |
    Parameters                 x
    ----------
    leading_edges : list (containing arrays)
                    Coordinates of the leading edge points Pi and Pf,
                    as arrays in a 2D euclidean space (x, y)
    chords : list
             Chord lenghts values
    n, m : integer
           n - nº of chordwise panels
           m - nº of spanwise panels

    Returns
    -------
    mesh_points : list
                  Mesh points
    mesh_panels : list
                  Mesh panels
    """

    def __init__(self, leading_edges, chords, n, m):
        self.leading_edges = leading_edges
        self.chords = chords
        self.n = n
        self.m = m
        self.mesh_points = []
        self.mesh_panels = []

    def points(self):
        """
        Yields a list of length (n+1)*(m+1) containing equally spaced
        points (x, y) coordinates (arrays), for each trapezoid geometry
        defined by the arguments.
        """

        Pi = self.leading_edges[0]
        Pf = self.leading_edges[1]

        chord_1 = np.array([self.chords[0], 0])
        chord_2 = np.array([self.chords[1], 0])

        n = self.n
        m = self.m

        for i in range(n + 1):
            PiPf = Pf - Pi
            P = Pi
            for j in range(m + 1):
                self.mesh_points.append(P)
                P = P + PiPf / m
            Pi = Pi + chord_1 / n
            Pf = Pf + chord_2 / n

        return self.mesh_points

    def panels(self):
        """
        Yields a list of length (n*m) containing the panels (objects),
        defined by 4 points previously calculated. The points are properly
        arranged to serve as locations for the horseshoe vortices.
        """

        Pi = self.leading_edges[0]
        chord_1 = np.array([self.chords[0], 0])

        n = self.n
        m = self.m

        N_panels = n * m

        for i in range(N_panels):
            # Panels list generation from mesh_points list
            k = int(i / m)

            P1 = self.mesh_points[i + k + m + 1]
            P2 = self.mesh_points[i + k]
            P3 = self.mesh_points[i + k + 1]
            P4 = self.mesh_points[i + k + m + 2]

            self.mesh_panels.append(Panel(P1, P2, P3, P4))

            # Chordwise position calculation
            P1_ = self.mesh_panels[k * m].P1
            P2_ = self.mesh_panels[k * m].P2

            chord = P1_ - P2_
            panel_center = P2_ + chord / 2

            leadEdge_2_panel = np.linalg.norm(panel_center - Pi)
            relative_pos = leadEdge_2_panel / np.linalg.norm(chord_1)

            self.mesh_panels[i].chordwise_position = relative_pos

        return self.mesh_panels

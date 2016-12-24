import numpy as np

from .panel import Panel


class Mesh(object):
    """
   Pi +......> y     Given a trapezoid defined by vertices Pi and
      | \            Pf and chords 1 and 2 representing a wing
      |  \           segment that complies with VLM theory, returns
      |   + Pf       the points and panels of the mesh along with
chord1|   |          the chordwise position of each panel.
      |   |
      |   |chord2    Points are presented as a list Np rows, being
      +---+          Np the sum of points of the mesh. Panels are
      |              given as a list of NP rows of 4 points, where
     x               NP is the sum of panels of the mesh.
                     The corner points of each panel are arranged
    x - chordwise    in a clockwise fashion following this order:
        direction
    y - spanwise
        direction            P2 +---+ P3...> y
                                |   |
                             P1 +   + P4
                                |
    Parameters                 x
    ----------
    leading_edges : list (containing arrays)
                    Coordinates of the leading edge points as
                    arrays in a 2D euclidean space (x, y)
    chords : list
             Chord lenghts
    n, m : integer
           n - nº of chordwise panels
           m - nº of spanwise panels

    Returns
    -------
    mesh_points : list
                  Mesh points
    mesh_panels : list
                  Mesh panels defined by 4 points
    panel_pos_chordwise: list
                         Mesh panels center position in
                         respect of the local chord
    """

    def __init__(self, leading_edges, chords, n, m):
        self.leading_edges = leading_edges
        self.chords = chords
        self.n = n
        self.m = m
        self.mesh_points = []
        self.mesh_panels = []
        self.panel_pos_chordwise = []
        self.panel_span = []

    def points(self):
        """ Yields (n+1)*(m+1) equally spaced points (x, y) coordinates,
            for each geometry defined with the arguments """

        Pi = self.leading_edges[0]
        Pf = self.leading_edges[1]
        chord_1 = np.array([self.chords[0], 0])
        chord_2 = np.array([self.chords[1], 0])
        n = self.n
        m = self.m

        for i in range(0, n + 1):
            PiPf = Pf - Pi
            P = Pi
            for j in range(0, m + 1):
                self.mesh_points.append(P)
                P = P + PiPf / m
            Pi = Pi + chord_1 / n
            Pf = Pf + chord_2 / n

        return self.mesh_points

    def panels(self):
        """ Yields n*m panels, each panel composed by 4 points
            previously calculated. The points are properly
            arranged to serve as framework for the horseshoe
            vortices """

        n = self.n
        m = self.m

        N_panels = n * m

        for i in range(0, N_panels):
            k = int(i / m)
            P1 = self.mesh_points[i + k + m + 1]
            P2 = self.mesh_points[i + k]
            P3 = self.mesh_points[i + k + 1]
            P4 = self.mesh_points[i + k + m + 2]

            self.mesh_panels.append([])
            self.mesh_panels[i].append(P1)
            self.mesh_panels[i].append(P2)
            self.mesh_panels[i].append(P3)
            self.mesh_panels[i].append(P4)

        return self.mesh_panels

    def panel_chord_positions(self):
        """ Yields the position of each panel referred to the
            local chord, which is needed to compute its
            inclination, aka corresponding camber gradient """

        Pi = self.leading_edges[0]
        chord_1 = np.array([self.chords[0], 0])
        n = self.n
        m = self.m

        N_panels = n * m

        for i in range(0, N_panels):
            k = int(i / m)
            P1 = self.mesh_panels[k * m][0]
            P2 = self.mesh_panels[k * m][1]

            chord = P1 - P2

            panel_center = P2 + chord / 2
            le2panel_distance = np.linalg.norm(panel_center - Pi)
            relative_pos = le2panel_distance / np.linalg.norm(chord_1)

            self.panel_pos_chordwise.append(relative_pos)

        return self.panel_pos_chordwise

    def panels_span(self):
        """ Yields the values of the span for each one of the n*m panels """

        n = self.n
        m = self.m

        N = n * m

        for i in range(0, N):
            P1, P2, P3, P4 = self.mesh_panels[i][:]
            panel_ = Panel(P1, P2, P3, P4)
            self.panel_span.append(panel_.span())

        return self.panel_span

import numpy as np

from .panel import Panel


class Mesh(object):
    """
   Pi +......> y     Given a trapezoid defined by vertices Pi and Pf
      | \            and chords 1 and 2 representing a wing segment
      |  \           that complies with the VLM theory, returns the
      |   + Pf       points and panels of the mesh along with the
chord1|   |          chordwise position of each panel.
      |   |
      |   |chord2       - Points are presented as a list of Np elements,
      +---+               being Np the number of points of the mesh.
      |
     x                  - Panels are given as a list of list of NP
                          elements, each element composed of 4 points,
    x - chordwise         where NP is the number of panels of the mesh.
        direction
    y - spanwise     The corner points of each panel are arranged in a
        direction    clockwise fashion following this order:

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
             Chord lenghts
    n, m : integer
           n - nº of chordwise panels
           m - nº of spanwise panels

    Returns
    -------
    mesh_points : list
                  Mesh points
    mesh_panels : list (of lists)
                  Mesh panels (defined by 4 points)
    panel_pos_chordwise: list
                         Mesh panels' center position
                         w.r.t. the local chord
    panels_span : list
                  Mesh panels' span
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
        """
        Yields a list of size (n+1)*(m+1) containing equally spaced
        points (x, y) coordinates, for each trapezoid geometry defined
        by the arguments.
        """

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
        """
        Yields a list of size (n*m) containing the panels, defined
        by 4 points previously calculated. The points are properly
        arranged to serve as locations for the horseshoe vortices.
        """

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
        """
        Yields a list of size (n*m), containing the chordwise position
        of each panel referred to the local chord, needed to compute its
        slope, aka its corresponding camber gradient.
        """

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
        """
        Yields a list of size (n*m), containing the span of each one of
        the panels.
        """

        n = self.n
        m = self.m

        N = n * m

        for i in range(0, N):
            P1, P2, P3, P4 = self.mesh_panels[i][:]
            panel_ = Panel(P1, P2, P3, P4)
            self.panel_span.append(panel_.span())

        return self.panel_span

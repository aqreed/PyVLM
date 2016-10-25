import numpy as np
import matplotlib.pyplot as plt

from .panel import Panel
from .mesh_generator import Mesh
from .airfoils import camber_gradient_NACA4


class PyVLM(object):
    """
    """

    def __init__(self, le_coord, ch_le, V, alpha, n, m):
        self.leading_edges_coord = le_coord
        self.chord_lengths = ch_le
        self.V = V
        self.alpha = alpha
        self.n = n
        self.m = m

        if len(self.leading_edges_coord) != len(self.chord_lengths):
            msg = 'Same number of chords and l.e. required'
            raise ValueError(msg)

    def _calculations(self):
        n = self.n
        m = self.m
        leading_edges_coord = self.leading_edges_coord
        chord_lengths = self.chord_lengths

        # Mesh generation
        Nle = len(leading_edges_coord)

        for k in range(0, Nle - 1):
            leading_edges = [leading_edges_coord[k],
                             leading_edges_coord[k + 1]]
            chords = [chord_lengths[k],
                      chord_lengths[k + 1]]

            mesh = Mesh(leading_edges, chords, n, m)
            Points_ = mesh.points()
            Panels_ = mesh.panels()
            Chordwise_pos_ = mesh.panel_position()

            self.Points.extend(Points_)
            self.Panels.extend(Panels_)
            self.Chord_pos.extend(Chordwise_pos_)

        # Computing of the matrix A (induced velocities)
        N = len(self.Panels)
        A = np.zeros(shape=(N, N))

        for i in range(0, N):
            P1, P2, P3, P4 = self.Panels[i][:]
            panel_pivot = Panel(P1, P2, P3, P4)
            s = panel_pivot.area()
            CP = panel_pivot.control_point()

            for j in range(0, N):
                PP1, PP2, PP3, PP4 = self.Panels[j][:]
                panel = Panel(PP1, PP2, PP3, PP4)
                w = panel.induced_velocity(CP)
                A[i, j] = w

        # Linear equation solving AX = Y
        Y = np.zeros(shape=len(self.Panels))

        for i in range(0, len(self.Panels)):
            Y[i] = self.alpha - camber_gradient_NACA4(self.Chord_pos[i])
            Y[i] *= -self.V

        X = np.linalg.solve(A, Y)

        self.Y = Y
        self.A = A
        self.gamma = X

    def get_geometry(self):
        self.Points = []
        self.Panels = []
        self.Chord_pos = []

        self.Y = 0
        self.A = 0
        self.gamma = 0
        self._calculations()

        return self.Points, self.Panels, self.Chord_pos

    def get_linear_eq(self):
        self.Points = []
        self.Panels = []
        self.Chord_pos = []

        self.Y = 0
        self.A = 0
        self.gamma = 0
        self._calculations()

        return self.Y, self.A, self.gamma


# gamma_plot = X
# cl_plot = (2.0 * X) / (V * c)
# cd_plot = (-2.0 * abs(X) * w * b) / (V**2 * S)
# cm_plot = - cl_plot[i] * (0.25 * c) / c


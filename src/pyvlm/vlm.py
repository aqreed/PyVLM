import numpy as np
import matplotlib.pyplot as plt

from .panel import Panel
from .mesh_generator import Mesh
from .airfoils import camber_gradient_NACA4


class PyVLM(object):
    """
    Given the geometry, angle of attack, upstream velocity and
    mesh chordwise and spanwise density, applies the VLM theory
    to the surface.

    Parameters
    ----------
    V : float
        Upstream flow velocity
    alpha : float
            Angle of attack of the surface
    le_coord : list (containing arrays)
                    Coordinates of the leading edge points as
                    arrays in a 2D euclidean space
    ch_le : list
             Chord lenghts corresponding to the sections defined
             by the leading edge coordinates
    n, m : integer
           n - nº of chordwise panels
           m - nº of spanwise panels
    """


    def __init__(self,  V, alpha):
        self.V = V
        self.alpha = alpha

        self.Points = []
        self.Panel_points = []
        self.Chords = []
        self.Chordwise_panel_position = []

    def create_geometry(self, le_coord, ch_le, n, m):
        if len(le_coord) != len(ch_le):
            msg = 'Same number of chords and l.e. required'
            raise ValueError(msg)

        # Mesh generation
        Nle = len(le_coord)

        for k in range(0, Nle - 1):
            leading_edges = [le_coord[k],
                             le_coord[k + 1]]
            chords = [ch_le[k],
                      ch_le[k + 1]]

            mesh = Mesh(leading_edges, chords, n, m)
            Points_ = mesh.points()
            Panel_points_ = mesh.panels()
            Chord_, Chordwise_pos_ = mesh.panel_chord_position()

            self.Points.extend(Points_)
            self.Panel_points.extend(Panel_points_)
            self.Chords.extend(Chord_)
            self.Chordwise_panel_position.extend(Chordwise_pos_)

        return (self.Points, self.Panel_points,
                self.Chords, self.Chordwise_panel_position)

    def vlm(self):
        Points = self.Points
        Panel_points = self.Panel_points
        Chordwise_panel_position = self.Chordwise_panel_position

        V = self.V
        alpha = self.alpha

        # Computing of the induced velocities
        N = len(Panel_points)
        A = np.zeros(shape=(N, N))

        for i in range(0, N):
            P1, P2, P3, P4 = Panel_points[i][:]
            panel_pivot = Panel(P1, P2, P3, P4)
            s = panel_pivot.area()
            CP = panel_pivot.control_point()

            for j in range(0, N):
                PP1, PP2, PP3, PP4 = Panel_points[j][:]
                panel = Panel(PP1, PP2, PP3, PP4)
                w = panel.induced_velocity(CP)
                A[i, j] = w

        # Circulation values by solving the linear equation (AX = Y)
        Y = np.zeros(shape=N)

        for i in range(0, N):
            Y[i] = alpha - camber_gradient_NACA4(Chordwise_panel_position[i])
            Y[i] *= -self.V

        X = np.linalg.solve(A, Y)

        return Y, A, X


# gamma_plot = X
# cl_plot = (2.0 * X) / (V * c)
# cd_plot = (-2.0 * abs(X) * w * b) / (V**2 * S)
# cm_plot = - cl_plot[i] * (0.25 * c) / c

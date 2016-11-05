import numpy as np
import matplotlib.pyplot as plt

from .panel import Panel
from .mesh_generator import Mesh
from .airfoils import NACA4


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
    lead_edge_coord : list (containing arrays)
                      Coordinates of the leading edge points
                      as arrays in a 2D euclidean space
    chord_lengths : list
                    Chord lenghts corresponding to the sections
                    defined by the leading edge coordinates
    n, m : integer
           n - nº of chordwise panels
           m - nº of spanwise panels
    """

    def __init__(self, V, alpha):
        self.V = V
        self.alpha = alpha

        self.Points = []
        self.Panel_points = []
        self.Chordwise_panel_position = []

    def add_geometry(self, lead_edge_coord, chord_lengths, n, m):
        """ Allows to add wings, stabilizers, canard wings or any
            other lifting surface to the mesh, defined by its chords
            location (leading edge) and length. Also the density of
            the mesh can be controlled by n and m """

        if len(lead_edge_coord) != len(chord_lengths):
            msg = 'Same number of chords and l.e. required'
            raise ValueError(msg)

        # MESH GENERATION
        Nle = len(lead_edge_coord)

        for k in range(0, Nle - 1):
            # When more than two chords are provided, it iterates
            # through the list containing both location and length

            leading_edges = [lead_edge_coord[k],
                             lead_edge_coord[k + 1]]
            chords = [chord_lengths[k],
                      chord_lengths[k + 1]]

            mesh = Mesh(leading_edges, chords, n, m)

            Points_ = mesh.points()
            Panel_points_ = mesh.panel()
            Chordwise_panel_position_ = mesh.panel_chord_position()

            self.Points.extend(Points_)
            self.Panel_points.extend(Panel_points_)
            self.Chordwise_panel_position.extend(Chordwise_panel_position_)

        return (self.Points, self.Panel_points,
                self.Chordwise_panel_position)

    def vlm(self):
        """ For a given set of panels (defined by its 4 points) and
            their chordwise position (referred to the local chord),
            both presented as lists, computes the induced velocity
            produced by all the associated horseshoe vortices on each
            panel, calculated on its control point where the boundary
            condition will be imposed. Computes the circulation by
            solving the linear equation """

        Panel_points = self.Panel_points
        Chordwise_panel_position = self.Chordwise_panel_position

        V = self.V
        alpha = self.alpha

        # INDUCED VELOCITIES
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

        # CIRCULATION by solving the linear equation (AX = Y)
        Y = np.zeros(shape=N)

        airfoil = NACA4()
        for i in range(0, N):
            Y[i] = alpha - airfoil.camber_gradient(Chordwise_panel_position[i])
            Y[i] *= -self.V

        X = np.linalg.solve(A, Y)

        return Y, A, X


# gamma_plot = X
# cl_plot = (2.0 * X) / (V * c)
# cd_plot = (-2.0 * abs(X) * w * b) / (V**2 * S)
# cm_plot = - cl_plot[i] * (0.25 * c) / c

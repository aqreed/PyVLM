import numpy as np
import matplotlib.pyplot as plt

from .panel import Panel
from .mesh_generator import Mesh
from .airfoils import NACA4


class PyVLM(object):
    """
    Given the geometry, angle of attack, upstream velocity and
    mesh chordwise and spanwise densities, applies the VLM theory
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
        self.Panels_points = []
        self.Panels_span = []
        self.Chordwise_panel_positions = []

    def add_geometry(self, lead_edge_coord, chord_lengths, n, m):
        """ Allows to add wings, stabilizers, canard wings or any
            other lifting surface to the mesh, defined by given
            chords. These are defined by their leading edges
            locations and their lengths. Also the density of the
            mesh can be controlled spanwise and chordwise with
            n and m """

        if len(lead_edge_coord) != len(chord_lengths):
            msg = 'Same number of chords and leading edges required'
            raise ValueError(msg)

        # MESH GENERATION

        # When more than two chords -with their respectives leading
        # edges coordinates- are provided, it iterates through the
        # list containing both location and length

        Nle = len(lead_edge_coord)

        for k in range(0, Nle - 1):
            leading_edges = [lead_edge_coord[k],
                             lead_edge_coord[k + 1]]
            chords = [chord_lengths[k],
                      chord_lengths[k + 1]]

            # The mesh is created taking into account the desired
            # mesh density spanwise -"n"- and chordwise -"m"-

            mesh = Mesh(leading_edges, chords, n, m)

            # The points of the mesh, its panels - sets of 4 points
            # orderly arranged -, the position of each panel relative to
            # its local chord and the span of each panel are calculated

            Points_ = mesh.points()
            Panels_points_ = mesh.panels()
            Panels_span_ = mesh.panels_span()
            Chordwise_panel_positions_ = mesh.panel_chord_positions()

            self.Points.extend(Points_)
            self.Panels_points.extend(Panels_points_)
            self.Panels_span.extend(Panels_span_)
            self.Chordwise_panel_positions.extend(Chordwise_panel_positions_)

        return (self.Points, self.Panels_points, self.Panels_span,
                self.Chordwise_panel_positions)

    def vlm(self):
        """ For a given set of panels (defined by its 4 points) and
            their chordwise position (referred to the local chord),
            both presented as lists, computes the induced velocity
            produced by all the associated horseshoe vortices on each
            panel, calculated on its control point where the boundary
            condition will be imposed. Computes the circulation by
            solving the linear equation """

        Panels_points = self.Panels_points
        Chordwise_panel_positions = self.Chordwise_panel_positions

        V = self.V
        alpha = self.alpha

        # 1. BOUNDARY CONDITION
        # To impose the boundary condition we have to calculate
        # the normal components of (a) induced velocities Wn and
        # (b) upstream velocity Vn_inf

        #     1.a INDUCED VELOCITIES
        #     stored in the matrix "A" where the element Aij is
        #     the velocity induced by the panel j on the panel i

        N = len(Panels_points)
        A = np.zeros(shape=(N, N))

        for i in range(0, N):
            P1, P2, P3, P4 = Panels_points[i][:]
            panel_pivot = Panel(P1, P2, P3, P4)
            s = panel_pivot.area()
            CP = panel_pivot.control_point()

            for j in range(0, N):
                PP1, PP2, PP3, PP4 = Panels_points[j][:]
                panel = Panel(PP1, PP2, PP3, PP4)
                Wn = panel.induced_velocity(CP)
                A[i, j] = Wn

        #     1.b UPSTREAM VELOCITIES
        #     that will depend on the angle of attach -"alpha"-
        #     and the camber gradient at each panel's position
        #     within the local chord

        Vinf_n = np.zeros(shape=N)

        airfoil = NACA4()
        for i in range(0, N):
            position = Chordwise_panel_positions[i]
            Vinf_n[i] = alpha - airfoil.camber_gradient(position)
            Vinf_n[i] *= -self.V

        # 2. CIRCULATION (gamma)
        # by solving the linear equation (AX = Y) where X = gamma
        # and Y = V_inf

        gamma = np.linalg.solve(A, Vinf_n)

        return Vinf_n, A, gamma


# gamma_plot = X
# cl_plot = (2.0 * X) / (V * c)
# cd_plot = (-2.0 * abs(X) * w * b) / (V**2 * S)
# cm_plot = - cl_plot[i] * (0.25 * c) / c

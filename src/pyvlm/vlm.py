import numpy as np
import matplotlib.pyplot as plt

from .panel import Panel
from .mesh_generator import Mesh
from .airfoils import NACA4


class PyVLM(object):
    """
    Given a geometry, angle of attack, upstream velocity and mesh
    chordwise and spanwise densities, applies the VLM theory to
    the defined lifting surface.

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

        self.rho = 1.225

    def add_geometry(self, lead_edge_coord, chord_lengths, n, m):
        """
        Allows to add wings, stabilizers, canard wings or any other
        lifting surface to the mesh. These are defined by their chords'
        lengths and leading edges locations. The spanwise and chordwise
        density of the mesh can be controlled through n and m.
        """

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

    def check_mesh(self):
        """
        Prints the points of the mesh, the disposition of each panel and
        plots them for visual check.
        """

        Points = self.Points
        Panels = self.Panels_points
        Panels_span = self.Panels_span
        Panels_chordwise_pos = self.Chordwise_panel_positions

        # Check for coincident points
        N = len(Points)
        for i in range(0, N):
            count = 0
            for j in range(0, N):
                if(((Points[j] == Points[i]).all()) is True):
                    count += 1
                    if(count > 1):
                        msg = "Two points of the mesh coincide"
                        raise ValueError(msg)

        # Check for incorrectly defined panels
        N = len(Panels)
        for i in range(0, N):
            P1, P2, P3, P4 = Panels[i][:]

            P1P2 = P2 - P1
            P1P3 = P3 - P1
            P1P4 = P4 - P1
            P3P4 = P4 - P3

            i_inf = np.array([1, 0])

            if np.cross(P1P2, i_inf) != 0:
                msg = 'P1P2 segment not aligned with OX'
                raise ValueError(msg)

            if np.cross(P1P2, P3P4) != 0:
                msg = 'Panel incorrectly defined, P1P2 and P3P4 not parallel'
                raise ValueError(msg)

            if np.sign(np.cross(P1P2, P1P3)) != np.sign(np.cross(P1P3, P1P4)):
                msg = 'Points not in a clockwise/counterclockwise fashion'
                raise ValueError(msg)

        # PRINTING AND PLOTTING
        # print('\n Point |    Coordinates ')
        # print('------------------------')
        # for i in range(0, len(Points)):
        #     print('  %2s   |' % i, np.round(Points[i], 2))

        print('\n Panel | Chrd %  |  Span  |  Points coordinates')
        print('------------------------------------------------')
        for i in range(0, len(Panels)):
            print('  %2s   |  %4.2f  | %5.4f | '
                  % (i, 100*Panels_chordwise_pos[i], Panels_span[i]),
                  np.round(Panels[i][0], 2), np.round(Panels[i][1], 2),
                  np.round(Panels[i][2], 2), np.round(Panels[i][3], 2))

        plt.style.use('ggplot')
        plt.xlim(-5, 15), plt.ylim(-10, 10)
        for i in range(0, len(Points)):
            P = Points[i]
            plt.plot(P[0], P[1], 'ro')
        plt.show()

    def vlm(self):
        """
        For a given set of panels (defined by its 4 points) and their
        chordwise position (referred to the local chord), both presented
        as lists, applies the VLM theory:

            - Calculates the induced velocity produced by all the
              associated horseshoe vortices of strength=1 on each panel,
              calculated on its control point where the boundary condition
              will be imposed.
            - Computes the circulation by solving the linear equation.

        Then it produces the forces acting on each panel.
        """

        Panels = self.Panels_points
        Panels_span = self.Panels_span
        Panels_chordwise_position = self.Chordwise_panel_positions

        V = self.V
        alpha = self.alpha
        rho = self.rho

        # 1. BOUNDARY CONDITION
        # To impose the boundary condition we must calculate the normal
        # components of (a) induced velocity "Wn" by horshoe vortices of
        # strength=1 and (b) upstream normal velocity "Vinf_n"

        #     1.a INDUCED VELOCITIES
        #     - "Wn", normal component of the total induced velocity by the
        #       horshoe vortices, stored in the matrix "A" where the element
        #       Aij is the velocity induced by the horshoe vortex in panel j
        #       on the control point of panel i
        #     - also the induced velocity by *only* trailing vortices "Wi" is
        #       calculated and stored in the array "W_induced", where the
        #       element Winduced[i] is the velocity induced by all the trailing
        #       vortices on the panel i

        N = len(Panels)
        A = np.zeros(shape=(N, N))
        W_induced = np.zeros(N)  # induced velocity by trailing vortices
        alpha_induced = np.zeros(N)  # induces angle of attack

        for i in range(0, N):
            P1, P2, P3, P4 = Panels[i][:]
            panel_pivot = Panel(P1, P2, P3, P4)
            s = panel_pivot.area()
            CP = panel_pivot.control_point()

            Wi_ = 0
            for j in range(0, N):
                PP1, PP2, PP3, PP4 = Panels[j][:]
                panel = Panel(PP1, PP2, PP3, PP4)
                Wn, Wi = panel.induced_velocity(CP)
                A[i, j] = Wn
                Wi_ += Wi

            W_induced[i] = Wi_
            alpha_induced[i] = np.arctan(abs(W_induced[i])/V)  # rad

        #     1.b UPSTREAM NORMAL VELOCITY
        #     that will depend on the angle of attach -"alpha"- and the
        #     camber gradient at each panel's position within the local
        #     chord

        Vinf_n = np.zeros(shape=N)

        airfoil = NACA4()
        for i in range(0, N):
            position = Panels_chordwise_position[i]
            Vinf_n[i] = alpha - airfoil.camber_gradient(position)
            Vinf_n[i] *= -V

        # 2. CIRCULATION (gamma)
        # by solving the linear equation (AX = Y) where X = gamma
        # and Y = Vinf_n

        gamma = np.linalg.solve(A, Vinf_n)

        l = np.zeros(N)
        d = np.zeros(N)
        for i in range(0, N):
            l[i] = V * rho * gamma[i] * Panels_span[i]
            d[i] = rho * abs(gamma[i]) * Panels_span[i] * abs(W_induced[i])

        L = sum(l)
        D = sum(d)

        print('\n Panel | Vinf_n | Gamma |   Wi   |alpha_i|    l   |   d  |')
        print('----------------------------------------------------------')
        for i in range(0, len(Panels)):
            print('  %2s   |  %5.2f | %5.2f | %6.3f | %5.3f |%7.1f | %4.2f |'
                  % (i, Vinf_n[i], gamma[i], W_induced[i],
                     np.rad2deg(alpha_induced[i]), l[i], d[i]))
        print('\n L = %6.3f     D = %6.3f ' % (L, D))

        return L, D

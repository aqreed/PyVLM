import numpy as np
import matplotlib.pyplot as plt

from .panel import Panel
from .mesh_generator import Mesh
from .airfoils import NACA4


class PyVLM(object):
    """
    Given a geometry, mesh chordwise and spanwise densities, angle of
    attack, upstream velocity, applies the VLM theory to the
    defined lifting surface.
    """

    def __init__(self):
        self.Points = []
        self.Panels = []

        self.AIC = 0
        self.alpha = []
        self.CL = []
        self.CD = []

        self.rho = 1.225

    def add_wing(self, lead_edge_coord, chord_lengths, n, m):
        """
        Allows the addition of a wing to the mesh, defined by its chords'
        lengths and leading edges locations. The spanwise and chordwise
        density of the mesh can be controlled through n and m.
        ONLY half a wing is needed to define it. A specular image will
        be used to create the other half.

        Parameters
        ----------
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

        if len(lead_edge_coord) != len(chord_lengths):
            msg = 'Same number of chords and leading edges required'
            raise ValueError(msg)

        # MESH GENERATION
        # When more than two chords -with their respectives leading
        # edges coordinates- are provided, it iterates through the
        # lists containing both location and length.

        Nle = len(lead_edge_coord)

        for k in range(Nle - 1):
            leading_edges = [lead_edge_coord[k],
                             lead_edge_coord[k + 1]]
            chords = [chord_lengths[k],
                      chord_lengths[k + 1]]

            # The mesh is created taking into account the desired
            # mesh density spanwise -"n"- and chordwise -"m"-

            mesh = Mesh(leading_edges, chords, n, m)

            # The points of the mesh and its panels - sets of 4 points
            # orderly arranged - are calculated

            Points_ = mesh.points()
            Panels_ = mesh.panels()

            self.Points.extend(Points_)
            self.Panels.extend(Panels_)

        # Specular image to generate the opposite semi-span of the wing
        lead_edge_coord_ = lead_edge_coord[::-1]
        chord_lengths_ = chord_lengths[::-1]

        for k in range(Nle - 1):
            leading_edges = [lead_edge_coord_[k]*[1, -1],
                             lead_edge_coord_[k + 1]*[1, -1]]
            chords = [chord_lengths_[k],
                      chord_lengths_[k + 1]]

            mesh = Mesh(leading_edges, chords, n, m)

            Points_ = mesh.points()
            Panels_ = mesh.panels()

            self.Points.extend(Points_)
            self.Panels.extend(Panels_)

    def check_mesh(self):
        """
        Prints the points of the mesh, the disposition of each panel and
        plots them for visual check.
        """

        Points = self.Points
        Panels = self.Panels

        # Check for coincident points
        N = len(Points)
        for i in range(N):
            count = 0
            for j in range(N):
                if(((Points[j] == Points[i]).all()) is True):
                    count += 1
                    if(count > 1):
                        msg = "Two points of the mesh coincide"
                        raise ValueError(msg)

        # Check for incorrectly defined panels
        N = len(Panels)
        for i in range(N):
            P1P2 = Panels[i].P2 - Panels[i].P1
            P1P3 = Panels[i].P3 - Panels[i].P1
            P1P4 = Panels[i].P4 - Panels[i].P1
            P3P4 = Panels[i].P4 - Panels[i].P3

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
        print('\nPanel| Chrd% |  Span |  Points coordinates')
        print('------------------------------------------------')
        for i in range(N):
            print(' %3s | %5.2f | %5.3f | '
                  % (i, 100*Panels[i].chordwise_position, Panels[i].span),
                  np.round(Panels[i].P1, 2), np.round(Panels[i].P2, 2),
                  np.round(Panels[i].P3, 2), np.round(Panels[i].P4, 2))

        plt.style.use('ggplot')
        plt.xlim(-5, 15), plt.ylim(-10, 10)
        for i in range(len(Points)):
            P = Points[i]
            plt.plot(P[0], P[1], 'ro')
        plt.show()

    def vlm(self, alpha, print_output=False):
        """
        For a given set of panels applies the VLM theory:

            1. Calculates the induced velocity produced by all the
               associated horseshoe vortices of strength=1 on each panel,
               calculated on its control point where the boundary condition
               will be imposed.
            2. Computes the circulation by solving the linear equation.
            3. Calculates the aerodynamic forces.

        Parameters
        ----------
        alpha : float
            Angle of attack of the wing
        """

        Panel = self.Panels
        rho = self.rho
        V = 1.0

        q_inf = (1 / 2) * rho * (V**2)

        # 1. BOUNDARY CONDITION
        # To impose the boundary condition we must calculate the normal
        # components of (a) induced velocity "Wn" by horshoe vortices of
        # strength=1 and (b) upstream normal velocity "Vinf_n"

        #   (a) INDUCED VELOCITIES
        #     - "Wn", normal component of the total induced velocity by
        #       the horshoe vortices, stored in the matrix "AIC" where the
        #       element Aij is the velocity induced by the horshoe vortex
        #       in panel j on panel i
        #     - also the induced velocity by *only* the trailing vortices
        #        "Wi" on panel i is calculated and stored in the Panel object
        #       attribute "accul_trail_induced_vel"

        N = len(Panel)
        AIC = np.zeros((N, N))  # Aerodynamic Influence Coefficient matrix

        for i in range(N):
            panel_pivot = Panel[i]
            CP = panel_pivot.CP

            Wi_ = 0
            for j in range(N):
                panel = Panel[j]
                Wn, Wi = panel.induced_velocity(CP)
                AIC[i, j] = Wn  # induced velocity (normal) by horshoe vortices
                Wi_ += Wi  # induced velocity (normal) by trailing vortices

            Panel[i].accul_trail_ind_vel = Wi_
            Panel[i].alpha_ind = np.arctan(abs(Wi_)/V)  # induced AoA(rad)

        self.AIC = AIC

        #   (b) UPSTREAM NORMAL VELOCITY
        #     It will depend on the angle of attach -"alpha"- and the camber
        #     gradient at each panel's position within the local chord

        Vinf_n = np.zeros(N)  # upstream (normal) velocity

        airfoil = NACA4()
        for i in range(N):
            position = Panel[i].chordwise_position
            Panel[i].Vinf_n = -V * (alpha - airfoil.camber_gradient(position))
            Vinf_n[i] = Panel[i].Vinf_n

        # 2. CIRCULATION (Γ or gamma)
        # by solving the linear equation (AX = Y) where X = gamma
        # and Y = Vinf_n

        gamma = np.linalg.solve(AIC, Vinf_n)

        # 3. AERODYNAMIC FORCES
        L = 0
        D = 0
        S = 0

        for i in range(N):
            Panel[i].gamma = gamma[i]
            Panel[i].l = V * rho * Panel[i].gamma * Panel[i].span
            Panel[i].cl = Panel[i].l / (q_inf * Panel[i].area)

            Panel[i].d = V * rho * abs(Panel[i].gamma) * Panel[i].span * \
                         abs(Panel[i].accul_trail_ind_vel)  # TODO: check
            Panel[i].cd = Panel[i].d / (q_inf * Panel[i].area)

            L += Panel[i].l
            D += Panel[i].d
            S += Panel[i].area

        CL = L / (q_inf * S)
        CD = D / (q_inf * S)

        # PRINTING
        if (print_output is True):
            print('\nPanel|  V∞_n |   Wi   |  α_i  |   Γ   |   cl   |   cd    |')
            print('----------------------------------------------------------')
            for i in range(N):
                print(' %3s | %5.2f | %6.2f | %5.2f | %5.2f |%7.3f | %7.5f |'
                      % (i, Panel[i].Vinf_n, Panel[i].accul_trail_ind_vel,
                         np.rad2deg(Panel[i].alpha_ind), Panel[i].gamma,
                         Panel[i].cl, Panel[i].cd))
            print('\n CL = %6.3f' % CL)
            print(' CD = %8.5f \n' % CD)

        return CL, CD

    def aerodyn_forces_coeff(self):
        """
        For a given geometry applies the VLM theory for angles of attack
        (alpha) between -15 and 15 degrees, returning CL and CD as lists.
        """
        for i in range(-15, 15, 2):
            cl_, cd_ = self.vlm(np.deg2rad(i), False)
            self.alpha.append(i)
            self.CL.append(cl_)
            self.CD.append(cd_)

        return self.alpha, self.CL, self.CD

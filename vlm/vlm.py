import numpy as np
import matplotlib.pyplot as plt

from .panel import Panel
from .mesh_generator import Mesh
from .airfoils import NACA4, flat_plate


class PyVLM(object):
    """
    Given a geometry, mesh chordwise and spanwise densities, angle
    of attack, upstream velocity, applies the VLM theory to the
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

    def reset(self):
        self.Points = []
        self.Panels = []
        self.AIC = 0
        self.alpha = []
        self.CL = []
        self.CD = []

    def add_surface(self, le_coords, ch_lens, n, m,
                    mirror=True, airfoil=NACA4()):
        """
        Allows the addition of a surface to the mesh, defined by its chords'
        lengths and leading edges locations. The spanwise and chordwise
        density of the mesh can be controlled through n and m.
        ONLY half a surface is needed to define it. A specular image will
        be used to create the other half.

        Parameters
        ----------
        le_coords : list (containing arrays)
            leading edge coordinates as arrays in a 2D euclidean space
        ch_lens : list
            chord lenghts corresponding to the sections defined by the
            leading edge coordinates
        n, m : integer
            n - nº of chordwise panels
            m - nº of spanwise panels
        mirror : boolean
            if True generates a specular surface, taking plane OXZ as reference
        airfoil : object
            airfoil of the surface

        TODO: add angle of incidence for each surface (twist distribution)
        """
        self.AIC = 0  # clears AIC when modifying the mesh

        if len(le_coords) != len(ch_lens):
            msg = 'Same number of chords and leading edges required'
            raise ValueError(msg)

        for le in le_coords:
            count = 1
            for le_ in le_coords:
                if np.array_equal(le, le_):
                    count += 1
                    if(count > 2):
                        msg = "Two leading edge coordinates coincide"
                        raise ValueError(msg)

        # MESH GENERATION
        # When more than two chords -with their respectives leading
        # edges coordinates- are provided, it iterates through the
        # lists containing both location and length.
        Nle = len(le_coords)

        for k in range(Nle - 1):
            leading_edges = [le_coords[k], le_coords[k + 1]]
            chords = [ch_lens[k], ch_lens[k + 1]]

            # The mesh is created taking into account the desired
            # mesh density spanwise -"n"- and chordwise -"m"-

            mesh = Mesh(leading_edges, chords, n, m, airfoil)

            # The points of the mesh and its panels - sets of 4 points
            # orderly arranged - are calculated

            points_ = mesh.points()
            panels_ = mesh.panels()

            self.Points.extend(points_)
            self.Panels.extend(panels_)

        # Specular image to generate the opposite semi-span of the surface
        le_coords_ = le_coords[::-1]
        ch_lens_ = ch_lens[::-1]

        if mirror:
            for k in range(Nle - 1):
                leading_edges = [le_coords_[k] * [1, -1],
                                 le_coords_[k + 1] * [1, -1]]
                chords = [ch_lens_[k], ch_lens_[k + 1]]

                mesh = Mesh(leading_edges, chords, n, m, airfoil)

                points_ = mesh.points()
                panels_ = mesh.panels()

                self.Points.extend(points_)
                self.Panels.extend(panels_)

    def show_mesh(self, print_mesh=False, plot_mesh=False):
        """
        Prints the points of the mesh, the disposition of each panel and
        plots them for visual check.
        Parameters
        ----------
        print_mesh : boolean
            Self-explained
        plot_mesh : boolean
            Self-explained
        """
        points = self.Points
        panels = self.Panels

        # PRINTING AND PLOTTING
        if print_mesh:
            print('\nPanel| Chrd% |  Span |  Points coordinates')
            print('------------------------------------------')
            for panel, i in zip(panels, range(len(panels))):
                print(' %3s | %5.2f | %5.3f | '
                      % (i, 100*panel.chordwise_position, panel.span),
                      np.round(panel.P1, 3), np.round(panel.P2, 3),
                      np.round(panel.P3, 3), np.round(panel.P4, 3))

        if plot_mesh:
            plt.style.use('ggplot')
            for point in points:
                plt.plot(point[0], point[1], 'ro')
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
            Angle of attack of the airplane(degrees)
        print_output : boolean
            Prints the calculation output
        """
        panels = self.Panels
        rho = self.rho
        alpha = np.deg2rad(alpha)
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
        N = len(panels)

        if (type(self.AIC) == int):
            # In case it is the first time the method is called, it proceeds
            # to compute the AIC matrix

            AIC = np.zeros((N, N))  # Aerodynamic Influence Coefficient matrix

            for panel_pivot, i in zip(panels, range(N)):
                Wi_ = 0
                for panel, j in zip(panels, range(N)):
                    Wn, Wi = panel.induced_velocity(panel_pivot.CP)
                    AIC[i, j] = Wn  # induced normal velocity by horshoe vortices
                    Wi_ += Wi  # induced normal velocity by trailing vortices

                panel_pivot.accul_trail_ind_vel = Wi_
                panel_pivot.alpha_ind = np.arctan(abs(Wi_)/V)  # induced AoA(rad)

            self.AIC = AIC

        #   (b) UPSTREAM NORMAL VELOCITY
        #     It will depend on the angle of attack -"alpha"- and the camber
        #     local slope (at each panel' position within the local chord)
        Vinf_n = np.zeros(N)  # upstream (normal) velocity

        for panel, i in zip(panels, range(N)):
            panel.Vinf_n = -V * (alpha - panel.loc_slope)
            Vinf_n[i] = panel.Vinf_n

        # 2. CIRCULATION (Γ or gamma)
        # by solving the linear equation (AX = Y) where X = gamma
        # and Y = Vinf_n
        gamma = np.linalg.solve(self.AIC, Vinf_n)

        # 3. AERODYNAMIC FORCES
        L = 0
        D = 0
        S = 0

        for panel, i in zip(panels, range(N)):
            panel.gamma = gamma[i]
            panel.l = V * rho * panel.gamma * panel.span
            panel.cl = panel.l / (q_inf * panel.area)

            # d0 = (panel.l * panel.accul_trail_ind_vel) / V
            d = -rho * abs(panel.gamma) * panel.span * panel.accul_trail_ind_vel
            # d2 = panels.l * np.sin(panel.alpha_ind)

            # print("%8.3f % 8.3f %8.3f" % (d0, d1, d2))

            panel.d = d
            panel.cd = panel.d / (q_inf * panel.area)

            L += panel.l
            D += panel.d
            S += panel.area

        CL = L / (q_inf * S)
        CD = D / (q_inf * S)

        # PRINTING
        if print_output:
            print('\nPanel|  V∞_n |   Wi   |  α_i  |   Γ   |   cl   |   cd    |')
            print('----------------------------------------------------------')
            for panel, i in zip(panels, range(N)):
                print(' %3s | %5.2f | %6.2f | %5.2f | %5.2f |%7.3f | %7.5f |'
                      % (i, panel.Vinf_n, panel.accul_trail_ind_vel,
                         np.rad2deg(panel.alpha_ind), panel.gamma,
                         panel.cl, panel.cd))
            print('\n For alpha = %3s degrees:' % np.rad2deg(alpha))
            print('	CL = %6.3f' % CL)
            print('	CD = %8.5f' % CD)
        else:
            return CL, CD

    def aerodyn_forces_coeff(self):
        """
        For a given geometry applies the VLM theory for angles of attack
        (alpha) between -15 and 15 degrees, returning CL and CD as lists.
        """
        for i in range(-15, 15, 2):
            cl_, cd_ = self.vlm(i, False)
            self.alpha.append(i)
            self.CL.append(cl_)
            self.CD.append(cd_)

        return self.alpha, self.CL, self.CD

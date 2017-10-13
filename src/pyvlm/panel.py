from .geometry import area_4points
from .vortices import (vortex_position_in_panel,
                       v_induced_by_horseshoe_vortex)


class Panel(object):
    """
             y ^
               |            Each panel is defined by the (x, y) coordinates
        P3--B--|--+--P4     of four points - namely P1, P2, P3 and P4 -
         |  |  |  |  |      ordered clockwise.
         |  |  |  |  |      Points defining the horseshoe are A, B and P.
         |  |  +--CP-|--->
         |  |     |  |   x
         |  |     |  |
        P2--A-----+--P1

    Parameters
    ----------
    P1, P2, P3, P4 : array_like
                     Corner points in a 2D euclidean space
    """

    def __init__(self, P1, P2, P3, P4):
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.P4 = P4

        self.CP, self.A, self.B = vortex_position_in_panel(P1, P2, P3, P4)
        self.area = area_4points(P1, P2, P3, P4)
        self.span = abs(self.P3[1] - self.P2[1])
        self.chordwise_position = 0  # position w.r.t. the local chord

        self.accul_trail_ind_vel = 0  # induced vel. by trailing vortices
        self.alpha_ind = 0  # induced angle of attack
        self.Vinf_n = 0  # local upstream normal velocity
        self.gamma = 0  # circulation value

        self.l = 0  # lift force
        self.d = 0  # drag force
        self.cl = 0  # lift force coefficient
        self.cd = 0  # drag force coefficient

    def induced_velocity(self, control_point_pos):
        """
        Returns the induced velocity by a horseshoe vortex and the induced
        velocity excluding the bounded segment at a control point, defined
        as argument of the method, that does not have to be its own CP.
        """

        v = v_induced_by_horseshoe_vortex(control_point_pos,
                                          self.A, self.B)

        return v[0], v[1]

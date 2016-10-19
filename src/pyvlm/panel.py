import numpy as np

from .geometry import area_4points
from .vortices import (vortex_position_in_panel,
                       v_induced_by_horseshoe_vortex)


class Panel(object):
    """
           y ^
             |              Points defining the panel are named
        P3-C-|-D-P4         clockwise. Points defining the horseshoe
         | | | |  |         are named clockwise as well.
         | | +-P--|--->
         | |   |  |   x
        P2-B---A-P1
    """

    def __init__(self, value1, value2, value3, value4):
        self.P1 = value1
        self.P2 = value2
        self.P3 = value3
        self.P4 = value4
        self.CP = 0  # control point
        self.w = 0

    def get_panel_position(self):
        return self.P1, self.P2, self.P3, self.P4

    def area(self):
        return area_4points(self.P1, self.P2, self.P3, self.P4)

    def _vortex_position(self):
        points_of_the_vortex = vortex_position_in_panel(self.P1, self.P2,
                                                        self.P3, self.P4)
        return points_of_the_vortex

    def control_point(self):
        control_point_position = self._vortex_position()[0]
        return control_point_position

    def induced_velocity(self, control_point_pos):
        _points_vortex = self._vortex_position()
        v = v_induced_by_horseshoe_vortex(control_point_pos, _points_vortex[1],
                                          _points_vortex[2], _points_vortex[3],
                                          _points_vortex[4])
        return v

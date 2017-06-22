"""
    This example shows the use of the PyVLM class in order
    to generate the wing planform of a Pilatus PC12 airplane.

    The left wing will be characterised using the following
    nomenclature while the right wing will be created as the
    specular image of the left wing:

    Y  ^   +----+
       |  /      \
       | /        \
       |/          \
       +------------+
       +-------------------->
     B +------------+        X
        \          /
         \        /
          \      /
         A +----+
"""

import numpy as np
import matplotlib.pyplot as plt

from pyvlm.vlm import PyVLM


pilatusPC12 = PyVLM()

# Geometry parameters
c, b = 2.15, 16.28  # root chord length, panel span length
n, m = 8, 6  # number of panels (chordwise, spanwise)

# Left wing
A, B = np.array([.414, -b/2]), np.array([0, -1.03])
leading_edges_coord = [A, B]
chord_lengths = [1.24, c]

pilatusPC12.add_wing(leading_edges_coord, chord_lengths, n, m)
pilatusPC12.check_mesh()

# Flight condition parameters
V, alpha = 140.0, np.deg2rad(0)

print('\nResults for the following flight conditions:'
      '\n    V = %4.1f m/s \n    alpha = %3.1f degrees'
      % (V, np.rad2deg(alpha)))

pilatusPC12.vlm(V, alpha, True)

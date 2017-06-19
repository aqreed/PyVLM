"""
    This example shows how to use the PyVLM class in order
    to generate the wing planform of a Pilatus PC12 airplane.

    After defining the flight conditions (airspeed and AOA),
    the geometry will be characterised using the following
    nomenclature:

    Y  ^  D +--+
       |   /    \
       |  /      \
       | /        \
       |/          \
     C +------------+
       +-------------------->
     B +------------+        X
        \          /
         \        /
          \      /
           \    /
          A +--+
"""

import numpy as np
import matplotlib.pyplot as plt

from pyvlm.vlm import PyVLM


pilatusPC12 = PyVLM()

# GEOMETRY DEFINITION #
# Parameters
c = 2.15  # root chord length
b = 16.28  # panel span length
n = 8  # number of panels (chordwise)
m = 6  # number of panels (spanwise)

# Left wing
A = np.array([.414, -b/2])
B = np.array([0, -1.03])
leading_edges_coord_lw = [A, B]
chord_lengths_lw = [1.24, c]

# Right wing
C = np.array([0, 1.03])
D = np.array([0.414, b/2])
leading_edges_coord_rw = [C, D]
chord_lengths_rw = [c, 1.24]

## Horizontal stabilizer
#A = np.array([8.284, -2.07])
#B = np.array([7.87, 0])
#C = np.array([8.284, 2.07])
#leading_edges_coord_hs = [A, B, C]
#chord_lengths_hs = [0.911, 1.33, 0.911]

pilatusPC12.add_geometry(leading_edges_coord_lw, chord_lengths_lw, n, m)
pilatusPC12.add_geometry(leading_edges_coord_rw, chord_lengths_rw, n, m)
#pilatusPC12.add_geometry(leading_edges_coord_hs, chord_lengths_hs, 4, 4)

pilatusPC12.check_mesh()

# SIMULATION
# Flight condition parameters
V = 140.0
alpha = np.deg2rad(0)

print('\nResults for the following flight conditions:'
      '\n    V = %4.1f m/s \n    alpha = %3.1f degrees'
      % (V, np.rad2deg(alpha)))

pilatusPC12.vlm(V, alpha, True)

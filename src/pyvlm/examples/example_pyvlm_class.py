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


# FLIGHT CONDITION PARAMETERS #
V = 20.0
alpha = np.deg2rad(3)

pilatusPC12 = PyVLM(V, alpha)

# GEOMETRY DEFINITION #
# Parameters
c = 2.15  # root chord length
b = 16.28  # panel span length
n = 3  # number of panels chordwise
m = 4  # number of panels spanwise

# Left wing
A = np.array([.414, -b/2])
B = np.array([0, -1.03])
leading_edges_coord = [A, B]
chord_lengths = [1.24, c]

Points, Panels, Panels_span, Chordwise_panel_pos = pilatusPC12.add_geometry(
                                                   leading_edges_coord,
                                                   chord_lengths, n, m)
# Right wing
C = np.array([0, 1.03])
D = np.array([0.414, b/2])
leading_edges_coord = [C, D]
chord_lengths = [c, 1.24]

Points, Panels, Panels_span, Chordwise_panel_pos = pilatusPC12.add_geometry(
                                                   leading_edges_coord,
                                                   chord_lengths, n, m)
# Horizontal stabilizer
# A = np.array([8.284, -2.07])
# B = np.array([7.87, 0])
# C = np.array([8.284, 2.07])

# leading_edges_coord = [A, B, C]
# chord_lengths = [0.911, 1.33, 0.911]

# Points, Panels, Chordwise_panel_pos = pilatusPC12.add_geometry(
#                                                   leading_edges_coord,
#                                                   chord_lengths, n, m)

pilatusPC12.check_mesh()

# SIMULATION
Vinf_n, matrix, gamma = pilatusPC12.vlm()


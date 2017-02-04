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


# SIMULATION
Vinf_n, matrix, gamma = pilatusPC12.vlm()

# PRINTING AND PLOTTING
print('\n Point |    Coordinates ')
print('--------------------------')
for i in range(0, len(Points)):
    print('  %2s   |' % i, np.round(Points[i], 2))

print('\n Panel | Chrd %  |  Span  |  Vinf_n  |  Gamma |   Points coordinates')
print('----------------------------------------------------------------------')
for i in range(0, len(Panels)):
    print('  %2s   |  %4.2f  | %5.4f |  %6.3f  | %5.4f | '
          % (i, 100*Chordwise_panel_pos[i], Panels_span[i],
          Vinf_n[i], gamma[i]), np.round(Panels[i][0], 2),
          np.round(Panels[i][1], 2), np.round(Panels[i][2], 2),
          np.round(Panels[i][3], 2))

plt.style.use('ggplot')
plt.xlim(-5, 15), plt.ylim(-10, 10)
for i in range(0, len(Points)):
    P = Points[i]
    plt.plot(P[0], P[1], 'ro')
plt.show()

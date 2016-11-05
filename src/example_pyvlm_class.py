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

Points, Panels, Chordwise_panel_pos = pilatusPC12.add_geometry(
                                                  leading_edges_coord,
                                                  chord_lengths, n, m)
# Right wing
C = np.array([0, 1.03])
D = np.array([0.414, b/2])
leading_edges_coord = [C, D]
chord_lengths = [c, 1.24]

Points, Panels, Chordwise_panel_pos = pilatusPC12.add_geometry(
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


# SIMULATION #
Y, A, X = pilatusPC12.vlm()


# PRINTING AND PLOTTING #
np.set_printoptions(precision=3)

print('\n', 'Nº of points = ', len(Points))
for i in range(0, len(Points)):
    print('Point %s =' % i, Points[i])

print('\n', 'Nº of Panels = ', len(Panels))
for i in range(0, len(Panels)):
    print('Panel %s' % i, Panels[i])

print('\n', 'Nº of Chordwise panel position = ', len(Chordwise_panel_pos))
for i in range(0, len(Chordwise_panel_pos)):
    print('Panel %s' % i, Chordwise_panel_pos[i])

print('\n', 'Matrix A =', '\n', A, '\n')
print('Y =', Y, '\n')
print('X =', X, '\n')

plt.style.use('ggplot')
plt.xlim(-5, 15), plt.ylim(-10, 10)
for i in range(0, len(Points)):
    P = Points[i]
    plt.plot(P[0], P[1], 'ro')
plt.show()

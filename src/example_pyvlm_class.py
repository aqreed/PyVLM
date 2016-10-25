import numpy as np
import matplotlib.pyplot as plt

from pyvlm.vlm import PyVLM
from pyvlm.panel import Panel
from pyvlm.mesh_generator import Mesh
from pyvlm.airfoils import camber_gradient_NACA4

V = 20.0
alpha = np.deg2rad(3)
c = 4  # panel chord length
b = 10  # panel span length
n = 5  # number of panels chordwise
m = 2  # number of panels spanwise
A = np.array([c, -b/2])
B = np.array([0, -b/10])
C = np.array([0, b/10])
D = np.array([c, b/2])

leading_edges_coord = [B, C]
chord_lengths = [c, c]
#leading_edges_coord = [A, B, C, D]
#chord_lengths = [c/4, c, c, c/4]

wing = PyVLM(leading_edges_coord, chord_lengths, V, alpha, n, m)

Y, A, X = wing.get_linear_eq()
Points, Panels, Chord_pos = wing.get_geometry()

np.set_printoptions(precision=3)
print('\n', 'Matrix A =', '\n', A, '\n')
print('Y =', Y, '\n')
print('X =', X, '\n')

# Plotting
print('\n', 'Nº of points = ', len(Points))
for i in range(0, len(Points)):
    print('Point %s =' % i, Points[i])

print('\n', 'Nº of Panels = ', len(Panels))
for i in range(0, len(Panels)):
    print('Panel %s' % i, Panels[i])

plt.style.use('ggplot')
for i in range(0, len(Points)):
    P = Points[i]
    plt.plot(P[0], P[1], 'ro')
plt.show()

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
m = 3  # number of panels spanwise
A = np.array([c, -b/2])
B = np.array([0, -b/5])
C = np.array([0, b/5])
D = np.array([c, b/2])

#leading_edges_coord = [B, C]
#chord_lengths = [c, c]
leading_edges_coord = [A, B, C, D]
chord_lengths = [c/4, c, c, c/4]

example = PyVLM(V, alpha)

Points, Panels, Chords, Chordwise_panel_pos = example.create_geometry(
                                              leading_edges_coord,
                                              chord_lengths, n, m)

Y, A, X = example.vlm()


np.set_printoptions(precision=3)

# Plotting
print('\n', 'Nº of points = ', len(Points))
for i in range(0, len(Points)):
    print('Point %s =' % i, Points[i])

print('\n', 'Nº of Panels = ', len(Panels))
for i in range(0, len(Panels)):
    print('Panel %s' % i, Panels[i])

print('\n', 'Matrix A =', '\n', A, '\n')
print('Y =', Y, '\n')
print('X =', X, '\n')

plt.style.use('ggplot')
for i in range(0, len(Points)):
    P = Points[i]
    plt.plot(P[0], P[1], 'ro')
plt.show()

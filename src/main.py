import numpy as np
import matplotlib.pyplot as plt

from pyvlm.panel import Panel
from mesh_generator import Mesh

# Initial data
V = 10.0
alpha = np.deg2rad(3)

# Grid generator
c = 1  # panel chord length
b = 4  # panel span length

n = 2  # number of panels chordwise
m = 4  # number of panels spanwise

A = np.array([0, -b/2])
B = np.array([0, b/2])
leading_edges = [A, B]
chord = [1, 1]

mesh = Mesh(leading_edges, chord, n, m)
Points, Panels = mesh.points_panels()

# Calculations
N = n * m
A = np.zeros(shape=(N, N))

for i in range(0, N):
    P1, P2, P3, P4 = Panels[i][:]
    panel_pivot = Panel(P1, P2, P3, P4)
    s = panel_pivot.area()
    CP = panel_pivot.control_point()

    print('---- Induced vel. on panel %s...' % i)
    print(P1, P2, P3, P4)
    print('area = ', s, 'control point = ', CP)

    for j in range(0, N):
        PP1, PP2, PP3, PP4 = Panels[j][:]
        panel = Panel(PP1, PP2, PP3, PP4)
        w = panel.induced_velocity(CP)
        print('	...by panel %s = %s' % (j, w))
        A[i, j] = w

np.set_printoptions(precision=4)
print('\n','Matrix A =', '\n', A, '\n')

plt.style.use('ggplot')
plt.plot(Points[:, 0], Points[:, 1], 'ro')
plt.show()

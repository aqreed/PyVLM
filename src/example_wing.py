import numpy as np
import matplotlib.pyplot as plt

from pyvlm.panel import Panel
from pyvlm.mesh_generator import Mesh
from pyvlm.airfoils import camber_gradient_NACA4

# Initial data
V = 20.0
alpha = np.deg2rad(3)

# Grid generator
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

Nle = len(leading_edges_coord)
Nch = len(chord_lengths)
if Nle != Nch:
    msg = 'Same number of chords and l.e. required'
    raise ValueError(msg)

Points = []
Panels = []
Chord_pos = []
for k in range(0, Nle - 1):
    leading_edges = [leading_edges_coord[k],
                     leading_edges_coord[k + 1]]
    chords = [chord_lengths[k],
              chord_lengths[k + 1]]

    mesh = Mesh(leading_edges, chords, n, m)
    Points_ = mesh.points()
    Panels_ = mesh.panels()
    Chordwise_pos_ = mesh.panel_position()

    Points.extend(Points_)
    Panels.extend(Panels_)
    Chord_pos.extend(Chordwise_pos_)

# Grid data output
np.set_printoptions(precision=3)
# print('\n', 'Nº of points = ', len(Points))
# for i in range(0, len(Points)):
#     print('Point %s =' % i, Points[i])

# print('\n', 'Nº of Panels = ', len(Panels))
# for i in range(0, len(Panels)):
#     print('Panel %s' % i, Panels[i])

# Calculations
N = len(Panels)
A = np.zeros(shape=(N, N))

for i in range(0, N):
    P1, P2, P3, P4 = Panels[i][:]
    panel_pivot = Panel(P1, P2, P3, P4)
    s = panel_pivot.area()
    CP = panel_pivot.control_point()
#    print('---- Induced vel. on panel %s...' % i)
#    print(P1, P2, P3, P4)
#    print('area = ', s, 'control point = ', CP)

    for j in range(0, N):
        PP1, PP2, PP3, PP4 = Panels[j][:]
        panel = Panel(PP1, PP2, PP3, PP4)
        w = panel.induced_velocity(CP)
        A[i, j] = w
#        print('	...by panel %s = %s' % (j, w))

# Linear equation solving AX = Y

Y = np.zeros(shape=len(Panels))

for i in range(0, len(Panels)):
    Y[i] = alpha - camber_gradient_NACA4(Chord_pos[i])
    Y[i] *= -V

X = np.linalg.solve(A, Y)

print('\n', 'Matrix A =', '\n', A, '\n')
print('Y =', Y, '\n')
print('X =', X, '\n')


# gamma_plot = X
# cl_plot = (2.0 * X) / (V * c)
# cd_plot = (-2.0 * abs(X) * w * b) / (V**2 * S)
# cm_plot = - cl_plot[i] * (0.25 * c) / c

# Plotting
plt.style.use('ggplot')
for i in range(0, len(Points)):
    P = Points[i]
    plt.plot(P[0], P[1], 'ro')
plt.show()

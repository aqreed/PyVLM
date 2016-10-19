import numpy as np
import matplotlib.pyplot as plt

from pyvlm.panel import Panel
from mesh_generator import mesh

# Initial data
V = 10.0
alpha = np.deg2rad(3)

# Grid generator
c = 1  # panel chord length
b = 4  # panel span length

n = 3  # number of panels chordwise
m = 3  # number of panels spanwise
N = n * m

A = np.array([0, -b/2])
B = np.array([c, -b/2])
C = np.array([0, b/2])
D = np.array([c, b/2])

Points, Panels = mesh(A, B, C, D, n, m)

# Calculations
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
print()
print('Matrix A =')
print(A)

import numpy as np
import matplotlib.pyplot as plt

from pyvlm.panel import Panel

# Initial data
V = 10.0
alpha = np.deg2rad(3)

# Grid generator
c = 1  # panel chord length
b = 4  # panel span length

n = 1  # number of panels chordwise
m = 4  # number of panels spanwise
N = n * m  # total number of panels

x = np.linspace(0, c, n + 1)
y = np.linspace(-b/2, b/2, m + 1)

# Calculations
A = np.zeros(shape=(N, N))
k = 0
for i in range(0, n):
    for j in range(0, m):
        P1 = np.array([x[i + 1], y[j]])
        P2 = np.array([x[i], y[j]])
        P3 = np.array([x[i], y[j + 1]])
        P4 = np.array([x[i + 1], y[j + 1]])
        panel_pivot = Panel(P1, P2, P3, P4)
        s = panel_pivot.area()
        CP = panel_pivot.control_point()

        print('---- Induced vel. on panel %s...' % k)
        print(P1, P2, P3, P4)
        print('area = ', s, 'control point = ', CP)
        kk = 0
        for ii in range(0, n):
            for jj in range(0, m):
                PP1 = np.array([x[ii + 1], y[jj]])
                PP2 = np.array([x[ii], y[jj]])
                PP3 = np.array([x[ii], y[jj + 1]])
                PP4 = np.array([x[ii + 1], y[jj + 1]])
                panel = Panel(PP1, PP2, PP3, PP4)
                w = panel.induced_velocity(CP)
                print('	...by panel %s = %s' % (kk, w))
                A[k, kk] = w
                kk += 1
        k += 1

np.set_printoptions(precision=4)
print()
print('Matrix A =')
print(A)

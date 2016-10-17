import numpy as np
import matplotlib.pyplot as plt

from panel import Panel

# Initial data
V = 10.0
alpha = np.deg2rad(3)

# Grid generator
b, c = 2, 1  # size of the panel (span, chord)
P1 = np.array([c, -b/2])
P2 = np.array([0, -b/2])
P3 = np.array([0, 0])
P4 = np.array([0, b/2])
P5 = np.array([c, b/2])
P6 = np.array([c, 0])

# Calculations
panel1 = Panel(P1, P2, P3, P6)
panel2 = Panel(P6, P3, P4, P5)

S1 = panel1.area()
S2 = panel2.area()

CP1 = panel1.control_point()
CP2 = panel2.control_point()

w11 = panel1.induced_velocity(CP1)
w12 = panel1.induced_velocity(CP2)
w22 = panel2.induced_velocity(CP2)
w21 = panel2.induced_velocity(CP1)

print('control point1 =', CP1, '  area1 =', '%4.3F' % S1)
print('control point2 =', CP2, '  area2 =', '%4.3F' % S2)
print('w11_induced =', '%4.3F' % w11, '  w12_induced =', '%4.3F' % w12)
print('w21_induced =', '%4.3F' % w21, '  w22_induced =', '%4.3F' % w22)

# Linear equation solving AX = Y
A = np.array([[w11, w12], [w21, w22]])
v1 = -V * np.sin(alpha)
v2 = -V * np.sin(alpha)
Y = np.array([[v1], [v2]])
X = np.linalg.solve(A, Y)
print(X)

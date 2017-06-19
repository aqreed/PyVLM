"""
    This example shows the use the PyVLM class to first
    generate the wing planform of a Pilatus PC12 airplane
    and then apply the VLM.

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
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator

from pyvlm.vlm import PyVLM


pilatusPC12 = PyVLM()

# GEOMETRY DEFINITION #
# Parameters
c = 2.15  # root chord length
b = 16.28  # panel span length

# Left wing
A = np.array([.414, -b/2])
B = np.array([0, -1.03])
leading_edges_coord_L = [A, B]
chord_lengths_L = [1.24, c]

# Right wing
C = np.array([0, 1.03])
D = np.array([0.414, b/2])
leading_edges_coord_R = [C, D]
chord_lengths_R = [c, 1.24]

V = 140.0
alpha = np.deg2rad(0)
N = 10
X, Y = np.zeros(N-1), np.zeros(N-1)
Zl, Zd = np.zeros((N-1, N-1)), np.zeros((N-1, N-1))

for i in range(1, N):  # number of panels (chordwise)
    X[i-1] = i
    for j in range(1, N):  # number of panels (spanwise)
        pilatusPC12.add_geometry(leading_edges_coord_L, chord_lengths_L, i, j)
        pilatusPC12.add_geometry(leading_edges_coord_R, chord_lengths_R, i, j)
        l, d = pilatusPC12.vlm(V, alpha)
        Y[j-1] = j
        Zl[i-1][j-1] = l       
        Zd[i-1][j-1] = d
        print('n =%2s  m =%2s  L = %6.3f  D = %6.3f ' % (i, j, l, d))
        pilatusPC12.reset()

# Plotting
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1, projection='3d')
ax2 = fig.add_subplot(2, 1, 2, projection='3d')

X, Y = np.meshgrid(X, Y)

ax1.plot_surface(X, Y, Zl)
ax2.plot_surface(X, Y, Zd)

ax1.set_xlabel('m - spanwise')
ax1.set_ylabel('n - chordwise')
ax2.set_xlabel('m - spanwise')
ax2.set_ylabel('n - chordwise')

ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

ax1.set_zlabel('Lift')
ax2.set_zlabel('Drag')

plt.show()

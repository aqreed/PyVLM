"""
    This example shows how to use the Mesh class in order
    to generate a geometry similar to those that may define
    a lifting surface planform.

   X ^   B              This geometry is positioned in space
     |   +---+          with two chords simulating the root
     |  /    |          and tip chords, using points A and B
     | /     | b        to store their respective leading edge
     |/      |          coordinates.
     +-------+---->
     A   c         Y    With the parameters n and m the grid
                        density in the chordwise and spanwise
                        directions will be defined.
"""

import numpy as np
import matplotlib.pyplot as plt

from vlm.mesh_generator import Mesh


# GEOMETRY DEFINITION #
# Parameters
c = 1  # root chord length
b = 10  # panel span length
n = 10  # number of panels chordwise
m = 20  # number of panels spanwise

# Wing
A = np.array([0, 0])  # root chord leading edge coordinates
B = np.array([c/2, b])  # tip chord leading edge coordinates

leading_edges_coord = [A, B]
chord_lengths = [c, c/2]

mesh = Mesh(leading_edges_coord, chord_lengths, n, m)

Points = mesh.points()
Panels = mesh.panels()

# PRINTING AND PLOTTING
print('\n Point |    Coordinates ')
print('--------------------------')
for i in range(0, len(Points)):
   print('  %2s   |' % i, np.round(Points[i], 2))

print('\n Panel | Chrd % |  Span  |   Points coordinates')
print('----------------------------------------------------------------------')
for i in range(0, len(Panels)):
   print('  %3s  |  %4.1f  | %6.2f | '
         % (i, 100*Panels[i].chordwise_position,  Panels[i].span),
            np.round(Panels[i].P1, 2), np.round(Panels[i].P2, 2),
            np.round(Panels[i].P3, 2), np.round(Panels[i].P4, 2))

plt.style.use('ggplot')
plt.xlim(0, c), plt.ylim(0, b)

for i in range(0, len(Points)):
   P = Points[i]
   plt.plot(P[0], P[1], 'ro')

plt.show()

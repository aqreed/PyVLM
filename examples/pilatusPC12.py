"""
    This example shows how to use the PyVLM class in to generate the
    wing planform of a Pilatus PC12 airplane.

    The right wing will be defined using the following nomenclature while
    the left wing will be created as the specular image of the other:

    Y  ^ B +----+
       |  /      \
       | /        \
       |/          \
     A +------------+
       +-------------------->
                             X

"""

import numpy as np
import matplotlib.pyplot as plt

from vlm import PyVLM


pilatusPC12 = PyVLM()

# Geometry parameters
A = np.array([0, 1.03])  # root chord leading edge position
B = np.array([.414, 8.14])  # tip chord leading edge position

leading_edges_position = [A, B]
chord_length = [2.15, 1.24]  # root, tip

n, m = 4, 3  # number of panels (chordwise, spanwise)
pilatusPC12.add_wing(leading_edges_position, chord_length, n, m)
pilatusPC12.check_mesh(plot_mesh=True)

pilatusPC12.vlm(alpha=2, print_output=True)
alpha, CL, CD = pilatusPC12.aerodyn_forces_coeff()

plt.style.use('ggplot')

plt.subplot(1, 2, 1)
plt.title("CL")
plt.xlabel("alpha")
plt.plot(alpha, CL)

plt.subplot(1, 2, 2)
plt.title("CD")
plt.xlabel("alpha")
plt.plot(alpha, CD)

plt.show()

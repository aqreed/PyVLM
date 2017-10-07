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

from pyvlm.vlm import PyVLM


pilatusPC12 = PyVLM()

# Geometry parameters
A = np.array([0, 1.03])  # root chord leading edge position
B = np.array([.414, 8.14])  # root chord leading edge position

leading_edges_coord = [A, B]
chord_lengths = [2.15, 1.24]  # root, tip

n, m = 3, 4  # number of panels (chordwise, spanwise)
pilatusPC12.add_wing(leading_edges_coord, chord_lengths, n, m)
pilatusPC12.check_mesh()

# Flight condition parameters
V, alpha = 140.0, np.deg2rad(0)

print('\nResults for the following flight conditions:'
      '\n    V = %4.1f m/s \n    alpha = %3.1f degrees'
      % (V, np.rad2deg(alpha)))

pilatusPC12.vlm(V, alpha, True)

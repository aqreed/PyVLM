import numpy as np
import matplotlib.pyplot as plt

from geometry import norm_direction_vector, vect_perpendicular,\
                     dist_point2line

from vortices import v_induced_by_finite_vortex_line


"""
    The purpose of this test is to check the correct behaviour
    of the function that calculates the velocity induced by a
                              straight line finite vortex: it
    Y			+ P(x, y)	  must be infinite if P approaches
     ^			|			  OX at 0 < x < 1 and zero if x<1
     |			|
     +=======+--------> X
    P1(0,0)  P2(0,1)
"""

P1, P2 = np.array([0, 0]), np.array([1, 0])

plt.style.use('ggplot')

for x in np.linspace(0.75, 1.25, 5):
    y_plot = np.zeros(40)
    v_plot = np.zeros(40)

    i = 0
    for y in np.linspace(0.0001, 2, 40):
        P = np.array([x, y])
        w = v_induced_by_finite_vortex_line(P, P1, P2)
        y_plot[i] = y
        v_plot[i] = abs(w)
        i += 1

    plt.plot(y_plot, v_plot, label='x/l= %s' % x)

plt.xlabel('y/l')
plt.ylabel('induced velocity')
plt.ylim(0, 0.25)
plt.legend(loc='upper right', shadow=True)
plt.show()

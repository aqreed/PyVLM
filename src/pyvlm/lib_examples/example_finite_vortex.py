"""
    The purpose of this example is to check the behaviour of the
    function that calculates the velocity induced by a straight
                              line finite vortex and compare it to
    Y			+ P(x, y)	  the predicted result showed in [1]
     ^			|			  or [2]: as P approaches OX it must
     |			|             go to infinite for values 0 < x < 1
     +=======+--+-----> X     and to zero for values x < 1.
    P1(0,0)  P2(0,1)

    The cited bibliography is:

    [1] Cummings, R.M., Mason, W.H., Morton, S.A., McDaniel, D.R.,
        "Applied Computational Aerodynamics", Cambridge University
        Press, 1998, Chapter 6 - 31, Figure 6-17
    [2] Gandía, F., Gonzalo, J., Margot, X., Meseguer Ruiz, J.,
        "Fundamentos de los Métodos Numéricos en Aerodinámica",
        Garceta, 2013, pp. 100, Figura 3.11
"""

import numpy as np
import matplotlib.pyplot as plt

from pyvlm.vortices import v_induced_by_finite_vortex_line

P1, P2 = np.array([0, 0]), np.array([1, 0])

plt.style.use('ggplot')
n = 30  # number of y-points
for x in (0.5, 1.5, 2.0, 3.0):
    y_plot = np.zeros(n)
    v_plot = np.zeros(n)

    i = 0
    for y in np.linspace(0.0001, 2, n):
        P = np.array([x, y])
        v = v_induced_by_finite_vortex_line(P, P1, P2, gamma=4*np.pi)
        y_plot[i] = y
        v_plot[i] = abs(v)
        i += 1

    plt.plot(y_plot, v_plot, label='x/l= %s' % x)

plt.xlabel('y/l')
plt.ylabel('induced velocity')
plt.ylim(0, 1.0)
plt.legend(loc='upper right', shadow=True)
plt.show()

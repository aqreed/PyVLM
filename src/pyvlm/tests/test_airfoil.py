"""
    This tests aims to validate the NACA4 airfoil series
    class by calculating the values for upper and lower
    surfaces, camber, camber gradient and thickness for
    the following airfoils:

        - NACA 0010
        - NACA 2412
        - NACA 4424

    Any other airfoil can be calculated by adding its
    specifications to the lists below.
"""

import numpy as np
import matplotlib.pyplot as plt

from pyvlm.airfoils import NACA4


# Data is entered by lists storing the 4 digits that
# define the airfoil specs
M = [0, 2, 4]
P = [0, 4, 4]
T = [10, 12, 24]


# Plotting of AIRFOIL profile
plt.style.use('ggplot')

for m, p, t in zip(M, P, T):
    airfoil = NACA4(m, p, t)

    n = 40
    X, Y = np.zeros(n), np.zeros(n)

    for beta, i in zip(np.linspace(0, 2*np.pi, n), range(0, n)):
        x = 0.5 * (1 - np.cos(beta))  # cosine spacing

        if beta > 0 and beta < np.pi:
            X[i], Y[i] = airfoil.upper_surface(x)
        else:
            X[i], Y[i] = airfoil.lower_surface(x)

    plt.figure(1)
    plt.title('Airfoil')
    name = 'naca' + str(m) + str(p) + str(t)
    plt.xlim(0, 1), plt.ylim(-.5, .5)
    plt.plot(X, Y, '-', label=name)
    plt.legend(shadow=True)


# Plotting of CAMBER, CAMBER GRADIENT AND THICKNESS
for m, p, t in zip(M, P, T):
    airfoil = NACA4(m, p, t)

    n = 21
    X, Z, dZ, thickness = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)

    for beta, i in zip(np.linspace(0, np.pi, n), range(0, n)):
        x = 0.5 * (1 - np.cos(beta))  # cosine spacing

        X[i], thickness[i] = x, airfoil.thickness(x)
        Z[i], dZ[i] = airfoil.camber_line(x), airfoil.camber_gradient(x)

    plt.figure(2)
    name = 'naca' + str(m) + str(p) + str(t)

    plt.subplot(311), plt.ylabel('Camber')
    plt.plot(X, Z, '-', label=name)
    plt.legend(shadow=True)

    plt.subplot(312), plt.ylabel('Camber gradient')
    plt.plot(X, dZ, '-', label=name)
    plt.legend(shadow=True)

    plt.subplot(313), plt.ylabel('Thickness')
    plt.plot(X, thickness, '-', label=name)
    plt.legend(shadow=True)

plt.show()

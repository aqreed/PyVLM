"""
    This example shows the use of the airfoil classes
    lib to create and plot profiles by calculating and
    displaying the values for upper and lower surfaces,
    camber, camber gradient and thickness for the
    following cases:

        - a flat plate
        - NACA 0010
        - NACA 2412
        - NACA 4424

    Any other airfoil of the series can be calculated by adding
    its specifications to the lists M, P, T below.
"""

import numpy as np
import matplotlib.pyplot as plt

from pyvlm.airfoils import (flat_plate, NACA4)

# Plotting a flat plate
airfoil = flat_plate()

n = 10
X, Y = np.zeros(n), np.zeros(n)

for beta, i in zip(np.linspace(0, 2*np.pi, n), range(0, n)):
    x = 0.5 * (1 - np.cos(beta))  # cosine spacing

    if beta > 0 and beta < np.pi:
        X[i], Y[i] = airfoil.upper_surface(x)
    else:
        X[i], Y[i] = airfoil.lower_surface(x)

plt.style.use('ggplot')
plt.figure(1)
plt.title('Airfoil')
plt.xlim(0, 1), plt.ylim(-.5, .5)
plt.plot(X, Y, '-', label='flat plate')
plt.legend(shadow=True)


# Plotting of the NACA4 airfoil profiles
# Data stored in lists with the defining 4 digits
M = [0, 2, 4]
P = [0, 4, 4]
T = [10, 12, 24]

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

    name = 'naca' + str(m) + str(p) + str(t)
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

import numpy as np
import matplotlib.pyplot as plt


def camber_gradient_NACA4(x, M=2, P=4):
    M /= 100
    P /= 10
    if x < P:
        # z = (M/P**2) * (2*P*x - x**2)
        dz = (2*M/P**2) * (P - x)
    else:
        # z = (M / (1 - P)**2) * (1 - 2*P + 2*P*x - x**2)
        dz = (2*M / (1 - P)**2) * (P - x)
    return dz

# Plotting
plt.style.use('ggplot')
for x in np.linspace(0, 1, 21):
    dz = camber_gradient_NACA4(x)
    plt.plot(x, dz, 'ro')
    print(np.rad2deg(dz))
plt.show()

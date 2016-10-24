import numpy as np
import matplotlib.pyplot as plt

from pyvlm.airfoils import camber_gradient_NACA4

# Plotting
plt.style.use('ggplot')
for x in np.linspace(0, 1, 21):
    dz = camber_gradient_NACA4(x)
    plt.plot(x, dz, 'ro')
    print(np.rad2deg(dz))
plt.show()

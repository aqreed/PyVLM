"""
    The purpose of this test is to check the correct behaviour
    of the Panel class, calculating the cl, cd and cm of a single
    panel for alpha values ranging from -5 to 5 degrees.
"""

import numpy as np
import matplotlib.pyplot as plt

from pyvlm.panel import Panel

# Initial data
V = 10.0

# Grid generator
b, c = 1, 1  # size of the panel (span, chord)
P1, P2 = np.array([c/2, -b/2]), np.array([-c/2, -b/2])
P3, P4 = np.array([-c/2, b/2]), np.array([c/2, b/2])

# Calculations
panel = Panel(P1, P2, P3, P4)
S = panel.area()
CP = panel.control_point()
w = panel.induced_velocity(CP)
print('w_induced =', '%4.3F' % w)

# Plots initialization
alpha_plot = np.linspace(-5, 5, 21)
gamma_plot = np.zeros_like(alpha_plot)
cl_plot = np.zeros_like(alpha_plot)
cd_plot = np.zeros_like(alpha_plot)
cm_plot = np.zeros_like(alpha_plot)

for i in range(len(alpha_plot)):
    alpha = np.deg2rad(alpha_plot[i])

    # Linear equation solving AX = Y
    A = np.array([[w]])
    Y = np.array([-V * np.sin(alpha)])
    X = np.linalg.solve(A, Y)

    gamma_plot[i] = X
    cl_plot[i] = (2.0 * X) / (V * c)
    cd_plot[i] = (-2.0 * abs(X) * w * b) / (V**2 * S)
    cm_plot[i] = - cl_plot[i] * (0.25 * c) / c

# Plotting
plt.style.use('ggplot')

values2plot = [gamma_plot, cl_plot, cd_plot, cm_plot]
values2plot_names = ["$\Gamma$", 'cl', 'cd', 'cm']

fig, ax = plt.subplots(len(values2plot), 1, sharex=True)

for j in range(len(values2plot)):
    ax[j].plot(alpha_plot, values2plot[j])
    ax[j].set_ylabel(values2plot_names[j])
    if j == (len(values2plot) - 1):
        ax[j].set_xlabel('alpha')
        # ax[j].a xhline(0, color='grey')

plt.xlim(-5, 5)
plt.show()

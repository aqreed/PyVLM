import numpy as np
import matplotlib.pyplot as plt

from geometry import norm_direction_vector, vect_perpendicular,\
                     dist_point2line, area_4points

from vortices import vortex_position_in_panel,\
                     v_induced_by_horseshoe_vortex


# Initial data #
V = 10.0  # TAS
b, c = 1, 1  # size of the panel (span, chord)
P1, P2 = np.array([c/2, -b/2]), np.array([-c/2, -b/2])
P3, P4 = np.array([-c/2, b/2]), np.array([c/2, b/2])
S = area_4points(P1, P2, P3, P4)  # panel area

# Calculations #
[P, A, B, C, D] = vortex_position_in_panel(P1, P2, P3, P4)
w = v_induced_by_horseshoe_vortex(P, A, B, C, D)
print('w_induced =', '%4.3F' % w)

# Plots initialization #
alpha_plot = np.linspace(-5, 5, 21)
gamma_plot = np.zeros_like(alpha_plot)
cl_plot = np.zeros_like(alpha_plot)
cd_plot = np.zeros_like(alpha_plot)
cm_plot = np.zeros_like(alpha_plot)

for i in range(len(alpha_plot)):
    alpha = np.deg2rad(alpha_plot[i])

    # Linear equation solving AX = Y
    a = np.array([[w]])
    y = np.array([-V * np.sin(alpha)])
    x = np.linalg.solve(a, y)

    gamma_plot[i] = x
    cl_plot[i] = (2.0 * x) / (V * c)
    cd_plot[i] = (-2.0 * abs(x) * w * b) / (V**2 * S)
    cm_plot[i] = - cl_plot[i] * (0.25 * c) / c

# Plotting #
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

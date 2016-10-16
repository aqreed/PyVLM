import numpy as np
import matplotlib.pyplot as plt

from panel import Panel

# Initial data
V = 10.0
alpha = np.deg2rad(3)

# Grid generator
c = 1  # panel chord length
b = 4  # panel span length

n = 1  # number of panels chordwise
m = 4  # number of panels spanwise
N = n * m  # total number of panels

x = np.linspace(0, c, n + 1)
y = np.linspace(-b/2, b/2, m + 1)
#xx, yy = np.meshgrid(x, y, sparse=True)

A = np.zeros(shape=(N,N))
k = 0
for i in range(0, n):
    for j in range(0, m):
        P1 = np.array([x[i + 1], y[j]])
        P2 = np.array([x[i], y[j]])
        P3 = np.array([x[i], y[j + 1]])
        P4 = np.array([x[i + 1], y[j + 1]])
        panel_pivot = Panel(P1, P2, P3, P4)
        s = panel_pivot.area()
        CP = panel_pivot.control_point()
#        print(P1, P2, P3, P4)
        print('-------------')
#        print('area = ', s, 'control point = ', CP)
        kk = 0
        for ii in range(0, n):            
            for jj in range(0, m):
                PP1 = np.array([x[ii + 1], y[jj]])
                PP2 = np.array([x[ii], y[jj]])
                PP3 = np.array([x[ii], y[jj + 1]])
                PP4 = np.array([x[ii + 1], y[jj + 1]])
                panel = Panel(PP1, PP2, PP3, PP4)
                w = panel.induced_velocity(CP)
                #print('---------(ii, jj) =', ii, jj)
                print('%5.4F' % w)
                A[k, kk] = w
                kk += 1
        k += 1

np.set_printoptions(precision=4)
print(A)

# Calculations
#panel1 = Panel(P1, P2, P3, P6)
#panel2 = Panel(P6, P3, P4, P5)
#S1 = panel1.area()
#S2 = panel2.area()
#CP1 = panel1.control_point()
#CP2 = panel2.control_point()
#print('control point1 =', CP1)
#print('control point2 =', CP2)
#w11 = panel1.induced_velocity(CP1)
#w12 = panel1.induced_velocity(CP2)

#w22 = panel2.induced_velocity(CP2)
#w21 = panel2.induced_velocity(CP1)

#print('area1 =', '%4.3F' % S1, 'w11_induced =', '%4.3F' % w11,
#      'w12_induced =', '%4.3F' % w12)
#print('area2 =', '%4.3F' % S2, 'w22_induced =', '%4.3F' % w22,
#      'w21_induced =', '%4.3F' % w21)

# # Plots initialization
# alpha_plot = np.linspace(-5, 5, 21)
# gamma_plot = np.zeros_like(alpha_plot)
# cl_plot = np.zeros_like(alpha_plot)
# cd_plot = np.zeros_like(alpha_plot)
# cm_plot = np.zeros_like(alpha_plot)

# for i in range(len(alpha_plot)):
#     alpha = np.deg2rad(alpha_plot[i])

#     gamma_plot[i] = x
#     cl_plot[i] = (2.0 * x) / (V * c)
#     cd_plot[i] = (-2.0 * abs(x) * w * b) / (V**2 * S)
#     cm_plot[i] = - cl_plot[i] * (0.25 * c) / c

# Linear equation solving AX = Y
#A = np.array([[w11, w12],[w21, w22]])
#v1 = -V * np.sin(alpha)
#v2 = -V * np.sin(alpha)
#Y = np.array([[v1], [v2]])
#X = np.linalg.solve(A, Y)
#print(X)
# # Plotting
# plt.style.use('ggplot')

# values2plot = [gamma_plot, cl_plot, cd_plot, cm_plot]
# values2plot_names = ["$\Gamma$", 'cl', 'cd', 'cm']

# fig, ax = plt.subplots(len(values2plot), 1, sharex=True)

# for j in range(len(values2plot)):
#     ax[j].plot(alpha_plot, values2plot[j])
#     ax[j].set_ylabel(values2plot_names[j])
#     if j == (len(values2plot) - 1):
#         ax[j].set_xlabel('alpha')
#         # ax[j].a xhline(0, color='grey')

# plt.xlim(-5, 5)
# plt.show()

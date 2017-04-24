from core import *

N = int(4096*0.5)
M_T = 5e10/1e7
M = 2*M_T/N
G = 44.97
diameter = 100#55
epsilon = diameter*0.001

system = simple_disk(N, diameter)

#system = np.zeros((3, N))
#r = np.random.randn(N)
#r = 55*r/max(r)
#theta = np.random.random(N)*np.pi*2
#
#x = r*np.cos(theta)
#y = r*np.sin(theta)
#z = 3*np.random.randn(N)
#
#pos = abs(r).argsort()
#pos_z = abs(z).argsort()[::-1]
#z_new = np.zeros_like(z)
#for i in range(N):
#    temp = z[pos_z[i]]
#    if abs(temp) > 5:
#        temp = 5*temp/abs(temp)
#    z_new[pos[i]] = np.random.normal(temp)
#system[:] = x, y, z_new

speeds = speeds_generator(system, G, M)

np.savetxt("0_speed.dat", speeds.T, fmt="%f")
np.savetxt("0_instant.dat", system.T, fmt="%f")
#sim = simulation(M, G, epsilon, tolerance = 0.5, pos = system, speeds = speeds)
#sim.start(0, 2.5, 0.01)
#
#data = read_output()
#
#"""
#plotting
#"""
#import numpy as np
#from glob import glob
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib.animation import FuncAnimation
#
#
#fig = plt.figure()
#ax = fig.gca(projection='3d')
#ax.set_aspect("equal")
#N_half = int(N/2)
#plot1 = ax.plot([], [], [], "o", ms=0.5, c="g", alpha = 0.5)[0]
#plot2 = ax.plot([],[],[], "o", ms=0.5, c="b", alpha = 0.5)[0]
#ax.set_xlabel("$x$ kpc")
#ax.set_ylabel("$y$ kpc")
#ax.set_zlabel("$z$ kpc")
#
#def update(i):
#    temp = data[i]
#    plot1.set_data(temp[:N_half,0], temp[:N_half,1])
#    plot1.set_3d_properties(temp[:N_half, 2])
#    plot2.set_data(temp[N_half:,0], temp[N_half:,1])
#    plot2.set_3d_properties(temp[N_half:, 2])
#
#min_value, max_value = -75, 75
#ax.set_xlim(min_value, max_value)
#ax.set_ylim(min_value, max_value)
#ax.set_zlim(min_value, max_value)
#fig.tight_layout()
#ani = FuncAnimation(fig, update, frames=len(data), interval=10)
##ani.save("animate.mp4", writer='ffmpeg', fps=24, dpi=72)
#plt.show()


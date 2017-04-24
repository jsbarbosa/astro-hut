from core import *

N = 4096
M_T = 5e10/1e7
M = 2.0*M_T/N #two galaxies
G = 44.97
epsilon = 0.1

N_first = int(0.5*N)
N_second = int(N-N_first)
theta = np.pi/4

rotx, roty, rotz = rotation_matrixes(theta)

galaxy1 = galaxy(N_first, 55)
galaxy2 = galaxy(N_second, 55)

speeds1 = speeds_generator(galaxy1, G, M)
speeds2 = speeds_generator(galaxy2, G, M)

galaxy2.positions = np.dot(rotx, galaxy2.positions)
speeds2 = np.dot(rotx, speeds2)

system = np.zeros((3, N))
system[:, :N_first] = galaxy1.positions
system[:, N_first:] = galaxy2.positions + 2*55
speeds = np.zeros_like(system)

speeds[:, :N_first] = speeds1
speeds[:, N_first:] = speeds2

sim = simulation(M, G, epsilon, tolerance = 1.0, pos = system, speeds = speeds)
sim.start(0, 1.0, 0.001)

data = read_output()

"""
plotting
"""
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")
plot1 = ax.plot([], [], [], "o", ms=0.5, c="g", alpha = 0.5)[0]
plot2 = ax.plot([],[],[], "o", ms=0.5, c="b", alpha = 0.5)[0]
ax.set_xlabel("$x$ kpc")
ax.set_ylabel("$y$ kpc")
ax.set_zlabel("$z$ kpc")

def update(i):
    temp = data[i]
    plot1.set_data(temp[:N_first,0], temp[:N_first,1])
    plot1.set_3d_properties(temp[:N_first, 2])
    plot2.set_data(temp[N_first:,0], temp[N_first:,1])
    plot2.set_3d_properties(temp[N_first:, 2])

min_value, max_value = -150, 150
ax.set_xlim(min_value, max_value)
ax.set_ylim(min_value, max_value)
ax.set_zlim(min_value, max_value)
fig.tight_layout()
ani = FuncAnimation(fig, update, frames=len(data), interval=0.1)
#ani.save("animate.mp4", writer='ffmpeg', fps=24, dpi=72)
plt.show()

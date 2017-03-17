import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")
x, y, z = np.genfromtxt("0_instant.dat").T
N = int(len(x)/2)
plot1 = ax.plot([], [], [], "o", ms=1, c="g")[0]
plot2 = ax.plot([],[],[], "o", ms=1, c="b")[0]
text = ax.text(0,0,0, "", color = "r")
ax.set_xlabel("$x$ (kpc)" )
ax.set_ylabel("$y$ (kpc)")
ax.set_zlabel("$z$ (kpc)")

frames = len(glob("*.dat"))
ratio = int(len(glob("*.dat"))/frames)

data = [np.genfromtxt("%d_instant.dat"%i) for i in range(0, frames, ratio)]


def update(i):
    temp = data[i]
    plot1.set_data(temp[:N,0], temp[:N,1])
    plot1.set_3d_properties(temp[:N, 2])
    plot2.set_data(temp[N:,0], temp[N:,1])
    plot2.set_3d_properties(temp[N:, 2])

min_value, max_value = -100, 200
ax.set_xlim(min_value, max_value)
ax.set_ylim(min_value, max_value)
ax.set_zlim(min_value, max_value)
fig.tight_layout()
ani = FuncAnimation(fig, update, frames=int(frames/ratio), interval=100)
ani.save("animate.gif", writer='imagemagick', dpi=72)
#plt.show()

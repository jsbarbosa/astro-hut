import numpy as np
from core import box, limits
from glob import glob
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation


prefix = "boxes_data"
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_axis_off()
#ax.set_facecolor("none")
x, y, z = np.genfromtxt("%s/0_instant.dat"%prefix).T
N = int(len(x)/2)
min_value, max_value = -100, 100
frames = len(glob("%s/*.dat"%prefix))
ratio = 1

data = [np.genfromtxt("%s/%d_instant.dat"%(prefix,i)) for i in range(0, frames, ratio)]
mass = 1
tolerance = 1
min_value, max_value = -100, 200
def update(i):
    if i != 0:
        ax.clear()
    x = data[i]
    x0, r0 = limits(x.T)
    ax.plot(x[:N, 0], x[:N, 1], x[:N, 2], "o", c="g", ms = 1)
    ax.plot(x[N:, 0], x[N:, 1], x[N:, 2], "o", c="b", ms = 1)
    boxes = box(x.T, x0, r0, [], True)
    tree = boxes.tree
    for box_ in tree:
        box_.plot(ax, c = "r", a = 0.3, child_only=False)
    ax.set_xlim(min_value, max_value)
    ax.set_ylim(min_value, max_value)
    ax.set_zlim(min_value, max_value)
    ax.set_xlabel("$x$ kpc")
    ax.set_ylabel("$y$ kpc")
    ax.set_zlabel("$z$ kpc")
    ax.set_aspect("equal")
#    ax.set_facecolor("none")
    ax.set_axis_off()

fig.tight_layout()
ani = FuncAnimation(fig, update, frames=int(frames/ratio), interval=100)
ani.save("boxes.gif", writer='imagemagick', dpi=100)
#plt.show()

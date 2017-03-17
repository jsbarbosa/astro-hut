import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#plt.style.use('dark_background')
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")
#ax.set_axis_off()
x, y, z = np.genfromtxt("0_instant.dat").T
N = int(len(x)/2)
plot1 = ax.plot([], [], [], "o", ms=0.5, c="g", alpha = 0.5)[0]
plot2 = ax.plot([],[],[], "o", ms=0.5, c="b", alpha = 0.5)[0]
text = ax.text(0,0,0, "", color = "r")
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_zlabel("$z$")

frames = len(glob("*_instant.dat"))
ratio = 1

data = [np.genfromtxt("%d_instant.dat"%i) for i in range(0, frames, ratio)]


def update(i):
    temp = data[i]
    plot1.set_data(temp[:N,0], temp[:N,1])
    plot1.set_3d_properties(temp[:N, 2])
    plot2.set_data(temp[N:,0], temp[N:,1])
    plot2.set_3d_properties(temp[N:, 2])
#    text.set_text("%d"%i)
#    ax.view_init(0, i*360/frames)

min_value, max_value = -250, 250
ax.set_xlim(min_value, max_value)
ax.set_ylim(min_value, max_value)
ax.set_zlim(min_value, max_value)
fig.tight_layout()
ani = FuncAnimation(fig, update, frames=int(frames/ratio), interval=0.1)
#ani.save("animate.gif", writer='imagemagick', dpi=72)
plt.show()

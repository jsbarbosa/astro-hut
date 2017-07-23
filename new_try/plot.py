import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

BOXES = True

files = glob("*.dat")
Nt = len(files)
N = 100
cornersX = np.zeros((Nt, N, 5))
cornersY = np.zeros((Nt, N, 5))

pointsX = np.zeros((Nt, N))
pointsY = np.zeros((Nt, N))

for i in range(Nt):
    data = np.genfromtxt("single_boxes%d.dat"%i)
    cornersX[i] = data[:, 2:7]
    cornersY[i] = data[:, 7:]
    pointsX[i] = data[:, 0]
    pointsY[i] = data[:, 1]

fig = plt.figure()

squares = []
points = []
for j in range(data.shape[0]):
    plot = plt.plot([], [])[0]
    if BOXES:
        squares.append(plot)
    points.append(plt.plot([], [], "o", alpha = 0.5, c = plot.get_color())[0])

plt.xlim(cornersX.min(), cornersX.max())
plt.ylim(cornersY.min(), cornersY.max())


def animate(i):
    for j in range(data.shape[0]):
        if BOXES:
            squares[j].set_data(cornersX[i][j], cornersY[i][j])
        points[j].set_data([pointsX[i, j]], [pointsY[i, j]])

    return tuple(squares + points)

ani = FuncAnimation(fig, animate, frames=Nt, interval=25)
ani.save("aniBoxes.gif", writer="imagemagick")
plt.show()

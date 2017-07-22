import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("single_boxes.dat")

def drawSquare(corners):
    sx = corners[:5]
    sy = corners[5:]
    return sx, sy

for i in range(data.shape[0]):
    sx, sy = drawSquare(data[i, 2:])
    plt.plot(sx, sy)
    plt.scatter([data[i, 0]], [data[i, 1]], alpha = 0.5)

plt.axes().set_aspect('equal')#, 'datalim')
plt.savefig("single_boxes.png")
# plt.show()

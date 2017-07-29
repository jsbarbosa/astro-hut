import numpy as np
from astrohut import *
import matplotlib.pyplot as plt

def gaussian(N, G = 1.0, mass_unit = 1.0):
    data = np.zeros((N, 4))
    data[:, 0] = x = np.random.normal(size=N)
    data[:, 1] = y = np.random.normal(size=N)

    r = (x**2 + y**2)**0.5
    theta = np.arctan2(y, x)

    speeds = np.zeros((N, 2))

    for i in range(N):
        n = len(np.where(r < r[i])[0])
        mag = np.sqrt(G*mass_unit*n/r[i])
        vx = -r[i]*np.sin(theta[i])
        vy = r[i]*np.cos(theta[i])
        mag_ = (vx**2 + vy**2)**0.5
        vx *= mag/mag_
        vy *= mag/mag_
        speeds[i, 0] = vx
        speeds[i, 1] = vy

    data[:, 2:] = speeds

    return data

# data1 = gaussian(100)
# data2 = gaussian(100)
#
# data2[:, 0] = data2[:, 0] + 5
# data2[:, 1] = data2[:, 1] + 5


# system = np.zeros((200, 4))
#
# system[:100] = data1
# system[100:] = data2

sim = Simulation("relaxed.csv", tau = 0.5, read_kwargs={"delimiter" : ","})

sim.start(1e4, 1, save_to_array_every = 100)
ani = sim.makeAnimation()
plt.show()

import numpy as np
import astrohut as ah
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

G = 1.0
m = 1.0

pos = np.random.normal(size=(10, 3))
speeds = ah.generateSpeeds(pos, G, m)

system = ah.createArray(pos, speeds)

sim = ah.Simulation(system, dim = 3, dt = 1e-3)

sim.start(1000, save_to_array_every = 25)

ani = sim.makeAnimation(boxed = True)

ani.save("test3d.gif", writer="imagemagick", dpi = 72, fps = 12)
# plt.show()

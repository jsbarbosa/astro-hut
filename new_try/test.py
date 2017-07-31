import numpy as np
import astrohut as ah
import matplotlib.pyplot as plt

temp = np.random.random((10, 6))
Nbodies, bodies = ah.fromArrayToBodies(temp)

sim = ah.Simulation(np.random.random((100, 6)))
sim.start(1e2, save_to_array_every = 10)

ani = sim.makeAnimation(color = "b", boxed = True)
plt.show()

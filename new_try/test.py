import numpy as np
import astrohut as ah
import matplotlib.pyplot as plt

sim = ah.Simulation(np.random.random((100, 6)), tau = 1.0, epsilon = 1e-1)

sim.start(1e4, save_to_array_every = 10, save_to_file_every = 0)

# ani = sim.makeAnimation(color = "k", boxed = True)

plt.plot(sim.getEnergies())

plt.show()

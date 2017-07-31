import numpy as np
import astrohut as ah
import matplotlib.pyplot as plt

from astrohut.constants import LIB

temp = np.random.random((10, 6))
Nbodies, bodies = ah.fromArrayToBodies(temp)

node = LIB.initFirstNode2d(Nbodies, bodies)

print(node.contents)
# ah.fromNodeToArray(node)
#
# sim = ah.Simulation(np.random.random((100, 6)))
# sim.start(1e2, save_to_array_every = 10, save_to_file_every = 10)
#
# ani = sim.makeAnimation()
# plt.show()

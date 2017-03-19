from core import *
import numpy as np

N = 4096
M = 2.0*1000/N
G = 44.97
diameter = 20
arms = 2
epsilon = diameter*0.001

system = np.zeros((3, N))
speeds = np.zeros((3, N))
system[0, :] = np.random.random(N)#0, 0, 0
system[1, :] = np.random.random(N)
system[2, :] = np.random.random(N)
#system[:, 2] = 0.25, 0.25, 0.25
sim = simulation(M, G, epsilon, pos = system, speeds = speeds)
sim.start(0, 1.0, 0.01)

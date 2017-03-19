from core import *
import numpy as np

N = 1000
M = 2.0*1000/N
G = 44.97
diameter = 20
arms = 2
epsilon = diameter*0.001

system = np.zeros((3, N))
speeds = np.zeros((3, N))
system[:,-1] = 0.5
sim = simulation(M, G, epsilon, pos = system, speeds = speeds)
sim.box()

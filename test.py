from core import *

N = 4096
M_T = 5e10/1e7
M = 2.0*M_T/N #two galaxies
G = 44.97
epsilon = 0.1

system, speeds = example(N, M, G, epsilon)

sim = simulation(M, G, epsilon, tolerance = 1.0, pos = system, speeds = speeds)
sim.start(0, 0.1, 0.01)

data = read_output()
animate(data, N, name = "animation_approx.mp4", show = False, save = True)

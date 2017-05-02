from astrohut import *

N = 4096
M_T = 5e10/1e7
M = 2.0*M_T/N #two galaxies
G = 44.97
epsilon = 0.01

system, speeds = example(N, M, G)

sim = simulation(M, G, epsilon, tolerance = 1.0, pos = system, speeds = speeds)
sim.start(0, 10.0, 0.01)

data = read_output()
N_data = len(data)
step = 1
if N_data > 1000:
    step = int(N_data/1000)
    
ani = animate(data, N)
ani.save("approx.mp4", writer = "ffmpeg", fps = 24, dpi = 120)

sim.tolerance = 0

sim.start(0, 10.00, 0.01)

data = read_output()
N_data = len(data)
step = 1
if N_data > 1000:
    step = int(N_data/1000)
    
ani = animate(data, N)
ani.save("exact.mp4", writer = "ffmpeg", fps = 24, dpi = 120)

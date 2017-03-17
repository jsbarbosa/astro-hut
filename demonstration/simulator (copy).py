import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from core import *

def galaxy(N, size, arms = 5):
    a = 0.4
    b = 0.7
    n = int(N/arms)
    t = np.random.randn(n)
    excess = np.where(t>2)[0]
    t[excess] = np.random.rand(len(excess))/1000
    x = np.array([0])
    y = np.array([0])

    for i in range(arms):
        xt = a*np.exp(b*t)*np.cos(t+2*i*np.pi/arms) + np.random.normal(0, a*0.2, n)
        yt = a*np.exp(b*t)*np.sin(t+2*i*np.pi/arms) + np.random.normal(0, a*0.2, n)
        x = np.hstack((x, xt))
        y = np.hstack((y, yt))
            
    rank = max(x) - min(x)
    return x[1:]*size/rank, y[1:]*size/rank

G = 44.97
N = 1000
mass = 2.0*1000/N
diameter = 20
arms = 5
epsilon = diameter*0.001

N_half = int(0.5*N)
theta = np.pi/4
rotx, roty, rotz = rotation_matrixes(theta)
x1, y1 = galaxy(N_half, diameter, arms=arms)
x2, y2 = galaxy(N_half, diameter, arms=arms)
z1 = np.random.randn(N_half)*0.01*diameter
z2 = np.random.randn(N_half)*0.01*diameter
   
galaxy1 = np.zeros((3, N_half))
galaxy2 = np.zeros((3, N_half))
galaxy1[:] = x1, y1, z1
galaxy2[:] = x2, y2, z2
       
center1 = np.mean(galaxy1, axis = 1)
distances1 = np.array([galaxy1[i] - center1[i] for i in range(3)])
speeds1 = speeds_generator(distances1, G, mass)

center2 = np.mean(galaxy2, axis = 1)
distances2 = np.array([galaxy2[i] - center2[i] for i in range(3)])
speeds2 = speeds_generator(distances2, G, mass)

galaxy2 = np.dot(rotx, galaxy2)
speeds2 = np.dot(rotx, speeds2)       
       
system = np.zeros((3, N))
system[:, :N_half] = galaxy1 - 0.5*diameter
system[:, N_half:] = galaxy2 + 0.5*diameter 
speeds = np.zeros_like(system)

speeds[:, :N_half] = speeds1
speeds[:, N_half:] = speeds2

density = mass/np.sqrt(epsilon)**3
dt = round(np.sqrt(1/(G*density)), 2)
dt = 3**-0.5/np.max(speeds)

print(dt)
n = solver(system, speeds, N, 0.002, 0.001, G, filename='exact/', tolerance = 0, mass = mass, epsilon = epsilon)

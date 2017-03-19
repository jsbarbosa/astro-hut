from core import *

N = 1000
M = 2.0*1000/N
G = 44.97
diameter = 20
arms = 5
epsilon = diameter*0.001

def galaxy(N_, size, arms = 5):
    """
    Construye una espiral dos dimensional con arms cantidad de brazos, usando N/arms puntos en cada uno.
    Normaliza el tamano usando size.
    """
    a = 0.4
    b = 0.7
    N = int(N_/(arms+1))
    t = np.random.randn(N) + 0.5
#    t = 5*(np.random.random(N) - 0.5)
    excess = np.where(t>2)[0]
    t[excess] = np.random.rand(len(excess))/1000
    x = np.array([0])
    y = np.array([0])
    
    for i in range(arms):   
        xv = a*np.exp(b*t)*np.cos(t+2*i*np.pi/arms)
        yv = a*np.exp(b*t)*np.sin(t+2*i*np.pi/arms)
        r = np.sqrt(xv**2 + yv**2)
        u = 0.1*abs(np.log(r))#0.05*np.exp(r)/r
        u = 0.04*np.exp(r)
        xt = xv + np.random.normal(0, u, N)
        yt = yv + np.random.normal(0, u, N)
            
        x = np.hstack((x, xt))
        y = np.hstack((y, yt))

    r = np.random.random(N)*0.15*arms
    theta = np.random.random(N)*2*np.pi
    xt = r*np.cos(theta)
    yt = r*np.sin(theta)
    x = np.hstack((x, xt))
    y = np.hstack((y, yt))
    must_have = N_ - x.shape[0] + 1
    if must_have != 0:
        xt = np.random.random(must_have)*0.1
        yt = np.random.random(must_have)*0.1
        x = np.hstack((x, xt))
        y = np.hstack((y, yt))
    rank = max(x) - min(x)
    return x[1:]*size/rank, y[1:]*size/rank

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
distances1 = galaxy1
distances1 = np.array([galaxy1[i] - center1[i] for i in range(3)])
speeds1 = speeds_generator(distances1, G, M)

center2 = np.mean(galaxy2, axis = 1)
distances2 = np.array([galaxy2[i] - center2[i] for i in range(3)])
speeds2 = speeds_generator(distances2, G, M)

galaxy2 = np.dot(rotx, galaxy2)
speeds2 = np.dot(rotx, speeds2)       
       
system = np.zeros((3, N))
system[:, :N_half] = galaxy1 - diameter
system[:, N_half:] = galaxy2 + diameter 
speeds = np.zeros_like(system)

speeds[:, :N_half] = speeds1
speeds[:, N_half:] = speeds2

sim = simulation(M, G, epsilon, tolerance = 0, pos = system, speeds = speeds)#, pos_name = "pos_init.txt", speed_name = "speed_init.txt")
sim.start(0, 2.5, 0.01)

data = read_output()

"""
plotting
"""
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")
N_half = int(N/2)
plot1 = ax.plot([], [], [], "o", ms=0.5, c="g", alpha = 0.5)[0]
plot2 = ax.plot([],[],[], "o", ms=0.5, c="b", alpha = 0.5)[0]
ax.set_xlabel("$x$ kpc")
ax.set_ylabel("$y$ kpc")
ax.set_zlabel("$z$ kpc")

def update(i):
    temp = data[i]
    plot1.set_data(temp[:N_half,0], temp[:N_half,1])
    plot1.set_3d_properties(temp[:N_half, 2])
    plot2.set_data(temp[N_half:,0], temp[N_half:,1])
    plot2.set_3d_properties(temp[N_half:, 2])

min_value, max_value = -50, 50
ax.set_xlim(min_value, max_value)
ax.set_ylim(min_value, max_value)
ax.set_zlim(min_value, max_value)
fig.tight_layout()
ani = FuncAnimation(fig, update, frames=len(data), interval=10)
#ani.save("animate.gif", writer='imagemagick', dpi=72)
plt.show()


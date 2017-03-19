import os
import ctypes
import numpy as np
from glob import glob

cwd = os.getcwd()
wd = '%s/bruteforce.so'%cwd
lib = ctypes.CDLL(wd)#'/home/juan/Documents/astro-hut/c_build/bruteforce.so')

"""
argtypes
"""
lib.init_conditions.argtypes = (ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
lib.solver.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_char_p)
"""
"""

class simulation:
    def __init__(self, M, G, epsilon, pos = None, speeds = None, pos_name = None, speed_name = None, output="Data/"):
        self.M = M
        self.G = G
        self.epsilon = epsilon
        if pos_name != None and speed_name != None:
            self.pos = np.genfromtxt(pos_name).T
            self.speeds = np.genfromtxt(speed_name).T
        elif type(pos) == np.ndarray and type(speeds) == np.ndarray:
            self.pos = pos
            self.speeds = speeds
        else:
            raise("simulation init failed.")
        self.N = self.pos.shape[1]

        """
        c init
        """
        lib.init_conditions(self.N, self.M, self.G, self.epsilon)
        c_double_p = ctypes.POINTER(ctypes.c_double)
        lib.init_from_ram.argtypes = (c_double_p, c_double_p, c_double_p,
                            c_double_p, c_double_p, c_double_p)

        x = self.pos[0].ctypes.data_as(c_double_p)
        y = self.pos[1].ctypes.data_as(c_double_p)
        z = self.pos[2].ctypes.data_as(c_double_p)
        vx = self.speeds[0].ctypes.data_as(c_double_p)
        vy = self.speeds[1].ctypes.data_as(c_double_p)
        vz = self.speeds[2].ctypes.data_as(c_double_p)
        lib.init_from_ram(x, y, z, vx, vy, vz)

        self.output = output
        
        if os.path.isdir(self.output):
            files = glob("%s%s"%(self.output, "*.dat"))
            list(map(os.remove, files))
        else:
            os.makedirs(self.output)

    def start(self, t0, tmax, dt):
        lib.solver(t0, tmax, dt, self.output.encode())
        del self

    def box(self):
        lib.temp()

def read_output(output="Data/"):
    files = glob("%s*_instant.dat"%output)
    return [np.genfromtxt("%s%d_instant.dat"%(output, i)) for i in range(len(files))]

def speeds_generator(distances, G, m = 1):
    r = np.sqrt(np.sum(distances**2, axis=0))
    theta = np.arctan2(distances[1, :], distances[0, :])
    n = len(r)
    s = np.zeros((3, n))
    for i in range(n):
        pos = np.where(r < r[i])[0]
        M = m*pos.shape[0]
        theta = np.arctan2(distances[1, i], distances[0, i])
        if M != 0:
            mag = np.sqrt(G*M/r[i])
            s[:2, i] = -r[i]*np.sin(theta), r[i]*np.cos(theta)
            s[:2, i] *= 1/np.sqrt(np.dot(s[:, i], s[:, i]))
            s[:2, i] *= mag
            s[2, i] = 20*(np.random.random() - 0.5)
        else:
            s[:, i] = 0
    return s

def rotation_matrixes(theta):
    x = np.array([[1, 0, 0], [0, np.cos(theta), - np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    y = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    z = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    return x, y, z
    

import ctypes
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ctypes import POINTER, c_char_p, c_int, pointer

from .constants import DOUBLE, LIB
from .structs2d import body2d, node2d
from .core import fromArrayToBodies, fromBodiesToArray, fromNodeToArray

LIB.malloc.restype = ctypes.c_void_p
LIB.calloc.restype = ctypes.c_void_p

LIB.setConstants.argtypes = DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE

LIB.loadFile2d.argtypes = c_char_p, c_char_p, c_int
LIB.loadFile2d.restype = POINTER(body2d)

LIB.initFirstNode2d.argtypes = c_int, POINTER(body2d)
LIB.initFirstNode2d.restype = POINTER(node2d)

LIB.solveInterval2d.argtypes = c_int, POINTER(POINTER(node2d)), POINTER(body2d)
LIB.solveInterval2d.restype = POINTER(body2d)

LIB.solveInstant2d.argtypes = POINTER(POINTER(node2d)), POINTER(body2d)
LIB.solveInstant2d.restype = POINTER(body2d)

LIB.setPrint.argtypes = c_char_p, c_int

LIB.omp_set_num_threads.argtypes = c_int,

def __setPrint__(prefix = "", frames_every = 0):
    LIB.setPrint(prefix.encode(), frames_every)

def __setConstants__(mass_unit, G, tau, dt, epsilon):
    LIB.setConstants(mass_unit, G, tau, dt, epsilon)

class Simulation():
    def __init__(self, data, dim = 2, mass_unit = 1.0, G = 1.0, tau = 0.5, dt = 1e-4, epsilon = 1e-4,
                read_kwargs = {}):
        self.data = data
        self.dim = dim
        self.mass_unit = mass_unit
        self.G = G
        self.tau = tau
        self.dt = dt
        self.epsilon = epsilon

        if type(self.data) is str:
            self.data = np.genfromtxt(data, **read_kwargs)

        self.Nbodies, self.bodies = fromArrayToBodies(self.data, self.dim)
        self.node = None
        self.results_nodes = None
        self.results_bodies = None
        self.setConstants()

        self.file_number = 0

    def setConstants(self):
        __setConstants__(self.mass_unit, self.G, self.tau, self.dt, self.epsilon)

    def setFilePrefix(self, prefix):
        __setPrint__(prefix)

    def start(self, Ninstants, threads = 0, save_to_file_every = 0, save_to_array_every = 1):
        if type(self.node) == type(None):
            self.node = LIB.initFirstNode2d(self.Nbodies, self.bodies)

        if threads > 0:
            LIB.omp_set_num_threads(threads)

        Ninstants = int(Ninstants)
        new = LIB.solveInstant2d(ctypes.byref(self.node), self.bodies)
        array_number = 0

        if save_to_array_every != 0:
            instant_points = np.zeros((Ninstants//save_to_array_every, self.Nbodies, 3*self.dim))
            instant_nodes = np.zeros((Ninstants//save_to_array_every, self.Nbodies, 6))

        for i in range(Ninstants):
            new2 = LIB.solveInstant2d(ctypes.byref(self.node), new)

            if save_to_file_every > 0:
                if i%save_to_file_every == 0:
                    LIB.printInstant2d(self.node, new, self.file_number)
                    self.file_number += 1

            if save_to_array_every > 0:
                if i%save_to_array_every == 0:
                    instant_points[array_number] = fromBodiesToArray(new, self.Nbodies)
                    array_number += 1

            LIB.swapBody2d(ctypes.byref(new2), ctypes.byref(new))
            LIB.free(new2)

        if save_to_array_every != 0:
            if type(self.results) == type(None):
                self.results = instant_points
            else:
                self.results = np.vstack((self.results, instant_points))
            return self.results
        else:
            return fromBodiesToArray(new, self.Nbodies)

    def animate(self, i, values, points):
        for j in range(len(points)):
            body = values[i, j]
            points[j].set_data(body[0], body[1])
        return points

    def makeAnimation(self, data = None):
        if type(data) == type(None):
            if type(self.results) == type(None):
                self.start(100)
            else:
                data = self.results

        Ninstants = data.shape[0]

        fig = plt.figure()

        points = [plt.plot([], [], "o", alpha = 0.5)[0] for i in range(self.Nbodies)]

        plt.xlim(data[:, :, 0].min(), data[:, :, 0].max())
        plt.ylim(data[:, :, 1].min(), data[:, :, 1].max())

        ani = FuncAnimation(fig, self.animate, frames = Ninstants,
                            interval = 25, fargs=(data, points))

        return ani

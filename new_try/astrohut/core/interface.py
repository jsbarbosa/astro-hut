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
            instant_points = np.zeros((Ninstants//save_to_array_every, self.Nbodies, 3*self.dim + 1))
            instant_nodes = np.zeros((Ninstants//save_to_array_every, self.Nbodies, 12))

        for i in range(Ninstants):
            new2 = LIB.solveInstant2d(ctypes.byref(self.node), new)

            if save_to_file_every > 0:
                if i%save_to_file_every == 0:
                    LIB.printInstant2d(self.node, new, self.file_number)
                    self.file_number += 1

            if save_to_array_every > 0:
                if i%save_to_array_every == 0:
                    instant_points[array_number] = fromBodiesToArray(new, self.Nbodies)
                    instant_nodes[array_number] = fromNodeToArray(self.node, self.dim)
                    array_number += 1

            LIB.swapBody2d(ctypes.byref(new2), ctypes.byref(new))
            LIB.free(new2)

        if save_to_array_every != 0:
            if type(self.results_bodies) == type(None):
                self.results_bodies = instant_points
            if type(self.results_nodes) == type(None):
                self.results_nodes = instant_nodes
            else:
                self.results_bodies = np.vstack((self.results_bodies, instant_points))
                self.results_nodes = np.vstack((self.results_nodes, instant_nodes))
            return self.results_bodies, self.results_nodes
        else:
            return fromBodiesToArray(new, self.Nbodies), fromNodeToArray(self.node)

    def animate2d(self, i, values, points, boxes):
        nboxes = len(boxes)
        npoints = len(points)
        if len(boxes) > 0:
            for j in range(nboxes):
                box = values[i, j, 2:]
                boxes[j].set_data(box[:5], box[5:])

        for j in range(npoints):
            body = values[i, j]
            points[j].set_data(body[0], body[1])

        if nboxes > 0:
            return points, boxes
        else:
            return points,

    def makeAnimation(self, data = None, boxed = False, color = None, alpha = 0.5):
        if type(data) == type(None):
            if boxed:
                data_to_use = self.results_nodes
            else:
                data_to_use = self.results_bodies

            if type(data_to_use) == type(None):
                self.start(100)

        data = data_to_use

        Ninstants = data.shape[0]

        fig = plt.figure()

        if color == None:
            points = [plt.plot([], [], "o", alpha = alpha)[0] for i in range(self.Nbodies)]
        else:
            points = [plt.plot([], [], "o", color = color, alpha = alpha)[0] for i in range(self.Nbodies)]
        boxes = []

        if boxed:
            boxes = [plt.plot([], [], c = points[i].get_color(), alpha = alpha)[0] for i in range(self.Nbodies)]

        plt.xlim(data[:, :, 0].min(), data[:, :, 0].max())
        plt.ylim(data[:, :, 1].min(), data[:, :, 1].max())

        if self.dim == 2:
            animation = self.animate2d

        ani = FuncAnimation(fig, animation, frames = Ninstants,
                            interval = 25, fargs=(data, points, boxes))

        return ani

    def getEnergies(self):
        if type(self.results_bodies) != type(None):
            return self.results_bodies[:, :, -1].sum(axis=1)
        else:
            raise(Exception("No simulation has been started."))

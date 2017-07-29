import os
import sys
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ctypes import POINTER, c_char_p, c_int, pointer

DOUBLE = ctypes.c_float

NAME = "astrohutc.cpython-%d%dm.so"%sys.version_info[:2]
PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), NAME)
LIB = ctypes.CDLL(PATH)

class point2d(ctypes.Structure):
    _fields_ = [('x', DOUBLE),
                ('y', DOUBLE)]

    def __str__(self):
        return "x = %f, y = %f"%(self.x, self.y)

    def getX(self):
        return self.x

class body2d(ctypes.Structure):
    _fields_ = [('p', point2d),
                ('v', point2d),
                ('a', point2d)]

    def __str__(self):
        values = ["%s: %s"%(item, str(getattr(self, item))) for item, _ in self._fields_]
        return "\n".join(values)

    def asList(self):
        return [self.p.x, self.p.y, self.v.x, self.v.y, self.a.x, self.a.y]

    def asarray(self):
        return np.array(self.asList())

class node2d(ctypes.Structure):
    pass

class node2d(ctypes.Structure):
    _fields_ = [('xs', ctypes.POINTER(DOUBLE)),
                ('ys', ctypes.POINTER(DOUBLE)),
                ('Nbodies', ctypes.c_int),
                ('mass', DOUBLE),
                ('width', DOUBLE),
                ('height', DOUBLE),
                ('cmass', point2d),
                ('center', point2d),

                ('subnode1', ctypes.POINTER(node2d)),
                ('subnode2', ctypes.POINTER(node2d)),
                ('subnode3', ctypes.POINTER(node2d)),
                ('subnode4', ctypes.POINTER(node2d))]

    def __str__(self):
        toprint = ["Nbodies", "mass", "width", "height", "center", "cmass"]
        values = ["%s: %s"%(item, str(getattr(self, item))) for item in toprint]
        return "\n".join(values)

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

def fromBodiesToArray(bodies, N, dim = 2):
    array = np.zeros((N, dim*3))
    for i in range(N):
        array[i] = bodies[i].asList()

    return array

def __setConstants__(mass_unit, G, tau, dt, epsilon):
    LIB.setConstants(mass_unit, G, tau, dt, epsilon)

def fromArrayToBodies(array, dim = 2):
    rows, cols = array.shape[:2]
    bodies = LIB.malloc(rows * ctypes.sizeof(body2d))
    bodies = ctypes.cast(bodies, POINTER(body2d))

    if cols//dim == 3:
        for i in range(rows):
            bodies[i] = body2d(point2d(*array[i, :2]), point2d(*array[i, 2:4]),
                                point2d(*array[i, 4:]))
    elif cols//dim == 2:
        for i in range(rows):
            bodies[i] = body2d(point2d(*array[i, :2]), point2d(*array[i, 2:4]))
    else:
        raise(Exception("Input file has wrong data format."))
    return rows, bodies

class Simulation():
    def __init__(self, data, mass_unit = 1.0, G = 1.0, tau = 0.5, dt = 1e-4, epsilon = 1e-4,
                read_kwargs = {}):
        self.data = data
        self.mass_unit = mass_unit
        self.G = G
        self.tau = tau
        self.dt = dt
        self.epsilon = epsilon

        if type(self.data) is str:
            self.data = np.genfromtxt(data, **read_kwargs)

        self.Nbodies, self.bodies = fromArrayToBodies(self.data)
        self.node = None
        self.results = None
        self.setConstants()

        self.file_number = 0

    def setConstants(self):
        __setConstants__(self.mass_unit, self.G, self.tau, self.dt, self.epsilon)

    def setFilePrefix(self, prefix):
        __setPrint__(prefix)

    def start(self, Ninstants, threads = 0, save_to_file_every = 0, save_to_array_every = 1):#, save_to_file_last = True):
        if type(self.node) == type(None):
            self.node = LIB.initFirstNode2d(self.Nbodies, self.bodies)

        if threads > 0:
            LIB.omp_set_num_threads(threads)

        Ninstants = int(Ninstants)
        new = LIB.solveInstant2d(ctypes.byref(self.node), self.bodies)
        array_number = 0

        if save_to_array_every != 0:
            instant_points = np.zeros((Ninstants//save_to_array_every, self.Nbodies, 6))

        for i in range(Ninstants):
            new2 = LIB.solveInstant2d(ctypes.byref(self.node), new)

            if save_to_file_every > 0:
                if i%save_to_file_every == 0:
                    LIB.printInstant2d(self.node, file_number)
                    self.file_number += 1

            if save_to_array_every > 0:
                if i%save_to_array_every == 0:
                    instant_points[array_number] = fromBodiesToArray(new, self.Nbodies)
                    array_number += 1

            LIB.swapBody2d(ctypes.byref(new2), ctypes.byref(new))
            LIB.free(new2)

        # if save_to_file_last:
        #     if save_to_file_every != 0:
        #         if i%save_to_file_every != 0:
        #             LIB.printInstant2d(self.node, self.file_number)
        #             self.file_number += 1
        #     else:
        #         LIB.printInstant2d(self.node, self.file_number)
        #         self.file_number += 1

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

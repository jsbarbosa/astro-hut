import ctypes
from .constants import DOUBLE

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

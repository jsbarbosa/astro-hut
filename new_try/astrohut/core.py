import os
import sys
import ctypes
import numpy as np
from .constants import DOUBLE, LIB
from .structs2d import body2d, node2d, point2d

def fromBodiesToArray(bodies, N, dim = 2):
    array = np.zeros((N, dim*3))
    for i in range(N):
        array[i] = bodies[i].asList()

    return array

def fromArrayToBodies(array, dim = 2):
    rows, cols = array.shape[:2]
    bodies = LIB.malloc(rows * ctypes.sizeof(body2d))
    bodies = ctypes.cast(bodies, ctypes.POINTER(body2d))

    if dim == 2:
        body = body2d
    elif dim == 3:
        body = body3d

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

def fromNodeToArray(node, dim = 2):
    def internalNode(node, dim):
        if node.contents.Nbodies == 1:
            c1 = point2d()
            c2 = point2d()
            c3 = point2d()
            c4 = point2d()

            c1.x = node.contents.center.x - node.contents.width*0.5
            c1.y = node.contents.center.y + node.contents.height*0.5

            c2.x = node.contents.center.x + node.contents.width*0.5
            c2.y = node.contents.center.y + node.contents.height*0.5

            c3.x = node.contents.center.x + node.contents.width*0.5
            c3.y = node.contents.center.y - node.contents.height*0.5

            c4.x = node.contents.center.x - node.contents.width*0.5
            c4.y = node.contents.center.y - node.contents.height*0.5

            return [node.contents.xs[0], node.contents.ys[0], c1.x, c2.x, c3.x, c4.x, c1.x,
                    c1.y, c2.y, c3.y, c4.y, c1.y]

        else:
            answer = []
            if dim == 2:
                answer.append(internalNode(node.contents.subnode1, dim))
                answer.append(internalNode(node.contents.subnode2, dim))
                answer.append(internalNode(node.contents.subnode3, dim))
                answer.append(internalNode(node.contents.subnode4, dim))
            else:
                raise(Exception("Not implemented yet"))

            return answer

    answer = internalNode(node, dim)
    print(answer)

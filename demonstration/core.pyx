#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 12:45:40 2017

@author: juan
"""

import numpy as np
cimport numpy as np
import copy


cdef class box:
#    cdef public np.ndarray points, lower_bound, coordinate_size, bound_data
    cdef public np.ndarray points, lower_bound, bound_data 
#    cdef public np.ndarray box_half_size, upper_bound, box_half, tmatrix, center_mass
    cdef public np.ndarray upper_bound, box_half, tmatrix, center_mass
    cdef public int number_of_points
    cdef public list children, tree
    cdef public bint parent
#    cdef double length, mass, tolerance, mass_unit
    cdef double length, mass, tolerance, mass_unit, coordinate_size, box_half_size #
    cdef Py_ssize_t i, j, k, l
    
#    def __init__(self, np.ndarray[np.float64_t, ndim=2] points, np.ndarray[np.float64_t, ndim=1] lb, np.ndarray[np.float64_t, ndim=1] cs,
#                 list tr, bint parent = False, double mass = 1, double tolerance = 1):
    def __init__(self, np.ndarray[np.float64_t, ndim=2] points, np.ndarray[np.float64_t, ndim=1] lb,  double cs,
                 list tr, bint parent = False, double mass = 1, double tolerance = 1):
        cdef np.ndarray inter
        
        self.points = points
        self.parent = parent
        self.coordinate_size = cs
        self.lower_bound = lb
        self.number_of_points = points.shape[1]
        self.box_half_size = 0.5*self.coordinate_size
        self.upper_bound = self.lower_bound + self.coordinate_size
        self.box_half = self.lower_bound + self.box_half_size
        self.bound_data = np.zeros((6, self.number_of_points))
        self.mass_unit = mass
        self.mass = mass*self.number_of_points
        self.tolerance = tolerance
        self.children = []
        self.tree = tr
        if self.number_of_points > 0:
            self.tree.append(self)
            if self.number_of_points == 1:
                self.points = points[:, 0]
                self.center_mass = self.points
            else:
                self.center_mass = np.sum(self.points, axis=-1)/self.mass
        
        self.tmatrix = np.zeros((3, 2))
        self.tmatrix[0] = self.lower_bound[0], self.box_half[0]
        self.tmatrix[1] = self.lower_bound[1], self.box_half[1]
        self.tmatrix[2] = self.lower_bound[2], self.box_half[2]
        
        self.length = self.coordinate_size#max(self.coordinate_size)#np.sqrt(np.sum(self.coordinate_size**2))
        
        if self.number_of_points > 1:
            for i in range(3):
                half = self.box_half[i]
                low = self.points[i] <= half
                high = self.points[i] > half
                self.bound_data[2*i] = low
                self.bound_data[2*i+1] = high
                
            for i in range(8):
                j = i%2
                k = int(i/2)%2
                l = int(i/4)
                inter = (self.bound_data[j]==1) & (self.bound_data[k+2]==1) & (self.bound_data[l + 4]==1)
                num = sum(inter)
                points = self.points[:, inter]
                if num > 0:
                    if num == 1:
                        parent = False
                    else:
                        parent = True
                    son_box = box(points, np.array([self.tmatrix[0, j], self.tmatrix[1, k],
                             self.tmatrix[2, l]]), 0.5*self.coordinate_size, self.tree, parent,
                            self.mass_unit, self.tolerance)
    
                    self.children.append(son_box)
                    
    cpdef force(self, np.ndarray[np.float64_t, ndim=1] point, double epsilon):
        cdef double l, d, theta
        cdef box child
        cdef Py_ssize_t i
        cdef np.ndarray[np.float64_t, ndim=1] a
        l = self.length
        a = np.zeros(3)
        if not np.array_equal(point, self.center_mass):
            r = self.center_mass - point
            d = np.sqrt(np.sum(r**2) + epsilon)
            theta = l/d
            if theta > self.tolerance:
                if not self.parent:
                    return r*self.mass/(d**3)
                else:
                    for child in self.children:
                        a += child.force(point, epsilon)
                    return a
            else:
                return r*self.mass/(d**3)
        else:
            return a

    def plot(self, ax, a = 1, c = "b", w = 0.5, child_only = True):
        if child_only:
            if not self.parent:
                xy, yx = np.meshgrid([self.lower_bound[0], self.upper_bound[0]], [self.lower_bound[1], self.upper_bound[1]])
                xz, zx = np.meshgrid([self.lower_bound[0], self.upper_bound[0]], [self.lower_bound[2], self.upper_bound[2]])
                yz, zy = np.meshgrid([self.lower_bound[1], self.upper_bound[1]], [self.lower_bound[2], self.upper_bound[2]])
                self.surface(xy, yx, self.upper_bound[2], a, c, w, ax)
                self.surface(xy, yx, self.lower_bound[2], a, c, w, ax)
                self.surface(xz, self.lower_bound[1], zx, a, c, w, ax)
                self.surface(xz, self.upper_bound[1], zx, a, c, w, ax)
                self.surface(self.upper_bound[0], yz, zy, a, c, w, ax)
                self.surface(self.lower_bound[0], yz, zy, a, c, w, ax)
        else:
            xy, yx = np.meshgrid([self.lower_bound[0], self.upper_bound[0]], [self.lower_bound[1], self.upper_bound[1]])
            xz, zx = np.meshgrid([self.lower_bound[0], self.upper_bound[0]], [self.lower_bound[2], self.upper_bound[2]])
            yz, zy = np.meshgrid([self.lower_bound[1], self.upper_bound[1]], [self.lower_bound[2], self.upper_bound[2]])
            self.surface(xy, yx, self.upper_bound[2], a, c, w, ax)
            self.surface(xy, yx, self.lower_bound[2], a, c, w, ax)
            self.surface(xz, self.lower_bound[1], zx, a, c, w, ax)
            self.surface(xz, self.upper_bound[1], zx, a, c, w, ax)
            self.surface(self.upper_bound[0], yz, zy, a, c, w, ax)
            self.surface(self.lower_bound[0], yz, zy, a, c, w, ax)
            
            
    def surface(self, x, y, z, a, c, w, ax):
        ax.plot_wireframe(x, y, z, alpha=a, color=c, linewidth = w)

def speeds_generator(distances, G, m = 1):
    r = np.sqrt(np.sum(distances**2, axis=0))
    n = len(r)
    s = np.zeros((3, n))
    for i in range(n):
        pos = np.where(r < r[i])[0]
        M = m*pos.shape[0]
        if M != 0:
            s[:, i] = np.sqrt(G*M/r[i])
        else:
            s[:, i] = 0
    e1 = np.zeros((3, n))
    e1[:] = -distances[1,:], distances[0,:], distances[2, :]
    e2 = np.array([np.cross(distances[:,i], e1[:,i]) for i in range(n)]).T
    n1 = e1/np.sqrt(np.sum(e1**2, axis=0))
    n2 = e2/np.sqrt(np.sum(e2**2, axis=0))
    omega = -np.pi
    vel = np.cos(omega)*n1 + np.sin(omega)*n2
    vel[2, :] = 0
    vel = vel/np.sqrt(np.sum(vel**2, axis = 0))
    vel *= s/np.sqrt(2)
    return vel

def rotation_matrixes(theta):
    x = np.array([[1, 0, 0], [0, np.cos(theta), - np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    y = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    z = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    return x, y, z
    
cpdef limits(matrix):
    cdef Py_ssize_t i
    cdef list x_min, x_max, rank
    x_min = [min(matrix[i]) if min(matrix[i]) > 0 else min(matrix[i]) for i in range(3)]
    x_max = [max(matrix[i]) for i in range(3)]
    rank = [(x_max[i] - x_min[i]) for i in range(3)]
#    return np.array(x_min), np.array(rank)
    return np.array(x_min), max(rank)
        
def solver(np.ndarray[np.float64_t, ndim=2] positions, np.ndarray[np.float64_t, ndim=2] speeds,
           int N, double t, double dt , double G, filename='Data/', double tolerance = 1, double mass = 1, double epsilon = 0.1):
    cdef int n, i
    cdef Py_ssize_t j
    cdef np.ndarray[np.float64_t, ndim=2] x, v, v_half, accelerations
#    cdef np.ndarray[np.float64_t, ndim=1] x0, r0
    cdef np.ndarray[np.float64_t, ndim=1] x0
    cdef double r0 #
    cdef box tree
    n = int(t/dt)
    x = positions
    v = speeds
    accelerations = np.zeros((3, N))
    np.savetxt("%s%d_instant.dat"%(filename, 0), x.T)
    np.savetxt("%s%d_speed.dat"%(filename, 0), v.T)
    pos = []
    trees = []
    for i in range(n):
        print(i)
        x0, r0 = limits(x)
        tree = box(x, x0, r0, [], True, mass, tolerance)
        for j in range(N):
            accelerations[:, j] = tree.force(x[:,j], epsilon)
        v_half = v + 0.5*dt*accelerations*G
        x += dt*v_half
        x0, r0 = limits(x)
        tree = box(x, x0, r0, [], True, mass, tolerance)
        for j in range(N):
            accelerations[:, j] = tree.force(x[:,j], epsilon)
        v = v_half + 0.5*dt*accelerations*G
        np.savetxt("%s%d_instant.dat"%(filename, i+1), x.T) 
        np.savetxt("%s%d_speed.dat"%(filename, i+1), v.T)       
    return n

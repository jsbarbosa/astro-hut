import numpy as np

def smallGaussian():
    return np.genfromtxt("small_size_gaussian2d.dat")

def mediumGaussian():
    return np.genfromtxt("medium_size_gaussian2d.dat")

def largeGaussian():
    return np.genfromtxt("large_size_gaussian2d.dat")

def twosmallGaussians():
    return np.genfromtxt("two_small_size_gaussian2d.dat")

def twomediumGaussians():
    return np.genfromtxt("two_medium_size_gaussian2d.dat")

def twolargeGaussians():
    return np.genfromtxt("two_large_size_gaussian2d.dat")

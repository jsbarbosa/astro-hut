import os
import sys
from ctypes import c_double, c_float, CDLL

DOUBLE = c_float

NAME = "astrohutc.cpython-%d%dm.so"%sys.version_info[:2]
PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), NAME)
LIB = CDLL(PATH)

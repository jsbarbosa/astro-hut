#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 19:33:32 2017

@author: juan
"""

import numpy as np
from core import *

N = 8
p = np.zeros((3, N))

p[0] = -1, -1, -1, -1, 1, 1, 1, 1
p[1] = -1, 1, -1, 1, -1, 1, -1, 1
p[2] = -1, -1, 1, 1, -1, -1, 1, 1

solver(p, np.zeros_like(p), N, 10.0, 0.05, 1, filename='data/',
       tolerance = 0)
 
import numpy as np

N = 100
data = np.zeros((N, 4))
data[:, 0] = np.random.normal(size=N)
data[:, 1] = np.random.normal(size=N)

np.savetxt("initial.csv", data, fmt='%f')

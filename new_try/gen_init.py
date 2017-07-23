import numpy as np

G = 1
MASS_UNIT = 1

N = 100
data = np.zeros((N, 4))
data[:, 0] = x = np.random.normal(size=N)
data[:, 1] = y = np.random.normal(size=N)

r = (x**2 + y**2)**0.5
theta = np.arctan2(y, x)

speeds = np.zeros((N, 2))

for i in range(N):
    n = len(np.where(r < r[i])[0])
    mag = np.sqrt(G*MASS_UNIT*n/r[i])
    vx = -r[i]*np.sin(theta[i])
    vy = r[i]*np.cos(theta[i])
    mag_ = (vx**2 + vy**2)**0.5
    vx *= mag/mag_
    vy *= mag/mag_
    speeds[i, 0] = vx
    speeds[i, 1] = vy

data[:, 2:] = speeds
np.savetxt("initial.csv", data, fmt='%f')

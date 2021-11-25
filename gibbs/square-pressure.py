import matplotlib.pyplot as plt
import numpy as np
import math

file = 'square-lattice-output'

def extrapolate(s, dx, xmax, degree=5):
  s = s[:int(math.ceil(xmax/dx))]
  x = np.arange(0,xmax,dx)
  x += dx/2
  x = x[:len(s)]
  p = np.polyfit(x, s, degree)
  return np.polyval(p, 0.0)

full_volume_data = np.loadtxt(file + '.vol',skiprows=1)
sdf_data = np.loadtxt(file + '.sdf')
sdf_t = sdf_data[:,0]
sdf_data = sdf_data[:,1:]
volume_data = []
t_steps = list(map(int,sdf_t))

for vol in full_volume_data:
    if int(vol[0]) in t_steps:
        volume_data.append(float(vol[1]))

N = full_volume_data[0,2]
n = len(sdf_data)
dim = 2
xmax = 0.01
dx = 1e-5


s0 = []
for i in range(n):
    s0.append(extrapolate(sdf_data[i], dx, xmax, degree = 5))
s0 = np.array(s0)

n_density = N/volume_data
betaP = n_density*(1.0 + s0/(2*dim))

with open("square-data.data",'w') as pv:
    pv.writelines('timestep:    volume:     betaP:\n')
    for i in range(len(volume_data)):
        pv.writelines(str(t_steps[i]) + ' ' + str(volume_data[i]) + '  ' + str(betaP[i]) + '\n')

plt.plot(volume_data,betaP,'o')
plt.show()
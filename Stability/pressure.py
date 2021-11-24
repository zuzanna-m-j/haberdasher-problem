n_cell = 20
import math

import numpy as np
import matplotlib.pyplot as plt

## extrapolation function
def extrapolate(s, dx, xmax, degree=5):
    # determine the number of values to fit
    n_fit = int(math.ceil(xmax/dx));
    s_fit = s[0:n_fit];
    # construct the x coordinates
    x_fit = np.arange(0,xmax,dx)
    x_fit += dx/2
    #added that line
    x_fit = x_fit[:len(s_fit)]
    #########################
    # perform the fit and extrapolation
    p = np.polyfit(x_fit, s_fit, degree)
    return(np.polyval(p, 0.0))

#find function
def find(lst1, lst2):
    result = []
    for i, x in enumerate(lst1):
        if x in lst2:
            result.append(i)
    return result

#inputs needed
file = "tests"
N = 2 * n_cell**2

dim = 2
xmax = 0.02 # must be same variables used to GENERATE sdf.dat file
dx = 1e-4

#stuff
sdf_f = np.loadtxt(file + ".sdf")
sdf_t = sdf_f[:,0]
sdf_data = sdf_f[:,1:]
nsamples = len(sdf_data)

# make array containing s(0+) values
s0_arr = np.empty((nsamples,), dtype=np.float32)
for i in range(nsamples):
    s0_arr[i] = extrapolate(sdf_data[i], dx, xmax, degree = 5)

#autocalculating the number density
vol_f = np.loadtxt(file + ".vol",skiprows=1)
vol_t = vol_f[:,0]
vol_d = vol_f[:,1]

vol_i = find(vol_t, sdf_t)

vol_data = np.empty((nsamples,), dtype=np.float32)
i = 0
for y in vol_i:
    vol_data[i] = vol_d[y]
    i += 1

# make array containing calculated values for beta*P
rho = N/vol_data
betaP = rho*(1.0 + s0_arr/(2*dim))

x = N/vol_data * (2.0 + 4.0)/2
y = betaP * (2.0 + 4.0)/2

fig, ax = plt.subplots()
ax.plot(x, y, lw = 1.2)
ax.plot(x,x, ls = '--', c = 'blue')
fig.savefig(file + ".png")
plt.show()

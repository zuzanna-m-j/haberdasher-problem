'''
Created on Jun 22, 2020

@author: yuelingxu
'''

import hoomd
from hoomd import hpmc

import compress_helper_2d

import math

import numpy as np
import random

import matplotlib
import matplotlib.pyplot as plt

## extrapolation function
def extrapolate(s, dx, xmax, degree=5):
    # determine the number of values to fit
    n_fit = int(math.ceil(xmax/dx));
    s_fit = s[0:n_fit];
    # construct the x coordinates
    x_fit = np.arange(0,xmax,dx)
    x_fit += dx/2;
    # perform the fit and extrapolation
    p = np.polyfit(x_fit, s_fit, degree);
    return(np.polyval(p, 0.0));

#find function
def find(lst1, lst2):
    result = []
    for i, x in enumerate(lst1):
        if x in lst2:
            result.append(i)
    return result

#inputs needed
file = "phi60"
N = 400

dim = 2
xmax = 0.02 # must be same variables used to GENERATE sdf.dat file
dx = 1e-4

#stuff
sdf_f = np.loadtxt(file + ".dat")
sdf_t = sdf_f[:,0]
sdf_data = sdf_f[:,1:]
nsamples = len(sdf_data)

# make array containing s(0+) values
s0_arr = np.empty((nsamples,), dtype=np.float32)
for i in range(nsamples):
    s0_arr[i] = extrapolate(sdf_data[i], dx, xmax, degree = 5)

#autocalculating the number density
vol_f = np.loadtxt(file + ".txt")
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

#calculating the average value after whatever;
#betaP_run = betaP[30:]

#betaP_avg = sum(betaP_run) / len(betaP_run)
#error = np.std(betaP_run) / math.sqrt(len(betaP_run))

#x = rho
x = sdf_t
#x = [100*(area1+area2+area3+area4)/x1 for x1 in [645.0394551, 516.0768647, 440.6347072, 378.107271, 335.6765949, 300.7022799, 270.7225277, 244.4642068, 221.1948299]]
y = betaP

#print(betaP_avg)

'''print(np.std(betaP_run))'''

fig, ax = plt.subplots()
ax.plot(x, y, lw = 1.2)
#marker: marker = '.', markersize = 5
#ax.plot(sdf_t[500], betaP[500], 'ro', label = 'compression stopped; t =' + str(sdf_t[46]))
#ax.plot(sdf_t[1500], betaP[1500], 'go', label = 'equilibrium; t =' + str(sdf_t[2500]))

ax.set(xlabel='N/V', ylabel='betaP',
       title=file)
'''ax.axhline(y = betaP_avg, xmin = .18, xmax = .98, color = 'purple', lw = 1.2, 
           label = 'avg. betaP = %.3f' % (betaP_avg))
ax.axhline(y = betaP_avg + np.std(betaP_run), xmin = .18, xmax = .98, color = 'green', lw = 1, 
           ls = '--', label = 'STDev = +/- %.3f' % (np.std(betaP_run)))
ax.axhline(y = betaP_avg - np.std(betaP_run), xmin = .18, xmax = .98, color = 'green', lw = 1, 
           ls = '--')
ax.axhline(y = betaP_avg + error, xmin = .18, xmax = .98, color = 'black', lw = .8, 
           ls = '-.', label = 'uncertainty in mean = %.3f' % (error))
ax.axhline(y = betaP_avg - error, xmin = .18, xmax = .98, color = 'black', lw = .8, 
           ls = '-.')
plt.legend(bbox_to_anchor=(.9, .4))'''

fig.savefig(file + ".png")
plt.show()

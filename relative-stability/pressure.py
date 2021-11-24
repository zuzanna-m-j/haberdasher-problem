'''
Created on Jun 22, 2020

@author: yuelingxu
'''

import hoomd
import hoomd.dem
from hoomd import hpmc



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

vAs = [(-0.21799013664766403, -0.5023571793344106),(0.43806861572454686, 0.25235264134888885),(-0.21996612497820883, 0.2506258175372971)]
vBs = [(-0.5845343621823524, -0.12771177916537713),(0.4002733778408708, -0.30136003049648535),(0.3889689778694574, 0.26161490951675265),(-0.2689354095542138, 0.24840434931275862)]
vCs = [(0.37900872267547725, -0.35788779037693047),(0.05343979731237958, 0.587630519777832),(-0.28050392925997647, 0.20347157435381596),(-0.2790260172522079, -0.3596149095167526)]
vDs = [(-0.5592972649748391, 0.48861096202561094),(-0.22549069130706167, -0.45403063019074075),(0.4325039292599765, -0.446561949111819),(0.4239575873822218, 0.30637513866397204)]


vAu = [(-0.5220179221316321, -0.16503966450482788),(0.47798207786836777, -0.16503966450482788),(0.04496937597614856, 0.3304527187789308)]
vBu = [(0.4740585927875667, -0.36545839924993373),(-0.025942184562527393, 0.5005665557307537),(-0.44993932042913276, 0.13003315464721044),(-0.01692617377975303, -0.3654588399612012)]
vCu = [(0.021942184562527278, 0.5210690568864235),(-0.4780585927875667, -0.34495589809426397),(0.03095664064471082, -0.34495635498980115),(0.4549544416972373, 0.025576284927716575)]
vDu = [(0.014417099295431987, 0.7420396645048278),(-0.4931218469408215, -0.11958915236087647),(-0.06444990268382092, -0.6188416597147626),(0.506840070215735, -0.1283163647786042)]

vAd = [(0.5220179189906603, 0.16503999736020913),(-0.4779820810084331, 0.16503865095000192),(-0.04496871198060394, -0.3304531493205859)]
vBd = [(-0.4740585897588976, 0.36545668411237353),(0.02594335361558253, -0.5005675976613787),(0.4499399905918503, -0.1300336257040997),(0.01692617680738384, 0.36545778589054234)]
vCd = [(-0.014941021565904156, -0.5570686822378279),(0.4850585897588976, 0.30895694594822487),(-0.023956643673533673, 0.30895671750045606),(-0.4479539458367474, -0.06157649329169301)]
vDd = [(-0.023414729954361082, -0.7730399973602091),(0.4841230561755986, 0.08858950286033201),(0.055450439720314625, 0.5878414330454843),(-0.5158388727304595, 0.09731536891911975)]


area1 = hoomd.dem.utils.area(vertices=vAs, factor=1.0)
area2 = hoomd.dem.utils.area(vertices=vBs, factor=1.0)
area3 = hoomd.dem.utils.area(vertices=vCs, factor=1.0)
area4 = hoomd.dem.utils.area(vertices=vDs, factor=1.0)

file = 'data'
N = 3200

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
vol_f = np.loadtxt(file + ".txt",skiprows=1)
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
y = betaP
x = np.arange(len(y))
#x = sdf_t
#x = [100*(area1+area2+area3+area4)/x1 for x1 in [645.0394551, 516.0768647, 440.6347072, 378.107271, 335.6765949, 300.7022799, 270.7225277, 244.4642068, 221.1948299]]


#print(betaP_avg)

'''print(np.std(betaP_run))'''

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(x, y, lw = 2)
ax2.plot(x, y, lw = 2)

ax2.plot(x,x,'--')

#marker: marker = '.', markersize = 5
#ax.plot(sdf_t[500], betaP[500], 'ro', label = 'compression stopped; t =' + str(sdf_t[46]))
#ax.plot(sdf_t[1500], betaP[1500], 'go', label = 'equilibrium; t =' + str(sdf_t[2500]))

# ax1.set(xlabel='N/V', ylabel='betaP',
#        title=file)
# ax2.set(xlabel='N/V', ylabel='betaP',
#        title=file)
#
# ax.axvline(y = betaP_avg, xmin = .18, xmax = .98, color = 'purple', lw = 1.2,
#            label = 'avg. betaP = %.3f' % (betaP_avg))

# ax.axhline(y = betaP_avg + np.std(betaP_run), xmin = .18, xmax = .98, color = 'green', lw = 1,
#            ls = '--', label = 'STDev = +/- %.3f' % (np.std(betaP_run)))
# ax.axhline(y = betaP_avg - np.std(betaP_run), xmin = .18, xmax = .98, color = 'green', lw = 1,
#            ls = '--')
# ax.axhline(y = betaP_avg + error, xmin = .18, xmax = .98, color = 'black', lw = .8,
#            ls = '-.', label = 'uncertainty in mean = %.3f' % (error))
# ax.axhline(y = betaP_avg - error, xmin = .18, xmax = .98, color = 'black', lw = .8,
#            ls = '-.')
# plt.legend(bbox_to_anchor=(.9, .4))

fig.savefig(file + ".png")
plt.show()

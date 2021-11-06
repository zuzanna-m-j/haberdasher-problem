'''
Created on Jun 12, 2020

@author: yuelingxu
'''
import hoomd
from hoomd import hpmc
from hoomd import dem

import math

#import compress_helper_2d

import numpy as np
import random

# initial packing fraction of system = N*vol/V
phi_init = 0.4

# final packing fraction of system
phi_fin = 0.3

## thermalization parameters for MC randomization
therm_steps = 100
seed = random.randint(1,1e7)

file = "squares"


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

## defining area of vertices
# area1 = hoomd.dem.utils.area(vertices=vAu, factor=1.0)
# area2 = hoomd.dem.utils.area(vertices=vBu, factor=1.0)
# area3 = hoomd.dem.utils.area(vertices=vCu, factor=1.0)
# area4 = hoomd.dem.utils.area(vertices=vDu, factor=1.0)

######
hoomd.context.initialize("--mode=cpu")

#to establish phi_init, a square unit cell should have the following lattice constant:
#a = pow(1./phi_init, 1./2.)

#system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sq(a=a), n=10)

c = 0.72
d = 0.7
positions =[]
positions.append((c - 0.451 , d + 0.419, 0))
positions.append((c + 0.269 , d + 0.419, 0))
positions.append((c - 0.391 , d - 0.321, 0))
positions.append((c + 0.239 , d - 0.221, 0))
uc = hoomd.lattice.unitcell(N = 4,
                            a1 = [1.4,0,0],
                            a2 = [0,1.4,0],
                            a3 = [0,0,1.0],
                            dimensions = 2,
                            position = positions,
                            type_name = ['As', 'Bs', 'Cs', 'Ds']);
#

# sx = 1.9070982572923945/2 + 0.15
# sy = 1.7620793290096557
# positions =[]
# positions.append((0.027, -0.716, 0))
# positions.append((0.552, -0.511, 0))
# positions.append((-0.548, -0.536,0))
# positions.append((-0.015, 0.139, 0))
# positions.append((-0.027 + sx , 0.716, 0))
# positions.append((-0.552 + sx, 0.511, 0))
# positions.append((0.541 + sx , 0.572, 0))
# positions.append((0.024 + sx, -0.108, 0))
# uc = hoomd.lattice.unitcell(N = 8,
#                             a1 = [2.2,0,0],
#                             a2 = [0,1.8,0],
#                             a3 = [0,0,1.0],
#                             dimensions = 2,
#                             position = positions,
#                             type_name = ['Au', 'Bu', 'Cu', 'Du', 'Ad', 'Bd', 'Cd', 'Dd']);

n_sys = 10

system = hoomd.init.create_lattice(unitcell=uc, n=n_sys)

#defining monte carlo simulation
mc = hoomd.hpmc.integrate.convex_polygon(d=0.1, a=0.1, seed=seed)
mc.shape_param.set('As', vertices=vAs)
mc.shape_param.set('Bs', vertices=vBs)
mc.shape_param.set('Cs', vertices=vCs)
mc.shape_param.set('Ds', vertices=vDs)

# mc.shape_param.set('Au', vertices=vAu)
# mc.shape_param.set('Bu', vertices=vBu)
# mc.shape_param.set('Cu', vertices=vCu)
# mc.shape_param.set('Du', vertices=vDu)
# mc.shape_param.set('Ad', vertices=vAd)
# mc.shape_param.set('Bd', vertices=vBd)
# mc.shape_param.set('Cd', vertices=vCd)
# mc.shape_param.set('Dd', vertices=vDd)

gsd = hoomd.dump.gsd(file + ".gsd",
                   period=10,
                   group=hoomd.group.all(),
                   overwrite=True,
                   dynamic=['momentum'])

gsd.dump_shape(mc)


snapshot = system.take_snapshot(particles=True)
# r0 = snapshot.particles.position
# q0 = snapshot.particles.orientation

hoomd.run(100)
## calculating volume every 100 time steps
hoomd.analyze.log(filename=file + '.txt', quantities=['volume', 'N'], period=10, overwrite=True)

### calculating pressure
hoomd.hpmc.analyze.sdf(mc=mc, filename=file + '.dat', xmax=0.02, dx=1e-4, navg=100, period=100, overwrite=True)
# log = hoomd.hpmc.analyze.log(quantities=['lattice_energy'], period=1, filename='log.dat', overwrite=True);

### then compress the system
# vol = n_sys**2*(area1 + area2 + area3 + area4)
# compress_helper_2d.length_geom(system, mc, phi_fin, scale = 0.9995, tot_part_vol = vol)

### run for a very long period of time
# hoomd.run(100)
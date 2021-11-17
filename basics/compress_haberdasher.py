'''
Created on Jun 12, 2020

@author: yuelingxu
'''
import hoomd
from hoomd import hpmc
from hoomd import dem

import math

import compress_helper_2d

import numpy as np
import random 

# initial packing fraction of system = N*vol/V
phi_init = 0.3

# final packing fraction of system
phi_fin = 0.90

## thermalization parameters for MC randomization
therm_steps = 1e5
seed = random.randint(1,1e7)

file = "pf90"


## defining vertices
piece1_verts = [[3**(.5)/4-1, -3**(.25)*(4-3**(.5))**.5/8], 
                [3**(.5)/4, -3**(.25)*(4-3**(.5))**.5/8], 
                [0, 3**(.25)*(4-3**(.5))**.5/8]]

piece2_verts = [[-0.5, -3**(.5)*(3**(.25)*(4-3**(.5))**.5-1)/8], 
                [0.5, -3**(.5)*(3**(.25)*(4-3**(.5))**.5-1)/8], 
                [.5-math.cos(2*(math.pi)/3-math.asin(3**.25/2))*(3**.25-(4-3**(.5))**.5/2), 3**(.5)*(3**(.25)*(4-3**(.5))**.5-1)/8+3**.25/2*math.sin(math.asin(3**.25/2)-math.pi/6)], 
                [(3**(.25)*(4-3**(.5))**.5-1)/4-.5, 3**(.5)*(3**(.25)*(4-3**(.5))**.5-1)/8]]

piece3_verts = [[-0.5, -3**(.5)*(3-3**(.25)*(4-3**(.5))**.5)/8], 
                [0.5, -3**(.5)*(3-3**(.25)*(4-3**(.5))**.5)/8], 
                [0.5-(3-3**(.25)*(4-3**(.5))**.5)/4, 3**(.5)*(3-3**(.25)*(4-3**(.5))**.5)/8], 
                [3**(.25)/2*math.cos(math.pi/6+math.asin(3**(.25)/2))-.5, 3**(.5)*(3-3**(.25)*(4-3**(.5))**.5)/8+math.sin(math.pi/3-math.asin(3**(.25)/2))*(3**(.25)-(4-3**(.5))**(.5)/2)]]

piece4_verts = [[-3**(.5)/2, 0],
                [0, -0.5],
                [3**(.25)*(4-3**(.5))**.5/4,3**(.5)/4-0.5],
                [0, 0.5]]

## defining area of vertices
area1 = hoomd.dem.utils.area(vertices=piece1_verts, factor=1.0)
area2 = hoomd.dem.utils.area(vertices=piece2_verts, factor=1.0)
area3 = hoomd.dem.utils.area(vertices=piece3_verts, factor=1.0)
area4 = hoomd.dem.utils.area(vertices=piece4_verts, factor=1.0)

######
hoomd.context.initialize("--mode=cpu")

#to establish phi_init, a square unit cell should have the following lattice constant:
#a = pow(1./phi_init, 1./2.)

#system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sq(a=a), n=10)

#defining unit cell for the lattice
side = 3
uc = hoomd.lattice.unitcell(N = 4,
                            a1 = [side,0,0],
                            a2 = [0,side,0],
                            a3 = [0,0,1.0],
                            dimensions = 2,
                            position = [[-.75,.75,0], [.75,.75,0], [.75,-.75,0], [-.75,-.75,0]],
                            type_name = ['A', 'B', 'C', 'D']);

n_sys = 10

system = hoomd.init.create_lattice(unitcell=uc, n=n_sys)

#defining monte carlo simulation
mc = hoomd.hpmc.integrate.convex_polygon(d=0.2, a=0.2, seed=seed)

mc.shape_param.set('A', vertices=piece1_verts)
mc.shape_param.set('B', vertices=piece2_verts)
mc.shape_param.set('C', vertices=piece3_verts)
mc.shape_param.set('D', vertices=piece4_verts)


gsd = hoomd.dump.gsd(file + ".gsd",
                   period=1000,
                   group=hoomd.group.all(),
                   overwrite=True,
                   dynamic=['momentum'])

gsd.dump_shape(mc)

### thermalize first
hoomd.run(therm_steps)

## calculating volume every 100 time steps
hoomd.analyze.log(filename=file + '.txt', quantities=['volume', 'N'], period=10, overwrite=True)

### calculating pressure
hoomd.hpmc.analyze.sdf(mc=mc, filename=file + '.dat', xmax=0.02, dx=1e-4, navg=100, period=100, overwrite=True)

### then compress the system
vol = n_sys**2*(area1 + area2 + area3 + area4)
compress_helper_2d.length_geom(system, mc, phi_fin, scale = 0.9995, tot_part_vol = vol)

### run for a very long period of time
hoomd.run(5e6)

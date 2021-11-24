a1 = 8
a2 = 8
n_repeat = 10

import hoomd
import hoomd.hpmc
import numpy as np
from hoomd import dem
import math
#import compress_helper_2d
import random

hoomd.context.initialize("--mode=cpu")

# Shape definitions #

vAs = [(-0.21799013664766403, -0.5023571793344106),(0.43806861572454686, 0.25235264134888885),(-0.21996612497820883, 0.2506258175372971)]
vBs = [(-0.5845343621823524, -0.12771177916537713),(0.4002733778408708, -0.30136003049648535),(0.3889689778694574, 0.26161490951675265),(-0.2689354095542138, 0.24840434931275862)]
vCs = [(0.37900872267547725, -0.35788779037693047),(0.05343979731237958, 0.587630519777832),(-0.28050392925997647, 0.20347157435381596),(-0.2790260172522079, -0.3596149095167526)]
vDs = [(-0.5592972649748391, 0.48861096202561094),(-0.22549069130706167, -0.45403063019074075),(0.4325039292599765, -0.446561949111819),(0.4239575873822218, 0.30637513866397204)]

# Unit cell configuration #

unit_cell = hoomd.lattice.unitcell(N = 4,
                            a1 = [a1,0,0],
                            a2 = [0,a2,0],
                            a3 = [0,0,1.0],
                            dimensions = 2,
                            position = [[2,2,0], [6,2,0], [2,6,0], [6,6,0]],
                            type_name = ['As', 'Bs', 'Cs', 'Ds'])


system = hoomd.init.create_lattice(unitcell=unit_cell, n=n_repeat)

mc = hoomd.hpmc.integrate.convex_polygon(d=0.1, a=0.1, seed=seed)

mc.shape_param.set('As', vertices=vAs)
mc.shape_param.set('Bs', vertices=vBs)
mc.shape_param.set('Cs', vertices=vCs)
mc.shape_param.set('Ds', vertices=vDs)

lx = system.box.Lx
ly = system.box.Ly

walls = hoomd.hpmc.compute.wall(mc)
walls.add_plane_wall(normal = [1, 0, 0], origin = [-lx, 0, 0])
walls.add_plane_wall(normal = [0, 1, 0], origin = [0, -ly, 0])
walls.add_plane_wall(normal = [-1, 0, 0], origin = [lx, 0, 0])
walls.add_plane_wall(normal = [0, -1, 0], origin = [0, ly, 0])
walls.set_volume(2*lx * 2*ly)
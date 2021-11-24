from __future__ import division
from __future__ import print_function

import numpy as np
import sys

import hoomd
from hoomd import hpmc
from hoomd import deprecated



navg = 100
sdfperiod = 100
volperiod = sdfperiod

eq_step = sdfperiod * navg + 99
therm_step = 1e3

# this is from Chrisy's InitializeWrapper.py. Thanks Chrisy!

# compress the system by geometrically scaling all lengths of the box by scale
def length_geom(system, mc, phi, scale = 0.99, tot_part_vol = 1.0):
    # Calculate initial system packing fraction
    V_init = system.box.get_volume()
    Lx_init = system.box.Lx
    Ly_init = system.box.Ly
    Lz_init = system.box.Lz
    phi_init = tot_part_vol/V_init
    if hoomd.comm.get_rank() == 0:
        print("Beginning fast compression routine")
        print("Current packing fraction is {}".format(phi_init))
    # this is equivalent to V_init/V_final
    alpha = pow(phi_init/phi, 1./2.)

    # run for a hot second to enable overlap checking
    hoomd.run(1)

    # Test whether to expand or compress
    if alpha > 1:
        # Expand the box
        if hoomd.comm.get_rank() == 0: print(" Expanding the box to {}!".format(phi))
        hoomd.update.box_resize(system.box.Lx*alpha, system.box.Ly*alpha,
                                system.box.Lz*alpha, system.box.xy, system.box.xz,
                                system.box.yz, period=None)
    else:
        # Compress the box
        if hoomd.comm.get_rank() == 0: print(" Shrinking the box!")
        curr_phi = phi_init
        while curr_phi < phi:
            if hoomd.comm.get_rank() == 0: print("Current density is {}".format(curr_phi))
            hoomd.update.box_resize(system.box.Lx*scale, system.box.Ly*scale,
                                    system.box.Lz*scale, system.box.xy,
                                    system.box.xz, system.box.yz, period = None)
            overlaps = mc.count_overlaps()
            while overlaps > 0:
                hoomd.run(100, quiet = True)
                overlaps = mc.count_overlaps()
                if hoomd.comm.get_rank() == 0: print(overlaps, end=' ')
                sys.stdout.flush()
            curr_phi = tot_part_vol/system.box.get_volume()
            hoomd.run(500)
            lc.enable()
            sc.enable()
            hoomd.run(eq_step)
            lc.disable()
            sc.disable()

        # update to exactly phi to make things kosher.
        hoomd.update.box_resize(Lx = Lx_init*alpha,
                                Ly = Ly_init*alpha,
                                Lz = Lz_init*alpha,
                                xy = system.box.xy, xz = system.box.xz, yz = system.box.yz, period = None)
        hoomd.run(1)
        overlaps = mc.count_overlaps()
        assert(overlaps == 0)
        if hoomd.comm.get_rank() == 0: print("Compression finished! Current density calculated to be {}.".format(tot_part_vol/system.box.get_volume()))
fname = "tests"
a1 = 10
a2 = 10
n_cell = 10
seed = 12345



area1 = 2.0
area2 = 4.0

pf_final = 90.0
import hoomd
import hoomd.hpmc
import numpy as np
from hoomd import dem
import math
#import compress_helper_2d
import random

hoomd.context.initialize("--mode=cpu")

# Shape definitions #

vT = [(-1,-1),(1,-1),(0,1)]
vS = [(-1,-1),(1,-1),(1,1),(-1,1)]


# Unit cell configuration #

unit_cell = hoomd.lattice.unitcell(N = 2,
                            a1 = [a1,0,0],
                            a2 = [0,a2,0],
                            a3 = [0,0,1.0],
                            dimensions = 2,
                            position = [[2,2,0], [8,8,0]],
                            type_name = ['T', 'S'])


system = hoomd.init.create_lattice(unitcell=unit_cell, n=n_cell)
mc = hoomd.hpmc.integrate.convex_polygon(d=0.2, a=0.2, seed=seed)

mc.shape_param.set('T', vertices=vT)
mc.shape_param.set('S', vertices=vS)

gsd = hoomd.dump.gsd(fname + ".gsd",
                   period=1000,
                   group=hoomd.group.all(),
                   overwrite=True)

gsd.dump_shape(mc)

particle_volume = n_cell**2 * (area1 + area2)

hoomd.run(therm_step)

lc = hoomd.analyze.log(filename=fname + '.vol', quantities=['volume'], period=volperiod, overwrite=True)
sc = hoomd.hpmc.analyze.sdf(mc=mc, filename=fname + '.sdf', xmax=0.02, dx=1e-4, navg=navg, period=sdfperiod, overwrite=True)
lc.disable()
sc.disable()

# print(hoomd.get_step())
# log = hoomd.analyze.log(filename=None, quantities=['volume', 'N', 'potential_energy'], period=None)

length_geom(system, mc, pf_final, scale = 0.9995, tot_part_vol = particle_volume)

hoomd.run(1000)
print("Done!")
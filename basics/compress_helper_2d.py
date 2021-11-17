from __future__ import division
from __future__ import print_function

import numpy as np
import sys

import hoomd
from hoomd import hpmc
from hoomd import deprecated

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
            print();
            curr_phi = tot_part_vol/system.box.get_volume()

        # update to exactly phi to make things kosher.
        hoomd.update.box_resize(Lx = Lx_init*alpha,
                                Ly = Ly_init*alpha,
                                Lz = Lz_init*alpha,
                                xy = system.box.xy, xz = system.box.xz, yz = system.box.yz, period = None)
        hoomd.run(1)
        overlaps = mc.count_overlaps()
        assert(overlaps == 0)
        if hoomd.comm.get_rank() == 0: print("Compression finished! Current density calculated to be {}.".format(tot_part_vol/system.box.get_volume()))

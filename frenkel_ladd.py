#!/usr/bin/env python

import hoomd
import hoomd.hpmc
import numpy as np
hoomd.context.initialize('--mode=cpu');
system = hoomd.init.create_lattice(unitcell=hoomd.lattice.fcc(a=1.56635089489599), n=4);
mc = hoomd.hpmc.integrate.sphere(d=0.06, seed=81954)

mc.shape_param.set('A', diameter=1.0);
log = hoomd.analyze.log(filename="test_HS.out", quantities=['lx','ly','lz','volume',"hpmc_overlap_count"], period=10)

ref_pos=[]
ref_ori=[]
for i in range(len(system.particles)):
    p = system.particles.pdata.getPosition(i)
    ref_pos.append([p.x,p.y,p.z])



hoomd.run(2000)

fl_filename="FL_fcc_0736.out"
fl = hoomd.hpmc.field.frenkel_ladd_energy(mc=mc, ln_gamma=0.0, q_factor=10.0, r0=ref_pos, q0=[(1,0,0,0)]*len(system.particles), drift_period=1)
log_fl = hoomd.analyze.log(filename=fl_filename,quantities=["lattice_energy","lattice_translational_spring_constant","lattice_energy_pp_avg","lattice_energy_pp_sigma","lattice_num_samples"],period=1)


mc_step=500
lambda_max=632.026
ks = np.logspace(np.log10(0.00001),np.log10(lambda_max), 100);
for k in ks:
    fl.set_params(ln_gamma=np.log(k), q_factor=0.0);
    fl.reset_statistics();
    hoomd.run(mc_step)

print("Success!")
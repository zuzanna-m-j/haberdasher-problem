import numpy as np
import math
import sys
import inspect
import os
import random
import argparse
import datetime

# from teich_utils import write_pos as poswriter

import hoomd
from hoomd import *
from hoomd import hpmc
from hoomd.deprecated import dump

context.initialize()

userargs=option.get_user()

parser = argparse.ArgumentParser(
    description='Takes a particle type and number of particles, and compresses system within a spherical container to a given final packing fraction via HPMC integration'
    )

parser.add_argument(
    '-shape',
    '--shape',
    type=str,
    dest='shape',
    help='particle shape. must have *shapeinfo.npz file'
    )

parser.add_argument(
    '-N',
    '--N',
    type=int,
    dest='N',
    help='number of particles'
    )

parser.add_argument(
    '-phi',
    '--phi',
    type=float,
    dest='phi_final',
    help='final packing fraction at which to run NVT integration'
    )

parser.add_argument(
    '-steps',
    '--steps',
    type=float,
    dest='steps',
    help='steps to run at final packing fraction'
    )

parser.add_argument(
    '-scale',
    '--scale',
    type=float,
    dest='scale',
    help='amount by which to scale container radius during compression.'
    )

# user params
args=parser.parse_args(userargs)

shape=args.shape
N=args.N
phi_final=args.phi_final
steps=args.steps
scale=args.scale

equil_time=1000 # time between each compression

comp_dump_period=100000
dump_period=int(steps/100)
seed = random.randint(1,1e8);
cont_scale = 1.25;
delta = 1.0;
tuner_period = 50;

class Sphere:
    # create a spherical container defined by a radius

    def __init__(self, ext_wall, rad):
        self.R=rad
        self.ext_wall=ext_wall

        self.ext_wall.add_sphere_wall(self.R,[0.,0.,0.])

    def modify(self, new_rad):
        self.R=new_rad

        self.ext_wall.set_sphere_wall(0, self.R,[0.,0.,0.])

    def container_def(self, timestep):
        color='666666'

        # to visualize the mesh
        # shape_def=poswriter.build_shapedef("container", [], r_circ=self.R, sphere=True)
        # shape_str=str(shape_def)
        shape_str = "def container" + " \"sphere " + str(2*self.R) + "\"" + "\n"
        shape_str += "container " + color + " 0 0 0\n"

        return shape_str

if shape == "Sphere":
    particle_tunables = ['d']
    max_part_moves = [0.3]

    r_circ = 1.0;
    volume = 4.0/3.0*math.pi*pow(r_circ,3.0);

else:
    particle_tunables = ['d','a']
    max_part_moves = [0.3, 0.5]

    p = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    f = np.load(p+'/../shapefiles/%s_shapeinfo.npz'%shape)
    verts = f['scaled_verts']
    r_circ = f['r_circ']
    volume = f['vol']

nn = int(N**(1.0/3.0))+1
bottom = -(nn-1)*r_circ*delta
top = (nn-1)*r_circ*delta

cont_rad = (np.sqrt(3.0*pow(top, 2.0))+r_circ*delta)*cont_scale
start_L = 2*cont_rad*cont_scale


# initialize system
system = init.read_snapshot(data.make_snapshot(N=N, box=data.boxdim(L=start_L, dimensions=3), particle_types=[shape]));

# set up positions and quaternions
x = np.linspace(bottom,top,nn,True)
y = np.linspace(bottom,top,nn,True)
z = np.linspace(bottom,top,nn,True)

# make an initial grid of particles
ppos = []
for xx in x :
    for yy in y :
        for zz in z :
            ppos.append([xx,yy,zz])

# initialize particles a simple cubic array but sill in the sphere
for i, p in enumerate(system.particles):
    p.position = ppos[i];
    p.type=shape


# setup the MC integration
if shape == "Sphere":
    mc = hpmc.integrate.sphere(seed=seed, d=0.3);
    mc.shape_param.set(shape, diameter=2.0*r_circ);
else:
    mc = hpmc.integrate.convex_polyhedron(seed=seed, d=0.3, a=0.5);
    mc.shape_param.set(shape, vertices = verts)

# set up the tuner
particle_tuner = hpmc.util.tune(obj=mc, tunables=particle_tunables, max_val=max_part_moves, gamma=0.3)

# set up the wall
ext_wall = hpmc.field.wall(mc);
container=Sphere(ext_wall,cont_rad);

# dump pos frames to monitor the compression
# pos = dump.pos(str(shape)+"_"+str(N)+"_"+str(phi_final)+"_"+str(scale)+"_"+str(steps)+"_comp"+".pos", period=int(comp_dump_period), addInfo=container.container_def);
pos = dump.pos(str(shape)+"_"+str(N)+"_"+str(phi_final)+"_"+str(scale)+"_"+str(steps)+"_comp"+".pos", period=int(comp_dump_period));
if shape == "Sphere":
    pos.set_def(typ=shape, shape="sphere %f"%(2.0*r_circ)+" ffff0000");
else:
    mc.setup_pos_writer(pos, colors=dict(A='ffff0000'));

# log listed parameters
analyze.log(filename=str(shape)+'_'+str(N)+'_'+str(phi_final)+'_'+str(scale)+'_'+str(steps)+"_comp"+'.log',
    quantities=['hpmc_translate_acceptance',
                'hpmc_overlap_count',
                'time',
                'lx',
                'hpmc_sweep',
                'hpmc_wall_sph_rsq-0'],
    period=int(comp_dump_period),
    overwrite=True);

# metadata
now=datetime.datetime.now()
date_string=str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(now.hour)+"-"+str(now.minute)
# metadata = meta.dump_metadata(filename = date_string+".json", user = {"seed":seed})

r_final = pow(N*volume*3.0/4.0/math.pi/phi_final, 1./3);

m = 0

while (cont_rad > r_final):

    print(cont_rad)

    run(equil_time)
    m += equil_time

    cont_rad=max(scale*cont_rad, r_final);
    update.box_resize(Lx=2.0*cont_rad*cont_scale, Ly=2.0*cont_rad*cont_scale, Lz=2.0*cont_rad*cont_scale, period=None); # box resize is not required but is good to redo domain decomp.
    container.modify(cont_rad);

    # run the tuner for a second to get appropriate mc move sizes. is this enough tuning?
    for i in range(4):
        run(tuner_period, quiet=True)
        particle_tuner.update()
        m += tuner_period

    overlaps=mc.count_overlaps();
    wall_overlaps=container.ext_wall.count_overlaps();
    while overlaps+wall_overlaps > 0:
        run(100, quiet=True);
        overlaps = mc.count_overlaps();
        wall_overlaps = container.ext_wall.count_overlaps();
        m += 100


# dump pos frames to monitor the compression
pos = dump.pos(str(shape)+"_"+str(N)+"_"+str(phi_final)+"_"+str(scale)+"_"+str(steps)+".pos", period=int(dump_period), addInfo=container.container_def);
if shape == "Sphere":
    pos.set_def(typ=shape, shape="sphere %f"%(2.0*r_circ)+" ffff0000");
else:
    mc.setup_pos_writer(pos, colors=dict(A='ffff0000'));

# log listed parameters
analyze.log(filename=str(shape)+'_'+str(N)+'_'+str(phi_final)+'_'+str(scale)+'_'+str(steps)+'.log',
            quantities=['hpmc_translate_acceptance',
                        'hpmc_overlap_count',
                        'time',
                        'lx',
                        'hpmc_sweep',
                        'sph_wall_rsq-0'],
            period=int(dump_period),
            overwrite=True);

# run
run(steps);
m += steps;
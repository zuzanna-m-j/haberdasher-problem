import numpy as np
import random
import gsd.hoomd
import hoomd
import os


def CleanUp(name):

    cmd = f'rm {name}_traj.gsd'
    cmd2 = f'rm {name}_log.gsd'
    os.system(f'rm initial_lattice.gsd')
    os.system(cmd)
    os.system(cmd2)

CleanUp('blank')

cpu = hoomd.device.CPU()
simulation = hoomd.Simulation(device=cpu,seed = 1)
integrator = hoomd.hpmc.integrate.ConvexPolygon(default_d= 0.2, default_a=0.2)
A = [(-0.21799013664766403, -0.5023571793344106),(0.43806861572454686, 0.25235264134888885),(-0.21996612497820883, 0.2506258175372971)]
B = [(-0.5845343621823524, -0.12771177916537713),(0.4002733778408708, -0.30136003049648535),(0.3889689778694574, 0.26161490951675265),(-0.2689354095542138, 0.24840434931275862)]
C = [(0.37900872267547725, -0.35788779037693047),(0.05343979731237958, 0.587630519777832),(-0.28050392925997647, 0.20347157435381596),(-0.2790260172522079, -0.3596149095167526)]
D = [(-0.5592972649748391, 0.48861096202561094),(-0.22549069130706167, -0.45403063019074075),(0.4325039292599765, -0.446561949111819),(0.4239575873822218, 0.30637513866397204)]


integrator.shape['A'] = dict(vertices = A)
integrator.shape['B'] = dict(vertices = B)
integrator.shape['C'] = dict(vertices = C)
integrator.shape['D'] = dict(vertices = D)

simulation.operations.integrator = integrator

#Square dimensions: x-span: 1.3521188387767291, y-span: 1.3612298190335053
#[(2-0.451, 0.419,0), (2.269, 0.419,0), (2-0.391, -0.321, 0), (2.239, -0.221, 0 )]
vx = 1.4
vy = 1.4
c = 0.72
d = 0.7
positions =[]

for i in range(-5,5):
    for j in range(-5,5):
        positions.append((c-0.451 + i * vx, d +0.419 + j * vy, 0))
        positions.append((c + 0.269 + i * vx,d + 0.419  + j * vy, 0))
        positions.append((c -0.391 + i * vx, d -0.321  + j * vy, 0))
        positions.append((c +0.239 + i * vx, d -0.221  + j * vy, 0 ))

snapshot = gsd.hoomd.Snapshot()
snapshot.particles.N = 400
snapshot.particles.position = positions
snapshot.particles.orientation = [(1,0,0,0)] * 400
snapshot.particles.typeid = [0,1,2,3] * 100
snapshot.particles.types = ['A','B','C','D']
snapshot.configuration.box = [14.15, 14.15, 0, 0, 0, 0]

with gsd.hoomd.open(name='initial_lattice.gsd', mode='xb') as f:
    f.append(snapshot)


simulation.create_state_from_gsd(filename='initial_lattice.gsd')

main_logger = hoomd.logging.Logger()
main_logger.add(integrator, quantities=['type_shapes'])
main_writer = hoomd.write.GSD(filename=f'blank_traj.gsd',
                             trigger=hoomd.trigger.Periodic(1),
                             mode='xb',
                             filter=hoomd.filter.All(),
                             log=main_logger)
simulation.operations.writers.append(main_writer)

sdf = hoomd.hpmc.compute.SDF(dx = 1e-4,xmax= 0.02)
sdf_logger = hoomd.logging.Logger()
sdf_logger.add(sdf, quantities=['betaP'])
sdf_writer = hoomd.write.GSD(filename=f'blank_log.gsd',
                             trigger=hoomd.trigger.Periodic(100),
                             mode='xb',
                             filter=hoomd.filter.Null(),
                             log = sdf_logger)
simulation.operations.writers.append(sdf_writer)
simulation.operations.computes.append(sdf)

simulation.run(1e3)
#
# initial_box = simulation.state.box
# final_box = hoomd.Box.from_box(initial_box)
# final_box.volume = particle_number/4 * combined_area / final_packing_fraction
# box_compression = hoomd.hpmc.update.QuickCompress(trigger=hoomd.trigger.Periodic(10),
#                                            target_box=final_box)
# simulation.operations.updaters.append(box_compression)
#
# tuner = hoomd.hpmc.tune.MoveSize.scale_solver(moves=['a', 'd'],
#                                              target=0.2,
#                                              trigger=hoomd.trigger.Periodic(10),
#                                              max_translation_move=0.2,
#                                              max_rotation_move=0.2)
# simulation.operations.tuners.append(tuner)
#
# while not box_compression.complete and simulation.timestep < 1e6:
#     simulation.run(100)
#
# simulation.run(1e5)
# print(f"Final packing fraction: {(combined_area * particle_number/4)/simulation.state.box.volume}")

traj = gsd.hoomd.open('blank_traj.gsd', 'rb')
print(traj[0].particles.orientation)
print(traj[-1].particles.orientation)

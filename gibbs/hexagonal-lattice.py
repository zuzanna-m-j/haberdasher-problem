F_pressure = True
p_start = 55.0

import hoomd
import hoomd.hpmc
import numpy as np
import random


file = 'square-lattice-output'
seed = random.randint(1,1e7)

vAs = [(-0.21799013664766403, -0.5023571793344106),(0.43806861572454686, 0.25235264134888885),(-0.21996612497820883, 0.2506258175372971)]
vBs = [(-0.5845343621823524, -0.12771177916537713),(0.4002733778408708, -0.30136003049648535),(0.3889689778694574, 0.26161490951675265),(-0.2689354095542138, 0.24840434931275862)]
vCs = [(0.37900872267547725, -0.35788779037693047),(0.05343979731237958, 0.587630519777832),(-0.28050392925997647, 0.20347157435381596),(-0.2790260172522079, -0.3596149095167526)]
vDs = [(-0.5592972649748391, 0.48861096202561094),(-0.22549069130706167, -0.45403063019074075),(0.4325039292599765, -0.446561949111819),(0.4239575873822218, 0.30637513866397204)]


######
hoomd.context.initialize("--mode=cpu")

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

sx = 1.9070982572923945/2 + 0.15
ux = 1.9070982572923945/2 + 0.15
sy = 1.7620793290096557 + 0.075

n = 12
system = hoomd.init.create_lattice(unitcell=uc, n=n)
mc = hoomd.hpmc.integrate.convex_polygon(d=0.2, a=0.2, seed=seed)


mc.shape_param.set('As', vertices=vAs)
mc.shape_param.set('Bs', vertices=vBs)
mc.shape_param.set('Cs', vertices=vCs)
mc.shape_param.set('Ds', vertices=vDs)

gsd = hoomd.dump.gsd(file + ".gsd",
                   period=100,
                   group=hoomd.group.all(),
                   overwrite=True,)

gsd.dump_shape(mc)
hoomd.analyze.log(filename=file + '.vol', quantities=['volume', 'N'], period=100, overwrite=True)
hoomd.hpmc.analyze.sdf(mc=mc, filename=file + '.sdf', xmax=0.01, dx=1e-5, navg=100, period=100, overwrite=True)
move_tuner = hoomd.hpmc.util.tune(mc, tunables=['d', 'a'], target=0.2, gamma=0.5)
for _ in range(100):
    hoomd.run(1e3)
    move_tuner.update()

if F_pressure == True:
    boxMC = hoomd.hpmc.update.boxmc(mc, betaP=p_start, seed=12345)
    boxMC.volume(delta=1.0, weight=1.0)
    v_tuner = hoomd.hpmc.util.tune_npt(boxMC, tunables=['dV'], target=0.3, gamma=3.0)
    for _ in range(100):
        hoomd.run(1000)
        v_tuner.update()

        betaP = np.arange(p_start, 0.1, -0.1)
        for i in range(1,len(betaP)):
            p = betaP[i]
            boxMC.set_betap(p)
            for _ in range(100):
                hoomd.run(1000)
                v_tuner.update()
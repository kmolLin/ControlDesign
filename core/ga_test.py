# -*- coding: utf-8 -*-

import os
from ga_algorithm.planpath import build_path
from ga_algorithm.rga import Genetic
from ga_algorithm.kinematic import forward_kinematic
from time import time
from vrep_commucation.vrepper import vrepper

t0 = time()
Target= [(150, 0, 300), (155, 0, 300), (160, 0, 300)]
func = build_path({'Target':Target})
GeneticPrams = {'nPop':500, 'pCross':0.95, 'pMute':0.05, 'pWin':0.95, 'bDelta':5.,'maxGen':1000 , 'report':0}
foo = Genetic(func, GeneticPrams)
angles, f = foo.run()
print(time()-t0)

for angle in angles:
    print(tuple(round(v, 4) for v in forward_kinematic(angle)))
    

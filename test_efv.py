#!/usr/bin/env python3

import re
import os
import sys
import argparse
import numpy as np
from glob import glob
from deepmd.Data import DeepmdData
from deepmd import DeepEval
from deepmd import DeepPot
from deepmd import DeepDipole
from deepmd import DeepPolar
from deepmd import DeepWFC
from tensorflow.python.framework import ops
from monty.serialization import dumpfn,loadfn

def l2err (diff) :    
    return np.sqrt(np.average (diff*diff))

def test_ener (dp,system,set_prefix='set',numb_test=100000,shuffle_test=False,rand_seed=None, detail_file='detail') :
    if rand_seed is not None :
        np.random.seed(rand_seed % (2**32))

    data = DeepmdData(system, set_prefix, shuffle_test = shuffle_test, type_map = dp.get_type_map())
    data.add('energy', 1, atomic=False, must=False, high_prec=True)
    data.add('force',  3, atomic=True,  must=False, high_prec=False)
    data.add('virial', 9, atomic=False, must=False, high_prec=False)
    if dp.get_dim_fparam() > 0:
        data.add('fparam', dp.get_dim_fparam(), atomic=False, must=True, high_prec=False)
    if dp.get_dim_aparam() > 0:
        data.add('aparam', dp.get_dim_aparam(), atomic=True,  must=True, high_prec=False)

    test_data = data.get_test ()
    natoms = len(test_data["type"][0])
    nframes = test_data["box"].shape[0]
    numb_test = min(nframes, numb_test)
    coord = test_data["coord"][:numb_test].reshape([numb_test, -1])
    box = test_data["box"][:numb_test]
    atype = test_data["type"][0]
    if dp.get_dim_fparam() > 0:
        fparam = test_data["fparam"][:numb_test] 
    else :
        fparam = None
    if dp.get_dim_aparam() > 0:
        aparam = test_data["aparam"][:numb_test] 
    else :
        aparam = None

    energy, force, virial, ae, av = dp.eval(coord, box, atype, fparam = fparam, aparam = aparam, atomic = True)
    energy = energy.reshape([numb_test,1])
    force = force.reshape([numb_test,-1])
    virial = virial.reshape([numb_test,9])
    ae = ae.reshape([numb_test,-1])
    av = av.reshape([numb_test,-1])

    l2e = (l2err (energy - test_data["energy"][:numb_test].reshape([-1,1])))
    l2f = (l2err (force  - test_data["force"] [:numb_test]))
    l2v = (l2err (virial - test_data["virial"][:numb_test]))
    l2ea= l2e/natoms
    l2va= l2v/natoms



    if detail_file is not None :
        pe = np.concatenate((np.reshape(test_data["energy"][:numb_test]/natoms, [-1,1]),
                             np.reshape(energy/natoms, [-1,1])), 
                            axis = 1)
        np.savetxt(detail_file+".e.out", pe, 
                   header = 'data_e pred_e')
        pf = np.concatenate((np.reshape(test_data["force"] [:numb_test], [-1,3]), 
                             np.reshape(force,  [-1,3])), 
                            axis = 1)
        np.savetxt(detail_file+".f.out", pf,
                   header = 'data_fx data_fy data_fz pred_fx pred_fy pred_fz')
        pv = np.concatenate((np.reshape(test_data["virial"][:numb_test], [-1,9]), 
                             np.reshape(virial, [-1,9])), 
                            axis = 1)
        np.savetxt(detail_file+".v.out", pv,
                   header = 'data_vxx data_vxy data_vxz data_vyx data_vyy data_vyz data_vzx data_vzy data_vzz pred_vxx pred_vxy pred_vxz pred_vyx pred_vyy pred_vyz pred_vzx pred_vzy pred_vzz')        
    return numb_test ,l2e, l2ea, l2f, l2v, l2va


if __name__=="__main__":
    import os
    if os.path.isdir('ret'):
        pass
    else:
        os.mkdir('ret')
    model="frozen_model.pb"
    print ("#Index Ntest  E_L2err  E_L2err/Natoms  F_L2err V_L2err V_L2err/Natoms")
    dp = DeepPot(model)
    fs=glob("/home/dgx/haidi/work/Li/iter.00*/02.fp/data.*")
    fs.sort()
    fs_ret=dict(zip(range(len(fs)),fs))
    dumpfn(fs_ret,'fs.json',indent=4)
    for i,system in enumerate(fs):
        try:
            numb_test ,l2e, l2ea, l2f, l2v, l2va =test_ener (dp,
                    system,
                    set_prefix='set',
                    numb_test=100000,
                    shuffle_test=False,
                    rand_seed=None,
                    detail_file=os.path.join('ret',str(i)))
            print("{:d}\t{:d}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}".format(i, numb_test,l2e, l2ea, l2f, l2v, l2va))
        except:
            print("error %s"%system)

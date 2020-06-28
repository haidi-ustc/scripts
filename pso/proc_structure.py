# -*- coding: utf-8 -*-
import os
import sys
from pymatgen import Composition,Structure
from pymatgen.entries.computed_entries import ComputedEntry
from pymatgen.io.vasp import Vasprun,Poscar
from monty.serialization import dumpfn,loadfn
import glob
import numpy as np
sys.path.append("/home/me/soft/CALYPSO_x64_6.0/Tools/CALYPSO_ANALYSIS_KIT")
from cak import *
from multiprocessing import Pool
def worker(paths):
    cwd=os.getcwd()
    for path in paths:
       os.chdir(path)
       nume=map(int,path.split('/')[-2].split('-')[1].split('_'))
       comp0='Mg'+str(nume[1])+'Al'+str(nume[0])+'-new.json'
       comp1='Al'+str(nume[0])+'Mg'+str(nume[1])+'-new.json'
       if os.path.exists(comp0) or os.path.exists(comp1):
          os.chdir(cwd)
          return

       (sysname, name_ele, npop, mol, hard, vsc, vsce, d2, cl, hm, lsur, bg, xrd, ts, num_neb) = readinput()
       struct = parseStruct()
       structure = struct[:]
       structure.sort(key=lambda x:x[0])
       ele_num=structure[0][4][2]
       ele_tol=sum(ele_num)
       ele=["Al","Mg"]
       sp=[]
       for el,num in zip(ele,ele_num):
           sp.extend([el]*num)
       comp=ele[0]+str(ele_num[0])+ele[1]+str(ele_num[1])
       E_al=-3.744576  # dft-3.74654110;
       E_mg=-1.5358274444444444 #
       fa=0.02 # 20 meV/atom
       energies=[st[0] for st in structure]
       
       ef=np.array([(ii*ele_tol-ele_num[0]*E_al-ele_num[1]*E_mg)/ele_tol for ii in energies])
       idx=np.where(ef<fa)
       sel_sts=[structure[i] for i in idx[0].tolist()]
       print('effect_struct')
       print(len(sel_sts))
       entries=[]
       for st in sel_sts:
           pst=Structure(st[4][0],sp,st[4][1],coords_are_cartesian=False)
           comp=str(pst.composition).replace(' ','')
           entry=ComputedEntry(comp,st[0]*ele_tol,parameters={"potcar_symbols":['pbe Al','pbe Mg']},data={'path':'.','st':pst})
           entries.append(entry)
           #pos=Poscar(pst, str(st[0]))
       dumpfn(entries,comp+'-new.json')
       os.chdir(cwd) 
    print('------------count is %s-----------------'%df)

if __name__ == '__main__':
    _l = glob.glob('/home/me/mgal/paper/download/sys-*/results')
    pool = Pool(processes=4)
    for i in _l:
        ret=pool.apply_async(worker,([i],))
    pool.close()
    pool.join()
    if ret.successful():
       print('finished')


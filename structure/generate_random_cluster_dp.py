import os
import time
from ase import Atoms
from ase.optimize import BFGS
from pprint import pprint
from deepmd.calculator import DP
from pymatgen.io.ase import AseAtomsAdaptor,Structure
from pyxtal.symmetry import get_symbol_and_number
from pymatgen.io.cif import CifWriter
from pymatgen.symmetry.analyzer import PointGroupAnalyzer
from pyxtal.crystal import random_crystal, random_crystal_1D, random_crystal_2D, random_cluster
from pymatgen import Molecule,Structure
import numpy as np
from monty.serialization import loadfn,dumpfn
import random
vac=15
calc=DP(model="frozen_model.pb",type_dict={'Au':0})

def gen_cluster(system,numIons,sg=None,dimension=0,factor=1.0):
    #space group
    random.seed(int(time.time()*1e5))
    if sg:
       pass
    else:
       sg=random.choice(range(1,57))
    symbol, sg = get_symbol_and_number(sg, dimension)

    numIons0 = np.array(numIons)
    cluster = random_cluster(sg, system, numIons0, factor)
    if cluster.valid:
       comp = str(cluster.struct.composition)
       comp = comp.replace(" ", "")
       #outpath ='./' + comp + '.xyz'
       #print('out file name %s'%outpath)
       #cluster.molecule.to('xyz,', outpath)
       #cluster.to_file(filename = outpath, fmt='xyz')
       #mol=Molecule.from_file(outpath)
       mol=cluster.molecule
       ans = PointGroupAnalyzer(mol).sch_symbol
       print('Symmetry requested: {:d}({:s}), generated: {:s}'.format(sg, symbol, ans))
       a=max(mol.cart_coords[:,0])-min(mol.cart_coords[:,0])
       b=max(mol.cart_coords[:,1])-min(mol.cart_coords[:,1])
       c=max(mol.cart_coords[:,2])-min(mol.cart_coords[:,2])
       lx,ly,lz=sorted([a,b,c])
       if lz/ly>2 or ly/lx>2 or lz/lx>2:
          print('too long')
          return None
       st=mol.get_boxed_structure(a+vac,b+vac,c+vac)
       #st.to('POSCAR','rand_'+comp+'.vasp')
       #print(st)
       print('valid')
       return st
    else:
       print('cannot generate corresponding structure, retry it!')
       return None

def opt(st):
   comp = str(st.composition)
   comp = comp.replace(" ", "")
   aaa=AseAtomsAdaptor()
   atoms=aaa.get_atoms(st)
   atoms.set_calculator(calc)
   dyn = BFGS(atoms)
   #dyn = BFGS(atoms,trajectory=comp+'.traj')
   ret=dyn.run(fmax=0.01,steps=800)
   if ret:
      aaa.get_structure(atoms)
      return aaa.get_structure(atoms)
   else:
      return None
#   opted.to('poscar','rand_'+comp+'_opted.vasp')

atom_range=range(10,41)
perturb_numb=10
sg_numb=6

system=["Au"]
#cluster dimension=0
dimension=0
#scaling fator ,default 1.0
factor=1.0
all_sts={}
for i in atom_range:
    print('---------'+str(i)+'-----------------')
    sts=[]
    #numatom atoms
    numIons=[i]          
    while True:
        try:
           st=gen_cluster(system,numIons,sg=None,dimension=0,factor=1.0) 
           if st is not None:
                opted=opt(st)
                if opted is not None:
                   mol=Molecule(opted.species,opted.cart_coords)
                   a=max(mol.cart_coords[:,0])-min(mol.cart_coords[:,0])
                   b=max(mol.cart_coords[:,1])-min(mol.cart_coords[:,1])
                   c=max(mol.cart_coords[:,2])-min(mol.cart_coords[:,2])
                   opted=mol.get_boxed_structure(a+vac,b+vac,c+vac)
                   min_dist=(np.eye(len(opted))*1000+opted.distance_matrix).min()
                   if min_dist <2.0:
                      continue
                   opted.to('poscar','init_clusters/N-'+str(i)+'-sg-'+str(len(sts))+'.vasp')
                   sts.append({'origin':st,'opted':opted})
        except:
           pass
        if len(sts)>=sg_numb:
           break
    all_sts[i]=sts         
dumpfn(all_sts,'all.json',indent=4)

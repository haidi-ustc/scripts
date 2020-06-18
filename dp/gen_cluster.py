import os

import traceback

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

calc=DP(model="frozen_model.pb",type_dict={'Pt':0})
def gen_cluster(system,numIons,sg=None,dimension=0,factor=1.0):
    #space group
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

       xmax=mol.cart_coords[:,0].max()
       xmin=mol.cart_coords[:,0].min()
       ymax=mol.cart_coords[:,1].max()
       ymin=mol.cart_coords[:,1].min()
       zmax=mol.cart_coords[:,2].max()
       zmin=mol.cart_coords[:,2].min()
       lx=xmax-xmin
       ly=ymax-ymin
       lz=zmax-zmin
       _a,_b,_c=sorted([lx,ly,lz])
       if _b/_a>2 or _c/_b>2 or _c/_a>2:
           print("too long")
           return None

       ans = PointGroupAnalyzer(mol).sch_symbol
       print('Symmetry requested: {:d}({:s}), generated: {:s}'.format(sg, symbol, ans))
       #a=b=c=np.max(mol.distance_matrix)+10
       a=lx+10
       b=ly+10
       c=lz+10
       st=mol.get_boxed_structure(a,b,c)
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
   #atoms.set_calculator(DP(model="frozen_model.pb",type_dict={'Pt':0}))
   dyn = BFGS(atoms)
   #dyn = BFGS(atoms,trajectory=comp+'.traj')
   ret=dyn.run(fmax=1e-4,steps=1000)
   if ret:
      aaa.get_structure(atoms)
      return aaa.get_structure(atoms)
   else:
      return None
#   opted.to('poscar','rand_'+comp+'_opted.vasp')

atom_range=range(10,41)
perturb_numb=10
sg_numb=6

#element ['Cu','O'] for more than 1 elemnts
system=["Pt"]
#cluster dimension=0
dimension=0
#scaling fator ,default 1.0
factor=1.0
all_sts={}
for i in atom_range:
    print('---------'+str(i)+'-----------------')
    sts=[]
#    for j in range(sg_numb):
    #numatom atoms
    numIons=[i]          
    while True:
        try:
           st=gen_cluster(system,numIons,sg=None,dimension=0,factor=1.0) 
           if st is not None:
                opted=opt(st)
                if opted is not None:
                   mol=Molecule(opted.species,opted.cart_coords)
                   a=b=c=np.max(mol.distance_matrix)+10
                   opted=mol.get_boxed_structure(a,b,c)
                   opted.to('poscar','structs/N-'+str(i)+'-sg-'+str(len(sts))+'.vasp')
                   sts.append({'origin':st,'opted':opted})
        
        except Exception as e:
               traceback.print_exc()
               info = traceback.format_exc()
               print(info)

        if len(sts)>=sg_numb:
           break
    all_sts[i]=sts         
dumpfn(all_sts,'all.json',indent=4)

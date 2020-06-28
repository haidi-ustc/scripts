import os
from ase import Atoms
from ase.optimize import BFGS
from deepmd.calculator import DP
from pymatgen.io.ase import AseAtomsAdaptor,Structure
from pymatgen import Molecule,Structure
import numpy as np
from monty.serialization import loadfn,dumpfn
import random

st=Structure.from_file("rand_Cu16.vasp")
comp = str(st.composition)
comp = comp.replace(" ", "")
aaa=AseAtomsAdaptor()
atoms=aaa.get_atoms(st)
atoms.set_calculator(DP(model="frozen_model.pb",type_dict={'Cu':0}))
dyn = BFGS(atoms)
#dyn = BFGS(atoms,trajectory=comp+'.traj')
dyn.run(fmax=1e-4)
aaa.get_structure(atoms)
opted=aaa.get_structure(atoms)

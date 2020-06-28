from ase import Atoms
from ase.optimize import BFGS
from ase.io import read
from deepmd.calculator import DP

calc=DP(model="frozen_model.pb",type_dict={'Pt':0})
atoms=read('POSCAR')
atoms.set_calculator(calc)
dyn = BFGS(atoms)
ret=dyn.run(fmax=1e-4,steps=1)


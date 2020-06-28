from pymatgen import Molecule
from glob import glob
from ase.io import read
fs=glob('*.mol')
vac=10
for f in fs:
    print(f)
    atom=read(f)
    mol=Molecule(atom.get_chemical_symbols(),atom.get_positions())
    x=mol.cart_coords[:,0]
    y=mol.cart_coords[:,1]
    z=mol.cart_coords[:,2]
    a=x.max()-x.min()
    b=y.max()-y.min()
    c=z.max()-z.min()
    st=mol.get_boxed_structure(a+vac,b+vac,c+vac)
    st.to('cif',f.replace('mol','cif'))

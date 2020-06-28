from pymatgen import Element,Structure,Molecule
import numpy as np
from glob import glob
fs=glob("*.vasp")
for f in fs:
    st=Structure.from_file(f)
    for i in range(4):
        stb=st.copy()
        stb.perturb(0.1)
        fname='P-'+str(i)+'-'+f
        stb.to('poscar',fname)
        min_dist=(np.eye(len(stb))*1000+stb.distance_matrix).min()
        if min_dist <2.0:
           print(fname) 


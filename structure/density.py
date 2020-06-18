import numpy as np
from maptool.core.analysis import rdf
from dpdata import System
ls=System('dump_nvt_470.atom',fmt='lammps/dump',type_map=['Li'])
sls=ls.sub_system(range(1000,len(ls)))
pmg_sts=sls.to_pymatgen_structure()
d=[st.density for st in pmg_sts]
print(np.mean(d))


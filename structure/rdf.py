import numpy as np
from maptool.core.analysis import rdf
from dpdata import System
ls=System('dump_npt_470.atom',fmt='lammps/dump',type_map=['Li'])
sls=ls.sub_system(range(int(0.5*len(ls)),len(ls)))
pmg_sts=sls.to_pymatgen_structure()
d=[st.density for st in pmg_sts]

print(np.std(d))
print(np.mean(d))
rdf, radii=rdf(pmg_sts,10,200,(0,10))
ret=np.vstack((radii,rdf)).T
print(ret.shape)
np.savetxt('rn.txt',ret)

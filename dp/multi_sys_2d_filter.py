from dpdata import LabeledSystem,MultiSystems
from glob import glob
from tqdm import tqdm
"""
process multi systems
"""
fs=glob('iter.0000[3-5]*/02.fp/task*/OUTCAR')
maxf=1.0
ms=MultiSystems()
ic=0
for f in tqdm(fs):
    try:
        ls=LabeledSystem(f)
    except:
        print(f)
    if len(ls)>0:
        st=ls.to_pymatgen_structure()[0]
        z=st.cart_coords[:,2]
        if st.lattice.c-(z.max()-z.min())<14:
            pass
        else:
            if ls.sub_system([0]).data['forces'].max() >maxf:
               pass
            else:
               ic+=1
               ms.append(ls)

print(len(fs))
print(ic)
ms.to_deepmd_raw('deepmd-f%s'%maxf)
ms.to_deepmd_npy('deepmd-f%s'%maxf)

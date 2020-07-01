from dpdata import LabeledSystem,MultiSystems
from dpgen.generator.run import check_cluster
from glob import glob
from tqdm import tqdm
"""
process multi systems
"""
fs=glob('iter.0000[4-7]*/02.fp/task*/OUTCAR')
maxf=3.0
ms=MultiSystems()
ic=0
vacuum_size=13
for f in tqdm(fs):
    if check_cluster(f.replace('OUTCAR','POSCAR'),vacuum_size,fmt='POSCAR'):
       print(f)
       continue
    try:
        ls=LabeledSystem(f)
    except:
        print(f)
        continue
    if len(ls)>0:
        if ls.sub_system([0]).data['forces'].max() >maxf:
           pass
        else:
           ic+=1
           ms.append(ls)

print(len(fs))
print(ic)
ms.to_deepmd_raw('deepmd-f%s'%maxf)
ms.to_deepmd_npy('deepmd-f%s'%maxf)

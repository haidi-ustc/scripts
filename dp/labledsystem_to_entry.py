from glob import glob
from dpdata import LabeledSystem
from monty.serialization import dumpfn,loadfn
from tqdm import tqdm
fs=glob('usefull-[1-3]/sys-*/OUTCAR')
entries=[]
for f in tqdm(fs):
    ls=LabeledSystem(f)
    ls.sub_system([-1]).to_pymatgen_ComputedStructureEntry()
    entry=ls.sub_system([-1]).to_pymatgen_ComputedStructureEntry()[0]
    entries.append(entry)
dumpfn(entries,'all-vasp-entries.json')

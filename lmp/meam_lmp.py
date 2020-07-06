from glob import glob
from dpdata import LabeledSystem,System
from pymatgen import Structure
import os
from monty.serialization import dumpfn,loadfn

paths=loadfn("ret.json")
f1="""
clear
atom_style atomic 
units metal
boundary p p p 
atom_modify sort 0 0.0 
box tilt large

read_data lmp.conf

### interactions
pair_style meam/c
pair_coeff * * ../library.meam AlS SiS MgS CuS FeS ../AlSiMgCuFe.meam AlS MgS
"""
f3="""
### run
fix fix_nve all nve
dump dump_all all custom 1 dump.dat id type x y z vx vy vz fx fy fz
thermo_style custom step press ke pe etotal vol lx ly lz atoms
thermo_modify flush yes format float %15.8g
thermo 1
run 0
"""
pwd=os.getcwd()
#fs=["Mg2Al10-2-170.vasp"]
#fs=["Mg9-166-23.vasp"]
#fs=["Al4-225-24.vasp"]
paths=["1.03"]
for path in paths:
    os.chdir(path)
    s=System('CONTCAR',fmt='poscar')
    st=s.copy()
    etyp=s.get_atom_names()
    s.apply_type_map(['Al','Mg'])
    s.to_lammps_lmp('lmp.conf')
    if etyp==['Al']:
        f2="""
mass 1 26.981538 
"""
    else :
        f2="""
mass 1 26.981538 
mass 2 24.305000 
"""
    with open('in.lmp','w') as fid:
        fid.write(f1+f2+f3)
    os.system('/fs0/home/haidi/dev/lammps-3Mar20/src/lmp_mpi -in in.lmp >out.log ')
    with open('log.lammps', 'r') as fid:
         s=fid.readlines()
    try:
      eng=float(s[s.index('Step Press KinEng PotEng TotEng Volume Lx Ly Lz Atoms \n')+1].split()[3])
      #print("%20s\t%.6f"%(f,eng/sum(st.get_atom_numbs())))
      print("%s is ok"%path) 
    except:
      eng=0
      print("%s fails"%path) 
      #print("%20s\t%.6f"%(f,0000))
    dumpfn(eng,'eng.json')
    os.chdir(pwd)
  

from pymatgen.io.vasp import Incar,Poscar,Kpoints,Potcar
from monty.serialization import loadfn,dumpfn
potd={"Li":"Li_sv","Be":"Be","B":"B","C":"C","Mg":"Mg","Al":"Al",
      "Si":"Si","P":"P","S":"S","Ti":"Ti_sv","Cu":"Cu",
      "Zn":"Zn","Ge":"Ge_d","Zr":"Zr_sv","Nb":"Nb_pv","Ag":"Ag",
      "Sn":"Sn_d","Ta":"Ta_pv","W":"W_sv","Pt":"Pt","Au":"Au"}
print(potd.keys())
dumpfn(potd,'pp.json',indent=4)
incars=["INCAR_metal_md", "INCAR_metal_rlx", "INCAR_metal_scf", "INCAR_semi_scf"]
for incar in incars:
    incar_handle=Incar.from_file(incar)
    dumpfn(incar_handle.as_dict(),incar+'.json',indent=4)

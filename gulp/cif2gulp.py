from gulp_caller import *
from pymatgen import Structure
from pymatgen.io.cif import CifParser
import sys

def cif2gulp(fname):
  assert '.cif' in fname
  system=fname.split('.')[0]
  cif=CifParser(fname)
  _list= list(cif.as_dict().items())
  _,cifd =_list[0][0],_list[0][1]
  #st=Structure.from_file('2222.cif')
  go=GulpIO()
  l0=go.keyword_line("opti conp orthorhombic  noauto\n")
  l1=go.keyword_line("pressure 0 GPa")
  l2=go.keyword_line("ftol 0.0001")
  l3=go.keyword_line("gtol 0.001")
  l4=go.keyword_line("xtol 0.0001")
  l5=go.keyword_line("maxcyc 10000\n")
  
  lst=go.cif_structure_lines(cifd)+'\n'
  #st=go.structure_lines(st)
  ls=eval('+'.join(['l'+str(i) for i in range(6)]))
  lt=f"""title
GULP calculation for {system}
end\n
"""
  lp="""Species
C core C_R
Cu core Cu4+2
H core H_
N core N_3
O core O_2
Br core Br 
F core F_
S core S_R\n
"""
  
  ll=f"""library uff4mof.lib

dump {system}.grs
output cif {system}-relax
"""
  
  ret=ls+lt+lst+lp+ll
  with open(fname.replace('.cif','.in'),'w') as f:
      f.write(ret)

if __name__=="__main__":
   cif2gulp("2222.cif")

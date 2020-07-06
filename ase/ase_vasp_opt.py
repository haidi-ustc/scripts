#!/bin/bash
#MSUB -A emsla50834
#MSUB -l nodes=3:ppn=16,walltime=24:00:00
#MSUB -o out_%j.log
#MSUB -e out_%j.err
#MSUB -N vasp_job
#MSUB -m ea
#MSUB -V

############################################################################
# Print out some information for refund purposes
############################################################################

echo "refund: UserID = ${USER}"
echo "refund: Number of nodes          = 3"
echo "refund: Number of cores per node = 16"
echo "refund: Number of cores          = 48"
echo "refund: Amount of time requested = 18:00"
echo "refund: SLURM Job ID = ${SLURM_JOBID}"
echo "refund: Directory = ${PWD}"
echo " "
echo Processor list:
echo "${SLURM_JOB_NODELIST}"
echo " "

source /etc/profile.d/modules.bash
module purge 

ulimit -s unlimited

module load intel/14.0.3
module load impi/5.1.2.150
# export I_MPI_PROCESS_MANAGER=mpd
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so

# VASPBIN=${HOME}/apps/vasp/5.4.4/vasp_gam_dri
# VASPBIN=${HOME}/apps/vasp/5.4.4/vasp_ncl_dri
# VASPBIN=${HOME}/apps/vasp/5.4.4/vasp_std_dri
# VASPBIN=${HOME}/apps/vasp/5.4.4/vasp_vtst_gam
# VASPBIN=${HOME}/apps/vasp/5.4.4/vasp_vtst_ncl
# VASPBIN=${HOME}/apps/vasp/5.4.4/vasp_vtst_std
VASPBIN=${HOME}/apps/vasp/5.4.4/vasp_gam
# VASPBIN=${HOME}/apps/vasp/5.4.4/vasp_ncl
# VASPBIN=${HOME}/apps/vasp/5.4.4/vasp_std

cp  $VASPBIN              vasp
# [ -f vasp ] || cp  $VASPBIN              vasp
ln -sf ${HOME}/apps/vasp/5.4.4/vdw_kernel.bindat
 
############################################################################
# if [ ! -f ${TMPDIR}/vasp ]; then
#     cp  $VASPBIN              $TMPDIR/vasp
# fi
# if [ ! -d ${TMPDIR}/run ]; then
#     cp  $WORKDIR/INCAR        $TMPDIR
#     cp  $WORKDIR/POSCAR       $TMPDIR
#     cp  $WORKDIR/POTCAR       $TMPDIR
#     cp  $WORKDIR/KPOINTS      $TMPDIR
#     cp  -r $WORKDIR/run       $TMPDIR
# fi
#
#############################################################################
# Run code (or multiple codes by repeating the vasp command)
#############################################################################

# srun --wait=60 --kill-on-bad-exit  -n 48 -N 3 ./vasp
# srun --wait=60 --kill-on-bad-exit  ./vasp

# mpirun -n ${SLURM_NPROCS} ./vasp
# srun -n ${SLURM_NPROCS} ./vasp
# srun -n ${SLURM_NPROCS} ./vasp -h  130.20.235.2 -p  31416 
############################################################
python << EOF
import os
import numpy as np
from ase.io import read, write
from ase.calculators.vasp import Vasp
from ase.constraints import UnitCellFilter, FixBondLength
from ase.optimize import BFGS as QuasiNewton

os.environ['VASP_COMMAND'] = "srun -n ${SLURM_NPROCS} ./vasp"
os.environ['VASP_PP_PATH'] = "$HOME/apps/vasp/pp/"

# the starting configuration
geo  = read('init.vasp', format='vasp')
# setting the c-axis parameter
# geo.cell[-1,-1] = 20

calc = Vasp(
        ###############################
        # General
        ###############################
        system = 'vaspCalc',
        prec   = 'High',
        encut  = 400,
        ispin  = 1,
        istart = 0,
        icharg = 1,
        ###############################
        # Electronic relaxation
        ###############################
        # isym   = 0,
        algo   = 'Fast',
        nelmin = 4,
        nelm   = 120,
        xc     = 'pbe',
        ediff  = 1E-7,
        ismear = 0,
        sigma  = 0.1,
        npar   = 4,
        lorbit = 11,
        nelect = 1291,
        ###############################
        # k-points grid
        ###############################
        kpts   = (1, 1, 1),
        ###############################
        # Writing Flat
        ###############################
        nwrite = 1,
        lwave  = True,
        lcharg = True,
        ###############################
        # Vdw Correction
        ###############################
        ivdw   = 10,
        ###############################
        # Dipole Correction
        ###############################
        # ldipol = True,
        # idipol = 3,
        # dipol  = (0.5, 0.5, 0.5)
       )
geo.set_calculator(calc)

# stress mask [XX, YY, ZZ, YZ, XZ, XY]
# 0 if fixed else 1
# unf = UnitCellFilter(geo, mask=[1,1,1,1,1,1])
# unf = UnitCellFilter(geo, mask=[1,1,0,0,0,1])
ch_bond_fix = FixBondLength(129, 143)
geo.constraints += [ch_bond_fix]
dyn = QuasiNewton(geo, logfile='opt.log', trajectory='opt.traj')

dyn.run(fmax=0.01)

write('final.vasp', geo, vasp5=True, direct=True)
EOF

rm -rf vasp


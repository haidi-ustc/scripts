#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=40
#SBATCH -t 23:0:0
#SBATCH -w gpu04
#SBATCH --partition=gpu4 
#SBATCH --gres=gpu:1

export PATH=/software/soft/vasp-5.4.4:$PATH

source /public/intel/parallel_studio_xe_2018.1.038/psxevars.sh intel64
list="N-11-sg-0 N-12-sg-0 N-13-sg-0"
for i in $list
do 
cd $path
mkdir  $path/$i
cp $path/${i}.vasp $i/POSCAR
cp INCAR_metal_scf $i/INCAR
cp POTCAR_Au $i/POTCAR
cd $i
/public/intel/compilers_and_libraries_2018.1.163/linux/mpi/intel64/bin/mpirun -np 40 vasp_std
done

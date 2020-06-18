path=`pwd`
ppath=$path/structs
cd $ppath
list=`seq 10 11`
for i in $list
do 
  cd $path
  echo $i
  if [ ! -d $path/work/$i ]; then
     mkdir  $path/work/$i
  fi
  cd $path/work/$i
cat>sub.sh<<!
#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=40
#SBATCH -t 100:0:0
#SBATCH --partition=cpu

export PATH=/software/soft/vasp-5.4.4:\$PATH
source /public/intel/parallel_studio_xe_2018.1.038/psxevars.sh intel64
!
  cd $ppath
  listj=`ls *-${i}-*vasp` 
  for _j in $listj
  do 
  j=`basename ${_j} .vasp`
  mkdir $path/work/$i/$j
  cd  $path/work/$i/$j
  ln -s $ppath/${_j}  $path/work/$i/$j/POSCAR
  ln -s $path/INCAR .
  ln -s $path/POTCAR .

cat>>$path/work/$i/sub.sh<<!

cd $path/work/$i/$j
mpirun -n 40 vasp_std > runlog
echo $i-$j is ok
!
   done  
 cd $path/work/$i/
 sbatch sub.sh
done

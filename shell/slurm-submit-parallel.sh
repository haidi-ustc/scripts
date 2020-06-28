path=`pwd`
if [ ! -d $path/job ];then
  mkdir $path/job
fi
group_size=5
total_task=1495
numb_task=`python -c "print(int($total_task/$group_size)-1)"`
echo $numb_task
list=`seq 0 $numb_task`
for i in $list
do 
  k1=`echo "${group_size}*$i+1" | bc`
  k2=`echo "${group_size}*($i+1)" | bc`
  echo $k1 $k2
cat>$path/job/job-${i}-opt.sub<<!
#!/usr/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=28
#SBATCH --partition=cpu
#SBATCH --get-user-env
#SBATCH --job-name=AlMg-$i
#SBATCH --output=out-$i
#SBATCH --error=err-$i
#SBATCH --mem=200G
module load intel/2018.4
module load vasp/5.4.4


!
  for kk in `seq $k1 $k2`
  do
cat>>$path/job/job-${i}-opt.sub<<!
echo -----------sys-$kk----------
if [ -f $path/$kk/tago ];then
   echo "ok"
else
   cd $path/$kk/
   mpirun -np 28 vasp_std > runlog
   touch tago
fi

!
  done
cd $path/job
#sbatch job-${i}-opt.sub
done

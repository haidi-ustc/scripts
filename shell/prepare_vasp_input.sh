path=`pwd`
list=`ls -d $path/prim-*/*.vasp`
kk=1
for i in $list
do
  if [ ! -d $path/$kk ];then
    mkdir $path/$kk
  fi
   
  cd $path/$kk
  rm -f POSCAR INCAR POTCAR
  ln -s $i POSCAR
  ln -s $path/INCAR .
  ele=`sed -n 6p POSCAR`
  for i in $ele
  do
  cat $path/POT_$i >>POTCAR
  done
  let kk=kk+1
done

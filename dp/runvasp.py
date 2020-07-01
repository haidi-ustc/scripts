import os
import sys
import shutil
from glob import glob
from dpgen.remote.decide_machine import decide_fp_machine
from dpgen.dispatcher.Dispatcher import Dispatcher, make_dispatcher 
from monty.serialization import loadfn,dumpfn

def create_path (path,backup=False) :
    if  path[-1] != "/":
        path += '/'
    if os.path.isdir(path) :
        if backup:
           dirname = os.path.dirname(path)
           counter = 0
           while True :
               bk_dirname = dirname + ".bk%06d" % counter
               if not os.path.isdir(bk_dirname) :
                   shutil.move (dirname, bk_dirname)
                   break
               counter += 1
           os.makedirs (path)
           return path
        else:
           return path

    os.makedirs (path)
    return path
#--------------------------------------------------
pwd=os.getcwd()
work_path = os.path.join(pwd,'fp')

fs=glob(os.path.join(pwd,'configs','*.vasp'))
fs.sort()

for i in range(len(fs)):
    task_name="task.%05d"%i
    task_path=os.path.join(work_path,task_name)
    create_path(task_path)
    os.chdir(task_path)
    shutil.copyfile(os.path.abspath(fs[i]), os.path.basename(fs[i]))
    shutil.copyfile(os.path.basename(fs[i]),'POSCAR')
    shutil.copyfile(os.path.join(pwd,'INCAR'),'INCAR')
    shutil.copyfile(os.path.join(pwd,'POTCAR'),'POTCAR')
    shutil.copyfile(os.path.join(pwd,'KPOINTS'),'KPOINTS')
os.chdir(pwd)
#os._exit(0)
fp_tasks = glob(os.path.join(work_path, 'task.*'))
fp_tasks.sort()
run_tasks = [os.path.basename(ii) for ii in fp_tasks]
#----------------------------------------------------
forward_files = ['POSCAR', 'INCAR', 'POTCAR','KPOINTS']
backward_files = ['OUTCAR','vasprun.xml','CONTCAR']
forward_common_files=[]
mark_failure =False
log_file='runlog'
err_file='errlog'
mdata=loadfn('machine.json')
mdata  = decide_fp_machine(mdata)
#dumpfn(mdata,'new.json',indent=4)
fp_command = mdata['fp_command']
fp_group_size = mdata['fp_group_size']
#---------------------------------------------------


dispatcher = make_dispatcher(mdata['fp_machine'], 
                             mdata_resource=mdata['fp_resources'],
                             work_path=work_path, 
                             run_tasks=run_tasks, 
                             group_size=fp_group_size)
dispatcher.run_jobs(mdata['fp_resources'],
                        [fp_command],
                        work_path,
                        run_tasks,
                        fp_group_size,
                        forward_common_files,
                        forward_files,
                        backward_files,
                        mark_failure=mark_failure,
                        outlog = log_file,
                        errlog = err_file)


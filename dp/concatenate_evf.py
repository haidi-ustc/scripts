import numpy as np
from glob import glob
fs_f=glob("*.f.out")
fs_e=glob("*.e.out")
fs_v=glob("*.v.out")

for i,fs in enumerate(fs_e):
    if i==0:
        ret=np.loadtxt(fs)
        if ret.shape==(2,):
            ret=ret.reshape(1,-1)
    else:
        tmp=np.loadtxt(fs)
        if tmp.shape==(2,):
            tmp=tmp.reshape(1,-1)
        ret=np.concatenate((ret,tmp),axis=0)
print(ret.shape)
np.savetxt("all.e.out", ret, header = 'data_e pred_e')

for i,fs in enumerate(fs_f):
    if i==0:
        ret=np.loadtxt(fs)
        if ret.shape==(6,):
            ret=ret.reshape(1,-1)
    else:
        tmp=np.loadtxt(fs)
        if tmp.shape==(6,):
            tmp=tmp.reshape(1,-1)
        ret=np.concatenate((ret,tmp),axis=0)
np.savetxt("all.f.out", ret,
          header = 'data_fx data_fy data_fz pred_fx pred_fy pred_fz')

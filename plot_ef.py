import os
import numpy as np
from uuid import uuid4
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

shift=0.20
e=np.loadtxt('all.e.out')
emin,emax=e[:,0].min()*(1-shift),e[:,0].max()*(1+shift)
ex=ey=np.linspace(emin,emax,1000)
f=np.loadtxt('all.f.out')
fminx,fmaxx=f[:,0].min()*(1-shift),f[:,0].max()*(1+shift)
fminy,fmaxy=f[:,1].min()*(1-shift),f[:,1].max()*(1+shift)
fminz,fmaxz=f[:,2].min()*(1-shift),f[:,2].max()*(1+shift)

fx1=fy1=np.linspace(fminx,fmaxx,1000)
fx2=fy2=np.linspace(fminy,fmaxy,1000)
fx3=fy3=np.linspace(fminz,fmaxz,1000)

fig, axs = plt.subplots(2, 2, constrained_layout=False)
#fig, axs = plt.subplots(2, 2, constrained_layout=True)

print(axs)

axs[0][0].plot(ex, ey, '-', e[:,0], e[:,1], 'o')
axs[0][0].set_title('Energy')
axs[0][0].set_xlabel('DFT Energy (eV/atom)')
axs[0][0].set_ylabel('DP Energy (eV/atom)')
#fig.suptitle('This is a somewhat long figure title', fontsize=16)

axs[0][1].plot(fx1,fy1,'-', f[:,0],f[:,3], 'o')
axs[0][1].set_title('Force x')
axs[0][1].set_xlabel(r'DFT Force (eV/$\AA$)')
axs[0][1].set_xlabel(r'DP Force (eV/$\AA$)')

axs[1][0].plot(fx2,fy2,'-', f[:,1],f[:,4], 'o')
axs[1][0].set_title('Force y')
axs[1][0].set_xlabel(r'DFT Force (eV/$\AA$)')
axs[1][0].set_xlabel(r'DP Force (eV/$\AA$)')

axs[1][1].plot(fx3,fy3,'-', f[:,2],f[:,5], 'o')
axs[1][1].set_title('Force z')
axs[1][1].set_xlabel(r'DFT Force (eV/$\AA$)')
axs[1][1].set_xlabel(r'DP Force (eV/$\AA$)')
plt.tight_layout()
plt.show()
plt.savefig('efv.png')

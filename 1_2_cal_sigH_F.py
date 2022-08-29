# -*- coding: utf-8 -*-
"""
Created on Thu May 12 09:28:37 2022

@author: Zikang He
"""



# this code is used to filter ocean variable and re-calculate sigma



import numpy as np
from toolbox import my_lowfilter as mf
xx = np.load('true_h.npy')

xx_l=mf(xx, 27)
ivar36 = [
        0,  1,  2,  3,  4,  5, 12, 13, 14, 15, #psi
        20, 21, 22, 23, 24, 25, 32, 33, 34, 35, #theta
        40, 41, 42, 43, 44, 45, 46, 47, #A
        48, 49, 50, 51, 52, 53, 54, 55 #T
]
dx = xx - xx_l
sigma_hf = np.std(dx, axis=0)
np.save('sigma_hf_h.npy',sigma_hf)
sigma_hf2 = sigma_hf[ivar36]
np.save('sigma_hf.npy',sigma_hf2)
#np.savetxt('sigma_hf.txt',sigma_hf2)
#np.savetxt('data.txt',xx)
# In[]
import numpy as np
from toolbox import my_lowfilter as mf
xx = np.load('true_l.npy')
yy = np.load('obs_l.npy')
sigma_hf = np.load('sigma_hf.npy')
dx = xx[1:]-yy
std=np.zeros((36,3))
std[:,0] =np.var(dx,axis=0)
std[:,1]=sigma_hf
std[:,2]=sigma_hf2
# In[]
import matplotlib.pyplot as plt

[xgrd,ygrd] = np.meshgrid(range(40001),range(56))
plt.figure(figsize=(12,9))
plt.subplot(311)
plt.title('Truth',fontsize=20)
levels = np.linspace(-0.2, 0.2, 9)
plt.contourf(xgrd,ygrd,xx.T,levels=levels.round(5),cmap=plt.cm.rainbow)
plt.axhline(y=9,linestyle='--')
plt.axhline(y=39,linestyle='--')
plt.axhline(y=47,linestyle='--')
plt.colorbar()
plt.title(str('observe Noise').title(),fontsize=10)
#plt.savefig("RMSE3.tiff", dpi=300)
plt.subplot(312)
plt.title('Truth',fontsize=20)
levels = np.linspace(-0.2, 0.2, 9)
plt.contourf(xgrd,ygrd,xx_l.T,levels=levels.round(5),cmap=plt.cm.rainbow)
plt.axhline(y=9,linestyle='--')
plt.axhline(y=39,linestyle='--')
plt.axhline(y=47,linestyle='--')
plt.colorbar()
plt.title(str('observe Noise').title(),fontsize=10)
plt.subplot(313)
plt.title('Truth',fontsize=20)
levels = np.linspace(-0.02, 0.02, 9)
plt.contourf(xgrd,ygrd,xx.T-xx_l.T,levels=levels.round(5),cmap=plt.cm.rainbow)
plt.axhline(y=9,linestyle='--')
plt.axhline(y=39,linestyle='--')
plt.axhline(y=47,linestyle='--')
plt.title(str('observe Noise').title(),fontsize=10)
plt.colorbar()
#plt.savefig("RMSE3.tiff", dpi=300)
plt.show()
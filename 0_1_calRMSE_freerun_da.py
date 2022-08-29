# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:17:38 2022

@author: Zikang He
"""

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

xx = np.load('true_l.npy')

E = np.load('E.npz')
da =E['E']

E = np.load('freerunE.npz')
fr =E['xx']

from dapper import Chronology
integration_time = 4.e5
to_time = integration_time
dt = 10.0
dto = 10.0
f0 = 1.032e-4  # Coriolis parameter at 45 degrees latitude
chrono = Chronology(dt, dtObs=dto, T=to_time,  BurnIn=0)
tt = chrono.tt[::chrono.dkObs]/f0/(3600*24*365) #in year
tt = tt[1:40001]
# In[]
Rmse_da = np.ones((40000,36))
Rmse_fr = np.ones((40000,36))
for i in range(40000):
   mse = np.sum((da[i,0:50,:] - xx[i+1,:]) ** 2,axis=0) / 50
   Rmse_da[i,:] = np.sqrt(mse.T)
   mse = np.sum((fr[i,0:50,:] - xx[i+1,:]) ** 2,axis=0) / 50
   Rmse_fr[i,:] = np.sqrt(mse)

# In[]
a_nx = 2
a_ny = 2
o_nx = 2
o_ny = 4
Na = a_ny*(2*a_nx+1)
No = o_ny*o_nx
Nx = 2*Na+2*No
Ns =5
o_T   = 2*Na+2
o_psi = 2*Na+No+2
Ns = 5
plt.figure(figsize=(12,9))
plt.subplot(211)
plt.plot(tt,Rmse_da[:,o_psi],label = 'analysis')
#plt.plot(tt,Rmse_fr[:,o_psi],label = 'freerun')
#plt.xticks([0,9,19,27,35],fontsize = 10);
plt.legend(fontsize=10,ncol=1)
plt.title(('$\Psi$'),fontsize=10)
#plt.ylim([0,0.08]);
#plt.savefig("data RMSE.tiff", dpi=300)
plt.subplot(212)
plt.plot(tt,Rmse_da[:,o_T],label = 'analysis')
#plt.plot(tt,Rmse_fr[:,o_T],label = 'freerun')
#plt.xticks([0,9,19,27,35],fontsize = 10);
plt.legend(fontsize=10,ncol=1)
plt.title(str('$\Theta$').title(),fontsize=10)
plt.xlim([0,10])
#plt.savefig("Compare truth_DA time series.tiff", dpi=300)
plt.show()

# In[]
[xgrd,ygrd] = np.meshgrid(tt,range(36))
levels = np.linspace(-0.05, 0.05, 9)

plt.figure(figsize=(12,9))
plt.subplot(211)
plt.title('DA',fontsize=20)
plt.contourf(xgrd,ygrd,Rmse_da.T,levels=levels.round(5),cmap=plt.cm.rainbow)
plt.axhline(y=9,linestyle='--',color='black')
plt.axhline(y=19,linestyle='--',color='black')
plt.axhline(y=27,linestyle='--',color='black')
plt.yticks([9,19,27],fontsize=18)
plt.ylabel('Variable Index',fontsize=18)
plt.ylim([0,35])
plt.xlim([0,100])
plt.xticks([])
plt.colorbar()
plt.subplot(212)
plt.title('freerun',fontsize=20)
plt.contourf(xgrd,ygrd,Rmse_fr.T,levels=levels.round(5),cmap=plt.cm.rainbow)
plt.axhline(y=9,linestyle='--',color='black')
plt.axhline(y=19,linestyle='--',color='black')
plt.axhline(y=27,linestyle='--',color='black')
plt.yticks([9,19,27],fontsize=18)
plt.ylabel('Variable Index',fontsize=18)
plt.ylim([0,35])
plt.xlim([0,100])
plt.xlabel('Model Steps',fontsize=18)
plt.xlabel('Lead Times(year)',fontsize=18)
plt.colorbar()
#plt.savefig("Pcolor Compare truth_DA.tiff", dpi=300)
plt.show()

# In[]
plt.figure(figsize=(12,9))
plt.plot(Rmse_da,label = 'analysis')
plt.plot(Rmse_fr,label = 'Free Run')
plt.xlim([0,35]);
plt.axvline(x=9,linestyle='--')
plt.axvline(x=19,linestyle='--')
plt.axvline(x=27,linestyle='--')
plt.xticks([0,9,19,27,35],fontsize = 10);
plt.legend(fontsize=10,ncol=1)
plt.title(str('RMSE').title(),fontsize=10)
plt.ylim([0,0.1]);
plt.savefig("data RMSE.tiff", dpi=300)
plt.show()


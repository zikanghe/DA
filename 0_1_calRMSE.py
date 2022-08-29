# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 10:09:45 2022

@author: Zikang
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:17:38 2022

@author: Zikang He
"""

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

xx = np.load('true_l.npy')

E = np.load('daPF.npz')
da1 =E['mua']

E = np.load('daPF_001.npz')
da2 =E['mua']
fr = np.load('freerun.npy')

from dapper import Chronology
integration_time = 4.e5
to_time = integration_time
dt = 10.0
dto = 10.0
f0 = 1.032e-4  # Coriolis parameter at 45 degrees latitude
chrono = Chronology(dt, dtObs=dto, T=to_time,  BurnIn=0)
tt = chrono.tt[::chrono.dkObs]/f0/(3600*24*365) #in year
# In[]
Rmse_fr = np.zeros(36)
Rmse_da1 = np.zeros(36)
Rmse_da2 = np.zeros(36)
for i in range(36):
   mse = np.sum((da1[:,i] - xx[1:,i]) ** 2) / len(da1[:,i])
   Rmse_da1[i] = sqrt(mse)
   mse = np.sum((da2[:,i] - xx[1:,i]) ** 2) / len(da2[:,i])
   Rmse_da2[i] = sqrt(mse)
   mse = np.sum((fr[1:,i] - xx[1:,i]) ** 2) / len(fr[:,i])
   Rmse_fr[i] = sqrt(mse)

Rmse = np.zeros((36,3))

Rmse[:,0]=Rmse_da1
Rmse[:,1]=Rmse_da2
Rmse[:,2]=Rmse_fr
# In[]
plt.figure(figsize=(12,9))
plt.plot(Rmse_da1,label = 'analysis')
#plt.plot(Rmse_da2,label = 'analysis2')
plt.plot(Rmse_fr,label = 'Free Run')
plt.xlim([0,35]);
plt.axvline(x=9,linestyle='--')
plt.axvline(x=19,linestyle='--')
plt.axvline(x=27,linestyle='--')
plt.xticks([0,9,19,27,35],fontsize = 10);
plt.legend(fontsize=10,ncol=1)
plt.title(str('RMSE').title(),fontsize=10)
plt.ylim([0,0.1]);
#plt.savefig("data RMSE.tiff", dpi=300)
plt.show()


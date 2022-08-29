# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 16:43:39 2022

@author: Zikang
"""

import numpy as np
data =np.load('../../DA/daPF.npz')
xx_f =np.load('../../DA/freerun.npy')
xx_l =np.load('../../DA/true_l.npy')
obs_l =np.load('../../DA/obs_l.npy')
sighf_l =np.load('../../DA/obs_l.npy')
xx = data['mua']
o_psi = 21

# In[]
import matplotlib.pyplot as plt
from dapper import Chronology
integration_time = 400000
to_time = integration_time
dt = 10.0
dto = 10.0
f0 = 1.032e-4  # Coriolis parameter at 45 degrees latitude
chrono = Chronology(dt, dtObs=dto, T=to_time,  BurnIn=0)
tt = chrono.tt[::chrono.dkObs]/f0/(3600*24*365) #in year
plt.figure(figsize=(9,9))

plt.plot(tt[1:],obs_l[:,o_psi],label = 'observation',color='k')
plt.plot(tt[1:],xx[:,o_psi],label = 'analysis',color='b')
plt.plot(tt[1:],xx_f[1:,o_psi],label = 'free run',color='g')
plt.plot(tt[1:],xx_l[1:,o_psi],label = 'truth',color='r')

#plt.xticks([0,9,19,27,35],fontsize = 10);
plt.legend(fontsize=18,ncol=1)
plt.title(str('$\Psi_{o,2} Correlation$').title(),fontsize=18)

#plt.xlim([0,10])

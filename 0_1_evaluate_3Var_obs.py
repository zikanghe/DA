# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 07:13:55 2022

@author: Zikang
"""



import numpy as np
xx_l =np.load('true_l.npy')
obs_l =np.load('obs_l.npy')
obs_l2 =np.load('obs_l2.npy')
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
plt.plot(tt[1:],obs_l[:,o_psi],label = 'observation_0.1sigmahf',color='k')
plt.plot(tt[1:],obs_l2[:,o_psi],label = 'observation_0.01sigmahf',color='b')
plt.plot(tt[1:],xx_l[1:,o_psi],label = 'truth',color='r')

#plt.xticks([0,9,19,27,35],fontsize = 10);
plt.legend(fontsize=18,ncol=1)
plt.title(str('$\Psi_{o,2} Correlation$').title(),fontsize=18)

#plt.xlim([0,10])
# In[plot 3 var]
key_features = [(0,'psi_a_1'), (21, 'psi_o_2'), (29, 'theta_o_2')]
nfeat = len(key_features)

fig, ax = plt.subplots(nrows=nfeat,figsize=(8,4*nfeat),sharex='all')


for i, (ivar, name) in enumerate(key_features):
    ax[i].plot(obs_l[:,ivar],label = 'observation_0.1sigmahf',color='k')
    ax[i].plot(obs_l2[:,ivar],label = 'observation_0.01sigmahf',color='b')
    ax[i].plot(xx_l[:,ivar],label = 'truth',color='r')
    ax[i].set_title(name)
    ax[i].legend(fontsize=18,ncol=1)

ax[-1].set_xlabel('time');
plt.savefig('3Var_truth.png')
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 17:34:16 2022

@author: Zikang
"""
import os
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import ParameterGrid
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

from toolbox import my_lowfilter as mf
data_da = np.load('daPF.npz')
data_t = np.load('true_l.npy')
burn =50
xx_t = data_t[1:]
xx_da = data_da['mua']

yy_f = np.ones((40000,16))
yy_f = np.copy(xx_da[:,20:36])
yy_f = mf(yy_f,51)

xx_l = xx_da
xx_l[:,20:36]=yy_f

lvar2plot = [(21,'psio2',r'$\Psi_{o,2}$'),(29,'thetao2',r'$\theta_{o,2}$'),(0,'psia1',r'$\Psi_{a,1}$')]
#Mask for 36 variables
ivar36 = [
	 0,  1,  2,  3,  4,  5, 12, 13, 14, 15, #psi
	20, 21, 22, 23, 24, 25, 32, 33, 34, 35, #theta
	40, 41, 42, 43, 44, 45, 46, 47, #A
	48, 49, 50, 51, 52, 53, 54, 55 #T
]

ioce36 = np.arange(20,36)
iatm36 = np.arange(0,20)
nfeat = len(lvar2plot)

burn = 50

# In[]
fig, ax = plt.subplots(nrows=nfeat,figsize=(8,4*nfeat),sharex='all')

for i, (ivar, var, name) in enumerate(lvar2plot):
    ax[i].plot(xx_da[:,ivar],label='non smooth')
    ax[i].plot(xx_t[:,ivar], label='truth')
    ax[i].plot(xx_l[:,ivar], label='smooth_filter')
    ax[i].set_title(name)

ax[-1].set_xlabel('time');
ax[0].legend();
d = xx_l[:,ivar]-xx_da[:,ivar]
# In[]
fig, ax = plt.subplots(nrows=nfeat,figsize=(8,4*nfeat),sharex='all')
for i, (ivar, var, name) in enumerate(lvar2plot):
	ax[i].plot(xx_da[2500:3000,ivar],label='non smooth')
	ax[i].plot(xx_train[2500:3000,ivar], label='smooth')
	ax[i].plot(xx_l[2500:3000,ivar], label='smooth_filter')
	ax[i].set_title(name)
	ax[-1].set_xlabel('time');
ax[0].legend();

# In[]
p2 =21
plt.figure(figsize=(12,9))
#plt.plot(xx_da[:,p2],label='non smooth')
plt.plot(xx_train[:,p2], label='smooth')
plt.plot(xx_l[:,p2], label='smooth_filter')

#plt.savefig("data RMSE.tiff", dpi=300)
plt.show()

# In[compare with truth]
fig, ax = plt.subplots(nrows=nfeat,figsize=(8,4*nfeat),sharex='all')


for i, (ivar, var, name) in enumerate(lvar2plot):
    ax[i].plot(xx_da[:,ivar],label='non smooth')
    ax[i].plot(xx_t[:,ivar], label='smooth')
    ax[i].plot(xx_t[:,ivar], label='smooth_filter')
    ax[i].set_title(name)

ax[-1].set_xlabel('time');
ax[0].legend();
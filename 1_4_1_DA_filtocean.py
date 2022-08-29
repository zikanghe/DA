# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:25:20 2022

@author: Zikang He
"""

# code 3_ is used to carry out assimilation experiments
# The difference is mainly reflected in the setting of observation error and model error
#3_0 model noise:calculated by High resolution truth
#2-3-3 obs noise  : calculated by High resolution and observation

import numpy as np
from dapper.admin import HiddenMarkovModel

from multiprocessing import freeze_support, get_start_method
from dapper import *
from dapper.tools.convenience import simulate

from dapper.mods.Qgs.qgs.params.params import QgParams
from dapper.mods.Qgs.qgs.functions.tendencies import create_tendencies
from dapper.mods.Qgs.qgs.integrators.integrator import RungeKuttaIntegrator


if __name__ == "__main__":

    if get_start_method() == "spawn":
        freeze_support()
        
    a_nx = 2 
    a_ny = 2 
    o_nx = 2 
    o_ny = 4 
    Na = a_ny*(2*a_nx+1) 
    No = o_ny*o_nx


    Nx = 2*Na+2*No
    #start Time
    ################
    # General parameters
    # Setting some model parameters
    # Model parameters instantiation with default specs
    model_parameters = QgParams()
    # Mode truncation at the wavenumber 2 in both x and y spatial coordinate
    model_parameters.set_atmospheric_channel_fourier_modes(a_nx, a_ny)
    # Mode truncation at the wavenumber 2 in the x and at the
    # wavenumber 4 in the y spatial coordinates for the ocean
    model_parameters.set_oceanic_basin_fourier_modes(o_nx, o_ny)

# Setting MAOOAM parameters according to the publication linked above
    model_parameters.set_params({'kd': 0.0290, 'kdp': 0.0290, 'n': 1.5, 'r': 1.e-7,
                                 'h': 136.5, 'd': 1.1e-7})
    model_parameters.atemperature_params.set_params({'eps': 0.7, 'T0': 289.3, 'hlambda': 15.06, })
    model_parameters.gotemperature_params.set_params({'gamma': 5.6e8, 'T0': 301.46})

    model_parameters.atemperature_params.set_insolation(103.3333, 0)
    model_parameters.gotemperature_params.set_insolation(310., 0)

    model_parameters.print_params()

    f, Df = create_tendencies(model_parameters)   
    integrator = RungeKuttaIntegrator()
    integrator.set_func(f)
    
    # Saving the model state n steps
    def step(x0, t0, dt):
       y = x0
       integrator.integrate(t0, t0+dt, 0.01, ic=y, write_steps=0)
       t0, y0 = integrator.get_trajectories()
       return y0

    integration_time = 4.e5
    dt = 10.0
    dto= 10.0
    t = Chronology(dt=dt, dtObs=dto, T=integration_time,  BurnIn=0)
    xx = np.load('true_l.npy')
    yy_o = np.load('obs_l.npy')
    yy = np.copy(yy_o)
    from toolbox import my_lowfilter as filt
    Ns = 51
    yy_f = np.ones((40000,16))
    yy_f = np.copy(yy_o[:,20:36])
    yy_f = filt(yy_f,Ns)

    yy[:,20:36] = yy_f

    sig_hf = np.load('sigma_hf.npy')
#parameter setting
    #1:Dyn
    sig_m = np.copy(sig_hf)*0.001
    sig_m[20:36]=0.0
    Dyn = {
        'M': Nx,
        'model': step,
        'linear': Df,
        'noise': sig_m,
    }
    #2:Time

    #3:X0
    from utils import sampling
    X0 = RV(36, func=sampling)
	
    sig_o = 0.01*np.copy(sig_hf)
    jj = np.arange(Nx)  # obs_inds
    Obs = partial_direct_Obs(Nx, jj)
    Obs['noise'] = GaussRV(C=sig_o.T*np.eye(Nx))
    HMM = HiddenMarkovModel(Dyn, Obs, t, X0)


    N = 50  # Size of the ensemble

    import dapper.da_methods as da
    from dapper import print_averages
    xp = da.ensemble.EnKF_N(N=N)
    stats = xp.assimilate(HMM, xx, yy)
    mua=stats.mu.a
    muf=stats.mu.f
    mus=stats.mu.s
    E=stats.E
# =============================================================================
    np.savez('daPF.npz', mua=stats.mu.a, muf=stats.mu.f, mus=stats.mu.s, vara=stats.var.a,
        varf=stats.var.f, vars=stats.var.s, infl=stats.infl)


    avrgs = stats.average_in_time()
    print_averages(xp, avrgs, [], ['rmse_a', 'rmv_a'])
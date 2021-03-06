# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:56:05 2014

@author: joser
"""

import derivativesFunc as dx
import initialConditions as ic


#To add new function is needed to include the functions in the dictionaries
dxFunSelect = {"Hyperbolic":dx.dX_dt_Hyperbolic, 
               "Simple":dx.dX_dt_Simple, 
               "Magnetic":dx.dX_dt_Magnetic, 
               "Duffing":dx.dX_dt_Duffing,
               "Vanderpol":dx.dX_dt_Vanderpol,
               "Violin":dx.dX_dt_Violin,
               "Pendulum":dx.dX_dt_Pendulum}
                 
dx2FunSelect = {"Hyperbolic":dx.d2X_dt2_Hyperbolic, 
                "Simple":dx.d2X_dt2_Simple, 
                "Magnetic":dx.d2X_dt2_Magnetic, 
                "Duffing":dx.d2X_dt2_Duffing,
                "Vanderpol":dx.d2X_dt2_Vanderpol,
                "Violin":dx.d2X_dt2_Violin,
                "Pendulum":dx.d2X_dt2_Pendulum}

ICFunSelect = {"Hyperbolic": [ic.X_f0_Hyperbolic, ic.X_f1_Hyperbolic], 
               "Simple": [ic.X_f0_Simple, ic.X_f1_Simple], 
               "Magnetic": [ic.X_f0_Magnetic, ic.X_f1_Magnetic], 
               "Duffing": [ic.X_f0_Duffing, ic.X_f1_Duffing],
               "Vanderpol":[ic.X_f0_Vanderpol, ic.X_f1_Vanderpol],
               "Violin":[ic.X_f0_Violin, ic.X_f1_Violin],
               "Pendulum":[ic.X_f0_Pendulum, ic.X_f1_Pendulum]}
                 
                 
def init(funName):
    dxfun = dxFunSelect[funName]
    dx2fun = dx2FunSelect[funName]
    icfun = ICFunSelect[funName]
    return dxfun, dx2fun, icfun

    
    
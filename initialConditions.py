# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:54:02 2014

@author: joser
"""

from numpy import *


#Set initial conditions: (#Check for points differents than zero)
#================== Hyperbolic Equilibrium point ==================
X_f0_Hyperbolic = array([     0. ,  0.])
X_f1_Hyperbolic = array([     1. ,  0.])
#========================================================
    
#================== Simple Harmonic Oscilator ==================
X_f0_Simple = array([     0. ,  0.])
X_f1_Simple = array([     1. ,  0.])
#========================================================

#================== Magnetic Suspension ==================
X_f0_Magnetic = array([     0. ,  0.])
X_f1_Magnetic = array([     1. ,  0.])
#========================================================

#================== Duffing oscillator ==================
#epsi = 0.1 beta = 0.1 alpha = -0.1 
X_f0_Duffing = array([     0. ,  0.])
X_f1_Duffing = array([     1. ,  0.])
#========================================================

#================== Vanderpol oscillator ==================
#r,w = 1,1
X_f0_Vanderpol = array([     0. ,  0.])
X_f1_Vanderpol = array([     1. ,  0.])
#========================================================

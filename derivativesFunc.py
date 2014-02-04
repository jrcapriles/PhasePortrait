# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:43:55 2014

@author: joser
"""
from numpy import *


# Definition of parameters 

#================== Vanderpol oscillator ==================
mu = 1.
r=1.       #Evaluate diff conditions (r,ω) = {(1,1), (0.1,1), (2,1), (1,2), (2,2)}
w = 1.
#================== Duffing oscillator ==================
epsi = 0.1     #epsi = 0.1, 2.0
beta = 0.1     #beta = 0.1, 1.0
alpha = -0.1   #alpha = -0.1, 0.1, 0.5
#================== Magnetic Suspension ==================
m = 2.5
b = 1.5
mu_mag = 0.0    #0.0, 0.5, 2.0
lamb = 0.1  #0.1, 1.0
k_mag = 0.5     #0.0, 0.5, 2.0
r_mag = 0.0     #0.0, 0.5
g = 0.0
#================== Simple Harmonic Oscilator ==================
k = 1.5
m = 2
#================== Hyperbolic Equilibrium point ==================
alpha_hyper = 2    # alpha 2., -2.
#=========================================================


# Definition of the equations:

# Definition of the first derivative:
    
#================== Hyperbolic Equilibrium point ==================
def dX_dt_Hyperbolic(X,t=0):
    """ Return the Your Choise derivative """
    return array([X[1],
                  -X[0]-X[0]**3-alpha_hyper*X[1]])
#=========================================================

#================== Your Choise ==================
def dX_dt_Simple(X,t=0):
    """ Return the Your Choise derivative """
    return array([X[1],
                  -k*X[0]/m])
#=========================================================

#================== Magnetic Suspension ==================
def dX_dt_Magnetic(X,t=0):
    """ Return the Magnetic Suspension derivative """
    return array([X[1],
                  (1/m)*(-b*X[1] - m*g + 0.5*((lamb*mu_mag*(-k_mag*(r_mag-X[0]))**2)/(1+mu_mag*X[0])**2))])
#=========================================================

#================== Duffing oscillator ===================
def dX_dt_Duffing(X,t=0):
    """ Return the Duffing oscillator derivative """
    return array([X[1],
                  -epsi*X[1] -X[0]*(beta*X[0]**2+alpha)])
#=========================================================

#================== Vanderpol oscillator =================
def dX_dt_Vanderpol(X,t=0):
    """ Return the vanderpol oscilator derivative """
    return array([X[1],
                  -r*(X[0]**2-1)*X[1]-w**2*X[0]])
#=========================================================


# Definition of the Jacobian matrix:

#================== Hyperbolic Equilibrium point ==================
def d2X_dt2_Hyperbolic(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    return array([[0, 1],
                  [-1-3*X[0]**2, -alpha_hyper]])  
#========================================================

#================== Simple Harmonic Oscillator ==================
def d2X_dt2_Simple(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    return array([[0, 1],
                  [-k/m, 0]])  
#========================================================

#================== Magnetic Suspension ==================
def d2X_dt2_Magnetic(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    return array([[0, 1],
                  [((lamb*mu_mag*((-k_mag)**2))/(2*m))*((-2*r_mag + 2*X[0])*(1+2*mu_mag*X[0]+X[0]**2)-((r_mag**2-2*r_mag*X[0]+X[0]**2)*(2*mu_mag+2*X[0]))),  -b/m]])  
#========================================================

#================== Duffing oscillator ==================
def d2X_dt2_Duffing(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    return array([[0, 1],

                  [-3*beta*X[0]**2-alpha,  -epsi]])  
#========================================================

#================== Vanderpol oscillator ==================
def d2X_dt2_Vanderpol(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    return array([[0,   1     ],
                  [-2*r*X[1]*X[0]-w**2 ,   r*(1-X[0]**2)]])  
#========================================================

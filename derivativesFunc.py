# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:43:55 2014

@author: joser
"""
from numpy import *
import math


# Definition of parameters 
#=====================Playing Violin =======================
l=0.32     #centimeters
epse_vio = 0.65
A = 440
mu_dyn =1.2
mu_sta = 1.5
alpha_vio = mu_sta/mu_dyn - 1
vb = 0.012 
N = 3/mu_dyn
m_vio = 0.02
xc = 0.003
v = 1 
k_vio = 1;

#================== Vanderpol oscillator ==================
mu = 1.
r=1.       #Evaluate diff conditions (r,ω) = {(1,1), (0.1,1), (2,1), (1,2), (2,2)}
w = 1.
#================== Duffing oscillator ==================
epsi = 0.1     #epsi = 0.1, 2.0
beta = 0.1     #beta = 0.1, 1.0
alpha = -0.1   #alpha = -0.1, 0.1, 0.5
#================== Magnetic Suspension ==================
m_mag = 2.5
b_mag = 1.5
mu_mag = 2.0    #0.0, 0.5, 2.0
lamb = 1.0  #0.1, 1.0
k_mag = 4.95     #0.0, 0.5, 2.0
r_mag = 0.5     #0.0, 0.5
g = 9.8
#================== Simple Harmonic Oscilator ==================
k = 1.5
m = 2
#================== Hyperbolic Equilibrium point ==================
alpha_hyper = -2.    # alpha 2., -2.
#=========================================================
k_pen = 1.0

bb= 2.1
cc= 2.0
dd= 3.0
# Definition of the first derivative:

def fb_Violin(seda):
#    print seda
    if seda.all>0.:
        fb = (1+alpha_vio*(seda-1)**2)*mu_dyn*N  #1+alpha_vio*(seda - 1)**2
    else:
        fb = -(1+alpha_vio*(seda+1)**2)*mu_dyn*N #1-alpha_vio*(seda + 1)**2

    return fb

#=====================Playing Violin =======================
def dX_dt_Violin(X,t=0):
    """ Return the Your Choise derivative """
    seda = (X[1]-vb)/v
    
    if seda.all > 0.3 and seda.all < -0.3:
        seda = 0.
    #fb = ((1+alpha_vio*(seda-sign(seda)))**2)*sign(seda)*mu_dyn*N
    #fk = k*(X[0]-xc)
    fb = fb_Violin(seda)
    fk = k_vio*(X[0]-xc)
    print 'Equilibrium points'
    print X[1]
    print (1/m_vio)*(sign(seda)*(1+alpha_vio*(seda-sign(seda))**2)*mu_dyn*N - fk)
                  
    return array([X[1],
                  (1/m_vio)*(sign(seda)*(1+alpha_vio*(seda-sign(seda))**2)*mu_dyn*N - fk)])#(fb-fk)]) #-(1/m_vio)*(fb_Violin(X[1])+k*(X[0]-xc))])

#================== Hyperbolic Equilibrium point ==================
def dX_dt_Hyperbolic(X,t=0):
    """ Return the Your Choise derivative """
    return array([X[1],
                  -X[0]-X[0]**3-alpha_hyper*X[1]])

#================== Your Choise ==================
def dX_dt_Simple(X,t=0):
    """ Return the Your Choise derivative """
    return array([X[1],
                  -k*X[0]/m])

#================== Magnetic Suspension ==================
def dX_dt_Magnetic(X,t=0):
    """ Return the Magnetic Suspension derivative """
    coef2 = (lamb*mu_mag*k_mag**2)/(2*m_mag)
    return array([X[1],
                -g + coef2*((X[1]**2-2*X[1]*r_mag+r**2)/(1+2*mu_mag*X[1]+(mu_mag*X[1])**2))-(b_mag*X[1]/m_mag)])

#================== Duffing oscillator ===================
def dX_dt_Duffing(X,t=0):
    """ Return the Duffing oscillator derivative """
    return array([X[1],
                  -epsi*X[1] -X[0]*(beta*X[0]**2+alpha)])

#================== Vanderpol oscillator =================
def dX_dt_Vanderpol(X,t=0):
    """ Return the vanderpol oscilator derivative """
    return array([X[1],
                  -r*(X[0]**2-1)*X[1]-w**2*X[0]])
                  
#================== Simple Pendulum =================
def dX_dt_Pendulum(X,t=0):
    """ Return the pendulum derivatives """
    return array([X[1],
                  -k_pen*X[0]])
#=========================================================


# Definition of the Jacobian matrix:

#================== Hyperbolic Equilibrium point ==================
def d2X_dt2_Violin(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    seda = (X[1]-vb)/v
    fb = fb_Violin(seda)
    fk = k_vio*(X[0]-xc)
    
    return array([[0, 1],
                  [-k_vio/m_vio, (2*alpha_vio/(v**2))*(X[1]-vb-v)]]) #(1/m_vio)*(sign(seda)*(alpha_vio*2*(seda-sign(seda))*(1/v)))*mu_dyn*N ]])#[-k_vio/m_vio, -(2/m_vio)*(cc-bb)]])
                  #(2*alpha_vio/(v**2))*(X[1]-vb-v)]])  
                  
#================== Hyperbolic Equilibrium point ==================
def d2X_dt2_Hyperbolic(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    return array([[0, 1],
                  [-1-3*X[0]**2, -alpha_hyper]])  

#================== Simple Harmonic Oscillator ==================
def d2X_dt2_Simple(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    return array([[0, 1],
                  [-k/m, 0]])  
#========================================================

#================== Magnetic Suspension ==================
def d2X_dt2_Magnetic(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    coef2 = (lamb*mu_mag*k_mag**2)/(2*m_mag)    
    den = (1+2*mu_mag*X[1]+(mu_mag*X[1])**2)
    num = (X[1]**2-2*X[1]*r_mag+r**2)
    return array([[0, 1],
                  [(den*(2*(X[0]-r_mag))-num*(2*mu_mag+(mu_mag*X[0])**2))/(den**2),-b_mag/m_mag]])  
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

#================== Simple Pendulum =================
def d2X_dt2_Pendulum(X,t=0):
    """ Return the pendulum derivatives """
    return array([[0, 1],
                  [-k_pen,0]])
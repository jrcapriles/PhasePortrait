# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 16:09:43 2014

@author: joser
"""

# du/dt =  a*u -   b*u*v
# dv/dt = -c*v + d*b*u*v 
# We will use X=[u, v] to describe the states
#
# Definition of the equations:
# 

from numpy import *
import pylab as p

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
mu = 0.0    #0.0, 0.5, 2.0
lamb = 0.1  #0.1, 1.0
k = 0.5     #0.0, 0.5, 2.0
r = 0.0     #0.0, 0.5
g = 0.0

#================== Simple Harmonic Oscilator ==================
k = 1.5
m = 2

#================== Hyperbolic Equilibrium point ==================
alpha = 2    # alpha 2., -2.

#================== Hyperbolic Equilibrium point ==================
def dX_dt(X,t=0):
    """ Return the Your Choise derivative """
    return array([X[1],
                  -X[0]-X[0]**3-alpha*X[1]])
#=========================================================

#================== Your Choise ==================
#def dX_dt(X,t=0):
#    """ Return the Your Choise derivative """
#    return array([X[1],
#                  -k*X[0]/m])
#=========================================================

#================== Magnetic Suspension ==================
#def dX_dt(X,t=0):
#    """ Return the Magnetic Suspension derivative """
#    return array([X[1],
#                  (1/m)*(-b*X[1] - m*g + 0.5*((lamb*mu*(-k*(r-X[0]))**2)/(1+mu*X[0])**2))])
#=========================================================

#================== Duffing oscillator ===================
#def dX_dt(X,t=0):
#    """ Return the Duffing oscillator derivative """
#    return array([X[1],
#                  -epsi*X[1] -X[0]*(beta*X[0]**2+alpha)])
#=========================================================

#================== Vanderpol oscillator =================
#def dX_dt(X,t=0):
#    """ Return the vanderpol oscilator derivative """
#    return array([X[1],
#                  -r*(X[0]**2-1)*X[1]-w**2*X[0]])
#=========================================================


# Before using SciPy to integrate this system, we will have a closer look on 
# position equilibrium. Equilibrium occurs when the x_dot is equal to 0.
# This gives fixed points:
# 

#Set initial conditions:
#================== Hyperbolic Equilibrium point ==================
X_f0 = array([     0. ,  0.])
X_f1 = array([     0. ,  0.])
#========================================================
    
#================== Simple Harmonic Oscilator ==================
#X_f0 = array([     0. ,  0.])
#X_f1 = array([     0. ,  0.])
#========================================================

#================== Magnetic Suspension ==================
#X_f0 = array([     1. ,  0.])
#X_f1 = array([     0. ,  0.])
#========================================================

#================== Duffing oscillator ==================
#epsi = 0.1 beta = 0.1 alpha = -0.1 
#X_f0 = array([     0. ,  0.])
#X_f1 = array([     1. ,  0.])
#========================================================

#================== Vanderpol oscillator ==================
#r,w = 1,1
#X_f0 = array([     0. ,  0.])
#X_f1 = array([     0. ,  0.])
#========================================================

#Test initial condition (should be true)
all(dX_dt(X_f0) == zeros(2) ) and all(dX_dt(X_f1) == zeros(2)) # => True 

#Check for points differents than zero
#X_f1 = array([ c/(d*b), a/b])


# === Stability of the fixed points ===
# Near theses two points, the system can be linearized:
# dX_dt = A_f*X where A is the Jacobian matrix evaluated at the corresponding point.

# We have to define the Jacobian matrix:

#================== Hyperbolic Equilibrium point ==================
def d2X_dt2(X, t=0):
    """ Return the Jacobian matrix evaluated in X. """
    return array([[0, 1],
                  [-1-3*X[0]**2, -alpha]])  
#========================================================

#================== Simple Harmonic Oscillator ==================
#def d2X_dt2(X, t=0):
#    """ Return the Jacobian matrix evaluated in X. """
#    return array([[0, 1],
#                  [-k/m, 0]])  
#========================================================

#================== Magnetic Suspension ==================
#def d2X_dt2(X, t=0):
#    """ Return the Jacobian matrix evaluated in X. """
#    return array([[0, 1],
#                  [((lamb*mu*((-k)**2))/(2*m))*((-2*r + 2*X[0])*(1+2*mu*X[0]+X[0]**2)-((r**2-2*r*X[0]+X[0]**2)*(2*mu+2*X[0]))),  -b/m]])  
#========================================================

#================== Duffing oscillator ==================
#def d2X_dt2(X, t=0):
#    """ Return the Jacobian matrix evaluated in X. """
#    return array([[0, 1],
#                  [-3*beta*X[0]**2-alpha,  -epsi]])  
#========================================================

#================== Vanderpol oscillator ==================
#def d2X_dt2(X, t=0):
#    """ Return the Jacobian matrix evaluated in X. """
#    return array([[0,   1     ],
#                  [-2*r*X[1]*X[0]-w**2 ,   r*(1-X[0]**2)]])  
#========================================================

   
# A_f0 = d2X_dt2(X_f0)                    # >>> array([[ 1. , -0. ],
                                          #            [ 0. , -1.5]])
# Near X_f1, we have:
#A_f1 = d2X_dt2(X_f1)                    # >>> array([[ 0.  , -2.  ],
                                        #            [ 0.75,  0.  ]])

A_f1 = d2X_dt2(X_f1)  

# whose eigenvalues are:
lambda1, lambda2 = linalg.eigvals(A_f1)
T_f1 = 2*pi/abs(lambda1)                # >>> 5.130199

# == Integrating the ODE using scipy.integate ==
# Now we will use the scipy.integrate module to integrate the ODEs.
# This module offers a method named odeint, very easy to use to integrate ODEs:

from scipy import integrate

t = linspace(0, 15,  1000)              # time
X0 = array([1, 1])                     # load initials conditions

X, infodict = integrate.odeint(dX_dt, X0, t, full_output=True)
infodict['message']                     # >>> 'Integration successful.'
# 
# `infodict` is optional, and you can omit the `full_output` argument if you don't want it.
# Type "info(odeint)" if you want more information about odeint inputs and outputs.
# 
 
y1, y2 = X.T

f1 = p.figure()
p.plot(t, y1, 'r-', label='y1')
p.plot(t, y2  , 'b-', label='y2')
p.grid()
p.legend(loc='best')
p.xlabel('time')
p.ylabel('outputs')
p.title('Evolution of y1 and y2')
f1.savefig('y1_and_y2_1.png')
 
 
# == Plotting direction fields and trajectories in the phase plane ==
# We will plot some trajectories in a phase plane for different starting
# points between X__f0 and X_f1 (depending on the case).
# 
# We will use matplotlib's colormap to define colors for the trajectories.
# These colormaps are very useful to make nice plots.
# Have a look at [http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps ShowColormaps] if you want more information.
# 
values  = linspace(0.3, 0.9, 5)                          # position of X0 between X_f0 and X_f1
vcolors = p.cm.autumn_r(linspace(0.3, 1., len(values)))  # colors for each trajectory

f2 = p.figure()

#-------------------------------------------------------
# plot trajectories
for v, col in zip(values, vcolors): 
    X0 = v * X_f1                               # starting point
    X = integrate.odeint( dX_dt, X0, t)         # we don't need infodict here
    p.plot( X[:,0], X[:,1], lw=3.5*v, color=col, label='X0=(%.f, %.f)' % ( X0[0], X0[1]) )

#-------------------------------------------------------
# define a grid and compute direction at each point
ymax = p.ylim(ymin=-5)[1]                        # get axis limits
xmax = p.xlim(xmin=-5)[1] 
nb_points   = 30                      

x = linspace(-xmax, xmax, nb_points)
y = linspace(-ymax, ymax, nb_points)

X1 , Y1  = meshgrid(x, y)                         # create a grid
DX1, DY1 = dX_dt([X1, Y1])                      # compute growth rate on the gridt
M = (hypot(DX1, DY1))                           # Norm of the growth rate 
M[ M == 0] = 1.                                 # Avoid zero division errors 
DX1 /= M                                        # Normalize each arrows
DY1 /= M                                  

#-------------------------------------------------------
# Drow direction fields, using matplotlib 's quiver function
# I choose to plot normalized arrows and to use colors to give information on
# the growth speed

p.title('Trajectories and direction fields')
Q = p.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.jet)
p.xlabel('Number of y1')
p.ylabel('Number of y2')
p.legend()
p.grid()
p.xlim(-xmax, xmax)
p.ylim(-ymax, ymax)
f2.savefig('y1_and_y2_2.png')

print 'OK!'
#print 'v %d X0=(%2.f,%2.f)' % (v, X0[0], X0[1])
    
p.show()

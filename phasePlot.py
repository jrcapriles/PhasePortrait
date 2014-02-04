# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 16:09:43 2014

@author: joser
"""

# du/dt =  a*u -   b*u*v
# dv/dt = -c*v + d*b*u*v 
# We will use X=[u, v] to describe the states

from numpy import *
import pylab as p
import init as init

#List of the function names availables
FuntionNameList = ["Hyperbolic", "Simple", "Magnetic", "Duffing", "Vanderpol"]

#Select the function that you want to work with
functionName = "Simple"

dxfunction, dx2function, dxic = init.init(functionName)

# load initials conditions to test
X0 = array([1, 1])                      

# Before using SciPy to integrate this system, we will have a closer look on 
# position equilibrium. Equilibrium occurs when the x_dot is equal to 0.

#Test initial condition (should be true)
def testIC( fun, *args ):
    all(fun(args[0]) == zeros(2) ) and all(fun(args[1]) == zeros(2) )
    print 'IC test passed!'


testIC(dxfunction,dxic[0],dxic[1])

# === Stability of the fixed points ===
# Near equilibrium points the system can be linearized:
# dX_dt = A_f*X where A is the Jacobian matrix evaluated at the corresponding point.

def evalJacobian( fun, *args ):
    A = fun(args[0])
    print 'Jacobian evaluation test passed!'
    return A
    
#Call eval Jacobian function
A_f1 = evalJacobian(dx2function,dxic[1])  
# whose eigenvalues are:
lambda1, lambda2 = linalg.eigvals(A_f1)
T_f1 = 2*pi/abs(lambda1)               

# == Integrating the ODE using scipy.integate ==
# Now we will use the scipy.integrate module to integrate the ODEs.

from scipy import integrate

t = linspace(0, 15,  1000)              # time


def integrateFucn( fun, *args ):
    X, infodict = integrate.odeint(fun, args[0], args[1], full_output=True)
    print 'Integrate function test passed!'
    return X, infodict


X, infodict = integrateFucn(dxfunction, X0, t)
infodict['message']                     # >>> 'Integration successful.'
 
y1, y2 = X.T

#plot time response of the system
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
# We will use matplotlib's colormap to define colors for the trajectories.

values  = linspace(0.3, 0.9, 5)                          # position of X0 between X_f0 and X_f1
vcolors = p.cm.autumn_r(linspace(0.3, 1., len(values)))  # colors for each trajectory

# plot trajectories
f2 = p.figure()
for v, col in zip(values, vcolors): 
    X0 = v * dxic[1]                               # starting point
    X = integrate.odeint( dxfunction, X0, t)                 # we don't need infodict here
    p.plot( X[:,0], X[:,1], lw=3.5*v, color=col, label='X0=(%.3f, %.3f)' % ( X0[0], X0[1]) )
    #print 'X0=(%2.f,%2.f) => I ~ %.1f |delta = %.3G %%' % (X0[0], X0[1], I_mean, delta) Add feedback

# define a grid and compute direction at each point
ymax = p.ylim(ymin=-5)[1]                        # get axis limits
xmax = p.xlim(xmin=-5)[1] 
nb_points   = 30                      

x = linspace(-xmax, xmax, nb_points)
y = linspace(-ymax, ymax, nb_points)

X1 , Y1  = meshgrid(x, y)                       # create a grid


def computeGrowth( fun, *args ):
    DX1, DY1 = fun([args[0], args[1]])          # compute growth rate on the gridt
    print 'Computed Growth test passed!'
    return DX1, DY1


DX1, DY1 = computeGrowth(dxfunction,X1,Y1)      # compute growth rate on the gridt

#DX1, DY1 = dX_dt_Vanderpol([X1, Y1])           # compute growth rate on the gridt
M = (hypot(DX1, DY1))                           # Norm of the growth rate 
M[ M == 0] = 1.                                 # Avoid zero division errors 
DX1 /= M                                        # Normalize each arrows
DY1 /= M                                  


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
p.show()


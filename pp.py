# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:53:18 2014

@author: joser
"""

from numpy import *
import pylab as p
import init as init
from scipy import integrate

#Test initial condition (should be true)
def testIC( fun, *args ):
    result = all(fun(args[0]) == zeros(2) ) and all(fun(args[1]) == zeros(2) )
    if not result: 
        print 'Error, equilibrium point should be equal to zero! Check initial conditions!'
        
def evalJacobian( fun, *args ):
    A = fun(args[0])
    print 'Computing Jacobians..'
    return A

def integrateFucn( fun, *args ):
    X, infodict = integrate.odeint(fun, args[0], args[1], full_output=True)
    print 'Solving differential equations..'
    return X, infodict   

def computeGrowth( fun, *args ):
    DX1, DY1 = fun([args[0], args[1]])          # compute growth rate on the gridt
    print 'Computing growing rate..'
    return DX1, DY1

    
def phasePlane(functionName, IC = None):
    
    dxfunction, dx2function, dxic = init.init(functionName)
    print dxic
    if (IC is not None):
        dxic = IC
    
    X0 = array([1, 1])                      

    testIC(dxfunction,dxic[0],dxic[1])
    A_f1 = evalJacobian(dx2function,dxic[1])  

    lambda1, lambda2 = linalg.eigvals(A_f1)
    t = linspace(0, 15,  1000)              # time
    
    X, infodict = integrateFucn(dxfunction, X0, t)
    infodict['message']                     # >>> 'Integration successful.'
 
    y1, y2 = X.T


    f1 = p.figure()
    p.plot(t, y1, 'r-', label='y1(t)')
    p.plot(t, y2  , 'b-', label='y2(t)')
    p.grid()
    p.legend(loc='best')
    p.xlabel('time')
    p.ylabel('outputs')
    p.title('Evolution of y1 and y2')
    f1.savefig('plots/' + functionName + '_y1_and_y2_outputs.png')
 
    values  = linspace(0.3, 0.9, 5)                          # position of X0 between X_f0 and X_f1
    vcolors = p.cm.autumn_r(linspace(0.3, 1., len(values)))  # colors for each trajectory


    f2 = p.figure()
    for v, col in zip(values, vcolors): 
        X0 = v * dxic[1]                               # starting point
        X = integrate.odeint( dxfunction, X0, t)                 # we don't need infodict here
        p.plot( X[:,0], X[:,1], lw=3.5*v, color=col, label='Xo=(%.3f, %.3f)' % ( X0[0], X0[1]) )



    ymax = p.ylim(ymin=-5)[1]                        # get axis limits
    xmax = p.xlim(xmin=-5)[1] 
    nb_points   = 30                      

    x = linspace(-xmax, xmax, nb_points)
    y = linspace(-ymax, ymax, nb_points)

    X1 , Y1  = meshgrid(x, y)                       # create a grid


    DX1, DY1 = computeGrowth(dxfunction,X1,Y1)      # compute growth rate on the gridt

    M = (hypot(DX1, DY1))                           # Norm of the growth rate 
    M[ M == 0] = 1.                                 # Avoid zero division errors 
    DX1 /= M                                        # Normalize each arrows
    DY1 /= M                                  


    p.title('Trajectories and direction fields')
    Q = p.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.jet)
    p.xlabel('Number of y1')
    p.ylabel('Number of y2')
    p.legend()
    p.grid()
    p.xlim(-xmax, xmax)
    p.ylim(-ymax, ymax)
    f2.savefig('plots/' + functionName + '_y1_and_y2_field.png')

    p.show()


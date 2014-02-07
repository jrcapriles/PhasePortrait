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
    return -DX1, -DY1


    
def phasePlane(functionName, IC = None, dim = None, numXo = None):
    
    dxfunction, dx2function, dxic = init.init(functionName)
    
    if (IC is not None):
        dxic = IC
   
    X0 = array([1, 1])                      

    testIC(dxfunction,dxic[0],dxic[1])
    
    A_f0 = evalJacobian(dx2function,dxic[0])
    A_f1 = evalJacobian(dx2function,dxic[1])  

    lambda1, lambda2 = linalg.eigvals(A_f1)
    t = linspace(0, 15,  1000)              # time
    
    X, infodict = integrateFucn(dxfunction, X0, t)
    infodict['message']                     # >>> 'Integration successful.'
 
    y1, y2 = X.T

    #Time response of the system
    f1 = p.figure()
    p.plot(t, y1, 'r-', label='y1(t)')
    p.plot(t, y2  , 'b-', label='y2(t)')
    p.grid()
    p.legend(loc='best')
    p.xlabel('time')
    p.ylabel('outputs')
    p.title('Evolution of y1 and y2')
    f1.savefig('plots/' + functionName + '_y1_and_y2_outputs.png')
    
    if (numXo is None):
        numXo = 5

    xvalues  = linspace(dxic[0][0], dxic[1][0], numXo)                          # position of X0 between X_f0 and X_f1
    yvalues  = linspace(dxic[0][1], dxic[1][1], numXo)                          # position of X0 between X_f0 and X_f1
        
    vcolors = p.cm.autumn_r(linspace(0.3, 0.9, len(xvalues)))  # colors for each trajectory

    #Phase plane of the system
    f2 = p.figure()
    t = linspace(0, 40,  1000)
    for xv, yv, col in zip(xvalues, yvalues, vcolors): 
        X0 = array([xv,yv])
        X = integrate.odeint( dxfunction, X0, t)                 # we don't need infodict here
        p.plot( X[:,0], X[:,1], lw=3.5, color=col, label='Xo=(%.3f, %.3f)' % ( X0[0], X0[1]) )

    if (dim is not None):
        #Using dimension from GUI or function arguments
        xmin = dim[0]  
        xmax = dim[1]
        ymin = dim[2]
        ymax = dim[3]

    #Set the number of points to be used
    points = int((abs(max(dim))+abs(min(dim)))/0.2)
    if points < 30:
        points =30                     

    x = linspace(-xmax, xmax, points)
    y = linspace(-ymax, ymax, points)

    X1 , Y1  = meshgrid(x, y)                       # create a grid
    DX1, DY1 = computeGrowth(dxfunction,X1,Y1)      # compute growth rate on the gridt
    M = (hypot(DX1, DY1))                           # Norm of the growth rate 
    M[ M == 0] = 1.                                 # Avoid zero division errors 
    DX1 /= M                                        # Normalize each arrows
    DY1 /= M                                  


    p.title('Trajectories and direction fields')
    Q = p.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.jet)
    p.xlabel('x')
    p.ylabel('x dot')
    p.legend()
    p.grid()
    p.xlim(-xmax, xmax)
    p.ylim(-ymax, ymax)
    f2.savefig('plots/' + functionName + '_y1_and_y2_field.png')

    p.show()


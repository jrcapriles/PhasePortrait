# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:53:18 2014

@author: joser
"""

from numpy import *
import pylab as p
import init as init
from scipy import integrate
from matplotlib.figure import Figure
#from matplotlib.pyplot import *

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
    
    if args[2]=='Default': 
        X, infodict = integrate.odeint(fun, args[0], args[1], full_output=True)
        print 'Solving differential equations..'
        print len(X)
        return X, infodict   
    else:
        
        solver = integrate.ode(fun).set_integrator(args[2], method= 'bdf').set_initial_value(args[0],args[1][0])
        i=0
        Y = []
        while solver.successful() and solver.t < args[1][-1]:
            print 'time'
            print args[1][i]
            solver.integrate(args[1][i])
            Y.append(solver.y)
            i+=1
#            
        print 'Solver finished OK? : %r' % (solver.successful())
        return Y
        #Check why it fails....
        
#time
#0.0
#time
#0.015015015015
# ZVODE--  ISTATE (=I1) .gt. 1 but ZVODE not initialized      
#      In above message,  I1 =         2
#/usr/lib/python2.7/dist-packages/scipy/integrate/ode.py:689: UserWarning: zvode: Illegal input detected. (See printed message.)
#  self.messages.get(istate, 'Unexpected istate=%s'%istate))
#Solver finished OK? : False
        
        

def computeGrowth( fun, *args ):
    DX1, DY1 = fun([args[0], args[1]])          # compute growth rate on the gridt
    print 'Computing growing rate..'
    return DX1, DY1


    
def phasePlane(functionName, IC = None, dim = None, numXo = None, ODESolver = 'Default', simSpecs = None):
    
    dxfunction, dx2function, dxic = init.init(functionName)
    
    if (IC is not None):
        dxic = IC
   
    if (simSpecs is not None):
        tInit = simSpecs[0]
        tFinal = simSpecs[1]
        numT = simSpecs[2]
    else:
        tInit = 0.0
        tFinal = 15
        numT = 1000
    
    #similiar to step response
    X0 = array([1, 1])                      

    testIC(dxfunction,dxic[0],dxic[1])
    
    A_f1 = evalJacobian(dx2function,dxic[1])  

    lambda1, lambda2 = linalg.eigvals(A_f1)
       
        
    t = linspace(tInit, tFinal,  numT)              # time
    
    X, infodict = integrateFucn(dxfunction, X0, t, ODESolver)
#    infodict['message']                     # >>> 'Integration successful.'

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

    # initial conditions points
    xvalues  = linspace(dxic[0][0], dxic[1][0], numXo)                          # position of X0 between X_f0 and X_f1
    yvalues  = linspace(dxic[0][1], dxic[1][1], numXo)                          # position of X0 between X_f0 and X_f1
    
    # set of colors used in each line
    vcolors = p.cm.autumn_r(linspace(0.3, 0.9, len(xvalues)))  # colors for each trajectory

    #Phase plane of the system
    f2 = p.figure()
    f21 = p.subplot(111)

    t = linspace(tInit, tFinal,  numT)
    
    
    
    for xv, yv, col in zip(xvalues, yvalues, vcolors): 
        X0 = array([xv,yv])
        X = integrate.odeint( dxfunction, X0, t)                 # we don't need infodict here
        f21.plot( X[:,0], X[:,1], lw=3.5, color=col, label='Xo=(%.3f, %.3f)' % ( X0[0], X0[1]) )

        # Shink current axis by 10%
    box = f21.get_position()
    f21.set_position([box.x0, box.y0, box.width * 0.9, box.height])

        # Put a legend to the right of the current axis
    f21.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  
    if (dim is not None):
        #Using dimension from GUI or function arguments
        xmin = dim[0]  
        ymin = dim[1]
        xmax = dim[2]
        ymax = dim[3]

    #Set the number of points to be used
    points = int((abs(max(dim))+abs(min(dim)))/0.2)
    if points < 30:
        points = 30                     

    x = linspace(xmin, xmax, points)
    y = linspace(ymin, ymax, points)

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
    #p.legend()
    p.grid()
    p.xlim(xmin, xmax)
    p.ylim(ymin, ymax)
    f2.savefig('plots/' + functionName + '_y1_and_y2_field.png')

    p.show()
    return p

def tResponse(functionName, IC = None, dim = None, numXo = None, ODESolver = 'Default', simSpecs = None):

    dxfunction, dx2function, dxic = init.init(functionName)
    
    if (simSpecs is not None):
        tInit = simSpecs[0]
        tFinal = simSpecs[1]
        numT = simSpecs[2]
    else:
        tInit = 0.0
        tFinal = 15
        numT = 1000
    
   
    #similiar to step response
    X0 = IC

    t = linspace(tInit, tFinal,  numT)              # time
   
    X, infodict = integrateFucn(dxfunction, X0, t, ODESolver)
#    infodict['message']                     # >>> 'Integration successful.'

    y1, y2 = X.T
 
    #Time response of the system
    f1 = p.figure(figsize=(5,4), dpi=100)
    p.plot(t, y1, 'r-', label='y1(t)')
    p.plot(t, y2  , 'b-', label='y2(t)')
    p.grid()
    p.legend(loc='best')
    p.xlabel('time')
    p.ylabel('outputs')
    p.title('Evolution of y1 and y2')
    #p.show()
    
    return f1
    
def phasePlaneGUI(functionName, IC = None, dim = None, numXo = None, ODESolver = 'Default', simSpecs = None):
    
    dxfunction, dx2function, dxic = init.init(functionName)
    
    if (IC is not None):
        dxic = IC
   
    if (simSpecs is not None):
        tInit = simSpecs[0]
        tFinal = simSpecs[1]
        numT = simSpecs[2]
    else:
        tInit = 0.0
        tFinal = 15
        numT = 1000
    
    #similiar to step response
    X0 = IC[1]                      

    testIC(dxfunction,dxic[0],dxic[1])
    
    A_f1 = evalJacobian(dx2function,dxic[1])  

    lambda1, lambda2 = linalg.eigvals(A_f1)
       
        
    t = linspace(tInit, tFinal,  numT)              # time
    
    X, infodict = integrateFucn(dxfunction, X0, t, ODESolver)
#    infodict['message']                     # >>> 'Integration successful.'

    y1, y2 = X.T

    #Time response of the system
#    f1 = p.figure()
#    p.plot(t, y1, 'r-', label='y1(t)')
#    p.plot(t, y2  , 'b-', label='y2(t)')
#    p.grid()
#    p.legend(loc='best')
#    p.xlabel('time')
#    p.ylabel('outputs')
#    p.title('Evolution of y1 and y2')
#    f1.savefig('plots/' + functionName + '_y1_and_y2_outputs.png')
#    
    if (numXo is None):
        numXo = 5

    # initial conditions points
    xvalues  = linspace(dxic[0][0], dxic[1][0], numXo)                          # position of X0 between X_f0 and X_f1
    yvalues  = linspace(dxic[0][1], dxic[1][1], numXo)                          # position of X0 between X_f0 and X_f1
    
    # set of colors used in each line
    vcolors = p.cm.autumn_r(linspace(0.3, 0.9, len(xvalues)))  # colors for each trajectory

    #Phase plane of the system
    #figsize=(6,6)
    f2 = Figure(figsize=(5,4), dpi=100)#p.figure()
    f21 = f2.add_subplot(111)

    t = linspace(tInit, tFinal,  numT)
    
    
    
    for xv, yv, col in zip(xvalues, yvalues, vcolors): 
        X0 = array([xv,yv])
        X = integrate.odeint( dxfunction, X0, t)                 # we don't need infodict here
        f21.plot( X[:,0], X[:,1], lw=3.5, color=col, label='Xo=(%.3f, %.3f)' % ( X0[0], X0[1]) )

        # Shink current axis by 10%
    box = f21.get_position()
    f21.set_position([box.x0, box.y0, box.width * 0.9, box.height])

        # Put a legend to the right of the current axis
    #f21.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  
    if (dim is not None):
        #Using dimension from GUI or function arguments
        xmin = dim[0]  
        ymin = dim[1]
        xmax = dim[2]
        ymax = dim[3]

    #Set the number of points to be used
    points = int((abs(max(dim))+abs(min(dim)))/0.2)
    if points < 30:
        points = 30                     

    x = linspace(xmin, xmax, points)
    y = linspace(ymin, ymax, points)

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
    #p.legend()
    p.grid()
    p.xlim(xmin, xmax)
    p.ylim(ymin, ymax)
    #p.savefig('plots/' + functionName + 'field.png')
    #p.show()
    
    
    ax = f2.gca()
    ax.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.jet)
    
    
#    f2.savefig('plots/' + functionName + '_y1_and_y2_field.png')
    
    #p.show()
    return f2

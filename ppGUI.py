# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 18:02:40 2014

@author: joser
"""

#!/usr/bin/python

import Tkinter
from numpy import array


from pp import phasePlane

class PhasePortraitGUI(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        
        #============Plot Button============#
        button = Tkinter.Button(self,text=u"Phase Plot Me!", command=self.plot)
        button.grid(column=3,row=1)
        
        #============Function Selector============#
        label = Tkinter.Label(self, text = "Functions:")
        label.grid(column=0,row=0)
        self.funcVar = Tkinter.StringVar()
        self.funcVar.set("Vanderpol")
        #list of function availables. Need to be updated each a new function is added        
        self.choices = ['Simple', 'Vanderpol', 'Duffing','Magnetic', 'Violin'] #'Hyperbolic'
        #Drop down menu to select function to plot
        option = Tkinter.OptionMenu(self, self.funcVar, *self.choices)
        option.grid(column = 1, row =0)

        #============ODE solver============#
        label = Tkinter.Label(self, text = "ODE Solver:")
        label.grid(column=0,row=1)
        self.ODESolver = Tkinter.StringVar()
        self.ODESolver.set('Default')
        self.ODEchoices = ['Default', 'vode', 'zvode','lsoda', 'dopri5','dop853'] #'Hyperbolic'
        ODESolverOp = Tkinter.OptionMenu(self, self.ODESolver, *self.ODEchoices)
        ODESolverOp.grid(column = 1, row =1)    
    
        #============Initial Conditions============#
        label = Tkinter.Label(self, text = "Initial Conditions:")
        label.grid(column=1,row=4)
        label = Tkinter.Label(self, text = "(X0,Y0) = (")
        label.grid(column=0,row=5)
        label = Tkinter.Label(self, text = "(X1,Y1) = (")
        label.grid(column=0,row=6)
        label = Tkinter.Label(self, text = ",")
        label.grid(column=2,row=5)
        label = Tkinter.Label(self, text = ",")
        label.grid(column=2,row=6)
        label = Tkinter.Label(self, text = ")")
        label.grid(column=4,row=5)
        label = Tkinter.Label(self, text = ")")
        label.grid(column=4,row=6)
        
        self.X0 = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.X0)
        self.entry.grid(column=1,row=5)
        self.X0.set("0.0")
        self.Y0 = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.Y0)
        self.entry.grid(column=3,row=5)
        self.Y0.set("0.0")
        self.X1 = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.X1)
        self.entry.grid(column=1,row=6)
        self.X1.set("1.0")
        self.Y1 = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.Y1)
        self.entry.grid(column=3,row=6)
        self.Y1.set("1.0")

        #============Plot Dimensions============#
        label = Tkinter.Label(self, text = "Plot Dimension:")
        label.grid(column=1,row=7)
        label = Tkinter.Label(self, text = "(Xmin,Xmax) = (")
        label.grid(column=0,row=8)
        label = Tkinter.Label(self, text = "(Ymin,Ymax) = (")
        label.grid(column=0,row=9)
        label = Tkinter.Label(self, text = ",")
        label.grid(column=2,row=8)
        label = Tkinter.Label(self, text = ",")
        label.grid(column=2,row=9)
        label = Tkinter.Label(self, text = ")")
        label.grid(column=4,row=8)
        label = Tkinter.Label(self, text = ")")
        label.grid(column=4,row=9)
        
        self.Xmin = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.Xmin)
        self.entry.grid(column=1,row=8)
        self.Xmin.set("-5.0")
        self.Ymin = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.Ymin)
        self.entry.grid(column=1,row=9)
        self.Ymin.set("-5.0")
        self.Xmax = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.Xmax)
        self.entry.grid(column=3,row=8)
        self.Xmax.set("5.0")
        self.Ymax = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.Ymax)
        self.entry.grid(column=3,row=9)
        self.Ymax.set("5.0")

        #============Num of Plots============#
        label = Tkinter.Label(self, text = "Num Lines:")
        label.grid(column=0,row=10)
        
        self.numPlots = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.numPlots)
        self.entry.grid(column=1,row=10)
        self.numPlots.set("5")
        
        #============Simulation Parameters============# 
        label = Tkinter.Label(self, text = "Simulation parameters:")
        label.grid(column=1,row=12)        
        label = Tkinter.Label(self, text = "T init:")
        label.grid(column=0,row=13)        
        label = Tkinter.Label(self, text = "T final:")
        label.grid(column=0,row=14)        
        label = Tkinter.Label(self, text = "Num points:")
        label.grid(column=0,row=15) 
        
        self.TInit = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.TInit)
        self.entry.grid(column=1,row=13)
        self.TInit.set("0.0")
        self.TFinal = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.TFinal)
        self.entry.grid(column=1,row=14)
        self.TFinal.set("15.0")
        self.NumPoints = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.NumPoints)
        self.entry.grid(column=1,row=15)
        self.NumPoints.set("1000")

        #============Set the GUI environment============#                 
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def plot(self):
        #Function to call phase plane plot function
        IC0=array([float(self.X0.get()), float(self.Y0.get())])
        IC1=array([float(self.X1.get()), float(self.Y1.get())])
        dim = [float(self.Xmin.get()),float(self.Ymin.get()),float(self.Xmax.get()),float(self.Ymax.get())]
        
        print phasePlane(self.funcVar.get(),[IC0,IC1],dim,int(self.numPlots.get()),self.ODESolver.get(),
                         [float(self.TInit.get()),float(self.TFinal.get()),int(self.NumPoints.get())])

if __name__ == "__main__":
    GUI = PhasePortraitGUI(None)
    GUI.title('Phase Plane GUI')
    GUI.mainloop()
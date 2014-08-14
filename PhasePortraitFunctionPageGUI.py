# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 22:32:52 2014

@author: joser
"""

import Tkinter as tk
import ttk

from pp import phasePlaneGUI
from pp import tResponse
from PhasePortraitHomePageGUI import HomePage


import matplotlib
matplotlib.use('TkAgg')

from numpy import array
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import *
from matplotlib.figure import Figure
import sys


TITLE_FONT = ("Helvetica", 18, "bold")

class FunctionPage(tk.Frame):
    def __init__(self, parent, controller,fun):
        tk.Frame.__init__(self, parent)

        self.grid()
        self.fun=fun
       
        #============Function===========#
        label = tk.Label(self, text="Function: "+fun, font=TITLE_FONT).grid(column=1,row=0, pady=10)

        self.createButtons(controller)
        
        self.createLabels()
        
        self.createVariables()
        
        self.createGrid()
       
        

        

    def createButtons(self,controller):
        self.button_go_back = tk.Button(self, text="Go back!", command=lambda: controller.show_screen(0)).grid(column = 3, row =19)
        self.button_phase_plot = tk.Button(self,text=u"Phase Plot Me!", command=self.plot).grid(column=3,row=20)
        self.button_time_response = tk.Button(self,text=u"Time Response!", command=self.tResponse).grid(column=3,row=21)

        self.ODESolver = tk.StringVar()
        self.ODESolver.set('Default')
        self.ODEchoices = ['Default', 'vode', 'zvode','lsoda', 'dopri5','dop853'] #'Hyperbolic'
        self.ODESolverOp = tk.OptionMenu(self, self.ODESolver, *self.ODEchoices).grid(column = 1, row =3)    
    
    
    def createGrid(self):
        ttk.Separator(self,orient="horizontal").grid(column=0,row=1, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=4, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=8, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=11, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=17, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=22, sticky="ew", columnspan="5")

    def createLabels(self):
        #============ODE solver============#
        label = tk.Label(self, text = "ODE Solver:").grid(column=0,row=3)
        #============PP Initial Conditions============#
        label = tk.Label(self, text = "PP Initial Conditions:").grid(column=0,row=5)
        label = tk.Label(self, text = "(X0,Y0) = (").grid(column=0,row=6)
        label = tk.Label(self, text = "(X1,Y1) = (").grid(column=0,row=7)
        label = tk.Label(self, text = ",").grid(column=2,row=6)
        label = tk.Label(self, text = ",").grid(column=2,row=7)
        label = tk.Label(self, text = ")").grid(column=4,row=6)
        label = tk.Label(self, text = ")").grid(column=4,row=7)
        #============Time Initial Conditions============#
        label = tk.Label(self, text = "Time Initial Conditions:").grid(column=0,row=9)
        label = tk.Label(self, text = "(t0,t1) = (").grid(column=0,row=10)
        label = tk.Label(self, text = ",").grid(column=2,row=10)
        label = tk.Label(self, text = ")").grid(column=4,row=10)
        #============Plot Dimensions============#
        label = tk.Label(self, text = "Plot Dimension:").grid(column=0,row=12)
        label = tk.Label(self, text = "(Xmin,Xmax) = (").grid(column=0,row=13)
        label = tk.Label(self, text = "(Ymin,Ymax) = (").grid(column=0,row=14)
        label = tk.Label(self, text = ",").grid(column=2,row=13)
        label = tk.Label(self, text = ",").grid(column=2,row=14)
        label = tk.Label(self, text = ")").grid(column=4,row=13)
        label = tk.Label(self, text = ")").grid(column=4,row=14)
        #============Num of Plots============#
        label = tk.Label(self, text = "Num Plots:")
        label.grid(column=0,row=16)
        #============Simulation Parameters============# 
        label = tk.Label(self, text = "Simulation parameters:").grid(column=0,row=18)        
        label = tk.Label(self, text = "T init:").grid(column=0,row=19)        
        label = tk.Label(self, text = "T final:").grid(column=0,row=20)        
        label = tk.Label(self, text = "Num points:").grid(column=0,row=21) 
        
    def createVariables(self):
        #============PP Initial Conditions============#
        self.X0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.X0).grid(column=1,row=6)
        self.X0.set("0.0")
        self.Y0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Y0).grid(column=3,row=6)
        self.Y0.set("0.0")
        self.X1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.X1).grid(column=1,row=7)
        self.X1.set("1.0")
        self.Y1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Y1).grid(column=3,row=7)
        self.Y1.set("1.0")
        #============Time Initial Conditions============#
        self.t0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.t0).grid(column=1,row=10)
        self.t0.set("0.0")
        self.t1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.t1).grid(column=3,row=10)
        self.t1.set("1.0")
        #============Plot Dimensions============#        
        self.Xmin = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Xmin).grid(column=1,row=13)
        self.Xmin.set("-5.0")
        self.Ymin = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Ymin).grid(column=1,row=14)
        self.Ymin.set("-5.0")
        self.Xmax = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Xmax).grid(column=3,row=13)
        self.Xmax.set("5.0")
        self.Ymax = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Ymax).grid(column=3,row=14)
        self.Ymax.set("5.0")
        #============Num of Plots============#
        self.numPlots = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.numPlots).grid(column=1,row=16)
        self.numPlots.set("5")
        #============Simulation Parameters============#
        self.TInit = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.TInit).grid(column=1,row=19)
        self.TInit.set("0.0")
        self.TFinal = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.TFinal).grid(column=1,row=20)
        self.TFinal.set("15.0")
        self.NumPoints = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.NumPoints).grid(column=1,row=21)
        self.NumPoints.set("1000")
        
    def enableZoom(self):
        self.button_zoom_in = tk.Button(self,text=u"+", command=self.zoom_in).grid(column=4,row=23)
        self.button_zoom_out = tk.Button(self,text=u"-", command=self.zoom_out).grid(column=5,row=23)
        
    def plot(self):
        self.enableZoom()
       #Function to call phase plane plot function
        IC0=array([float(self.X0.get()), float(self.Y0.get())])
        IC1=array([float(self.X1.get()), float(self.Y1.get())])
        dim = [float(self.Xmin.get()),float(self.Ymin.get()),float(self.Xmax.get()),float(self.Ymax.get())]
        
        p = phasePlaneGUI(self.fun,[IC0,IC1],dim,int(self.numPlots.get()),self.ODESolver.get(),
                         [float(self.TInit.get()),float(self.TFinal.get()),int(self.NumPoints.get())])
        
        canvas = FigureCanvasTkAgg(p, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(column=0, row= 24, columnspan=6)# side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def tResponse(self):
        #Function to call phase plane plot function
        IC=array([float(self.t0.get()), float(self.t1.get())])
        dim = [float(self.Xmin.get()),float(self.Ymin.get()),float(self.Xmax.get()),float(self.Ymax.get())]
        
        p = tResponse(self.fun,IC,dim,int(self.numPlots.get()),self.ODESolver.get(),
                         [float(self.TInit.get()),float(self.TFinal.get()),int(self.NumPoints.get())])

        canvas = FigureCanvasTkAgg(p, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(column=0, row= 24, columnspan=6)# side=tk.TOP, fill=tk.BOTH, expand=1)

    def zoom_in(self):
        #To do
        print "+"
        
        
    def zoom_out(self):
        #To do
        print "-"
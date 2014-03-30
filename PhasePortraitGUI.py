# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 11:45:37 2014

@author: joser
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 11:19:38 2014

@author: joser
"""

import Tkinter as tk
import ttk

from pp import phasePlane, phasePlaneGUI

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi, array
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import *
from matplotlib.figure import Figure
import sys


TITLE_FONT = ("Helvetica", 18, "bold")

class LieGUIApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # screens is a stack of frames
        screens = tk.Frame(self)
        screens.pack(side="top", fill="both", expand=True)
        screens.grid_rowconfigure(0, weight=1)
        screens.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (HomePage, PageSimple, PageVanderpol, PageDuffing, PageMagnetic, PageViolin):
            frame = F(screens, self)
            self.frames[F] = frame
            # stack all of the pages together; 
            # the one on the top will be visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_screen(HomePage)

    def show_screen(self, c):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.grid()
        
        self.label = tk.Label(self, text="Home page!", font=TITLE_FONT)
        self.label.grid(column=1,row=0, pady=10)

        self.label = tk.Label(self, text = "Functions:")
        self.label.grid(column=0,row=3)
        self.funcVar = tk.StringVar()
        self.funcVar.set("Vanderpol")
        self.choices = ['Simple', 'Vanderpol', 'Duffing','Magnetic', 'Violin'] #'Hyperbolic'
        #Drop down menu to select function to plot
        self.option = tk.OptionMenu(self, self.funcVar, *self.choices)
        self.option.grid(column = 1, row =3)
        
        self.select = tk.Button(self, text="Select",command=lambda: self.sel(self.funcVar.get(),controller))#lambda: controller.show_screen(PageOne))
        self.select.grid(column = 2, row =3)

    def sel(args,function,controller):
        #Switch to the coresponding page
        if function == 'Simple':
            controller.show_screen(PageSimple)
        elif function == 'Vanderpol':
            controller.show_screen(PageVanderpol)
        elif function == 'Duffing':
            controller.show_screen(PageDuffing)
        elif function == 'Magnetic':
            controller.show_screen(PageMagnetic)
        elif function == 'Violin': 
            controller.show_screen(PageViolin)



class PageSimple(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid()

        label = tk.Label(self, text="Simple Harmonic Oscillator", font=TITLE_FONT).grid(column=1,row=0, pady=10)
        #label = tk.Label(self, text = "A note...").grid(column=1,row=2, pady=10)
        
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_screen(HomePage)).grid(column = 3, row =14)
        
            #============Plot Button============#
        button2 = tk.Button(self,text=u"Phase Plot Me!", command=self.plot).grid(column=3,row=15)
    
        
        #============ODE solver============#
        label = tk.Label(self, text = "ODE Solver:").grid(column=0,row=3)
        self.ODESolver = tk.StringVar()
        self.ODESolver.set('Default')
        self.ODEchoices = ['Default', 'vode', 'zvode','lsoda', 'dopri5','dop853'] #'Hyperbolic'
        self.ODESolverOp = tk.OptionMenu(self, self.ODESolver, *self.ODEchoices).grid(column = 1, row =3)    
    
        #============Initial Conditions============#
        label = tk.Label(self, text = "Initial Conditions:").grid(column=0,row=5)
        label = tk.Label(self, text = "(X0,X1) = (").grid(column=0,row=6)
        label = tk.Label(self, text = "(Y0,Y1) = (").grid(column=0,row=7)
        label = tk.Label(self, text = ",").grid(column=2,row=6)
        label = tk.Label(self, text = ",").grid(column=2,row=7)
        label = tk.Label(self, text = ")").grid(column=4,row=6)
        label = tk.Label(self, text = ")").grid(column=4,row=7)
        
        self.X0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.X0).grid(column=1,row=6)
        self.X0.set("0.0")
        self.X1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.X1).grid(column=3,row=6)
        self.X1.set("1.0")
        self.Y0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Y0).grid(column=1,row=7)
        self.Y0.set("0.0")
        self.Y1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Y1).grid(column=3,row=7)
        self.Y1.set("1.0")

        #============Plot Dimensions============#
        label = tk.Label(self, text = "Plot Dimension:").grid(column=0,row=9)
        label = tk.Label(self, text = "(Xmin,Xmax) = (").grid(column=0,row=10)
        label = tk.Label(self, text = "(Ymin,Ymax) = (").grid(column=0,row=11)
        label = tk.Label(self, text = ",").grid(column=2,row=10)
        label = tk.Label(self, text = ",").grid(column=2,row=11)
        label = tk.Label(self, text = ")").grid(column=4,row=10)
        label = tk.Label(self, text = ")").grid(column=4,row=11)
        
        self.Xmin = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Xmin).grid(column=1,row=10)
        self.Xmin.set("-5.0")
        self.Ymin = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Ymin).grid(column=1,row=11)
        self.Ymin.set("-5.0")
        self.Xmax = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Xmax).grid(column=3,row=10)
        self.Xmax.set("5.0")
        self.Ymax = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.Ymax).grid(column=3,row=11)
        self.Ymax.set("5.0")

        #============Num of Plots============#
        label = tk.Label(self, text = "Num Lines:")
        label.grid(column=0,row=10)
        
        self.numPlots = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.numPlots).grid(column=1,row=10)
        self.numPlots.set("5")
        
        ttk.Separator(self,orient="horizontal").grid(column=0,row=1, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=4, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=8, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=12, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=19, sticky="ew", columnspan="5")
#        ttk.Separator(self,orient="vertical").grid(column=1,row=1, sticky="ns", rowspan="15")

        #============Simulation Parameters============# 
        label = tk.Label(self, text = "Simulation parameters:").grid(column=0,row=13)        
        label = tk.Label(self, text = "T init:").grid(column=0,row=14)        
        label = tk.Label(self, text = "T final:").grid(column=0,row=15)        
        label = tk.Label(self, text = "Num points:").grid(column=0,row=16) 
        
        self.TInit = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.TInit).grid(column=1,row=14)
        self.TInit.set("0.0")
        self.TFinal = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.TFinal).grid(column=1,row=15)
        self.TFinal.set("15.0")
        self.NumPoints = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.NumPoints).grid(column=1,row=16)
        self.NumPoints.set("1000")

        
    def plot(self):
        #Function to call phase plane plot function
        IC0=array([float(self.X0.get()), float(self.Y0.get())])
        IC1=array([float(self.X1.get()), float(self.Y1.get())])
        dim = [float(self.Xmin.get()),float(self.Ymin.get()),float(self.Xmax.get()),float(self.Ymax.get())]
        
        p = phasePlaneGUI('Simple',[IC0,IC1],dim,int(self.numPlots.get()),self.ODESolver.get(),
                         [float(self.TInit.get()),float(self.TFinal.get()),int(self.NumPoints.get())])
        
        
        canvas = FigureCanvasTkAgg(p, master=self)
        canvas.show()
        canvas.get_tk_widget().grid(column=6, row= 20)# side=tk.TOP, fill=tk.BOTH, expand=1)


        ##TODO: PASAR LA FIGURA COMO RETURN VALUE DE LA FUNCION Y AGREGAR LOS SELFS EN TODOS LADOS

class PageVanderpol(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="Vanderpol Oscillator", font=TITLE_FONT).grid(column=1,row=0, pady=10)
        #label = tk.Label(self, text = "A note...").grid(column=1,row=2, pady=10)
        
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_screen(HomePage)).grid(column = 3, row =14)
        
        #============ODE solver============#
        label = tk.Label(self, text = "ODE Solver:").grid(column=0,row=3)
        ODESolver = tk.StringVar()
        ODESolver.set('Default')
        ODEchoices = ['Default', 'vode', 'zvode','lsoda', 'dopri5','dop853'] #'Hyperbolic'
        ODESolverOp = tk.OptionMenu(self, ODESolver, *ODEchoices)
        ODESolverOp.grid(column = 1, row =3)    
    
        #============Initial Conditions============#
        label = tk.Label(self, text = "Initial Conditions:").grid(column=0,row=5)
        label = tk.Label(self, text = "(X0,X1) = (").grid(column=0,row=6)
        label = tk.Label(self, text = "(Y0,Y1) = (").grid(column=0,row=7)
        label = tk.Label(self, text = ",").grid(column=2,row=6)
        label = tk.Label(self, text = ",").grid(column=2,row=7)
        label = tk.Label(self, text = ")").grid(column=4,row=6)
        label = tk.Label(self, text = ")").grid(column=4,row=7)
        
        X0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=X0).grid(column=1,row=6)
        X0.set("0.0")
        X1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=X1).grid(column=3,row=6)
        X1.set("1.0")
        Y0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=Y0).grid(column=1,row=7)
        Y0.set("0.0")
        Y1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=Y1).grid(column=3,row=7)
        Y1.set("1.0")

        #============Plot Dimensions============#
        label = tk.Label(self, text = "Plot Dimension:").grid(column=0,row=9)
        label = tk.Label(self, text = "(Xmin,Xmax) = (").grid(column=0,row=10)
        label = tk.Label(self, text = "(Ymin,Ymax) = (").grid(column=0,row=11)
        label = tk.Label(self, text = ",").grid(column=2,row=10)
        label = tk.Label(self, text = ",").grid(column=2,row=11)
        label = tk.Label(self, text = ")").grid(column=4,row=10)
        label = tk.Label(self, text = ")").grid(column=4,row=11)
        
        Xmin = tk.StringVar()
        entry = tk.Entry(self,textvariable=Xmin).grid(column=1,row=10)
        Xmin.set("-5.0")
        Ymin = tk.StringVar()
        entry = tk.Entry(self,textvariable=Ymin).grid(column=1,row=11)
        Ymin.set("-5.0")
        Xmax = tk.StringVar()
        entry = tk.Entry(self,textvariable=Xmax).grid(column=3,row=10)
        Xmax.set("5.0")
        Ymax = tk.StringVar()
        entry = tk.Entry(self,textvariable=Ymax).grid(column=3,row=11)
        Ymax.set("5.0")

        #============Num of Plots============#
        label = tk.Label(self, text = "Num Lines:")
        label.grid(column=0,row=10)
        
        numPlots = tk.StringVar()
        entry = tk.Entry(self,textvariable=numPlots).grid(column=1,row=10)
        numPlots.set("5")
        
        ttk.Separator(self,orient="horizontal").grid(column=0,row=1, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=4, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=8, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=12, sticky="ew", columnspan="5")
#        ttk.Separator(self,orient="vertical").grid(column=1,row=1, sticky="ns", rowspan="15")

        #============Simulation Parameters============# 
        label = tk.Label(self, text = "Simulation parameters:").grid(column=0,row=13)        
        label = tk.Label(self, text = "T init:").grid(column=0,row=14)        
        label = tk.Label(self, text = "T final:").grid(column=0,row=15)        
        label = tk.Label(self, text = "Num points:").grid(column=0,row=16) 
        
        TInit = tk.StringVar()
        entry = tk.Entry(self,textvariable=TInit).grid(column=1,row=14)
        TInit.set("0.0")
        TFinal = tk.StringVar()
        entry = tk.Entry(self,textvariable=TFinal).grid(column=1,row=15)
        TFinal.set("15.0")
        NumPoints = tk.StringVar()
        entry = tk.Entry(self,textvariable=NumPoints).grid(column=1,row=16)
        NumPoints.set("1000")
        
        
        

class PageDuffing(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="Duffing Oscillator", font=TITLE_FONT).grid(column=1,row=0, pady=10)
        #label = tk.Label(self, text = "A note...").grid(column=1,row=2, pady=10)
        
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_screen(HomePage)).grid(column = 3, row =14)
        
        #============ODE solver============#
        label = tk.Label(self, text = "ODE Solver:").grid(column=0,row=3)
        ODESolver = tk.StringVar()
        ODESolver.set('Default')
        ODEchoices = ['Default', 'vode', 'zvode','lsoda', 'dopri5','dop853'] #'Hyperbolic'
        ODESolverOp = tk.OptionMenu(self, ODESolver, *ODEchoices)
        ODESolverOp.grid(column = 1, row =3)    
    
        #============Initial Conditions============#
        label = tk.Label(self, text = "Initial Conditions:").grid(column=0,row=5)
        label = tk.Label(self, text = "(X0,X1) = (").grid(column=0,row=6)
        label = tk.Label(self, text = "(Y0,Y1) = (").grid(column=0,row=7)
        label = tk.Label(self, text = ",").grid(column=2,row=6)
        label = tk.Label(self, text = ",").grid(column=2,row=7)
        label = tk.Label(self, text = ")").grid(column=4,row=6)
        label = tk.Label(self, text = ")").grid(column=4,row=7)
        
        X0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=X0).grid(column=1,row=6)
        X0.set("0.0")
        X1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=X1).grid(column=3,row=6)
        X1.set("1.0")
        Y0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=Y0).grid(column=1,row=7)
        Y0.set("0.0")
        Y1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=Y1).grid(column=3,row=7)
        Y1.set("1.0")

        #============Plot Dimensions============#
        label = tk.Label(self, text = "Plot Dimension:").grid(column=0,row=9)
        label = tk.Label(self, text = "(Xmin,Xmax) = (").grid(column=0,row=10)
        label = tk.Label(self, text = "(Ymin,Ymax) = (").grid(column=0,row=11)
        label = tk.Label(self, text = ",").grid(column=2,row=10)
        label = tk.Label(self, text = ",").grid(column=2,row=11)
        label = tk.Label(self, text = ")").grid(column=4,row=10)
        label = tk.Label(self, text = ")").grid(column=4,row=11)
        
        Xmin = tk.StringVar()
        entry = tk.Entry(self,textvariable=Xmin).grid(column=1,row=10)
        Xmin.set("-5.0")
        Ymin = tk.StringVar()
        entry = tk.Entry(self,textvariable=Ymin).grid(column=1,row=11)
        Ymin.set("-5.0")
        Xmax = tk.StringVar()
        entry = tk.Entry(self,textvariable=Xmax).grid(column=3,row=10)
        Xmax.set("5.0")
        Ymax = tk.StringVar()
        entry = tk.Entry(self,textvariable=Ymax).grid(column=3,row=11)
        Ymax.set("5.0")

        #============Num of Plots============#
        label = tk.Label(self, text = "Num Lines:")
        label.grid(column=0,row=10)
        
        numPlots = tk.StringVar()
        entry = tk.Entry(self,textvariable=numPlots).grid(column=1,row=10)
        numPlots.set("5")
        
        ttk.Separator(self,orient="horizontal").grid(column=0,row=1, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=4, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=8, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=12, sticky="ew", columnspan="5")
#        ttk.Separator(self,orient="vertical").grid(column=1,row=1, sticky="ns", rowspan="15")

        #============Simulation Parameters============# 
        label = tk.Label(self, text = "Simulation parameters:").grid(column=0,row=13)        
        label = tk.Label(self, text = "T init:").grid(column=0,row=14)        
        label = tk.Label(self, text = "T final:").grid(column=0,row=15)        
        label = tk.Label(self, text = "Num points:").grid(column=0,row=16) 
        
        TInit = tk.StringVar()
        entry = tk.Entry(self,textvariable=TInit).grid(column=1,row=14)
        TInit.set("0.0")
        TFinal = tk.StringVar()
        entry = tk.Entry(self,textvariable=TFinal).grid(column=1,row=15)
        TFinal.set("15.0")
        NumPoints = tk.StringVar()
        entry = tk.Entry(self,textvariable=NumPoints).grid(column=1,row=16)
        NumPoints.set("1000")

class PageMagnetic(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Magnetic Oscillator", font=TITLE_FONT).grid(column=1,row=0, pady=10)
        #label = tk.Label(self, text = "A note...").grid(column=1,row=2, pady=10)
        
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_screen(HomePage)).grid(column = 3, row =14)
        
        #============ODE solver============#
        label = tk.Label(self, text = "ODE Solver:").grid(column=0,row=3)
        ODESolver = tk.StringVar()
        ODESolver.set('Default')
        ODEchoices = ['Default', 'vode', 'zvode','lsoda', 'dopri5','dop853'] #'Hyperbolic'
        ODESolverOp = tk.OptionMenu(self, ODESolver, *ODEchoices)
        ODESolverOp.grid(column = 1, row =3)    
    
        #============Initial Conditions============#
        label = tk.Label(self, text = "Initial Conditions:").grid(column=0,row=5)
        label = tk.Label(self, text = "(X0,X1) = (").grid(column=0,row=6)
        label = tk.Label(self, text = "(Y0,Y1) = (").grid(column=0,row=7)
        label = tk.Label(self, text = ",").grid(column=2,row=6)
        label = tk.Label(self, text = ",").grid(column=2,row=7)
        label = tk.Label(self, text = ")").grid(column=4,row=6)
        label = tk.Label(self, text = ")").grid(column=4,row=7)
        
        X0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=X0).grid(column=1,row=6)
        X0.set("0.0")
        X1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=X1).grid(column=3,row=6)
        X1.set("1.0")
        Y0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=Y0).grid(column=1,row=7)
        Y0.set("0.0")
        Y1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=Y1).grid(column=3,row=7)
        Y1.set("1.0")

        #============Plot Dimensions============#
        label = tk.Label(self, text = "Plot Dimension:").grid(column=0,row=9)
        label = tk.Label(self, text = "(Xmin,Xmax) = (").grid(column=0,row=10)
        label = tk.Label(self, text = "(Ymin,Ymax) = (").grid(column=0,row=11)
        label = tk.Label(self, text = ",").grid(column=2,row=10)
        label = tk.Label(self, text = ",").grid(column=2,row=11)
        label = tk.Label(self, text = ")").grid(column=4,row=10)
        label = tk.Label(self, text = ")").grid(column=4,row=11)
        
        Xmin = tk.StringVar()
        entry = tk.Entry(self,textvariable=Xmin).grid(column=1,row=10)
        Xmin.set("-5.0")
        Ymin = tk.StringVar()
        entry = tk.Entry(self,textvariable=Ymin).grid(column=1,row=11)
        Ymin.set("-5.0")
        Xmax = tk.StringVar()
        entry = tk.Entry(self,textvariable=Xmax).grid(column=3,row=10)
        Xmax.set("5.0")
        Ymax = tk.StringVar()
        entry = tk.Entry(self,textvariable=Ymax).grid(column=3,row=11)
        Ymax.set("5.0")

        #============Num of Plots============#
        label = tk.Label(self, text = "Num Lines:")
        label.grid(column=0,row=10)
        
        numPlots = tk.StringVar()
        entry = tk.Entry(self,textvariable=numPlots).grid(column=1,row=10)
        numPlots.set("5")
        
        ttk.Separator(self,orient="horizontal").grid(column=0,row=1, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=4, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=8, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=12, sticky="ew", columnspan="5")
#        ttk.Separator(self,orient="vertical").grid(column=1,row=1, sticky="ns", rowspan="15")

        #============Simulation Parameters============# 
        label = tk.Label(self, text = "Simulation parameters:").grid(column=0,row=13)        
        label = tk.Label(self, text = "T init:").grid(column=0,row=14)        
        label = tk.Label(self, text = "T final:").grid(column=0,row=15)        
        label = tk.Label(self, text = "Num points:").grid(column=0,row=16) 
        
        TInit = tk.StringVar()
        entry = tk.Entry(self,textvariable=TInit).grid(column=1,row=14)
        TInit.set("0.0")
        TFinal = tk.StringVar()
        entry = tk.Entry(self,textvariable=TFinal).grid(column=1,row=15)
        TFinal.set("15.0")
        NumPoints = tk.StringVar()
        entry = tk.Entry(self,textvariable=NumPoints).grid(column=1,row=16)
        NumPoints.set("1000")


class PageViolin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Violin simulation", font=TITLE_FONT).grid(column=1,row=0, pady=10)
        #label = tk.Label(self, text = "A note...").grid(column=1,row=2, pady=10)
        
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_screen(HomePage)).grid(column = 3, row =14)
        
        #============ODE solver============#
        label = tk.Label(self, text = "ODE Solver:").grid(column=0,row=3)
        ODESolver = tk.StringVar()
        ODESolver.set('Default')
        ODEchoices = ['Default', 'vode', 'zvode','lsoda', 'dopri5','dop853'] #'Hyperbolic'
        ODESolverOp = tk.OptionMenu(self, ODESolver, *ODEchoices)
        ODESolverOp.grid(column = 1, row =3)    
    
        #============Initial Conditions============#
        label = tk.Label(self, text = "Initial Conditions:").grid(column=0,row=5)
        label = tk.Label(self, text = "(X0,X1) = (").grid(column=0,row=6)
        label = tk.Label(self, text = "(Y0,Y1) = (").grid(column=0,row=7)
        label = tk.Label(self, text = ",").grid(column=2,row=6)
        label = tk.Label(self, text = ",").grid(column=2,row=7)
        label = tk.Label(self, text = ")").grid(column=4,row=6)
        label = tk.Label(self, text = ")").grid(column=4,row=7)
        
        X0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=X0).grid(column=1,row=6)
        X0.set("0.0")
        X1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=X1).grid(column=3,row=6)
        X1.set("1.0")
        Y0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=Y0).grid(column=1,row=7)
        Y0.set("0.0")
        Y1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=Y1).grid(column=3,row=7)
        Y1.set("1.0")

        #============Plot Dimensions============#
        label = tk.Label(self, text = "Plot Dimension:").grid(column=0,row=9)
        label = tk.Label(self, text = "(Xmin,Xmax) = (").grid(column=0,row=10)
        label = tk.Label(self, text = "(Ymin,Ymax) = (").grid(column=0,row=11)
        label = tk.Label(self, text = ",").grid(column=2,row=10)
        label = tk.Label(self, text = ",").grid(column=2,row=11)
        label = tk.Label(self, text = ")").grid(column=4,row=10)
        label = tk.Label(self, text = ")").grid(column=4,row=11)
        
        Xmin = tk.StringVar()
        entry = tk.Entry(self,textvariable=Xmin).grid(column=1,row=10)
        Xmin.set("-5.0")
        Ymin = tk.StringVar()
        entry = tk.Entry(self,textvariable=Ymin).grid(column=1,row=11)
        Ymin.set("-5.0")
        Xmax = tk.StringVar()
        entry = tk.Entry(self,textvariable=Xmax).grid(column=3,row=10)
        Xmax.set("5.0")
        Ymax = tk.StringVar()
        entry = tk.Entry(self,textvariable=Ymax).grid(column=3,row=11)
        Ymax.set("5.0")

        #============Num of Plots============#
        label = tk.Label(self, text = "Num Lines:")
        label.grid(column=0,row=10)
        
        numPlots = tk.StringVar()
        entry = tk.Entry(self,textvariable=numPlots).grid(column=1,row=10)
        numPlots.set("5")
        
        ttk.Separator(self,orient="horizontal").grid(column=0,row=1, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=4, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=8, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=12, sticky="ew", columnspan="5")
#        ttk.Separator(self,orient="vertical").grid(column=1,row=1, sticky="ns", rowspan="15")

        #============Simulation Parameters============# 
        label = tk.Label(self, text = "Simulation parameters:").grid(column=0,row=13)        
        label = tk.Label(self, text = "T init:").grid(column=0,row=14)        
        label = tk.Label(self, text = "T final:").grid(column=0,row=15)        
        label = tk.Label(self, text = "Num points:").grid(column=0,row=16) 
        
        TInit = tk.StringVar()
        entry = tk.Entry(self,textvariable=TInit).grid(column=1,row=14)
        TInit.set("0.0")
        TFinal = tk.StringVar()
        entry = tk.Entry(self,textvariable=TFinal).grid(column=1,row=15)
        TFinal.set("15.0")
        NumPoints = tk.StringVar()
        entry = tk.Entry(self,textvariable=NumPoints).grid(column=1,row=16)
        NumPoints.set("1000")

if __name__ == "__main__":
    app = LieGUIApp()
    app.mainloop()
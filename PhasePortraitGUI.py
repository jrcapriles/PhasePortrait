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
#CHUA oscillator TODO
#LORENZ

import Tkinter as tk
import ttk

from pp import phasePlaneGUI
from pp import tResponse

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi, array
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import *
from matplotlib.figure import Figure
import sys


TITLE_FONT = ("Helvetica", 18, "bold")

class PPGUIApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # screens is a stack of frames
        screens = tk.Frame(self)
        screens.pack(side="top", fill="both", expand=True)
        screens.grid_rowconfigure(0, weight=1)
        screens.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.fun='name'
       
        fun = 'N/A' 
        i=0
        for F in (HomePage, FunctionPage, FunctionPage, FunctionPage, FunctionPage, FunctionPage, FunctionPage):
            if i==1:
                fun = 'Simple'
            elif i==2:
                fun = 'Vanderpol'
            elif i==3:
                fun = 'Duffing'
            elif i==4:
                fun = 'Magnetic'
            elif i==5:
                fun ='Violin'
            elif i==6:
                fun ='Pendulum'            
                
            frame = F(screens, self,fun)            
            self.frames[i] = frame
            # stack all of the pages together; 
            # the one on the top will be visible.
            frame.grid(row=0, column=0, sticky="nsew")
            i+=1

        self.show_screen(0)

    def show_screen(self, c):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller,fun):
        tk.Frame.__init__(self, parent) 
        self.grid()
        self.fun = fun
        self.label = tk.Label(self, text="Home page!", font=TITLE_FONT)
        self.label.grid(column=1,row=0, pady=10)

        self.label = tk.Label(self, text = "Functions:")
        self.label.grid(column=0,row=3)
        self.funcVar = tk.StringVar()
        self.funcVar.set("Vanderpol")
        self.choices = ['Simple', 'Vanderpol', 'Duffing','Magnetic', 'Violin', 'Pendulum'] #'Hyperbolic'
        #Drop down menu to select function to plot
        self.option = tk.OptionMenu(self, self.funcVar, *self.choices)
        self.option.grid(column = 1, row =3)
        
        self.select = tk.Button(self, text="Select",command=lambda: self.sel(self.funcVar.get(),controller))#lambda: controller.show_screen(PageOne))
        self.select.grid(column = 2, row =3)

        #This just clean the screen        
        #self.quit = tk.Button(self, text="Quit",command=lambda: tk.Frame.destroy(parent) )
        #self.quit.grid(column = 5, row =0)

    def sel(args,function,controller):
        #Switch to the coresponding page
        if function == 'Simple':
            controller.show_screen(1)
        elif function == 'Vanderpol':
            controller.show_screen(2)
        elif function == 'Duffing':
            controller.show_screen(3)
        elif function == 'Magnetic':
            controller.show_screen(4)
        elif function == 'Violin': 
            controller.show_screen(5)
        elif function == 'Pendulum': 
            controller.show_screen(6)
            
       


class FunctionPage(tk.Frame):
    def __init__(self, parent, controller,fun):
        tk.Frame.__init__(self, parent)
        self.grid()
        self.fun=fun
        
        label = tk.Label(self, text="Function: "+fun, font=TITLE_FONT).grid(column=1,row=0, pady=10)
        #label = tk.Label(self, text = "A note...").grid(column=1,row=2, pady=10)
        
        #============Butons============#
        button = tk.Button(self, text="Go back!", command=lambda: controller.show_screen(0)).grid(column = 3, row =19)
        
        button2 = tk.Button(self,text=u"Phase Plot Me!", command=self.plot).grid(column=3,row=20)
    
        button3 = tk.Button(self,text=u"Time Response!", command=self.tResponse).grid(column=3,row=21)
        #============ODE solver============#
        label = tk.Label(self, text = "ODE Solver:").grid(column=0,row=3)
        self.ODESolver = tk.StringVar()
        self.ODESolver.set('Default')
        self.ODEchoices = ['Default', 'vode', 'zvode','lsoda', 'dopri5','dop853'] #'Hyperbolic'
        self.ODESolverOp = tk.OptionMenu(self, self.ODESolver, *self.ODEchoices).grid(column = 1, row =3)    
    
        #============PP Initial Conditions============#
        label = tk.Label(self, text = "PP Initial Conditions:").grid(column=0,row=5)
        label = tk.Label(self, text = "(X0,Y0) = (").grid(column=0,row=6)
        label = tk.Label(self, text = "(X1,Y1) = (").grid(column=0,row=7)
        label = tk.Label(self, text = ",").grid(column=2,row=6)
        label = tk.Label(self, text = ",").grid(column=2,row=7)
        label = tk.Label(self, text = ")").grid(column=4,row=6)
        label = tk.Label(self, text = ")").grid(column=4,row=7)
        
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
        label = tk.Label(self, text = "Time Initial Conditions:").grid(column=0,row=9)
        label = tk.Label(self, text = "(t0,t1) = (").grid(column=0,row=10)
        label = tk.Label(self, text = ",").grid(column=2,row=10)
        label = tk.Label(self, text = ")").grid(column=4,row=10)
        
        self.t0 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.t0).grid(column=1,row=10)
        self.t0.set("0.0")
        self.t1 = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.t1).grid(column=3,row=10)
        self.t1.set("1.0")

        #============Plot Dimensions============#
        label = tk.Label(self, text = "Plot Dimension:").grid(column=0,row=12)
        label = tk.Label(self, text = "(Xmin,Xmax) = (").grid(column=0,row=13)
        label = tk.Label(self, text = "(Ymin,Ymax) = (").grid(column=0,row=14)
        label = tk.Label(self, text = ",").grid(column=2,row=13)
        label = tk.Label(self, text = ",").grid(column=2,row=14)
        label = tk.Label(self, text = ")").grid(column=4,row=13)
        label = tk.Label(self, text = ")").grid(column=4,row=14)
        
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
        label = tk.Label(self, text = "Num Plots:")
        label.grid(column=0,row=16)
        
        self.numPlots = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.numPlots).grid(column=1,row=16)
        self.numPlots.set("5")
        
        ttk.Separator(self,orient="horizontal").grid(column=0,row=1, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=4, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=8, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=11, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=17, sticky="ew", columnspan="5")
        ttk.Separator(self,orient="horizontal").grid(column=0,row=22, sticky="ew", columnspan="5")
#        ttk.Separator(self,orient="vertical").grid(column=1,row=1, sticky="ns", rowspan="15")

        #============Simulation Parameters============# 
        label = tk.Label(self, text = "Simulation parameters:").grid(column=0,row=18)        
        label = tk.Label(self, text = "T init:").grid(column=0,row=19)        
        label = tk.Label(self, text = "T final:").grid(column=0,row=20)        
        label = tk.Label(self, text = "Num points:").grid(column=0,row=21) 
        
        self.TInit = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.TInit).grid(column=1,row=19)
        self.TInit.set("0.0")
        self.TFinal = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.TFinal).grid(column=1,row=20)
        self.TFinal.set("15.0")
        self.NumPoints = tk.StringVar()
        entry = tk.Entry(self,textvariable=self.NumPoints).grid(column=1,row=21)
        self.NumPoints.set("1000")

        
    def plot(self):
        
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


if __name__ == "__main__":
    app = PPGUIApp()
    app.mainloop()
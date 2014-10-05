# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 19:24:12 2014

@author: joser
"""


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

class HomePage(tk.Frame):
    def __init__(self, parent, controller,fun):
        tk.Frame.__init__(self, parent) 
        self.grid()
        self.fun = fun
        self.label = tk.Label(self, text="Phase Portrait Plotter", font=TITLE_FONT).grid(column=1,row=0, pady=10)
        self.label = tk.Label(self, text = "Functions:").grid(column=0,row=3)
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
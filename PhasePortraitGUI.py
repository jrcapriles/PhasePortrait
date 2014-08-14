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

from PhasePortraitHomePageGUI import HomePage
from PhasePortraitFunctionPageGUI import FunctionPage

import matplotlib
matplotlib.use('TkAgg')

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
        self.createScreens(screens)
        self.show_screen(0)

    def createScreens(self,screens):
        i=0
        for F in (HomePage, FunctionPage, FunctionPage, FunctionPage, FunctionPage, FunctionPage, FunctionPage):
            if i==0:
                fun = 'N/A'
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

    def show_screen(self, c):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        frame.tkraise()


if __name__ == "__main__":
    app = PPGUIApp()
    app.mainloop()
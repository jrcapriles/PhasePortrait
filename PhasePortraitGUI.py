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
        screenOrder={0:'N/a',
                     1:'Simple',
                     2:'Vanderpol',
                     3:'Duffing',
                     4:'Magnetic',
                     5:'Violin',
                     6:'Pendulum'}
        i=0
        for F in (HomePage, FunctionPage, FunctionPage, FunctionPage, FunctionPage, FunctionPage, FunctionPage):
            fun = screenOrder[i]     
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
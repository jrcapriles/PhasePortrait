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
        
        #Labels for initial conditions
        label = Tkinter.Label(self, text = "(X0,Y0) = (")
        label.grid(column=0,row=3)
        label = Tkinter.Label(self, text = "(X1,Y1) = (")
        label.grid(column=0,row=4)
        
        label = Tkinter.Label(self, text = ",")
        label.grid(column=2,row=3)
        label = Tkinter.Label(self, text = ",")
        label.grid(column=2,row=4)

        label = Tkinter.Label(self, text = ")")
        label.grid(column=4,row=3)
        label = Tkinter.Label(self, text = ")")
        label.grid(column=4,row=4)
                
        #Entry variables for initial conditions
        self.X0 = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.X0)
        self.entry.grid(column=1,row=3)
        self.X0.set("0.0")
                
        self.Y0 = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.Y0)
        self.entry.grid(column=3,row=3)
        self.Y0.set("0.0")
        
        self.X1 = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.X1)
        self.entry.grid(column=1,row=4)
        self.X1.set("1.0")

        self.Y1 = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.Y1)
        self.entry.grid(column=3,row=4)
        self.Y1.set("1.0")

        #Button to plot 
        button = Tkinter.Button(self,text=u"Phase Plot Me!", command=self.plot)
        button.grid(column=3,row=0)
        
        #list of function availables. Need to be updated each a new function is added
        self.funcVar = Tkinter.StringVar()
        self.funcVar.set("Vanderpol")
        self.choices = ['Hyperbolic', 'Simple', 'Vanderpol', 'Duffing','Magnetic', 'Violin']
       
        #Drop down menu to select function to plot
        option = Tkinter.OptionMenu(self, self.funcVar, *self.choices)
        option.grid(column = 1, row =0)
    
        #Set the GUI environment
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
        print phasePlane(self.funcVar.get(),[IC0,IC1])
        

if __name__ == "__main__":
    GUI = PhasePortraitGUI(None)
    GUI.title('Phase Plane GUI')
    GUI.mainloop()



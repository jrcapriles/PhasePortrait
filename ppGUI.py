# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 18:02:40 2014

@author: joser
"""

#!/usr/bin/python

import Tkinter
from pp import phasePlane

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)


        button = Tkinter.Button(self,text=u"Phase Plot Me!", command=self.plot)
        button.grid(column=1,row=0)
        
        self.funcVar = Tkinter.StringVar()
        self.funcVar.set("Vanderpol")
        self.choices = ['Hyperbolic', 'Simple', 'Vanderpol', 'Duffing','Magnetic', 'Violin']
       
        option = Tkinter.OptionMenu(self, self.funcVar, *self.choices)
        option.grid(column = 2, row =0)
         

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def plot(self):
        print phasePlane(self.funcVar.get())
        #phasePlane(self.funcVar)

   

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Phase Plane GUI')
    app.mainloop()



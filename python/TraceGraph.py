#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys, time, re
from Tkinter import *

class TraceGraph(Canvas):
    def __init__(self, master, larg=700, haut=250 ):
        Canvas.__init__(self,master)
        self.configure(width=larg, height=haut)
        self.larg, self.haut = larg, haut
        # trace des axes de reference :
        self.create_line(10, haut-5, larg, haut-5, arrow=LAST)   # axe X
        self.create_line(10, haut-5, 10, 5, arrow=LAST)          # axe Y
        # trace d'une echelle avec 7 graduations :
        pas = (larg-25)/7. 
        for t in range(1, 9):
            stx = 10 + t*pas 
            self.create_line(stx, haut-8, stx, haut-2)
        
    def traceCourbe(self, x, y, min_y, max_y, coul='red'):
        curve =[] 
        for i in range(len(x)):     
            curve.append((10+(x[i]/x[-1])*(self.larg-25),self.haut-5-(y[i]-min_y)/(max_y-min_y)*(self.haut-5)))
        n = self.create_line(curve, fill=coul, smooth=1)
        return n


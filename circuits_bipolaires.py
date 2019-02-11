# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:50:22 2019

@author: Ulysse
"""

import numpy as np
from matplotlib.pyplot import *
#from math import *
import sympy as sp
sp.init_printing()

class CircuitBipolaire():
    def __init__(self,valeur):
        if isinstance(valeur,str):
            valeur = sp.Symbol(valeur)
        self.valeur = valeur
        
    def __repr__(self):
        return str(self.impedance)
    
    def __add__(self, autre_circuit):
        circuit_serie = Serie(self,autre_circuit)
        return circuit_serie
    
    def __or__(self, autre_circuit):
        circuit_parallele = Parallele(self,autre_circuit)
        return circuit_parallele
    
    def trace(self):
        self._trace(0,0)
        ax = gca()
        ax.set_aspect('equal')
        #rc('text', usetex=True)


class Serie(CircuitBipolaire):
    def __init__(self,circuit1,circuit2):
        self.circuit1 = circuit1
        self.circuit2 = circuit2
        
    def get_impedance(self,omega):
        return self.circuit1.get_impedance(omega)+self.circuit2.get_impedance(omega)
    
    def _trace(self,x0,y0):
        xf1,yf1 = self.circuit1._trace(x0,y0)
        xf2,yf2 = self.circuit2._trace(xf1,y0)
        return xf2,yf2

class Parallele(CircuitBipolaire):
    def __init__(self,circuit1,circuit2):
        self.circuit1 = circuit1
        self.circuit2 = circuit2

    def get_impedance(self,omega):
        return (self.circuit1.get_impedance(omega) * self.circuit2.get_impedance(omega))/(self.circuit1.get_impedance(omega) + self.circuit2.get_impedance(omega))
    
    def _trace(self,x0,y0):
        xf1,yf1 = self.circuit1._trace(x0,y0)
        xf2,yf2 = self.circuit2._trace(x0,yf1+0.5)
        plot([x0,x0],[y0,yf1+0.5],'k')
        plot([xf1,xf1],[y0,yf1+0.5],'k')
        plot([xf1,xf2],[yf1+0.5,yf1+0.5],'k')
        return max(xf1,xf2),(yf2)

# On définit ensuite une classe par type de composant
# pour lesquelles, on définit les impédances correspondantes
class Resistance(CircuitBipolaire):
    def get_impedance(self,omega):
        return self.valeur

    def _trace(self,x0,y0): 
        length=1; height=0.25
        plot([x0,x0+length/4],[y0,y0],'k')
        plot([x0+length/4,x0+length*3/4],[y0-height/2,y0-height/2],'k')
        plot([x0+length/4,x0+length*3/4],[y0+height/2,y0+height/2],'k')
        plot([x0+length/4,x0+length/4],[y0-height/2,y0+height/2],'k')
        plot([x0+length*3/4,x0+length*3/4],[y0-height/2,y0+height/2],'k')
        plot([x0+length*3/4,x0+length],[y0,y0],'k')
        text(x0+length/2-0.1,y0,self.valeur)
        return x0+length,y0+height/2

class Inductance(CircuitBipolaire):
    def get_impedance(self,omega):
        if isinstance(self.valeur,sp.Symbol):
            return self.valeur*sp.I*omega
        else:
            return self.valeur*1j*omega
        
    def _trace(self,x0,y0): 
        length=1; height=0.3; xlin = np.linspace(x0+length/4,x0+length*3/4,200)
        plot([x0,x0+length/4],[y0,y0],'k')
        plot(xlin,y0+np.sin(xlin*(20*np.pi)+np.pi)*height/2,'k')
        plot(xlin,y0+np.sin(xlin*(20*np.pi))*height/2,'k')
        plot([x0+length*3/4,x0+length],[y0,y0],'k')
        text(x0+0.05*length,y0+0.15*height,self.valeur)
        return x0+length,y0+height/2
    
class Capacite(CircuitBipolaire):
    def get_impedance(self,omega):
        if isinstance(self.valeur,sp.Symbol):
            return 1/(self.valeur*sp.I*omega)
        else:
            return 1/(self.valeur*1j*omega)
    
    def _trace(self,x0,y0): 
        length=1; height=0.5
        plot([x0,x0+length/3+length/8],[y0,y0],'k')
        plot([x0+length/3+length/8,x0+length/3+length/8],[y0-height/2,y0+height/2],'k')
        plot([x0+length*2/3-length/8,x0+length*2/3-length/8],[y0-height/2,y0+height/2],'k')
        plot([x0+length*2/3-length/8,x0+length],[y0,y0],'k')
        text(x0+0.2*length,y0+0.15*height,self.valeur)
        return x0+length,y0+height/2
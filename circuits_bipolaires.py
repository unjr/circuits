# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:50:22 2019

@author: Ulysse
"""

import numpy as np
from matplotlib.pyplot import *
from math import *
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

class Serie(CircuitBipolaire):
    def __init__(self,circuit1,circuit2):
        self.circuit1 = circuit1
        self.circuit2 = circuit2
        
    def get_impedance(self,omega):
        return self.circuit1.get_impedance(omega)+self.circuit2.get_impedance(omega)
    
    def trace(self,x0,y0):
        xf1,yf1 = self.circuit1.trace(x0,y0)
        xf2,yf2 = self.circuit2.trace(xf1,y0)
        return xf2,yf2

class Parallele(CircuitBipolaire):
    def __init__(self,circuit1,circuit2):
        self.circuit1 = circuit1
        self.circuit2 = circuit2

    def get_impedance(self,omega):
        return (self.circuit1.get_impedance(omega) * self.circuit2.get_impedance(omega))/(self.circuit1.get_impedance(omega) + self.circuit2.get_impedance(omega))
    
    def trace(self,x0,y0):
        xf1,yf1 = self.circuit1.trace(x0,y0)
        xf2,yf2 = self.circuit2.trace(x0,yf1+0.5)
        plot([x0,x0],[y0,yf1+0.5],'k')
        plot([xf1,xf1],[y0,yf1+0.5],'k')
        plot([xf1,xf2],[yf1+0.5,yf1+0.5],'k')
        return max(xf1,xf2),(yf2)

# On définit ensuite une classe par type de composant
# pour lesquelles, on définit les impédances correspondantes
class Resistance(Composant):
    def get_impedance(self,omega):
        return self.valeur

    def trace(self,x0,y0): 
        length=1; height=0.5
        plot([x0,x0+length/4],[y0,y0],'k')
        plot([x0+length/4,x0+length*3/4],[y0-height/2,y0-height/2],'k')
        plot([x0+length/4,x0+length*3/4],[y0+height/2,y0+height/2],'k')
        plot([x0+length/4,x0+length/4],[y0-height/2,y0+height/2],'k')
        plot([x0+length*3/4,x0+length*3/4],[y0-height/2,y0+height/2],'k')
        plot([x0+length*3/4,x0+length],[y0,y0],'k')
        text(x0+length/2-0.1,y0,self.valeur)
        return x0+length,y0+height/2

class Inductance(Composant):
    def get_impedance(self,omega):
        if isinstance(self.valeur,sp.Symbol):
            return self.valeur*sp.I*omega
        else:
            return self.valeur*1j*omega
        
    def trace(self,x0,y0): 
        length=1; height=0.5; xlin = np.linspace(x0+length/4,x0+length*3/4,200)
        plot([x0,x0+length/4],[y0,y0],'k')
        plot(xlin,y0+np.sin(xlin*(20*np.pi)+np.pi)*height/2,'k')
        plot(xlin,y0+np.sin(xlin*(20*np.pi))*height/2,'k')
        plot([x0+length*3/4,x0+length],[y0,y0],'k')
        return x0+length,y0+height/2
    
class Capacite(Composant):
    def get_impedance(self,omega):
        if isinstance(self.valeur,sp.Symbol):
            return 1/(self.valeur*sp.I*omega)
        else:
            return 1/(self.valeur*1j*omega)
    
    def trace(self,x0,y0): 
        length=1; height=0.5
        plot([x0,x0+length/3],[y0,y0],'k')
        plot([x0+length/3,x0+length/3],[y0-height/2,y0+height/2],'k')
        plot([x0+length*2/3,x0+length*2/3],[y0-height/2,y0+height/2],'k')
        plot([x0+length*2/3,x0+length],[y0,y0],'k')
        return x0+length,y0+height/2
        

#### TEST ###
f = 1; omega = sp.Symbol('omega') #omega = 2*pi*f

R1 = Resistance('R_1')
R2 = Resistance('R_2')
C1 = Capacite('C_1')
C2 = Capacite('C_2')
L1 = Inductance('L_1') 

circuit_final = ((R1+(C1|L1))|C2) + R2; circuit_final.trace(0,0)

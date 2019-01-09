# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:50:22 2019

@author: Ulysse
"""

import numpy as np
from matplotlib.pyplot import *
from math import *

class CircuitBipolaire():
    def __init__(self,impedance):
        self.impedance = impedance
        
    def __repr__(self):
        return str(self.impedance)

class CircuitElementaire(CircuitBipolaire):
    def __init__(self,impedance):
        CircuitBipolaire.__init__(self,impedance)
    
    def __add__(self, autre_circuit):
        impedance_totale = self.impedance + autre_circuit.impedance
        circuit_serie = CircuitElementaire(impedance_totale)
        return circuit_serie
    
    def __or__(self, autre_circuit):
        impedance_totale = (self.impedance * autre_circuit.impedance)/(self.impedance + autre_circuit.impedance)
        circuit_parallele = CircuitElementaire(impedance_totale)
        return circuit_parallele
    
class Composant(CircuitElementaire,list):
    def __init__(self,impedance):
        CircuitElementaire.__init__(self,impedance)
        
class Resistance(Composant):
    def __init__(self,R):
        Composant.__init__(self,R)

class Inductance(Composant):
    def __init__(self,L,w):
        Composant.__init__(self,1j*L*w)

class Capacite(Composant):
    def __init__(self,C,w):
        Composant.__init__(self,1/(1j*C*w))
        
        
        
        
        
        
        
        
class Circuit(list):
    def __init__(self,nb_noeuds):
        self.nb_noeuds = nb_noeuds

class Noeud(list):
    def __init__(self,nb_branches, potentiel=0):
        self.nb_branches = nb_branches
        self.potentiel = potentiel
        
E=1
noeud1 = Noeud(1,E); noeud1.potentiel = E;
noeud2 = Noeud(4)
noeud3 = Noeud(2)
noeud4 = Noeud(3)
noeud5 = Noeud(2)
noeud6 = Noeud(1,0)
noeud7 = Noeud(1,0)

R1 = Resistance(1); R1.append(noeud1, noeud2)
R2 = Resistance(1); R2.append(noeud2, noeud3)
R3 = Resistance(1); R3.append(noeud4, noeud5)
C1 = Capacite(1e-6); C1.append(noeud2, noeud7)
C2 = Capacite(1e-6); C2.append(noeud2, noeud4)
C3 = Capacite(1e-6); C3.append(noeud5, noeud6)
L1 = Inductance(1e-6); L1.append(noeud3, noeud4)



circuit = Circuit(7)
R1 = Resistance(1)
R2 = Resistance(2)


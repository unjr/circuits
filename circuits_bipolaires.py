# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:50:22 2019

@author: Ulysse
"""

import numpy as np
from matplotlib.pyplot import *
from math import *

class CircuitBipolaire():           # un objet de la classe CircuitBipolaire
    def __init__(self,impedance):   # est muni de la grandeur "impédance"
        self.impedance = impedance
        
    def __repr__(self):
        return str(self.impedance)

class CircuitElementaire(CircuitBipolaire):         # un circuit élémentaire hérite
    def __init__(self,impedance):                   # du circuit bipolaire et peut
        CircuitBipolaire.__init__(self,impedance)   # être placé en série (méthode add)
                                                    # ou en parallèle (méthode or),
    def __add__(self, autre_circuit):               # chaque méthode calcule l'impédance équivalente
        impedance_totale = self.impedance + autre_circuit.impedance
        circuit_serie = CircuitElementaire(impedance_totale)
        return circuit_serie
    
    def __or__(self, autre_circuit):
        impedance_totale = (self.impedance * autre_circuit.impedance)/(self.impedance + autre_circuit.impedance)
        circuit_parallele = CircuitElementaire(impedance_totale)
        return circuit_parallele
    
class Composant(CircuitElementaire,list):           # on définit une classe Composant
    def __init__(self,impedance):                   # même si ça n'apporte pas grand chose pour
        CircuitElementaire.__init__(self,impedance) # l'instant
        
# On définit ensuite une classe par type de composant
# pour lesquelles, on définit les impédances correspondantes
class Resistance(Composant):
    def __init__(self,R):
        Composant.__init__(self,R)

class Inductance(Composant):
    def __init__(self,L,w):
        Composant.__init__(self,1j*L*w)

class Capacite(Composant):
    def __init__(self,C,w):
        Composant.__init__(self,1/(1j*C*w))
        


#### TEST ###
f = 1; w = 2*pi*f

R1 = Resistance(1)
R2 = Resistance(1)
C1 = Capacite(1,w)
C2 = Capacite(1,w)
L1 = Inductance(1,w) 

circuit_final = ((R1 + (L1 | C1)) | C2) + R2

print(circuit_final)


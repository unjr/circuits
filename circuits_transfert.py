# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:50:22 2019

@author: Ulysse
"""

import numpy as np
from matplotlib.pyplot import *
from math import *
import sympy as sp

class Composant():
    def __init__(self,value):
        self.value = value
    
    def connect(self,n1,n2):
        self.n1=n1
        self.n2=n2
        n1._connect(self,1)
        n2._connect(self,2)
    
    def get_current(self,patte):
        current = (self.n1.potentiel-self.n2.potentiel)/self.value
        if patte==1:
            return current
        else:
            return -current
    
    
class Resistance(Composant):
    def __init__(self,R):
        Composant.__init__(self,R)
    

class Inductance(Composant):
    pass

class Capacite(Composant):
    pass
        
_noeud_id = 0        

class Noeud():
    def __init__(self, potentiel=None, alim=False):
        global _noeud_id
        _noeud_id += 1
        if potentiel is None:
            potentiel = sp.Symbol('U_'+str(_noeud_id), real=True)
        self.potentiel = potentiel
        self.composants = []
        self.alim = alim
    
    def _connect(self,composant,patte):
        self.composants.append((composant,patte))
    
    def millman(self):
        somme=0
        for composant,patte in self.composants:
            somme+=composant.get_current(patte)
        return somme
    

class Circuit():
    def __init__(self,liste_noeuds,liste_composants):
        self.liste_noeuds = liste_noeuds
        self.liste_composants = liste_composants
        self.check_circuit()
    def check_circuit(self):
        pass
    
    def millman(self):
        liste_equations=[]
        for noeud in self.liste_noeuds:
            if noeud.alim is False:
                liste_equations.append(noeud.millman())
        return liste_equations



E=sp.Symbol('E',real=True); S=sp.Symbol('S',real=True)
noeud1 = Noeud(E, alim=True);
noeud2 = Noeud()
noeud3 = Noeud(S)
noeud4 = Noeud(0, alim=True)

R1 = Resistance(sp.Symbol('R_1')); R1.connect(noeud1, noeud2)
R2 = Resistance(sp.Symbol('R_2')); R2.connect(noeud2, noeud3)
R3 = Resistance(sp.Symbol('R_3')); R3.connect(noeud3, noeud4)
C1 = Capacite(sp.Symbol('Z')); C1.connect(noeud2, noeud3)



circuit = Circuit([noeud1,noeud2,noeud3,noeud4],[R1,R2,R3,C1])



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

class Composant():
    def __init__(self,valeur): # Valeur : R ou C ou L
        self.valeur = valeur
    
    def connect(self,n1,n2):  # connexion aux noeuds n1 et n2
        self.n1 = n1
        self.n2 = n2
        n1._connect(self,1)
        n2._connect(self,2)
    
    def get_current(self,patte): # 
        omega = sp.Symbol('omega')
        current = (self.n1.potentiel-self.n2.potentiel)/self.get_impedance(omega)
        if patte == 1:
            return current
        else:
            return -current
    
class Resistance(Composant):
    def __init__(self,R):
        Composant.__init__(self,R)
    
    def get_impedance(self,omega):
        return self.valeur

class Inductance(Composant):
    def __init__(self,L):
        Composant.__init__(self,L)
    
    def get_impedance(self,omega):
        if isinstance(self.valeur,sp.Symbol):
            return self.valeur*sp.I*omega
        else:
            return self.valeur*1j*omega

class Capacite(Composant):
    def __init__(self,C):
        Composant.__init__(self,C)
    
    def get_impedance(self,omega):
        if isinstance(self.valeur,sp.Symbol):
            return 1/(self.valeur*sp.I*omega)
        else:
            return 1/(self.valeur*1j*omega)
        
_noeud_id = 0        

class Noeud():
    def __init__(self, potentiel=None, alim=False):
        global _noeud_id
        _noeud_id += 1
        if potentiel is None:
            potentiel = sp.Symbol('U_'+str(_noeud_id))
        self.potentiel = potentiel
        self.composants = []
        self.alim = alim
    
    def _connect(self,composant,patte):
        self.composants.append((composant,patte))
    
    def _millman(self):
        somme = 0
        for composant,patte in self.composants:
            somme += composant.get_current(patte)
        return somme
    
class Circuit():
    def __init__(self,liste_noeuds,liste_composants):
        self.liste_noeuds = liste_noeuds
        self.liste_composants = liste_composants
        self.check_circuit()
        
    def check_circuit(self):
        pass    
    
    def millman(self):
        liste_equations = []
        for noeud in self.liste_noeuds:
            if noeud.alim is False:
                liste_equations.append(noeud._millman())
        return liste_equations
    
    def solve(self, inconnue=None):
        systeme = self.millman()
        inconnues = tuple([noeud.potentiel for noeud in self.liste_noeuds if noeud.alim == False])
        sol = sp.solve(systeme,inconnues)
        if inconnue == None:
            return sol
        else:
            return sol[inconnue]


# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:18:24 2019

@author: Ulysse
"""
from circuits_bipolaires import Resistance, Capacite,Inductance 

f = 1; omega = sp.Symbol('omega') #omega = 2*pi*f

R1 = Resistance('R_1')
R2 = Resistance('R_2')
C1 = Capacite('C_1')
C2 = Capacite('C_2')
L1 = Inductance('L_1') 

circuit_final = ((R1+(C1|L1))|C2) + R2; circuit_final.trace()
circuit_final.get_impedance(omega)
#sp.simplify()

from circuits_transfert import Resistance, Capacite, Inductance, Noeud, Circuit    

E = sp.Symbol('E',real=True); S = sp.Symbol('S',real=True)
noeud1 = Noeud(E, alim=True);
noeud2 = Noeud()
noeud3 = Noeud(S)
noeud4 = Noeud(0, alim=True)

R1 = Resistance(sp.Symbol('R_1')); R1.connect(noeud1, noeud2)
R2 = Resistance(sp.Symbol('R_2')); R2.connect(noeud2, noeud3)
R3 = Resistance(sp.Symbol('R_3')); R3.connect(noeud3, noeud4)
C1 = Capacite(sp.Symbol('C_1')); C1.connect(noeud2, noeud3)
circuit = Circuit([noeud1,noeud2,noeud3,noeud4],[R1,R2,R3,C1])
solutions = circuit.solve(S)
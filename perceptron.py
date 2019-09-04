# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:35:30 2018

@author: Marcílio
"""

entradas = [1,7,5]
pesos = [0.8, 0.1, 0] # sinapses

def soma (ent, pes):
    s = 0
    
    for i in range(3):
        #print(ent[i], " - ", pes[i])
        s += ent[i]*pes[i]
    
    print ('Somatoria eh: ', s)
    return s
    
ret = soma(entradas, pesos)

def passoFunc (soma):
    
    if (soma >= 1):
        return 1
    
    return 0

res = passoFunc(ret)


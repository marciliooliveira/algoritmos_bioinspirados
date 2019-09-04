# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 19:21:06 2018

@author: Marcílio
Rede neural capaz de classificar o OPERADOR XOR --> NÃO CONSEGUE CONVERGIR 

"""

import numpy as np

entradas = np.array([[0,0],[0,1],[1,0],[1,1]]) # as entradas/parâmetros a seremm classificados
saidas = np.array([0,1,1,0]) # as saídas esperadas para tal classificação
pesos = np.array([0.0,0.0]) # pesos (sinapses) - serão iniciados em 0
txAprendizagem = 0.1 

def funcaoPasso (soma):
    
    if(soma >= 1):
        return 1
    
    return 0

def calculaSaida (registro):
    
    somatoria = registro.dot(pesos) # funcao do numpy para calculo escalar de matrizes
    
    return funcaoPasso(somatoria)

def treinaRede ():
    
    while True:     
        
        erroTotal = 0
        
        for i in range(len(saidas)):
            saida = calculaSaida(np.asarray(entradas[i]))
            erro = abs(saidas[i] - saida) # neste caso, a soma ocorre pelo fato do abs - se não, varia entre 0.4 a 0.5 e fica no looping
            erroTotal += erro
            
            for j in range(len(pesos)):
                pesos[j] = pesos[j] + (txAprendizagem * entradas[i][j] * erro)
                print ("Peso atualizado: " + str(pesos[j]))
        
        print ("Total de erros: " + str(erroTotal))
        
        if erroTotal == 0:
            break;
        
treinaRede () # treinamento da rede para encontrar o melhor ajuste de pesos
             # para então ter as saídas esperadas

print ("\nRede neural treinada \nAs saídas para cada entrada são:")

for i in range(len(entradas)):
    print (calculaSaida(entradas[i]))
            
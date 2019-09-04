#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 19:47:45 2018

@author: marcilio
"""

from random import random
import matplotlib.pyplot as pt

#criação da classe Produto com 3 atributos
#o self referencia o próprio objeto da classe (this - java)

global listaSolucoes
listaSolucoes = []

class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome # cria um atributo
        self.espaco = espaco
        self.valor = valor

class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0 # cada individuo possui uma determinada avaliação
        self.espaco_usado = 0
        self.geracao = geracao
        self.cromossomo = [] # a solução propriamente dita, ou seja, qual produto será ou não levado
        
        # inicialização dos individuos de forma aleatória
        # 0.5 significa probabilidade de 50% de ser 0 e 50% de ser 1
        # evita 14 1s ou evita 14 0s
        for i in range(len(espacos)):
    
            if random() < 0.5: # vai gerar um número entre 0 e 1 
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
                
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        
        for i in range (len(self.cromossomo)):
            
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espacos[i]
         
        # se a somatória de soluções (produtos que irá levar)
        # for maior que o limite do caminhão, abaixa-se a nota deste individuo
        # por default, 1
        if (soma_espacos > self.limite_espacos):
            nota = 1
        
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos
        
    def crossover(self, outro_individuo):
        # defino um ponto de corte - random de 0 a 1 - * tamanho - arredondando o valor
        corte = round(random() * len(self.cromossomo))
        
        # concateno parte de um cromossomo com parte de outro
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        # os filhos devem ser incluidos na população, por isso cria-se dois novos individuos
        # e passa a ser uma geração nova, logo em seguida, atribue-se os cromossomos com crossover 
        filhos = [ Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                   Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    def mutacao(self, taxa_mutacao):
        #print("Antes %s " % self.cromossomo)
        
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        
        #print("Depois %s " % self.cromossomo)
        
        return self
    
class GeneticAlgorithm():
        
    def __init__(self, tamanhoPopulacao):
        self.tamanhoPopulacao = tamanhoPopulacao
        self.populacao = []
        self.geracao = 0
        self.melhorSolucao = 0 # atributo guardará a melhor resposta
    
    # inicializa a geracao 0 de individuos    
    def inicializaPopulacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanhoPopulacao):
            self.populacao.append(Individuo(espacos, valores, limite))
        
        self.melhorSolucao = self.populacao[0]
    
    # ordena a população em ordem decrescente    
    def ordenaPopulacao(self):
        self.populacao = sorted(self.populacao, key = lambda populacao: populacao.nota_avaliacao, reverse = True)
    
    # verifica o melhor individuo e atribui ao atributo melhorSolucao
    def melhorIndividuo(self, individuo):
        if individuo.nota_avaliacao > self.melhorSolucao.nota_avaliacao:
            self.melhorSolucao = individuo
    
    # soma total para ser utilizada no método da roleta, definindo uma proporção para cada individuo
    def somaAvaliacoes(self):
        soma = 0
        
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        
        return soma
    
    #MÉTODO DA ROLETA
    # seleciona um pai proporcionalmente ao somatório das notas
    # retorna o indice do pai na roleta
    def selecionaPai(self, somaAvaliacao):
        pai = -1
        valorSorteado = random() * somaAvaliacao
        soma = 0
        i = 0
        
        while(i < len(self.populacao) and soma < valorSorteado):
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        
        return pai
    
    def visualizaGeracao(self):
        melhor = self.populacao[0] # o melhor individuo da população está na posição 0 devido a ordenação
        print("Geração %s - Nota %s -  Espaco %s - Cromossomo %s" % (melhor.geracao, 
                                                                     melhor.nota_avaliacao,
                                                                     melhor.espaco_usado,
                                                                     melhor.cromossomo))
        
    def resolver(self, txMutacao, nmGeracoes, espacos, valores, limiteEspacos):
        
        self.inicializaPopulacao(espacos, valores, limiteEspacos)
        
        for individuo in self.populacao:
            individuo.avaliacao()
            
        self.ordenaPopulacao()
        
        self.melhorSolucao = self.populacao[0]
        
        listaSolucoes.append(self.melhorSolucao.nota_avaliacao)
        
        self.visualizaGeracao()
        
        for geracao in range(nmGeracoes):
            somaAval = self.somaAvaliacoes() #a soma ocorre para que sejam selecionados os individios para uma nova população através
                                             # do método da ROLETA
            novaPop = []
            
            # seleção dos pais para uma nova população
            for individuos in range(0, self.tamanhoPopulacao, 2):
                pai1 = self.selecionaPai(somaAval)
                pai2 = self.selecionaPai(somaAval)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                novaPop.append(filhos[0].mutacao(txMutacao))
                novaPop.append(filhos[1].mutacao(txMutacao))
        
            self.populacao = list(novaPop)
            
            for ind in self.populacao:
                ind.avaliacao()
                
            self.ordenaPopulacao()
            
            self.visualizaGeracao() 
            
            melhor = self.populacao[0]
            
            listaSolucoes.append(melhor.nota_avaliacao)
            
            # se o melhor individuo da populacao atual for melhor que da anterior, ele é sobrescrito
            self.melhorIndividuo(melhor)
        
        print ("\nMelhor solucao: G: %s - V: %s - E: %s - Cromossomo: %s" %(self.melhorSolucao.geracao,
                                                                            self.melhorSolucao.nota_avaliacao,
                                                                            self.melhorSolucao.espaco_usado,
                                                                            self.melhorSolucao.cromossomo))
        
        print ("Tamanho da lista: ", len(listaSolucoes))
        
        return self.melhorSolucao.cromossomo
  
# método main
# se estiver rodando o código no próprio módulo, o python define a variável 
# __name__ reservada como main, se digitar Produto no console, output será __main__.Produto
if __name__ == "__main__":
        
    #p1 = Produto("IPhone 6", 0.000899, 2999.90) - criando um objeto da classe produto
    lista_produtos = [] #criando uma lista de produtos
    lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55'", 0.400, 4346.90))
    lista_produtos.append(Produto("TV 50'", 0.290, 3999.80))
    lista_produtos.append(Produto("TV 42'", 0.200, 2999.99))
    lista_produtos.append(Produto("Notebook dell", 0.00350, 2499.99))
    lista_produtos.append(Produto("Ventilador panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 2911.12))
    lista_produtos.append(Produto("Microondas LG", 0.0515, 419.12))
    lista_produtos.append(Produto("Geladeira brastemp", 0.768, 969.90))
    lista_produtos.append(Produto("Geladeira consul", 0.801, 849.29))
    lista_produtos.append(Produto("Notebook lenovo", 0.00513, 1999.99))
    lista_produtos.append(Produto("Notebook asus", 0.00420, 2399.89))
    lista_produtos.append(Produto("Microondas Brastemp", 0.0390, 299.99))
    """
    for produto in lista_produtos:
        print(produto.nome, produto.espaco, produto.valor)
    """
    espacos = []
    valores = []
    nomes = []
    
    # inicializando as listas de atributos individualmente
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
        
    limite = 3 # limite que o caminhão pode carregar
    
    tamanhoPopulacao = 4 # quantos individuos terão 
    
    txMutacao = 0.01
    
    nmGeracao = 4
    
    for i in range(1):
    
        ag = GeneticAlgorithm(tamanhoPopulacao)
        
        resultado = ag.resolver(txMutacao, nmGeracao, espacos, valores, limite)
        
        for i in range(len(lista_produtos)):
            if (resultado[i] == '1'):
                print("Nome: %s - RS %s" % (lista_produtos[i].nome,
                                           lista_produtos[i].valor))
        """
        for valor in ag.listaSolucoes:
            print(valor)
        """
        
    pt.plot(listaSolucoes)
    pt.title("Acompanhamento dos valores")
    pt.show()
from classe import Matrix, Atomo
import numpy as np
import random

linhas = 10  # quantidade de linhas da rede

sitios = Matrix(int(linhas))  # objeto criado

pp = random.random()  # gerando a prob inicial
pg = 1 - pp  # definindo pg 

#print(f"pp: {pp}  pg: {pg}")  # print para conferir a coerência da distribuição

sitios.distribute(pp, pg)  # função de preenchimento dos sítios
print(sitios)  # print dos sítios em tela para conferência

# pd H e Gd O
at = Atomo(sitios)
list_cvs = at.distcvs()
list_elet = at.distelet(sitios) #fazer uma funcao com for que percorre a lista gerada para criar ela 
at.olhos(linhas, sitios)
print(list_elet)


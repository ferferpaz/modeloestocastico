from datetime import datetime
from classe import Matrix
import numpy as np
import random
import csv

"""
    Realiza a distribuição das partículas em uma linha horizontal utilizando o conceito de voo de Lévy.

    A rede inicia vazia, preenchida apenas com zeros, e será gradualmente ocupada conforme as condições especificadas. 
    O preenchimento segue dois modos distintos: com difusão (voo de Lévy) ou sem difusão (tem uma prob de ocorrer ou não difusão).

    Funcionamento:
    1. Com difusão (voo de Lévy):
    - As partículas trocam de posição com base em uma probabilidade inicial, simulando o comportamento do voo de Lévy.

    2. Sem difusão:
    - Um sítio e uma partícula são sorteados.
    - Verifica-se se o sítio está vazio.
    - Se o sítio estiver vazio, verifica-se se a partícula pode ocupá-lo.
    - A particula G só pode ser inserida em locais onde seus vizinhos são zeros ou particulas pequenas, nunca uma G pode estar ao lado de outra
    - Caso a partícula possa ser inserida, ela é posicionada na matriz. Caso contrário, o processo é reiniciado.
    - Toda vez que tentamos inserir uma partícula, contabilizamos +1 em uma variável para saber quantas tentativas ocorreram de inserir partículas.
"""

quantidade = 10  # quantidade de linhas da rede
tempo = 5
t_simulacao = quantidade * tempo

sitios = Matrix(int(quantidade))

p_reacao = 1.0
p_levy = 0.9  # probabilidade de ocorrer o voo de Lévy
pps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  
sigma = 1

x = datetime.now().strftime("%m%d_%H%M%S")

def mostras(p_reacao, p_levy, pp, sigma, quantidade, tempo, t_simulacao):
    sitios.tentativas_totais = 0
    contador = 0
    
    with open(f"r{x}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Iteracao", "Densidade Vazia", "Densidade P", "Densidade G", "pp"])
        
        for i in range(t_simulacao):
            if random.random() < p_levy:
                sitios.voo_levy(p_reacao, sigma)
                sitios.inserir_particula(pp, p_reacao)
            else:
                sitios.inserir_particula(pp, p_reacao)

            contador += 1
            if contador == quantidade:
                sitios.salvar_estado()
                contador = 0
                writer.writerow([int((i + 1) / quantidade), 
                                 sitios.densidade_historico[-1], 
                                 sitios.d_his_P[-1], 
                                 sitios.d_his_G[-1], 
                                 pp])
                    
        print(f'Fazendo pp={pp}. Total de tentativas: {sitios.tentativas_totais}')

for pp in pps:
    mostras(p_reacao, p_levy, pp, sigma, quantidade, tempo, t_simulacao)

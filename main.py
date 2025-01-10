from classe import Matrix
import numpy as np
import random
import math
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
    - toda vez que nós tentamos inserir uma particula, contabilizamos +1 em uma variavel para saber quantas tentativas ocorreram de inserir particulas
"""
quantidade = 10 # quantidade de linhas da rede
tempo = 5
t_simulacao = quantidade * tempo

sitios = Matrix(int(quantidade))  # objeto criado

p_reacao= 1.0
p_levy = 0.9  # probabilidade de ocorrer o voo de Lévy
pps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
pp = 0.3
sigma = 1

    
def mostras(p_reacao, p_levy, pps, pp, sigma, quantidade, tempo, t_simulacao):
    sitios.tentativas_totais = 0
    contador = 0
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
            
            
    print(f'Total de tentativas: {sitios.tentativas_totais}\n')
    print(f'Densidade vazia: {sitios.densidade_historico}\n')
    print(f'Densidade P: {sitios.d_his_P}\n')
    print(f'Densidade G: {sitios.d_his_G}\n')

mostras(p_reacao, p_levy, pps, pp, sigma, quantidade, tempo, t_simulacao)

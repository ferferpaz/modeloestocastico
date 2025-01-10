import numpy as np
import matplotlib.pyplot as plt
import random

class Matrix:
    """
    Tudo relacionado a construção da matriz e suas manipulações
    """
    def __init__(self, linhas):
        """
        Construtor da classe Matrix.

        Inicializa uma matriz vazia de sitios.

        Argumentos:
            columns (int): Número de colunas da matriz.
        """
        self.data = np.array(['0'] * linhas)  
        self.historico = [] 
        self.densidade_historico = []
        self.d_his_G = []
        self.d_his_P = []
        self.tentativas_totais = 0

    def salvar_estado(self):
        self.historico.append(self.data.copy())
        self.densidade_historico.append(self.densidade())
        self.d_his_P.append(self.densidade_P())
        self.d_his_G.append(self.densidade_G())

    def __str__(self):
        return ' '.join(map(str, self.data)) 

    def densidade(self):
        num = np.sum(self.data == '0')
        return num / len(self.data)
    
    def densidade_P(self):
        """Calcula a densidade das partículas 'P'"""
        num_P = np.sum(self.data == 'P')
        return num_P / len(self.data)

    def densidade_G(self):
        """Calcula a densidade das partículas 'G'"""
        num_G = np.sum(self.data == 'G')
        return num_G / len(self.data)
                
    def reacao(self, prob):
        for i in range(len(self.data) - 1):
            if ((self.data[i] == 'G' and self.data[i + 1] == 'P') or 
                (self.data[i] == 'P' and self.data[i + 1] == 'G')):
                if random.random() < prob:
                    self.data[i] = self.data[i + 1] = '0'
                    #self.salvar_estado()
                    print(f'Reação entre posições {i} e {i + 1}')
                    print(self)
                    break

    def voo_levy(self, p_reacao):
        i, j = random.sample(range(len(self.data)), 2)
        self.reacao(p_reacao)
        if (self.data[i] != '0' and self.data[j] != '0') or (self.data[i] == '0' and self.data[j] != '0') or (self.data[i] != '0' and self.data[j] == '0'):  #Se i tem uma partícula e j esta vazio
            if self.data[i] == 'G':
                # Verifica vizinhos em j para garantir que G pode ser inserido
                vizinho_esq = self.data[j - 1] if j > 0 else '0'
                vizinho_dir = self.data[j + 1] if j < len(self.data) - 1 else '0'
                if vizinho_esq != 'G' and vizinho_dir != 'G':  # G pode ser inserido
                    self.data[j], self.data[i] = self.data[i], '0'
                    print(f"\nVoo de Lévy: Partícula G trocada de {i} para {j}.")
                    print(self)
                    
            else:  # Se não é G (é P), troca diretamente
                self.data[j], self.data[i] = self.data[i], '0'
                print(f"\nVoo de Lévy: Partícula P trocada de {i} para {j}.")
                print(self)
               

    def inserir_particula(self, prob_p, p_reacao):
        self.reacao(p_reacao)
        self.tentativas_totais += 1
        particula = 'P' if random.random() < prob_p else 'G'
        posicao = random.randint(0, len(self.data) - 1)

        if self.data[posicao] == '0':
            if particula == 'P' or \
               (particula == 'G' and not any(self.data[max(0, posicao-1):min(len(self.data), posicao+2)] == 'G')):
                self.data[posicao] = particula
                #self.salvar_estado()

                print(f'Partícula {particula} inserida na posição {posicao}')
                print(self)

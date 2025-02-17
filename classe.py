from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import csv
import os

class Matrix:
    """
    A classe Matrix cria e manipula uma matriz unidimensional para simular a dinâmica
    de partículas, permitindo inserções, movimentações e reações entre elas.
    """
    def __init__(self, quantidades):
        """
        Inicializa a matriz com um número especificado de sítios vazios.

        Args:
            quantidades (int): número de sitios na matriz.
        """
        self.data = np.array(['0'] * quantidades)  
        self.historico = [] 
        self.densidade_historico = []
        self.d_his_G = []
        self.d_his_P = []
        self.tentativas_totais = 0

    def salvar_estado(self):
        """
        Salva o estado atual da matriz e registra as densidades.
        """
        self.historico.append(self.data.copy())
        self.densidade_historico.append(self.densidade())
        self.d_his_P.append(self.densidade_P())
        self.d_his_G.append(self.densidade_G())
    
    def obter_estado(self):
        """
        Retorna uma cópia de como a matriz esta.

        Returns:
            np.ndarray: Cópia da matriz.
        """
        return self.data.copy()

    def __str__(self):
        """
        Representa a matriz como uma string formatada.

        Returns:
            str: Representação textual da matriz.
        """
        return ' '.join(map(str, self.data)) 

    def densidade(self):
        """
        Calcula a densidade de sítios vazios.

        Returns:
            float: densidade de sítios vazios.
        """
        num = np.sum(self.data == '0')
        return num / len(self.data)
    
    def densidade_P(self):
        """
        Calcula a densidade de partículas pequenas.

        Returns:
            float: densidade de partículas pequenas.
        """
        num_P = np.sum(self.data == 'P')
        return num_P / len(self.data)

    def densidade_G(self):
        """
        Calcula a densidade de partículas grandes.

        Returns:
            float: densidade de partículas grandes.
        """        
        num_G = np.sum(self.data == 'G')
        return num_G / len(self.data)
    
    def contar_sitios_vazios(self):
        """
        Conta o número de sítios vazios.

        Returns:
            int: Número de sítios vazios.
        """
        return np.sum(self.data == '0')  

    def contar_particulas_pequenas(self):
        """
        Conta o número de partículas pequenas.

        Returns:
            int: Número de partículas pequenas.
        """
        return np.sum(self.data == 'P')  

    def contar_particulas_grandes(self):
        """
        Conta o número de partículas grandes.

        Returns:
            int: Número de partículas grandes.
        """
        return np.sum(self.data == 'G')  
                
    def reacao(self, prob):
        """
        Realiza reações entre partículas  P e G adjacentes.

        Args:
            prob (float): Probabilidade de ocorrer uma reação.
        """
        for i in range(len(self.data) - 1):
            if ((self.data[i] == 'G' and self.data[i + 1] == 'P') or 
                (self.data[i] == 'P' and self.data[i + 1] == 'G')):
                if random.random() < prob:
                    self.data[i] = self.data[i + 1] = '0'
                    self.data[i] = self.data[i] = '0'
                    #self.salvar_estado()
                    #print(f'Reação entre posições {i} e {i + 1}')
                    #print(self)
            elif ((self.data[i] == 'G' and self.data[i - 1] == 'P') or 
                (self.data[i] == 'P' and self.data[i - 1] == 'G')):
                if random.random() < prob:
                    self.data[i] = self.data[i - 1] = '0'
                    self.data[i] = self.data[i] = '0'
                    #self.salvar_estado()
                    #print(f'Reação entre posições {i} e {i - 1}')
                    #print(self)

    def voo_levy(self, p_reacao, sigma):
        """
        Realiza o movimento aleatório do tipo Lévy, movendo partículas.

        Args:
            p_reacao (float): Probabilidade de reação.
            sigma (float): Parâmetro de controle do voo de Lévy.
        """
        i = random.randint(0, len(self.data) - 1)
        z = random.uniform(0.01, 1.0)
        r = z ** (-1 / sigma)
        quantidade = len(self.data)
        rj = int((r) % quantidade)
        p_direcao = 0.5
        if random.random() < p_direcao:
            j = i + rj
        else:
            j = i - rj

        j = j % quantidade
        #print(f"i: {i} rj: {rj} j: {j}")
        self.reacao(p_reacao)

        def troca_valida(pos_origem, pos_destino):
            if self.data[pos_origem] == 'G':  # Partícula G indo para pos_destino
                vizinho_esq = self.data[pos_destino - 1] if pos_destino > 0 else '0'
                vizinho_dir = self.data[pos_destino + 1] if pos_destino < len(self.data) - 1 else '0'
                return vizinho_esq != 'G' and vizinho_dir != 'G'
            elif self.data[pos_destino] == 'G':  # Partícula G indo para pos_origem
                vizinho_esq = self.data[pos_origem - 1] if pos_origem > 0 else '0'
                vizinho_dir = self.data[pos_origem + 1] if pos_origem < len(self.data) - 1 else '0'
                return vizinho_esq != 'G' and vizinho_dir != 'G'
            return True  # Sem restrições para outras partículas

        if troca_valida(i, j) and i != j:
            self.data[i], self.data[j] = self.data[j], self.data[i]
            #print(f"\nVoo de Lévy: Partículas trocadas entre {i} e {j}.")
            #print(self)
 
    def inserir_particula(self, prob_p, p_reacao):
        """
        Insere uma partícula aleatória na matriz.

        Args:
            prob_p (float): Probabilidade de inserir uma partícula pequena.
            p_reacao (float): Probabilidade de reação.
        """
        self.reacao(p_reacao)
        self.tentativas_totais += 1
        particula = 'P' if random.random() < prob_p else 'G'
        posicao = random.randint(0, len(self.data) - 1)

        if self.data[posicao] == '0':
            if particula == 'P' or \
               (particula == 'G' and not any(self.data[max(0, posicao-1):min(len(self.data), posicao+2)] == 'G')):
                self.data[posicao] = particula
                #print(f'Partícula {particula} inserida na posição {posicao}')
                #print(self)
                self.reacao(p_reacao)

class Graficos(Matrix):
    """
    Extensão da classe Matrix para graficos de simulações.
    """
    def pgxvazios(self, quantidade, tempo, levy, sigma, pasta, novo_arquivo, nomeg):
        """
        Cria um grafico de prob de particulas grandes por sitios vazios.
        G (partículas grandes): Linha azul
        P (partículas pequenas): Linha preta
        """
        dados_por_pg = defaultdict(lambda: {'soma_vazia': 0.0, 'soma_pequenas': 0.0, 'soma_grandes': 0.0, 'contagem': 0})

        for arquivo_nome in os.listdir(pasta):
            if arquivo_nome.endswith('.csv'):  
                with open(os.path.join(pasta, arquivo_nome), mode='r') as file:
                    reader = csv.DictReader(file)  
                    for row in reader:
                        iteracao = int(row['Iteracao'])
                        if 1 <= iteracao <= tempo:
                            pg = float(row['pg'])
                            dados_por_pg[pg]['soma_vazia'] += float(row['Sitios Vazios'])
                            dados_por_pg[pg]['soma_pequenas'] += float(row['Particulas Pequenas'])
                            dados_por_pg[pg]['soma_grandes'] += float(row['Particulas Grandes'])
                            dados_por_pg[pg]['contagem'] += 1

        with open(novo_arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["pg", "Sitios Vazios", "Particulas Pequenas", "Particulas Grandes"])
            for pg, valores in sorted(dados_por_pg.items()):
                contagem = valores['contagem']
                media_vazia = valores['soma_vazia'] / contagem
                media_pequenas = valores['soma_pequenas'] / contagem
                media_grandes = valores['soma_grandes'] / contagem
                writer.writerow([pg, media_vazia, media_pequenas, media_grandes])

        print(f"Arquivo '{novo_arquivo}' criado com sucesso.")

        dados = pd.read_csv(novo_arquivo)
        pg = dados['pg']
        densidade_p = dados['Particulas Pequenas']
        densidade_g = dados['Particulas Grandes']

        plt.figure(figsize=(10, 6))
        plt.plot(pg, densidade_p, marker='^', color='black', label='Ocupação por Partículas Pequenas')
        plt.plot(pg, densidade_g, marker='v', color='blue', label='Ocupação por Partículas Grandes')
        plt.suptitle('Diagrama de Fase da Ocupação de Sítios', fontsize=18, fontweight='bold')
        plt.title(f"levy = {levy}; sigma = {sigma}", fontsize=14, style='italic')
        plt.xlabel('Probabilidade de Absorção de Partículas Grandes $p_g$', fontsize=14)
        plt.ylabel('Quantidade de Sítios Ocupados', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.legend(loc='best')
        plt.grid(True)
        plt.savefig(nomeg, dpi=300)
        plt.show()



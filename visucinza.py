import numpy as np
import random
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap  
from classe import Matrix  

quantidade = 20 
tempo = 2
t_simulacao = quantidade * tempo
p_reacao = 1.0
p_levy = 0.5
pp = 0.5  
pg = 1 - pp  
sigma = 1

caminho_dos_arquivos = r'C:\Users\afern\OneDrive\Documentos\FURG\Fisicacomputacional\modeloestocastico\visualizacao'
os.makedirs(caminho_dos_arquivos, exist_ok=True)
x = datetime.now().strftime("%m%d_%H%M%S")
 
def inserir_particula(self, prob_p, p_reacao):
    """
    Insere uma partícula aleatória na matriz.

    Args:
        prob_p (float): Probabilidade de inserir uma partícula pequena.
        p_reacao (float): Probabilidade de reação.
    """
    #self.reacao(p_reacao)
    self.tentativas_totais += 1
    particula = 'P' if random.random() < prob_p else 'G'
    posicao = random.randint(0, len(self.data) - 1)

    if self.data[posicao] == '0':
        if particula == 'P' or \
            (particula == 'G' and not any(self.data[max(0, posicao-1):min(len(self.data), posicao+2)] == 'G')):
            self.data[posicao] = particula
            #print(f'Partícula {particula} inserida na posição {posicao}')
            #print(self)
            #self.reacao(p_reacao)

def simular_visualizacao(p_reacao, p_levy, sigma, quantidade, tempo, t_simulacao, pp, pg):
    sitios = Matrix(int(quantidade))
    contador = 0

    evolucao = []

    for i in range(t_simulacao):
        estado_numerico = []
        if random.random() < p_levy:
            sitios.voo_levy(p_reacao, sigma)
            inserir_particula(pp, p_reacao)
            estado = sitios.obter_estado()  
            
            for s in estado:
                if s == '0':
                    estado_numerico.append(0)
                elif s == 'P':
                    estado_numerico.append(1)
                elif s == 'G':
                    estado_numerico.append(2)
            evolucao.append(estado_numerico)
        else:
            inserir_particula(pp, p_reacao)
            for s in estado:
                if s == '0':
                    estado_numerico.append(0)
                elif s == 'P':
                    estado_numerico.append(1)
                elif s == 'G':
                    estado_numerico.append(2)
            evolucao.append(estado_numerico)
        sitios.reacao(p_reacao)
        
        contador += 1
        if contador == quantidade:
            contador = 0
            sitios.reacao(p_reacao)
    evolucao_array = np.array(evolucao)

    #tons de cinza
    cores_cinza = ['#FFFFFF', '#555555', '#000000']   
    cmap = ListedColormap(cores_cinza)

    fig, ax = plt.subplots(figsize=(10, 6))
    img = ax.imshow(evolucao_array, cmap=cmap, aspect='equal', interpolation='nearest')  # Aspect igual para quadrados

    #grade
    ax.set_xticks(np.arange(-0.5, quantidade, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(evolucao), 1), minor=True)
    ax.grid(which='minor', color='white', linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", size=0)  

    ax.set_yticks(np.arange(len(evolucao)))  # Escala inteira para iterações
    ax.set_yticklabels(np.arange(1, len(evolucao) + 1))  # Exibir valores começando em 1
    plt.title(f"Evolução da Simulação (pg={pg}; levy={p_levy}); sigma={sigma}")
    plt.xlabel("Posição")
    plt.ylabel("Iteração")

    arquivo_imagem = os.path.join(caminho_dos_arquivos, f"evolucao_r{x}.png")
    plt.savefig(arquivo_imagem)
    print(evolucao)
    plt.show()
    print(f"Imagem salva em: {arquivo_imagem}")

simular_visualizacao(p_reacao, p_levy, sigma, quantidade, tempo, t_simulacao, pp, pg)

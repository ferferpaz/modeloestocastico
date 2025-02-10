from datetime import datetime
from classe import Matrix, Graficos
import numpy as np
import random
import csv
import os

quantidade = 300  # quantidade de sítios da rede
tempo = 300
t_simulacao = quantidade * tempo

sitios = Matrix(int(quantidade))

p_reacao = 1.0
p_levy = 0.3
pps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
sigma = 2

pasta_resultados = r'C:\Users\afern\OneDrive\Documentos\FURG\Fisicacomputacional\modeloestocastico'
nome_pasta = f"levy{p_levy}s{sigma}"
pasta_resultados = os.path.join(pasta_resultados, nome_pasta)
novo_arquivo = f'mediar_clevy{p_levy}s{sigma}.csv'

os.makedirs(pasta_resultados, exist_ok=True)
x = datetime.now().strftime("%m%d_%H%M%S")

def mostras(p_reacao, p_levy, sigma, quantidade, tempo, t_simulacao, pps, c):
    contador = 0

    arquivo_nome = os.path.join(pasta_resultados, f"resultado_{c}_r{x}.csv")

    with open(arquivo_nome, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        if file.tell() == 0:
            writer.writerow(["Iteracao", "Sitios Vazios", "Particulas Pequenas", "Particulas Grandes", "pp", "pg"])
        
        for pp in pps:
            sitios = Matrix(int(quantidade))
            sitios.tentativas_totais = 0
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

                    sitios_vazios = sitios.contar_sitios_vazios()  
                    particulas_pequenas = sitios.contar_particulas_pequenas()  
                    particulas_grandes = sitios.contar_particulas_grandes() 
                    print(sitios_vazios, particulas_grandes, particulas_pequenas) 
                    pg = 1-pp

                    writer.writerow([int((i + 1) / quantidade), 
                                     sitios_vazios, 
                                     particulas_pequenas, 
                                     particulas_grandes, 
                                     pp, pg])
            
            print(f"Simulação para pp={pp}. Total de tentativas: {sitios.tentativas_totais}")

qtd_mostras = 20
for c in range(qtd_mostras):
    mostras(p_reacao, p_levy, sigma, quantidade, tempo, t_simulacao, pps, c)

nomeg = f"levy{p_levy}s{sigma}.png"
gera_grafico = Graficos(quantidade)
gera_grafico.pgxvazios(quantidade, tempo, p_levy, sigma, pasta_resultados, novo_arquivo, nomeg)




from datetime import datetime
from classe import Matrix, Graficos
import numpy as np
import random
import csv
import os

quantidade = 10  # quantidade de sítios da rede
tempo = 10
t_simulacao = quantidade * tempo

sitios = Matrix(int(quantidade))

p_reacao = 1.0
p_levy = 0.0
pps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
sigma = 2

caminho_dos_arquivos = r'C:\Users\afern\OneDrive\Documentos\FURG\Fisicacomputacional\modeloestocastico\r_semlevy'
os.makedirs(caminho_dos_arquivos, exist_ok=True)
x = datetime.now().strftime("%m%d_%H%M%S")

def mostras(p_reacao, p_levy, sigma, quantidade, tempo, t_simulacao, pps, c):
    contador = 0

    arquivo_nome = os.path.join(caminho_dos_arquivos, f"resultado_{c}_r{x}.csv")

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

qtd_mostras = 1
for c in range(qtd_mostras):
    mostras(p_reacao, p_levy, sigma, quantidade, tempo, t_simulacao, pps, c)




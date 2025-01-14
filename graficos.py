import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

tempo = 30
levy = 0.9
sigma = 2

caminho_dos_arquivos = r'C:\Users\afern\OneDrive\Documentos\FURG\Fisicacomputacional\modeloestocastico\r_clevy09s1'

dados_por_pg = defaultdict(lambda: {'soma_vazia': 0.0, 'soma_pequenas': 0.0, 'soma_grandes': 0.0, 'contagem': 0})

for arquivo_nome in os.listdir(caminho_dos_arquivos):
    if arquivo_nome.endswith('.csv'):  
        with open(os.path.join(caminho_dos_arquivos, arquivo_nome), mode='r') as file:
            reader = csv.DictReader(file)  
            for row in reader:
                iteracao = int(row['Iteracao'])
                if 1 <= iteracao <= tempo:
                    pg = float(row['pg'])
                    dados_por_pg[pg]['soma_vazia'] += float(row['Sitios Vazios'])
                    dados_por_pg[pg]['soma_pequenas'] += float(row['Particulas Pequenas'])
                    dados_por_pg[pg]['soma_grandes'] += float(row['Particulas Grandes'])
                    dados_por_pg[pg]['contagem'] += 1

novo_arquivo = 'mediar_clevy09s1.csv'
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
plt.title('Diagrama de Fase da Ocupação de Sítios')
plt.title(f"(pg={pg}; levy={levy}; sigma={sigma}")
plt.xlabel('Probabilidade de Absorção de Partículas Grandes $p_g$')
plt.ylabel('Quantidade de Sítios Ocupados')
plt.legend(loc='best')
plt.grid(True)
plt.savefig("r_clevy09s1", dpi=300)
plt.show()

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class Rede:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.data = ['0'] * tamanho

    def distribute(self, pp, pg):
        indices_vazios = [i for i, v in enumerate(self.data) if v == '0']
        if indices_vazios:  
            i = random.choice(indices_vazios)
            prob = random.random()
            if prob < pp:
                self.data[i] = 'P'  
            elif prob < pp + pg:
                if (i == 0 or self.data[i - 1] != 'G') and (i == self.tamanho - 1 or self.data[i + 1] != 'G'):
                    self.data[i] = 'G'

    def difusao(self):
        i, j = random.sample(range(self.tamanho), 2)  
        if self.data[i] != '0' and self.data[j] == '0':  
            if self.data[i] == 'G': 
                if (j > 0 and self.data[j - 1] != 'G') and (j < self.tamanho - 1 and self.data[j + 1] != 'G'):
                    self.data[i], self.data[j] = self.data[j], self.data[i]  
            elif self.data[j] == 'G':  
                if (i > 0 and self.data[i - 1] != 'G') and (i < self.tamanho - 1 and self.data[i + 1] != 'G'):
                    self.data[i], self.data[j] = self.data[j], self.data[i]  
            else:
                self.data[i], self.data[j] = self.data[j], self.data[i]  

rede = Rede(15)
pp = 0.2
pg = 1-pp

fig, ax = plt.subplots(figsize=(10, 2))

def atualizar(frame):
    rede.distribute(pp, pg)
    if random.random() < 0.3:
        rede.difusao()

    ax.clear()
    cores = {'0': 'black', 'P': 'pink', 'G': 'green'}
    bordas = {'0': 'black', 'P': 'black', 'G': 'black'}

    for i in range(rede.tamanho):
        ax.add_patch(plt.Circle((i, 0), 0.4, color=cores[rede.data[i]], edgecolor=bordas[rede.data[i]]))
    ax.set_xlim(-1, rede.tamanho)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.set_title(f'Iteração {frame}')

ani = animation.FuncAnimation(fig, atualizar, frames=100, interval=100, repeat=False)
plt.show()

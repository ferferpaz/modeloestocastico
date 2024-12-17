import numpy as np
import random


class Matrix:
    """
    Tudo relacionado a construção da matriz/linha e suas manipulações
    """
    def __init__(self, columns):
        """
        Construtor da classe Matrix.

        Inicializa uma matriz vazia de linhas.

        Argumentos:
            columns (int): Número de colunas da matriz.
        """
        self.data = np.array(['0'] * columns)  
    
    def __str__(self):
        return ' '.join(map(str, self.data)) 

    def distribute(self, pp, pg):
        """
        Faz a distribuição das partículas pela linha horizontal.

        Argumentos:
            pp (float): Probabilidade de colocar a partícula P.
            pg (float): Probabilidade de colocar a partícula G.
        """
        for i in range(len(self.data)):
            prob = random.random()
            
            if self.data[i] == '0':  
                if prob < pp:
                    self.data[i] = 'P'  
                elif prob < pg and ( 
                    (i == 0 or self.data[i - 1] != 'G') and
                    (i == len(self.data) - 1 or self.data[i + 1] != 'G')):
                    self.data[i] = 'G'

class Atomo(Matrix):
    """
    Definir todas as iterações atômicas e parâmetros dos átomos.
    """
    def __init__(self, matrix):
        """
        Construtor da classe Atomo.

        Argumentos:
            matrix (Matrix): Objeto Matrix com a distribuição dos átomos.
        """
        self.data = matrix.data  # Atribui os dados da matriz passada ao atributo `data` do objeto Atomo
    
    def distcvs(self):
        cvs = [-1, 0, 1]  
        listcv = []

        for i in range(len(self.data)):
            if self.data[i] != '0':  
                cv_value = random.choice(cvs)
                listcv.append(cv_value)  
            else:
                listcv.append('')  
        # Atribui listcv como atributo do objeto para acesso posterior, se necessário
        #self.listcv = listcv
        return listcv
    
    def distelet(self, sitios):
        list_elet=[]
        for i in range(len(self.data)):
            if self.data[i] == 'P':
                list_elet.append(2.1)
            elif self.data[i] == 'G':
                list_elet.append(3.5)
            elif self.data[i] == '0':
                list_elet.append(0)

    def olhos(self, linhas, sitios):
        for i in range(linhas):
            pos = random.randint(0, linhas - 1)
            valor = sitios.data[pos][0]
            
            if valor != '0':
                print(f"valor: {valor} posição: {pos+1}")
                r = random.randint(1, linhas - 1)  # para valores grandes tem que mudar, se não o raio fica grande demais
                rc = int(r / 2)  # metade dos campos para cada lado
                print(f"r: {r} rc: {rc}")

                #TROCAR A LOGICA DE LIMITE DE INDICE, TORNAR CIRCULAR
                for c in range(rc):
                    # Verificar os limites antes de acessar os índices
                    if pos + c + 1 < linhas:  # não vai ultrapassar o limite direito
                        dire = sitios.data[pos + c + 1][0]
                        print(f"na direita c={c+1} quem tá do lado={dire}")
                    else:
                        print(f"na direita c={c+1} fora dos limites")
                    
                    if pos - c - 1 >= 0:  #não vai ultrapassar o limite esquerdo
                        esq = sitios.data[pos - c - 1][0]
                        print(f"na esquerda c={c+1} quem tá do lado={esq}")
                    else:
                        print(f"na esquerda c={c+1} fora dos limites")






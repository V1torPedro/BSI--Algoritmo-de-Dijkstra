from queue import PriorityQueue
from prettytable import PrettyTable


class Grafo():

    def __init__(self, num_vertices):
        self.v = num_vertices
        self.arestas = [[0 for i in range(num_vertices)]
                        for j in range(num_vertices)]
        self.visitados = []

    def addAresta(self, u, v, peso):  # Adiciona aresta (na matriz de adjascência)
        self.arestas[u][v] = peso
        self.arestas[v][u] = peso

    def dijkstra(self, v_inicial):  # Calcula a distancia do vertice v para todos os outros

        # D = Distâncias
        # Inicializar com valores infinitos, para sempre escolher o menor valor
        D = {v: float('inf') for v in range(self.v)}
        D[v_inicial] = 0

        # Inicializar uma lista de prioridades, onde o menor valor é priorizado
        pq = PriorityQueue()
        pq.put((0, v_inicial))

        # Inicializar lista contendo cada caminho específico
        self.D_Caminhos = [[] for v in range(self.v)]
        # Inicializar lista com todos os caminhos testados
        self.Todos_Caminhos = []

        # Loop do programa:----------------------------------------------------
        while not pq.empty():  # Enquanto houverem prioridades(enquanto houver distancias ainda não calculadas)
            (dist, v_atual) = pq.get()
            self.visitados.append(v_atual)
            # Calcular o custo dos vertices adjacentes, e adiciona-los ao custo final de (vertice inicial -- vertice final).
            # Exemplo: A distancia de (a,c) = 3. Se ao calcular os vértices adjacentes de b, se perceber que (a,b,c) < (a,c), a distancia final de a até c será atualizada.
            for vizinho in range(self.v):  # Para cada possível vizinho
                if self.arestas[v_atual][vizinho] != 0:
                    # Diferente de 0 significa que são vizinhos
                    distancia = self.arestas[v_atual][vizinho]
                    custo_novo = D[v_atual] + distancia
                    if vizinho not in self.visitados:  # Se o vértice não foi visitado
                        custo_antigo = D[vizinho]

                        if custo_novo < custo_antigo:
                            pq.put((custo_novo, vizinho))
                            D[vizinho] = custo_novo
                            # Obs: O programa registra todas as arestas que já testou. Para atualizar o melhor caminho, ele
                            # apaga os caminhos anteriores e registra a ultima atualização do caminho:
                            self.D_Caminhos[vizinho] = [] \
                                + self.D_Caminhos[v_atual] \
                                + [(v_atual, vizinho)]
                            self.Todos_Caminhos.append(
                                [self.D_Caminhos[vizinho], custo_novo])
                        else:
                            # Registrar o caminho apenas para imprimir na tabela, se ele não já foi registrado
                            vert = [self.D_Caminhos[v_atual] +
                                    [(v_atual, vizinho)], custo_novo]
                            if vert not in self.Todos_Caminhos:
                                self.Todos_Caminhos.append(vert)
                    else:
                        # Vértice já visitado, registrar apenas para imprimir na tabela
                        if self.D_Caminhos[v_atual][-1] != (vizinho, v_atual):
                            # Ex: Não adicionar (0--1),(1--0)
                            vert = [self.D_Caminhos[v_atual] +
                                    [(v_atual, vizinho)], custo_novo]
                            if vert not in self.Todos_Caminhos:
                                self.Todos_Caminhos.append(vert)
        return D

    def tabela(self):  # Imprimir tabela:
        tabela = []
        v_impressos_finais = []
        Atualizacao_ordem = []
        t = PrettyTable(["Caminho", "Vértices", "Comprimento",
                        "Atualização", "Cancelamento"])
        t.align["Caminho"] = "l"
        t.align["Vértices"] = "l"
        t.align["Comprimento"] = "m"
        t.align["Atualização"] = "m"
        t.align["Cancelamento"] = "m"

        for c in range(0, len(self.Todos_Caminhos)):
            # Analisar cada vertice final e ver se ja houve uma rota até aquele ponto(Cancelamento)
            v_final = self.Todos_Caminhos[c][0][-1][-1]
            if v_final in v_impressos_finais:
                c_atual = self.Todos_Caminhos[c][1]
                c_anterior = self.Todos_Caminhos[v_impressos_finais.index(
                    v_final)][1]
                # Se houver cancelamento, cancelar o maior com o de menor comprimento
                if c_anterior < c_atual:
                    Cancelamento = f"Sim, para C{v_impressos_finais.index(v_final) + 1}"
                elif c_anterior == c_atual:
                    Cancelamento = "Não"
                elif c_anterior > c_atual:
                    Cancelamento = "Não"
                    tabela[v_impressos_finais.index(
                        v_final)][4] = f"Sim, para C{c + 1}"
            else:
                Cancelamento = "Não"
            v_impressos_finais.append(v_final)

            # Registrar atualizações
            Atualizacao = []
            # Ex: (0-1) procura por rotas de seu len + 1 (len+1 =2) que possuam (0-1)
            for dc in range(c, len(self.Todos_Caminhos)):
                if len(self.Todos_Caminhos[dc][0]) == len(self.Todos_Caminhos[c][0]) + 1:
                    if all(item in self.Todos_Caminhos[c][0] for item in self.Todos_Caminhos[dc][0][:-1]):
                        Atualizacao.append(f"C{c+1} --> C{dc +1}")
                        A_ordem = (c, self.Todos_Caminhos[c][1])
                        if A_ordem not in Atualizacao_ordem:
                            Atualizacao_ordem.append(A_ordem)
                            Atualizacao_ordem.sort(key=lambda x: x[1])
        # Adicionar na tabela
            if Atualizacao == []:
                tabela.append([f"C{c+1}", self.Todos_Caminhos[c][0],
                              self.Todos_Caminhos[c][1], "-", Cancelamento])
            else:
                tabela.append([f"C{c+1}", self.Todos_Caminhos[c][0],
                              self.Todos_Caminhos[c][1], " ou ".join(Atualizacao), Cancelamento])
        # Numerar as atualizações
        N_Atualizacao = 1
        for A, valor in Atualizacao_ordem:
            tabela[A][3] = f"At({N_Atualizacao}): " + tabela[A][3]
            N_Atualizacao += 1
        # Impressão final -----------------------
        for l in range(0, len(tabela)):
            t.add_row(tabela[l])
        print(t)
        return

    def imprimir_distancias(self, v_inicial):
        g.tabela()
        # Imprimir melhores percursos:
        m = PrettyTable(["Vértices", "Menores Distâncias", "Percurso"])
        for vertice in range(len(D)):
            # EX: Não imprimir (Vértice 1 ---> Vértice 1)
            if vertice != v_inicial:
                m.add_row([f"({v_inicial}) ---> ({vertice})",
                          f"Distância = {D[vertice]}", self.D_Caminhos[vertice]])
        print(m)

    # Calcula menor caminho entre 2 vértices
    def menor_caminho(self, v_inicial, v_final):
        print(
            f"#-- Vertices ({v_inicial})--({v_final}) , Menor distância = {D[v_final]}, Percurso = {self.D_Caminhos[v_final]} --#")


# ---------------------------------------------------
# Área editável: digite aqui:
g = Grafo(6)  # Numero de vértices
print("#---- Obs: SOMENTE Grafos NÃO ORIENTADOS ----#")
# e as Arestas(nomeadas com números, a partir de 0, e seu peso)
g.addAresta(0, 1, 3)
g.addAresta(0, 2, 4)
g.addAresta(2, 3, 4)
g.addAresta(0, 3, 2)
g.addAresta(2, 4, 6)
g.addAresta(3, 4, 1)
g.addAresta(4, 5, 2)
g.addAresta(3, 5, 4)
# --------------------------------------------------


def matriz_de_adjascencia(g):  # Extra: Imprimir matriz de adjascência do grafo
    for x in g.arestas:
        linha = []
        for y in x:
            if y == 0:
                linha.append(0)
            else:
                linha.append(1)
        print(linha)


# ------------------------------------------------------
# Main:
i = int(
    input("Imprimir todas as distâncias(Digite 1) ou o menor caminho(Digite 2):"))
if i == 1:
    v = int(input("A partir de qual vertice: "))
    D = g.dijkstra(v)
    g.imprimir_distancias(v)
elif i == 2:
    vi = int(input("Vertice inicial: "))
    vf = int(input("Vertice final: "))
    D = g.dijkstra(vi)
    g.tabela()
    g.menor_caminho(vi, vf)

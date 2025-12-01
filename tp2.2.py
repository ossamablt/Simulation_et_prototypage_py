from collections import deque
from pyvis.network import Network
import webbrowser

class ReseauDePetri:
    """Classe pour représenter et simuler un Réseau de Petri"""
    def __init__(self, P, T, Pre, Post, M0):
        self.P = P
        self.T = T
        self.Pre = Pre
        self.Post = Post
        self.M0 = M0
        self.C = [[Post[i][j] - Pre[i][j] for j in range(len(T))] for i in range(len(P))]

    def est_franchissable(self, M, t):
        return all(M[i] >= self.Pre[i][t] for i in range(len(self.P)))

    def franchir(self, M, t):
        return [M[i] + self.C[i][t] for i in range(len(self.P))]

    def RdPSim(self, sequence):
        M = self.M0[:]
        marquages = [M[:]]
        print(f"\nMarquage initial M0 = {M}")
        for i, t_name in enumerate(sequence):
            t = self.T.index(t_name)
            if not self.est_franchissable(M, t):
                print(f"{t_name} NON FRANCHISSABLE")
                break
            M = self.franchir(M, t)
            marquages.append(M[:])
            print(f"{t_name} franchie -> M{i+1} = {M}")
        return marquages

    def graphe_marquages_accessibles(self, max_marquages=100):
        marquages = {tuple(self.M0): 0}
        file = deque([self.M0[:]])
        arcs = []
        idx = 0

        while file and idx < max_marquages:
            M = file.popleft()
            M_tuple = tuple(M)
            for t in range(len(self.T)):
                if self.est_franchissable(M, t):
                    M_new = self.franchir(M, t)
                    M_new_tuple = tuple(M_new)
                    if M_new_tuple not in marquages:
                        idx += 1
                        marquages[M_new_tuple] = idx
                        file.append(M_new)
                    arcs.append((M_tuple, self.T[t], M_new_tuple))
        return marquages, arcs

    def visualiser(self, marquages, arcs, filename="petri_graph.html"):
        net = Network(height="600px", width="100%", directed=True)
        for m, i in marquages.items():
            net.add_node(f"M{i}", label=f"M{i}\n{list(m)}", shape="ellipse")
        for src, t, dst in arcs:
            net.add_edge(f"M{marquages[src]}", f"M{marquages[dst]}", label=t)
        net.write_html(filename)  # écrit l'HTML
        import webbrowser
        webbrowser.open(filename)  # ouvre dans le navigateur
        webbrowser.open(filename)  # ouvre automatiquement dans le navigateur
        print("Graph visualisé dans votre navigateur !")

    def afficher_matrice(self, matrice, nom):
        print(f"\n{nom}:")
        for i, ligne in enumerate(matrice):
            print(f"  {self.P[i]:4} {ligne}")


# ================== TEST ==================

def test_producteur_consommateur():
    P = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']
    T = ['t0', 't1', 't2', 't3', 't4']
    M0 = [2, 0, 0, 1, 0, 0]

    Pre = [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1]
    ]

    Post = [
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]

    rdp = ReseauDePetri(P, T, Pre, Post, M0)
    rdp.afficher_matrice(Pre, "Matrice Pré (Consommation)")
    rdp.afficher_matrice(Post, "Matrice Post (Production)")
    rdp.afficher_matrice(rdp.C, "Matrice d'Incidence C = Post - Pre")

    sequence = ['t0', 't1', 't2', 't3', 't4']
    marquages_sim = rdp.RdPSim(sequence)

    marquages_acc, arcs = rdp.graphe_marquages_accessibles()
    rdp.visualiser(marquages_acc, arcs)


if __name__ == "__main__":
    test_producteur_consommateur()

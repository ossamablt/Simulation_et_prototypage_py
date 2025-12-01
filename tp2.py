from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

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
        """Vérifie si M >= Pre[:,t]"""
        return all(M[i] >= self.Pre[i][t] for i in range(len(self.P)))
    
    def franchir(self, M, t):
        """Retourne M' = M + C[:,t]"""
        return [M[i] + self.C[i][t] for i in range(len(self.P))]
    
    def RdPSim(self, sequence):
        """Simule une séquence de transitions"""
        M = self.M0[:]
        marquages = [M[:]]
        
        print(f"\n{'='*60}\nSIMULATION DU RÉSEAU DE PETRI\n{'='*60}")
        print(f"Marquage initial M0 = {M}")
        print(f"Places: {self.P}")
        print(f"\nDéroulement de la séquence: {sequence}\n")
        
        for i, t_name in enumerate(sequence):
            t = self.T.index(t_name)
            
            print(f"Étape {i+1}: Tentative de franchissement de [{t_name}]")
            
            if not self.est_franchissable(M, t):
                print(f"  ❌ {t_name} NON FRANCHISSABLE")
                print(f"     Marquage actuel: {M}")
                print(f"     Pré-conditions requises: {[self.Pre[k][t] for k in range(len(self.P))]}")
                break
            
            M = self.franchir(M, t)
            marquages.append(M[:])
            print(f"  ✓ {t_name} franchie -> M{i+1} = {M}")
        
        print(f"\n{'='*60}")
        print(f"Marquage final: {M}")
        print(f"{'='*60}\n")
        
        return marquages
    
    def graphe_marquages_accessibles(self, max_marquages=100):
        """Génère le graphe des marquages accessibles"""
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
        
        print(f"\n{'='*60}\nGRAPHE DES MARQUAGES ACCESSIBLES\n{'='*60}")
        print(f"Nombre de marquages accessibles: {len(marquages)}")
        print(f"Nombre de transitions: {len(arcs)}\n")
        
        for m, i in sorted(marquages.items(), key=lambda x: x[1]):
            print(f"  M{i} = {list(m)}")
        
        print()
        return marquages, arcs
    
    def visualiser(self, marquages, arcs):
        """Visualise le graphe avec NetworkX"""
        G = nx.DiGraph()
        
        for m, i in marquages.items():
            G.add_node(f"M{i}\n{list(m)}")
        
        for src, t, dst in arcs:
            G.add_edge(
                f"M{marquages[src]}\n{list(src)}",
                f"M{marquages[dst]}\n{list(dst)}",
                label=t
            )
        
        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(G, k=2.5, iterations=50, seed=42)
        
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2500, alpha=0.9)
        nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, edge_color='gray', 
                              arrowstyle='->', connectionstyle='arc3,rad=0.1')
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'label'), 
                                     font_size=9, font_color='red')
        
        plt.title("Graphe des Marquages Accessibles - Producteur/Consommateur", 
                 fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def afficher_matrice(self, matrice, nom):
        """Affiche une matrice de manière formatée"""
        print(f"\n{nom}:")
        for i, ligne in enumerate(matrice):
            print(f"  {self.P[i]:4} {ligne}")

def test_producteur_consommateur():
 
    # Définition du réseau selon l'image
    P = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']
    T = ['t0', 't1', 't2', 't3', 't4']  # 5 transitions (corrigé)
    
    # Marquage initial
    M0 = [2, 0, 0, 1, 0, 0]
    
    # Matrice Pré (consumption) - 6 places x 5 transitions
    Pre = [
        [1, 0, 0, 0, 1],     # P0: Producer ready
        [0, 1, 0, 0, 0],     # P1: Buffer slot 1
        [0, 0, 1, 0, 0],     # P2: Buffer slot 2
        [0, 0, 0, 1, 0],     # P3: Consumer ready
        [0, 1, 1, 0, 0],     # P4: Item in production
        [0, 0, 0, 1, 1]      # P5: Item being consumed
    ]
    
    # Matrice Post (production) - 6 places x 5 transitions
    Post = [
        [0, 0, 0, 0, 1],     # P0: Producer ready
        [1, 0, 0, 0, 0],     # P1: Buffer slot 1
        [0, 1, 0, 0, 0],     # P2: Buffer slot 2
        [0, 0, 0, 0, 1],     # P3: Consumer ready
        [1, 0, 0, 0, 0],     # P4: Item in production
        [0, 0, 0, 1, 0]      # P5: Item being consumed
    ]
    
    # Créer le réseau
    rdp = ReseauDePetri(P, T, Pre, Post, M0)
    
    # Afficher les informations
    print("\n📊 INFORMATIONS SUR LE RÉSEAU")
    print(f"Places: {P}")
    print(f"Transitions: {T}")
    print(f"Marquage initial M0: {M0}")
    
    rdp.afficher_matrice(Pre, "Matrice Pré (Consommation)")
    rdp.afficher_matrice(Post, "Matrice Post (Production)")
    rdp.afficher_matrice(rdp.C, "Matrice d'Incidence C = Post - Pre")
    
    # Test 1: Simulation d'une séquence
    print("\n" + "▀"*60)
    print("TEST 1: SIMULATION D'UNE SÉQUENCE")
    print("▀"*60)
    
    sequence = ['t0', 't1', 't2', 't3', 't4']
    marquages = rdp.RdPSim(sequence)
    
    # Test 2: Graphe des marquages accessibles
    print("\n" + "▀"*60)
    print("TEST 2: GRAPHE DES MARQUAGES ACCESSIBLES")
    print("▀"*60)
    
    marquages_acc, arcs = rdp.graphe_marquages_accessibles()
    
    # Visualisation
    print("\n🎨 Génération de la visualisation graphique...")
    rdp.visualiser(marquages_acc, arcs)
    
    # Test 3: Vérification avec équation de changement d'état
    print("\n" + "▀"*60)
    print("TEST 3: VÉRIFICATION ÉQUATION DE CHANGEMENT D'ÉTAT")
    print("▀"*60)
    
    # Vecteur d'occurrence pour la séquence t0, t1, t2, t3, t4
    s = [1, 1, 1, 1, 1]  # Chaque transition franchie 1 fois
    
    print(f"\nSéquence: {sequence}")
    print(f"Vecteur d'occurrence s = {s}")
    print(f"\nÉquation: M' = M0 + C × s")
    
    # Calcul M' = M0 + C × s
    M_final = M0[:]
    for i in range(len(P)):
        for j in range(len(T)):
            M_final[i] += rdp.C[i][j] * s[j]
    
    print(f"\nM0 (initial)  = {M0}")
    print(f"M' (calculé)  = {M_final}")
    print(f"M' (simulé)   = {marquages[-1]}")
    print(f"\nRésultat: {'✓ CORRECT !' if M_final == marquages[-1] else '✗ ERREUR'}")
    
    print("\n" + "="*60)
    print("✅ SIMULATION TERMINÉE AVEC SUCCÈS")
    print("="*60)


# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    test_producteur_consommateur()
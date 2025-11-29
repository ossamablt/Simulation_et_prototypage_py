import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

class ReseauDePetri:
    """Classe pour représenter et simuler un Réseau de Petri"""
    
    def __init__(self, P, T, Pre, Post, M0):
        """
        Initialise un Réseau de Petri
        
        P: Liste des noms de places
        T: Liste des noms de transitions
        Pre: Matrice d'incidence avant (n x m)
        Post: Matrice d'incidence arrière (n x m)
        M0: Marquage initial (vecteur de taille n)
        """
        self.P = P  # Places
        self.T = T  # Transitions
        self.Pre = np.array(Pre)  # Matrice Pré
        self.Post = np.array(Post)  # Matrice Post
        self.M0 = np.array(M0)  # Marquage initial
        self.C = self.Post - self.Pre  # Matrice d'incidence
        
        # Validation des dimensions
        n = len(P)  # Nombre de places
        m = len(T)  # Nombre de transitions
        
        assert self.Pre.shape == (n, m), "Dimension incorrecte pour Pre"
        assert self.Post.shape == (n, m), "Dimension incorrecte pour Post"
        assert len(M0) == n, "Dimension incorrecte pour M0"
    
    def est_franchissable(self, M, t_index):
        """
        Vérifie si une transition t est franchissable pour le marquage M
        
        Condition: M >= Pre[:,t] (pour toutes les places)
        """
        return np.all(M >= self.Pre[:, t_index])
    
    def transitions_franchissables(self, M):
        """
        Retourne la liste des indices des transitions franchissables pour M
        """
        franchissables = []
        for t_idx in range(len(self.T)):
            if self.est_franchissable(M, t_idx):
                franchissables.append(t_idx)
        return franchissables
    
    def franchir_transition(self, M, t_index):
        """
        Franchit la transition t à partir du marquage M
        
        Retourne le nouveau marquage M' = M + C[:,t]
        """
        if not self.est_franchissable(M, t_index):
            raise ValueError(f"Transition {self.T[t_index]} non franchissable!")
        
        # Nouveau marquage selon l'équation: M' = M + C[:,t]
        M_nouveau = M + self.C[:, t_index]
        return M_nouveau
    
    def RdPSim(self, sequence_transitions):
        """
        Simule le franchissement d'une séquence de transitions
        
        sequence_transitions: Liste d'indices de transitions ou liste de noms
        
        Retourne: Liste des marquages successifs
        """
        marquages = [self.M0.copy()]
        M_courant = self.M0.copy()
        
        print("=" * 60)
        print("SIMULATION DU RÉSEAU DE PETRI")
        print("=" * 60)
        print(f"Marquage initial M0: {M_courant}")
        print()
        
        for i, t in enumerate(sequence_transitions):
            # Convertir le nom en indice si nécessaire
            if isinstance(t, str):
                t_idx = self.T.index(t)
            else:
                t_idx = t
            
            print(f"Étape {i+1}: Franchissement de {self.T[t_idx]}")
            
            # Vérifier si la transition est franchissable
            if not self.est_franchissable(M_courant, t_idx):
                print(f"  ❌ ERREUR: {self.T[t_idx]} n'est pas franchissable!")
                print(f"  Marquage actuel: {M_courant}")
                print(f"  Pré-conditions: {self.Pre[:, t_idx]}")
                break
            
            # Franchir la transition
            M_courant = self.franchir_transition(M_courant, t_idx)
            marquages.append(M_courant.copy())
            
            print(f"  ✓ Nouveau marquage: {M_courant}")
            print()
        
        print("=" * 60)
        print(f"Marquage final: {M_courant}")
        print("=" * 60)
        
        return marquages
    
    def graphe_marquages_accessibles(self, max_marquages=1000):
        """
        Génère le graphe des marquages accessibles
        
        Retourne: 
        - marquages_accessibles: dictionnaire {tuple(marquage): indice}
        - transitions_graphe: liste de (M_source, transition, M_dest)
        """
        print("\n" + "=" * 60)
        print("GÉNÉRATION DU GRAPHE DES MARQUAGES ACCESSIBLES")
        print("=" * 60)
        
        # Initialisation
        M0_tuple = tuple(self.M0)
        marquages_accessibles = {M0_tuple: 0}
        marquages_a_explorer = deque([self.M0])
        transitions_graphe = []
        compteur = 0
        
        while marquages_a_explorer and compteur < max_marquages:
            M_courant = marquages_a_explorer.popleft()
            M_courant_tuple = tuple(M_courant)
            
            # Explorer toutes les transitions franchissables
            for t_idx in self.transitions_franchissables(M_courant):
                M_nouveau = self.franchir_transition(M_courant, t_idx)
                M_nouveau_tuple = tuple(M_nouveau)
                
                # Ajouter le nouveau marquage s'il n'existe pas
                if M_nouveau_tuple not in marquages_accessibles:
                    compteur += 1
                    marquages_accessibles[M_nouveau_tuple] = compteur
                    marquages_a_explorer.append(M_nouveau)
                
                # Ajouter la transition au graphe
                transitions_graphe.append((M_courant_tuple, self.T[t_idx], M_nouveau_tuple))
        
        print(f"\n✓ Nombre de marquages accessibles: {len(marquages_accessibles)}")
        print(f"✓ Nombre de transitions dans le graphe: {len(transitions_graphe)}")
        
        # Afficher tous les marquages accessibles
        print("\nMarquages accessibles:")
        for marquage, idx in sorted(marquages_accessibles.items(), key=lambda x: x[1]):
            print(f"  M{idx}: {list(marquage)}")
        
        return marquages_accessibles, transitions_graphe
    
    def visualiser_graphe(self, marquages_accessibles, transitions_graphe):
        """
        Visualise le graphe des marquages accessibles avec matplotlib
        """
        G = nx.DiGraph()
        
        # Ajouter les nœuds
        for marquage, idx in marquages_accessibles.items():
            label = f"M{idx}\n{list(marquage)}"
            G.add_node(label)
        
        # Ajouter les arcs
        for M_source, transition, M_dest in transitions_graphe:
            idx_source = marquages_accessibles[M_source]
            idx_dest = marquages_accessibles[M_dest]
            label_source = f"M{idx_source}\n{list(M_source)}"
            label_dest = f"M{idx_dest}\n{list(M_dest)}"
            G.add_edge(label_source, label_dest, label=transition)
        
        # Dessiner le graphe
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Dessiner les nœuds
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=2000, alpha=0.9)
        
        # Dessiner les arcs
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                              arrows=True, arrowsize=20, 
                              arrowstyle='->', connectionstyle='arc3,rad=0.1')
        
        # Dessiner les labels des nœuds
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        
        # Dessiner les labels des arcs
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)
        
        plt.title("Graphe des Marquages Accessibles", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()


# ============================================================================
# EXEMPLE D'UTILISATION - Réseau de Petri du cours (Figure diapo 9)
# ============================================================================

print("╔" + "═" * 58 + "╗")
print("║" + " " * 10 + "SIMULATION RÉSEAU DE PETRI - EXEMPLE" + " " * 11 + "║")
print("╚" + "═" * 58 + "╝")

# Définition du réseau (Exemple du cours - diapo 9)
P = ['P1', 'P2', 'P3', 'P4', 'P5']
T = ['t1', 't2', 't3', 't4']

# Matrice Pré (5 places x 4 transitions)
Pre = [
    [1, 0, 0, 0],  # P1
    [0, 1, 0, 0],  # P2
    [0, 0, 1, 0],  # P3
    [0, 0, 0, 1],  # P4
    [0, 0, 0, 0]   # P5
]

# Matrice Post (5 places x 4 transitions)
Post = [
    [0, 0, 0, 0],  # P1
    [1, 0, 0, 0],  # P2
    [0, 1, 0, 0],  # P3
    [0, 0, 1, 0],  # P4
    [0, 0, 0, 1]   # P5
]

# Marquage initial [P1, P2, P3, P4, P5]
M0 = [1, 0, 0, 0, 0]

# Créer le réseau de Petri
rdp = ReseauDePetri(P, T, Pre, Post, M0)

# Afficher les informations du réseau
print("\nInformations sur le réseau:")
print(f"Places: {P}")
print(f"Transitions: {T}")
print(f"Matrice d'incidence C:\n{rdp.C}")

# ============================================================================
# TEST 1: Simulation d'une séquence de transitions
# ============================================================================
print("\n" + "▀" * 60)
print("TEST 1: SIMULATION D'UNE SÉQUENCE")
print("▀" * 60)

sequence = ['t1', 't3', 't4', 't1', 't3', 't4', 't1', 't2']
marquages = rdp.RdPSim(sequence)

# ============================================================================
# TEST 2: Génération du graphe des marquages accessibles
# ============================================================================
print("\n" + "▀" * 60)
print("TEST 2: GRAPHE DES MARQUAGES ACCESSIBLES")
print("▀" * 60)

marquages_acc, transitions_gr = rdp.graphe_marquages_accessibles()

# Visualiser le graphe
print("\nGénération de la visualisation du graphe...")
rdp.visualiser_graphe(marquages_acc, transitions_gr)

# ============================================================================
# TEST 3: Vérification avec l'équation de changement d'état
# ============================================================================
print("\n" + "▀" * 60)
print("TEST 3: ÉQUATION DE CHANGEMENT D'ÉTAT")
print("▀" * 60)

# Vecteur d'occurrence pour la séquence: t1 t3 t4 t1 t3 t4 t1 t2
# s_vec = [3, 1, 2, 2] (3 fois t1, 1 fois t2, 2 fois t3, 2 fois t4)
s_vec = np.array([3, 1, 2, 2])

print(f"Séquence: {sequence}")
print(f"Vecteur d'occurrence s: {s_vec}")
print(f"Marquage initial M0: {rdp.M0}")

# Calculer M' = M0 + C * s_vec
M_final = rdp.M0 + rdp.C @ s_vec

print(f"\nÉquation: M' = M0 + C × s")
print(f"Marquage final calculé M': {M_final}")
print(f"Marquage final simulé: {marquages[-1]}")
print(f"Vérification: {'✓ CORRECT' if np.array_equal(M_final, marquages[-1]) else '✗ ERREUR'}")

print("\n" + "═" * 60)
print("FIN DE LA SIMULATION")
print("═" * 60)
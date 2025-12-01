def Msim(i, P, n):
    """
    Simule la suite X_n conditionnellement à X_0 = i
    
    Paramètres:
    -----------
    i : int - État initial (index commence à 0)
    P : list of list - Matrice de transition
    n : int - Nombre d'étapes de simulation
    
    Retourne:
    ---------
    pi_n : list - Distribution de probabilités à l'instant n
    """
    nb_etats = len(P)
    
    # Initialisation: on part de l'état i avec certitude
    pi = [0.0] * nb_etats
    pi[i] = 1.0
    
    print(f"π(0) = {[round(p, 4) for p in pi]}")
    
    # Simulation pour n étapes
    for etape in range(1, n + 1):
        # Calcul de π(etape) = π(etape-1) * P
        pi_nouveau = [0.0] * nb_etats
        
        for j in range(nb_etats):
            for k in range(nb_etats):
                pi_nouveau[j] += pi[k] * P[k][j]
        
        pi = pi_nouveau
        print(f"π({etape}) = {[round(p, 6) for p in pi]}")
    
    return pi


def R_Stationnaire(P, epsilon=1e-10):
    """
    Trouve le régime stationnaire π tel que π = πP
    En résolvant le système linéaire avec la méthode de Gauss
    
    Système: (P^T - I)π = 0 avec la contrainte Σπ_i = 1
    
    Paramètres:
    -----------
    P : list of list - Matrice de transition
    epsilon : float - Seuil pour considérer un nombre comme zéro
    
    Retourne:
    ---------
    pi : list - Distribution stationnaire
    """
    n = len(P)
    
    print("\nRecherche du régime stationnaire (méthode de Gauss)...")
    
    # Construction de la matrice augmentée [A|b]
    A = []
    
    # Les n-1 premières équations: (P^T - I)π = 0
    for i in range(n - 1):
        ligne = []
        for j in range(n):
            if i == j:
                ligne.append(P[j][i] - 1.0)
            else:
                ligne.append(P[j][i])
        ligne.append(0.0)  # b[i] = 0
        A.append(ligne)
    
    # Dernière équation: π_0 + π_1 + ... + π_{n-1} = 1
    derniere_ligne = [1.0] * n + [1.0]
    A.append(derniere_ligne)
    
    # Pivot de Gauss - Triangularisation
    for col in range(n):
        # Choix du pivot (ligne avec plus grande valeur absolue)
        pivot_ligne = col
        for i in range(col + 1, n):
            if abs(A[i][col]) > abs(A[pivot_ligne][col]):
                pivot_ligne = i
        
        # Échange de lignes
        A[col], A[pivot_ligne] = A[pivot_ligne], A[col]
        
        # Vérifier si le pivot est non nul
        if abs(A[col][col]) < epsilon:
            continue  # Passer à la colonne suivante si pivot ≈ 0
        
        # Élimination
        for i in range(col + 1, n):
            if abs(A[i][col]) > epsilon:
                facteur = A[i][col] / A[col][col]
                for j in range(col, n + 1):
                    A[i][j] -= facteur * A[col][j]
    
    # Substitution arrière
    pi = [0.0] * n
    for i in range(n - 1, -1, -1):
        somme = A[i][n]  # Terme constant
        for j in range(i + 1, n):
            somme -= A[i][j] * pi[j]
        
        # Vérifier division par zéro
        if abs(A[i][i]) > epsilon:
            pi[i] = somme / A[i][i]
        else:
            pi[i] = 0.0  # Variable libre
    
    print(f"π stationnaire = {[round(p, 6) for p in pi]}")
    print(f"Somme = {round(sum(pi), 6)}")
    
    return pi


# ============= TESTS =============

print("=" * 60)
print("EXEMPLE 1: Labyrinthe de la souris")
print("=" * 60)

P_labyrinthe = [
    [0,    1/3,  1/3,  0,    1/3],
    [1/2,  0,    0,    1/2,  0  ],
    [1/2,  0,    0,    1/2,  0  ],
    [0,    0,    0,    1,    0  ],
    [0,    0,    0,    0,    1  ]
]

print("\nSimulation partant de l'état 1:")
pi_20 = Msim(0, P_labyrinthe, 20)

print("\n" + "-" * 60)
pi_stat = R_Stationnaire(P_labyrinthe)

print(f"\nProbabilité d'atteindre la nourriture (état 4): {round(pi_stat[3], 4)}")
print(f"Probabilité d'atteindre la tanière (état 5): {round(pi_stat[4], 4)}")


print("\n" + "=" * 60)
print("EXEMPLE 2: Chaîne ergodique")
print("=" * 60)

P_ergodique = [
    [1/2,  0,    1/2],
    [1/4,  1/2,  1/4],
    [1/3,  1/3,  1/3]
]

print("\nSimulation partant de l'état 0:")
pi_10 = Msim(0, P_ergodique, 10)

print("\n" + "-" * 60)
pi_stat_erg = R_Stationnaire(P_ergodique)

print(f"\nDistribution théorique: [3/8={3/8:.6f}, 1/4={1/4:.6f}, 3/8={3/8:.6f}]")
print(f"Distribution calculée:  [{pi_stat_erg[0]:.6f}, {pi_stat_erg[1]:.6f}, {pi_stat_erg[2]:.6f}]")


print("\n" + "=" * 60)
print("EXEMPLE 3: Météo")
print("=" * 60)

P_meteo = [
    [0.7,  0.3],
    [0.4,  0.6]
]

print("\nÉtats: 0=Ensoleillé, 1=Pluvieux")
print("\nSimulation partant d'un jour ensoleillé:")
pi_7 = Msim(0, P_meteo, 7)

print("\n" + "-" * 60)
pi_stat_meteo = R_Stationnaire(P_meteo)
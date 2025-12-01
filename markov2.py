def Msim(i, P, n):
    """
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
    
    print(f"π(0) = {pi}")
    
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


def R_Stationnaire(P, epsilon=1e-10, max_iter=1000):
    """
    Trouve le régime stationnaire π tel que π = πP
    
    Paramètres:
    -----------
    P : list of list - Matrice de transition
    epsilon : float - Précision pour la convergence
    max_iter : int - Nombre maximum d'itérations
    
    Retourne:
    ---------
    pi : list ou None - Distribution stationnaire si elle existe
    """
    nb_etats = len(P)
    
    # Vérification matrice stochastique
    for i in range(nb_etats):
        somme = sum(P[i])
        if abs(somme - 1.0) > epsilon:
            print(f"Erreur: La ligne {i} ne somme pas à 1 (somme = {somme})")
            return None
    
    # Initialisation uniforme
    pi = [1.0 / nb_etats] * nb_etats
    
    print("\nRecherche du régime stationnaire...")
    print(f"π initial = {[round(p, 6) for p in pi]}")
    
    # Itération jusqu'à convergence
    for iteration in range(max_iter):
        pi_nouveau = [0.0] * nb_etats
        
        # Calcul de π * P
        for j in range(nb_etats):
            for i in range(nb_etats):
                pi_nouveau[j] += pi[i] * P[i][j]
        
        # Vérification convergence
        distance = sum(abs(pi_nouveau[i] - pi[i]) for i in range(nb_etats))
        
        if distance < epsilon:
            print(f"\nConvergence atteinte après {iteration + 1} itérations")
            print(f"π stationnaire = {[round(p, 6) for p in pi_nouveau]}")
            print(f"Somme = {round(sum(pi_nouveau), 6)}")
            return pi_nouveau
        
        pi = pi_nouveau
        
        if (iteration + 1) % 100 == 0:
            print(f"Itération {iteration + 1}: distance = {distance:.10f}")
    
    print(f"\nPas de convergence après {max_iter} itérations")
    return None


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

if pi_stat:
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

if pi_stat_erg:
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
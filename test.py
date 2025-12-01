def Msim(i,P,n):

    nombre_etat = len(P)
    pi = [0] * nombre_etat
    pi[i] = 1

    for etap in range(n):
        pi = [sum(pi[k] * P[k][j] for k in range(nombre_etat)) for j in range(nombre_etat)]
    return pi


def R_Stationnaire(P, epsilon=1e-8, max_iter=1000):
    nombre_etat = len(P)
    pi = [1 / nombre_etat] * nombre_etat

    for _ in range(max_iter):
        pi_next = [sum(pi[i] * P[i][j] for i in range(nombre_etat)) for j in range(nombre_etat)]

        s = sum(pi_next)
        pi_next = [x / s for x in pi_next]

        if sum(abs(pi_next[i] - pi[i]) for i in range(nombre_etat)) < epsilon:
            return pi_next

        pi = pi_next

    return pi
def simuler_trajectoire(i, P, n):
    """Simule une trajectoire de n étapes."""
    etat = i
    chemin = [etat]

    for _ in range(n):
        r = random.random()
        cum = 0
        for j, p in enumerate(P[etat]):
            cum += p
            if r <= cum:
                etat = j
                break
        chemin.append(etat)

    return chemin
if __name__ == "__main__":
    P = [
        [0.7, 0.2, 0.1],
        [0.3, 0.4, 0.3],
        [0.2, 0.3, 0.5]
    ]

    print("=== Chaînes de Markov ===")

    # 1. Évolution de π(n)
    print("\nSimulation à partir de l'état 0:")
    pi_10 = Msim(0, P, 10)
    print(f"Distribution après 10 étapes: {[round(p, 6) for p
    in pi_10]}")                
    pi_20 = Msim(0, P, 20)
    print(f"Distribution après 20 étapes: {[round(p, 6) for p
    in pi_20]}")
    # 2. Distribution stationnaire
    pi_stat = R_Stationnaire(P)
    if pi_stat:
        print(f"\nDistribution stationnaire π = {[round(p, 6) for p in pi_stat]}")
        print(f"Somme = {round(sum(pi_stat), 6)}")
    # 3. Simulation de trajectoire
    print("\nSimulation d'une trajectoire de 15 étapes à partir de l'état0:")    
    trajectoire = simuler_trajectoire(0, P, 15)
    print(f"Trajectoire: {trajectoire}")        
    
def R_Stationnaire(P, epsilon=1e-8, max_iter=1000):
    """Calcule la distribution stationnaire π telle que π*P = π."""
    nb_etats = len(P)
    pi = [1 / nb_etats] * nb_etats

    for iteration in range(max_iter):
        pi_nouveau = [sum(pi[i] * P[i][j] for i in range(nb_etats)) for j in range(nb_etats)]

        # Normalisation
        s = sum(pi_nouveau)
        pi_nouveau = [x / s for x in pi_nouveau]


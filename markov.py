import random

# Simule une trajectoire de la chaîne de Markov (version avec des noms clairs)
def simulate_markov_chain(P, start_state, num_steps):
    state = start_state
    path = [state]
    for _ in range(num_steps):
        # Choisit l'état suivant en fonction des probabilités de la matrice P
        state = random.choices(range(len(P)), weights=P[state])[0]
        path.append(state)
    return path

# Calcule le régime stationnaire (version avec des noms clairs)
def calculate_stationary_distribution(P, tolerance=1e-8, max_iter=1000):
    n = len(P)
    # Commence avec une distribution de probabilité uniforme
    pi = [1.0 / n] * n

    for _ in range(max_iter):
        # Calcule les probabilités pour la prochaine étape
        # Utilise une "list comprehension" pour un code plus concis
        pi_next = [sum(pi[i] * P[i][j] for i in range(n)) for j in range(n)]

        # Normalise le vecteur pour s'assurer que la somme des probabilités est 1
        total = sum(pi_next)
        pi_next = [x / total for x in pi_next]

        # Arrête si les probabilités ne changent presque plus
        if sum(abs(pi_next[i] - pi[i]) for i in range(n)) < tolerance:
            break
        pi = pi_next

    return pi

# --- Point d'entrée principal du programme ---
if __name__ == "__main__":
    P = [
        [0.7, 0.2, 0.1],
        [0.3, 0.4, 0.3],
        [0.2, 0.3, 0.5]
    ]

    print("--- Exemple de Chaîne de Markov ---")
    print("Transition Matrix P:")
    for row in P:
        print(row)
    print("-" * 30)

    # 1. Simulation
    initial_state = 0
    steps_to_simulate = 20
    print(f"\n1. Simulation d'un chemin de {steps_to_simulate} étapes, partant de l'état {initial_state}...")
    path = simulate_markov_chain(P=P, start_state=initial_state, num_steps=steps_to_simulate)
    print("   Chemin simulé:", path)

    # 2. Calcul de la distribution stationnaire
    print(f"\n2. Calcul de la distribution stationnaire...")
    stationary_dist = calculate_stationary_distribution(P)
    print("   Distribution stationnaire (pi):", stationary_dist)

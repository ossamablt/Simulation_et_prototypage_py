import random

def Msin(i, P, n):
    """Distribution after n steps starting from state i."""
    s = len(P)
    pi = [0] * s
    pi[i] = 1

    for _ in range(n):
        pi = [sum(pi[k] * P[k][j] for k in range(s)) for j in range(s)]
    return pi


def R_Stationnaire(P, tol=1e-8, max_iter=1000):
    """Stationary distribution pi such that pi*P = pi."""
    n = len(P)
    pi = [1 / n] * n

    for _ in range(max_iter):
        pi_next = [sum(pi[i] * P[i][j] for i in range(n)) for j in range(n)]

        s = sum(pi_next)
        pi_next = [x / s for x in pi_next]

        if sum(abs(pi_next[i] - pi[i]) for i in range(n)) < tol:
            return pi_next

        pi = pi_next

    return pi


def simuler_trajectoire(i, P, n):
    """Simulate a trajectory of n steps."""
    state = i
    path = [state]

    for _ in range(n):
        r = random.random()
        cum = 0
        for j, p in enumerate(P[state]):
            cum += p
            if r <= cum:
                state = j
                break
        path.append(state)

    return path


if __name__ == "__main__":
    P = [
        [0.7, 0.2, 0.1],
        [0.3, 0.4, 0.3],
        [0.2, 0.3, 0.5]
    ]

    print("=== Markov Chains ===")

    # 1. Evolution of pi(n)
    print("\n1. Distributions pi(n) from initial state 0:")
    for n in [1, 2, 3, 4, 5, 10, 20]:
        print(f"  pi({n}) =", [round(x, 4) for x in Msin(0, P, n)])

    # 2. Stationary distribution
    print("\n2. Stationary distribution:")
    pi_star = R_Stationnaire(P)
    print("  pi* =", [round(x, 6) for x in pi_star])

    # Verification pi*P = pi*
    verif = [
        sum(pi_star[i] * P[i][j] for i in range(len(P)))
        for j in range(len(P))
    ]
    print("  pi*P =", [round(x, 6) for x in verif])

    # 3. Simulation
    print("\n3. Simulated trajectory (20 steps):")
    print("  ", simuler_trajectoire(0, P, 20))

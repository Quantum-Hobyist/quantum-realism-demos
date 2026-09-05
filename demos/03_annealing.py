import numpy as np
from itertools import permutations

# Problem: 5 Häfen
n = 5
d = np.array([
    [0, 2, 3, 5, 4],
    [2, 0, 4, 1, 6],
    [3, 4, 0, 7, 2],
    [5, 1, 7, 0, 3],
    [4, 6, 2, 3, 0]
])
A = 20.0
B = 1.0
N = n * n
Q = np.zeros((N, N))

def idx(i, t):
    return i * n + t

for t in range(n):
    t_next = (t + 1) % n
    for i in range(n):
        for j in range(n):
            if i != j:
                Q[idx(i, t), idx(j, t_next)] += B * d[i][j]
for i in range(n):
    for t1 in range(n):
        Q[idx(i, t1), idx(i, t1)] += A * (-1)
        for t2 in range(n):
            if t1 != t2:
                Q[idx(i, t1), idx(i, t2)] += A * 1
for t in range(n):
    for i1 in range(n):
        Q[idx(i1, t), idx(i1, t)] += A * (-1)
        for i2 in range(n):
            if i1 != i2:
                Q[idx(i1, t), idx(i2, t)] += A * 1

def qubo_energy(bits):
    x = np.array(bits)
    return x @ Q @ x

# Referenz: beste der 120 gültigen Routen
def route_to_bits(route):
    bits = np.zeros(N, dtype=int)
    for position, hafen in enumerate(route):
        bits[idx(hafen, position)] = 1
    return bits

best_energy, best_route = float('inf'), None
for route in permutations(range(n)):
    e = qubo_energy(route_to_bits(route))
    if e < best_energy:
        best_energy, best_route = e, route
print("Referenz (beste der 120 gültigen Routen):")
print("  Route:", best_route, " Energie =", best_energy)

def simulated_anneal(steps, T_start=10.0, T_end=0.01):
    state = np.random.randint(0, 2, N)
    energy = qubo_energy(state)
    temps = np.geomspace(T_start, T_end, steps)
    for T in temps:
        i = np.random.randint(N)
        candidate = state.copy()
        candidate[i] = 1 - candidate[i]
        cand_energy = qubo_energy(candidate)
        delta = cand_energy - energy
        if delta < 0 or np.random.random() < np.exp(-delta / T):
            state, energy = candidate, cand_energy
    return state, energy

def is_valid(state):
    m = np.array(state).reshape(n, n)
    return np.array_equal(m.sum(0), np.ones(n)) and \
           np.array_equal(m.sum(1), np.ones(n))

print("\n--- LANGSAM (20000 Schritte), 5 Laeufe ---")
for run in range(5):
    state, energy = simulated_anneal(steps=20000)
    print(f"  Lauf {run+1}:  Energie={energy:7.1f}  gueltige Route={is_valid(state)}")

print("\n--- SCHNELL (50 Schritte), 5 Laeufe ---")
for run in range(5):
    state, energy = simulated_anneal(steps=50)
    print(f"  Lauf {run+1}:  Energie={energy:7.1f}  gueltige Route={is_valid(state)}")
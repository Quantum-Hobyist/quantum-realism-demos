import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit_aer import AerSimulator
from itertools import product

# ============================================================
# 1. PROBLEMDEFINITION: 3 Häfen
# ============================================================
n = 3  # Anzahl Häfen
# Distanzmatrix (symmetrisch): d[i][j] = Distanz Hafen i -> Hafen j
d = np.array([
    [0, 2, 3],
    [2, 0, 4],
    [3, 4, 0]
])

A = 10.0   # Penalty-Gewicht für Constraints
B = 1.0    # Gewicht für Kostenterm

# ============================================================
# 2. QUBO AUFBAUEN
# ============================================================
# Variable x[i,t]: Hafen i an Position t. Index = i*n + t
N = n * n  # 9 Qubits

Q = np.zeros((N, N))

def idx(i, t):
    return i * n + t

# --- Kostenterm: aufeinanderfolgende Positionen ---
for t in range(n):
    t_next = (t + 1) % n          # Rundreise: nach letzter Position zurück zu erster
    for i in range(n):
        for j in range(n):
            if i != j:
                Q[idx(i, t), idx(j, t_next)] += B * d[i][j]

# --- Zeilen-Constraint: jeder Hafen genau einmal ---
for i in range(n):
    for t1 in range(n):
        Q[idx(i, t1), idx(i, t1)] += A * (-1)   # linearer Anteil aus (Σ-1)²
        for t2 in range(n):
            if t1 != t2:
                Q[idx(i, t1), idx(i, t2)] += A * 1

# --- Spalten-Constraint: jede Position genau einmal ---
for t in range(n):
    for i1 in range(n):
        Q[idx(i1, t), idx(i1, t)] += A * (-1)
        for i2 in range(n):
            if i1 != i2:
                Q[idx(i1, t), idx(i2, t)] += A * 1

# ============================================================
# 3. BRUTE-FORCE-REFERENZ (klassisch, zum Vergleich)
# ============================================================
def qubo_energy(bits):
    x = np.array(bits)
    return x @ Q @ x

best_energy = float('inf')
best_bits = None
for bits in product([0, 1], repeat=N):
    e = qubo_energy(bits)
    if e < best_energy:
        best_energy = e
        best_bits = bits

print("Beste klassische Lösung (Brute Force):")
print("  Bits:", best_bits)
print("  Energie:", best_energy)

# Bits als Matrix darstellen (Zeile=Hafen, Spalte=Position)
matrix = np.array(best_bits).reshape(n, n)
print("  Routen-Matrix (Zeile=Hafen, Spalte=Position):")
print(matrix)

# ============================================================
# 4. QAOA
# ============================================================
gamma = Parameter('γ')
beta = Parameter('β')

qc = QuantumCircuit(N)
qc.h(range(N))  # Start: Superposition über alle Zustände

# --- Cost-Layer: e^{-i γ H_C} ---
for i in range(N):
    for j in range(N):
        if Q[i][j] != 0:
            if i == j:
                qc.rz(2 * gamma * Q[i][j], i)
            else:
                qc.rzz(2 * gamma * Q[i][j], i, j)

# --- Mixer-Layer: e^{-i β H_M} ---
for i in range(N):
    qc.rx(2 * beta, i)

qc.measure_all()

# --- Ausführung mit festen Parametern (didaktisch, kein Training) ---
sim = AerSimulator()
bound = qc.assign_parameters({gamma: 0.1, beta: 0.3})
result = sim.run(bound, shots=2048).result()
counts = result.get_counts()

# Top 5 Ergebnisse
top = sorted(counts.items(), key=lambda x: -x[1])[:5]
print("\nTop 5 QAOA-Messungen:")
for bitstring, count in top:
    bits = [int(b) for b in bitstring[::-1]]  # Qiskit-Reihenfolge umdrehen
    e = qubo_energy(bits)
    print(f"  {bitstring}  count={count:4d}  energie={e:.1f}")

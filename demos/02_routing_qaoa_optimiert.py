import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit_aer import AerSimulator
from itertools import product
from scipy.optimize import minimize

# Problem: 3 Häfen
n = 3
d = np.array([[0, 2, 3], [2, 0, 4], [3, 4, 0]])
A = 10.0
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

# Brute-Force-Referenz
best_energy, best_bits = float('inf'), None
for bits in product([0, 1], repeat=N):
    e = qubo_energy(bits)
    if e < best_energy:
        best_energy, best_bits = e, bits
print("Brute-Force-Referenz:  Energie =", best_energy)
print("  Matrix:\n", np.array(best_bits).reshape(n, n))

# QAOA-Schaltkreis als Funktion
def build_circuit(gamma_val, beta_val):
    qc = QuantumCircuit(N)
    qc.h(range(N))
    for i in range(N):
        for j in range(N):
            if Q[i][j] != 0:
                if i == j:
                    qc.rz(2 * gamma_val * Q[i][j], i)
                else:
                    qc.rzz(2 * gamma_val * Q[i][j], i, j)
    for i in range(N):
        qc.rx(2 * beta_val, i)
    qc.measure_all()
    return qc

sim = AerSimulator()

def expected_energy(params):
    gamma_val, beta_val = params
    qc = build_circuit(gamma_val, beta_val)
    counts = sim.run(qc, shots=512).result().get_counts()
    total, shots = 0, 0
    for bitstring, count in counts.items():
        bits = [int(b) for b in bitstring[::-1]]
        total += qubo_energy(bits) * count
        shots += count
    return total / shots

history = []
def callback(params):
    e = expected_energy(params)
    history.append(e)
    print(f"  Schritt {len(history):2d}:  gamma={params[0]:+.3f}  beta={params[1]:+.3f}  <E>={e:7.2f}")

start = [0.1, 0.3]
print("\nStart-Durchschnittsenergie:", round(expected_energy(start), 2))
print("Optimierung laeuft:")
result = minimize(expected_energy, start, method='COBYLA', callback=callback, options={'maxiter': 40})
print("\nOptimierte Parameter:  gamma =", round(result.x[0], 3), " beta =", round(result.x[1], 3))

qc_final = build_circuit(result.x[0], result.x[1])
counts = sim.run(qc_final, shots=2048).result().get_counts()
top = sorted(counts.items(), key=lambda x: -x[1])[:5]
print("\nTop 5 nach Optimierung:")
for bitstring, count in top:
    bits = [int(b) for b in bitstring[::-1]]
    print(f"  {bitstring}  count={count:4d}  energie={qubo_energy(bits):.1f}")
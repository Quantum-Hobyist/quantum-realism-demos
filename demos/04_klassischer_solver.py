import numpy as np
from itertools import permutations
from ortools.sat.python import cp_model
import time

# Problem: 5 Häfen (identisch zu 03_annealing.py)
n = 5
d = np.array([
    [0, 2, 3, 5, 4],
    [2, 0, 4, 1, 6],
    [3, 4, 0, 7, 2],
    [5, 1, 7, 0, 3],
    [4, 6, 2, 3, 0]
])

model = cp_model.CpModel()
x = {}
for i in range(n):
    for t in range(n):
        x[i, t] = model.NewBoolVar(f"x_{i}_{t}")

# Jeder Hafen genau einmal
for i in range(n):
    model.Add(sum(x[i, t] for t in range(n)) == 1)
# Jede Position genau einmal
for t in range(n):
    model.Add(sum(x[i, t] for i in range(n)) == 1)

# Zielfunktion: Gesamtdistanz der Rundreise
cost_terms = []
for t in range(n):
    t_next = (t + 1) % n
    for i in range(n):
        for j in range(n):
            if i != j:
                pair = model.NewBoolVar(f"pair_{i}_{t}_{j}")
                model.AddBoolAnd([x[i, t], x[j, t_next]]).OnlyEnforceIf(pair)
                model.AddBoolOr([x[i, t].Not(), x[j, t_next].Not()]).OnlyEnforceIf(pair.Not())
                cost_terms.append(d[i][j] * pair)
model.Minimize(sum(cost_terms))

# Zwei Laeufe auf demselben Modell: Der erste Aufruf enthaelt einmalige
# Nebenkosten (Uebersetzung ins C++-Backend, Speicherallokation, Start der
# Worker-Threads). Bei einem Problem dieser Groesse dominieren diese festen
# Kosten die Messung - die eigentliche Suche faellt kaum ins Gewicht. Beide
# Zeiten stehen daher nebeneinander, statt eine davon als "die" Zeit auszugeben.
solver = cp_model.CpSolver()
start = time.perf_counter()
status = solver.Solve(model)
zeit_1 = (time.perf_counter() - start) * 1000

solver = cp_model.CpSolver()
start = time.perf_counter()
status = solver.Solve(model)
zeit_2 = (time.perf_counter() - start) * 1000

print(f"Status: {solver.StatusName(status)}")
print(f"Gefundene Gesamtdistanz: {solver.ObjectiveValue()}")
print(f"Rechenzeit 1. Lauf: {zeit_1:.2f} ms")
print(f"Rechenzeit 2. Lauf: {zeit_2:.2f} ms")

route = [None] * n
for t in range(n):
    for i in range(n):
        if solver.Value(x[i, t]) == 1:
            route[t] = i
print("Optimale Route (Reihenfolge der Häfen):", route)

# Gegenprobe
best_energy, best_route = float('inf'), None
for r in permutations(range(n)):
    dist = sum(d[r[k]][r[(k+1) % n]] for k in range(n))
    if dist < best_energy:
        best_energy, best_route = dist, r
print(f"\nBrute-Force-Gegenprobe: beste Distanz = {best_energy}, Route = {best_route}")
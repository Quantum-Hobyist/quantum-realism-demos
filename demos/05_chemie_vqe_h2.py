import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import StatevectorEstimator

# H2-Hamiltonian (Gleichgewichtsabstand 0.735 A, STO-3G, 2-Qubit-Form).
# Koeffizienten sind publizierte Standardwerte - vor ernsthafter
# Nutzung gegen eine Fachquelle pruefen.
hamiltonian = SparsePauliOp.from_list([
    ("II", -1.052373245772859),
    ("IZ",  0.39793742484318045),
    ("ZI", -0.39793742484318045),
    ("ZZ", -0.01128010425623538),
    ("XX",  0.18093119978423156),
])

print("Anzahl Qubits:", hamiltonian.num_qubits)
print("Anzahl Terme im Hamiltonian:", len(hamiltonian))

numpy_solver = NumPyMinimumEigensolver()
exact_result = numpy_solver.compute_minimum_eigenvalue(hamiltonian)
exact_energy = exact_result.eigenvalue.real
print(f"\nExakte Grundzustandsenergie (klassisch): {exact_energy:.6f} Hartree")

ansatz = TwoLocal(hamiltonian.num_qubits, rotation_blocks="ry",
                  entanglement_blocks="cz", reps=2)
optimizer = COBYLA(maxiter=200)
estimator = StatevectorEstimator()

counts = []
def callback(eval_count, params, value, meta):
    counts.append(eval_count)

vqe = VQE(estimator, ansatz, optimizer, callback=callback)
print("\nVQE laeuft...")
vqe_result = vqe.compute_minimum_eigenvalue(hamiltonian)
vqe_energy = vqe_result.eigenvalue.real

print(f"\nVQE-Grundzustandsenergie: {vqe_energy:.6f} Hartree")
print(f"Exakte Energie:           {exact_energy:.6f} Hartree")
print(f"Differenz:                {abs(vqe_energy - exact_energy):.6f} Hartree")
print(f"Optimizer-Auswertungen:   {len(counts)}")
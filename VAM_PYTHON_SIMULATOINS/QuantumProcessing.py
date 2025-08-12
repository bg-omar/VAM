from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from VAM_PYTHON_SIMULATOINS.secrets import IBM_TOKEN

qc = QuantumCircuit(2, 2)
qc.h(0); qc.cx(0,1); qc.measure([0,1],[0,1])

sim = AerSimulator()
result = sim.run(qc, shots=2000).result()
print(result.get_counts())



from qiskit.quantum_info import Statevector
qc2 = QuantumCircuit(2); qc2.h(0); qc2.cx(0,1)
print(Statevector.from_instruction(qc2))   # shows amplitudes ~1/√2 for |00>,|11|
print(qc2.draw('text'))                    # ASCII diagram


qx = QuantumCircuit(2,2)
qx.h(0); qx.cx(0,1)
qx.h([0,1])              # rotate to X basis
qx.measure([0,1],[0,1])  # still mostly 00 and 11
print(AerSimulator().run(qx, shots=2000).result().get_counts())


from math import pi
def counts_at(phi_a, phi_b, shots=20000):
    qc = QuantumCircuit(2,2)
    qc.h(0); qc.cx(0,1)
    qc.rz(phi_a,0); qc.h(0)     # measure σ_φa
    qc.rz(phi_b,1); qc.h(1)     # measure σ_φb
    qc.measure([0,1],[0,1])
    return AerSimulator().run(qc, shots=shots).result().get_counts()

def E(counts):  # correlation ⟨A·B⟩
    s = sum(counts.values())
    good = counts.get('00',0)+counts.get('11',0)
    bad  = counts.get('01',0)+counts.get('10',0)
    return (good - bad)/s

a, ap = 0, pi/2
b, bp = pi/4, -pi/4
S = abs(E(counts_at(a,b)) + E(counts_at(a,bp))
        + E(counts_at(ap,b)) - E(counts_at(ap,bp)))
print("CHSH S ≈", S)  # ideal ≈ 2.828 on Aer

from qiskit_aer.noise import NoiseModel, depolarizing_error
nm = NoiseModel()
nm.add_all_qubit_quantum_error(depolarizing_error(0.002,1), ['h','rz'])
nm.add_all_qubit_quantum_error(depolarizing_error(0.01,2), ['cx'])
sim_noisy = AerSimulator(noise_model=nm)
result = sim_noisy.run(qc, shots=2000).result()  # qc from your snippet
print(result.get_counts())                        # correlations degrade


from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, Sampler

# QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=IBM_TOKEN)

service = QiskitRuntimeService(channel="ibm_quantum_platform")  # uses saved token
backend = service.least_busy(min_num_qubits=2, simulator=False)

qc = QuantumCircuit(2)
qc.h(0); qc.cx(0,1); qc.measure_all()

with Session(backend=backend) as session:
    sampler = Sampler(options=Options(optimization_level=1))
    job = sampler.run(shots=1024)
    print(job.result().quasi_dists[0])
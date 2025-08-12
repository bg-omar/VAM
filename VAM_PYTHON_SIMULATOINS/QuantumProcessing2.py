from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit import QuantumCircuit

qc = QuantumCircuit(2); qc.h(0); qc.cx(0,1); qc.measure_all()

sampler = AerSampler(default_shots=4096)
job = sampler.run([qc])
counts = job.result()[0].join_data().get_counts()
print(counts)
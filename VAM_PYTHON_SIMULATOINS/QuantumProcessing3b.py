import numpy as np
from math import pi, cos
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit

def E_of_delta(delta, shots=8000):
    a = 0.0; b = a - delta
    qc = QuantumCircuit(2,2)
    qc.h(0); qc.cx(0,1)
    qc.rz(a,0); qc.h(0)
    qc.rz(b,1); qc.h(1)
    qc.measure([0,1],[0,1])
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()
    return (counts.get('00',0)+counts.get('11',0)
            -counts.get('01',0)-counts.get('10',0))/shots

grid = np.linspace(-pi/2, pi/2, 17)
vals = np.array([E_of_delta(d) for d in grid])
fit_err = np.mean((vals + np.cos(2*grid))**2)
print("MSE to -cos(2Δ):", fit_err)
for d,v in zip(grid, vals):
    print(f"Δ={d:+.3f}  E≈{v:+.4f}  target={-cos(2*d):+.4f}")
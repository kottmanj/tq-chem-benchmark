# script copied from
# https://docs.pennylane.ai/en/stable/code/api/pennylane.kUpCCGSD.html
# modifications:
# - extended to multiple H atoms
# - allow different devices
# - adapted conv_tol to 1.e-5 (from 1.e-6)
# times serve as baseline representing a state-of-the-art library that is actively developed and maintained

import pennylane as qml
from pennylane import numpy as np
import time
import sys
for n_atoms in [2,4,6,8]:
    start=time.time()
    # Build the electronic Hamiltonian
    device = 'default.qubit' #'lightning.qubit' 'qulacs.simulator'
    symbols = ["H"]*n_atoms
    electrons = n_atoms
    coordinates = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.5, 0.0, 0.0, 3.0, 0.0, 0.0, 4.5, 0.0, 0.0, 6.0, 0.0, 0.0, 7.5, 0.0, 0.0, 9.0, 0.0, 0.0, 10.5])[:3*n_atoms]
    H, qubits = qml.qchem.molecular_hamiltonian(symbols, coordinates)
    print("qubits=", qubits) 
    # Define the Hartree-Fock state
    ref_state = qml.qchem.hf_state(electrons, qubits)
    
    # Define the device
    dev = qml.device(device, wires=qubits)
    
    # Define the ansatz
    @qml.qnode(dev)
    def ansatz(weights):
        qml.kUpCCGSD(weights, wires=[i for i in range(qubits)],
                        k=1, delta_sz=0, init_state=ref_state)
        return qml.expval(H)
    # Get the shape of the weights for this template
    layers = 1
    shape = qml.kUpCCGSD.shape(k=layers,
                        n_wires=qubits, delta_sz=0)
   
    # Initialize the weight tensors
    np.random.seed(24)
    weights = np.random.random(size=shape)
    # converges better in this case
    weights *=0.0

    # Define the optimizer
    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    
    # Store the values of the cost function
    energy = [ansatz(weights)]
    
    # Store the values of the circuit weights
    angle = [weights]
    max_iterations = 100
    conv_tol = 1e-05
    for n in range(max_iterations):
        weights, prev_energy = opt.step_and_cost(ansatz, weights)
        energy.append(ansatz(weights))
        angle.append(weights)
        conv = np.abs(energy[-1] - prev_energy)
        print(f"Step = {n},  Energy = {energy[-1]:.8f} Ha")
        print("so far: ", time.time()-start)
        if conv <= conv_tol:
            break
    
    print("\n" f"Final value of the ground-state energy = {energy[-1]:.8f} Ha")
    end=time.time()
    print(n_atoms, "=", end-start)
    sys.stdout.flush()

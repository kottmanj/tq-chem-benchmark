import pennylane as qml
import tequila as tq
import time
import scipy
import qiskit
import copy
from numpy import pi

for n in [10,11]:
    n=n*2
    start = time.time()
    d = 1.5
    geometry = ""
    for i in range(n):
        geometry+= "H 0.0 0.0 {}\n".format(i*d)
    # PL will not do automatic mapping of hamiltonian
    # we switch to this encoding where no unused qubits will be present
    # this avoids manual "wireing" further down
    # with regular JW only the even qubits are touched by the circuit
    mol = tq.Molecule(geometry=geometry, transformation="ReorderedJordanWigner")
    H = mol.make_hardcore_boson_hamiltonian()
    U = mol.make_ansatz(name="HCB-SPA")

    #used to ensure same behaviour of optimizers
    #tq.minimize(tq.ExpectationValue(H=H, U=U))    
    
    # import Hamiltonian to pennnylane 
    Hpl = qml.import_operator(H.to_openfermion())
    
    # export circuit to qiskit
    Uc = tq.compile(U, backend="qiskit").circuit
    old_param = Uc.parameters
    # we need to rename the parameters (issues with sympy in pennylane-qiskit converter)
    param = [qiskit.circuit.Parameter("X{}".format(i)) for i in range(len(old_param))]
    Uc = Uc.assign_parameters({old_param[i]:param[i] for i in range(len(old_param))})
    
    # import the circuit to pennylane
    my_circuit = qml.load(Uc, format='qiskit')

    # form the ansatz
    dev = qml.device("default.qubit", wires=H.n_qubits)
    @qml.qnode(dev)
    def ansatz(weights):
        my_circuit({param[i]:weights[i] for i in range(len(old_param))},wires=[i for i in range(H.n_qubits)])
        return qml.expval(Hpl)

    # unfortunately can't do analytical gradient here
    # might work somehow, but don't know how
    # will emulate shift-rule by setting the finite-diff stencil accordingly
    # numerical gradient will then be the same as analytical one by a factor of 2
    # should result in approximately the same behaviour
    # trick only works for SPA circuits as they are Ry + CNOT only
    def df(x):
        result = []
        for i in range(len(x)):
            xp = copy.deepcopy(x)
            xp[i]+=pi/2
            tmp = ansatz(xp)
            xp[i]-=pi
            tmp -= ansatz(xp)
            result.append(0.5*tmp)
        return result

    x0 = [0.0]*len(old_param)
    asd = scipy.optimize.minimize(ansatz,x0=x0,method="bfgs",jac=df)
    end = time.time()
    print("H{} finished in {}s".format(n,end-start))

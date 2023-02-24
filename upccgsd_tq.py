import tequila as tq
import time

for n in [2,4,6,8]:
    start = time.time()
    d = 1.5
    geometry = ""
    for i in range(n):
        geometry+= "H 0.0 0.0 {}\n".format(i*d)
    mol = tq.Molecule(geometry=geometry, basis_set="sto-3g")
    H = mol.make_hamiltonian()
    U = mol.make_ansatz(name="UpCCGSD")
    E = tq.ExpectationValue(H=H, U=U)
    
    result = tq.minimize(E, silent=True)
    print(result.energy)
    end = time.time()
    print("H{} finished in {}s".format(n,end-start))

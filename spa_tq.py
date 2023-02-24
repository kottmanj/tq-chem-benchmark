import tequila as tq
import time

for n in range(1,11):
    n = 2*n
    start = time.time()
    d = 1.5
    geometry = ""
    for i in range(n):
        geometry+= "H 0.0 0.0 {}\n".format(i*d)
    mol = tq.Molecule(geometry=geometry)
    H = mol.make_hardcore_boson_hamiltonian()
    U = mol.make_ansatz(name="HCB-SPA")
    E = tq.ExpectationValue(H=H, U=U)
    
    result = tq.minimize(E, silent=True)
    end = time.time()
    print("H{} finished in {}s".format(n,end-start))

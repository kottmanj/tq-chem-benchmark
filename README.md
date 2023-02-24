A small benchmark showcasing an out-of-the-box VQE with methods implemented in [tequila](https://github.com/tequilahub/tequila).  
Timings from Intel(R) Xeon(R) W-2135 CPU @ 3.70GHz with Ubuntu.  

The fictive scenario is: I want to run an electronic VQE, how far do I get without manually tweaking code or parameters.  

<img src="benchmark.png" width=500>

## Note on the methods  

### SPA/MRA-PNO and UpCCGSD/MRA-PNO
- computed with [spa_tq.py](script_spa.py)  
- code taken from examples in [arxiv:2105.03836](https://arxiv.org/abs/2105.03836)  
- SPA/MRA-PNO uses HCB encoding (leads to identical energy but saves qubit and measurement resources)  
- Factorized form of SPA is not exploited in implementation (exponential bottleneck of full qubit simulation kicks in after 18 electrons)  
- uses MRA-PNOs via the madness interface (described in [arxiv:2008.02819](https://arxiv.org/abs/2008.02819)). In the beginning the increased runtime (compated to UpCCGSD/STO-3G) is due to the orbital determination.  
- install madness interface with `conda install madtequila -c kottmann` (only linux)  
- qubit count: UpCCGSD qubits=2x(N-Electrons), SPA qubits=N-Electrons  

### UpCCGSD/STO-3G
- computed with [upccgsd_tq.py](script_upccgsd.py)  
- described in [arxiv:2105.03836](https://arxiv.org/abs/2105.03836)  
- qubit count: qubits=2x(N-Electrons)

### UpCCGSD/STO-3G (Pennylane)
Pennylane timings (see [pl.py](pl.py)) are included as a representative for state-of-the-art code with industry standard.  
The code is taken from the [documentation](https://docs.pennylane.ai/en/stable/code/api/pennylane.kUpCCGSD.html) and only modified slightly to allow for different molecules and devices. `device=default.qubit` was here the default and is also the fastest for the task (others are included to see that `qulacs` is not always fastest in all packages).    

Possible way to speed-up the walltime:  
- Use the same optimizer as in the tq defaults (scipy implementation of BFGS with default values)  
- Exploit MRA-PNOs and SPA ansatz from [spa_tq.py](spa_tq.py) (can be imported from tequila)

```python
# convert tequila hamiltonian to pennylane hamiltonian
H_pl = H.to_openfermion()
UX = tq.compile(U, backend="qiskit").circuit
U_pl = qml.load(UX, format='qiskit')
```

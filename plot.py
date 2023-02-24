import matplotlib.pyplot as plt

time={}
time[2]=6.894924640655518
time[4]=15.806959867477417
time[6]=30.05142831802368
time[8]=47.97708439826965
time[10]=75.00666880607605
time[12]=101.60225510597229
time[14]=146.99105739593506
time[16]=181.02004861831665
time[18]=245.3044307231903
time[20]=689.9615657329559
time[22]=2212.8264150619507
plt.plot(list(time.keys()),list(time.values()), label="SPA/MRA-PNO (tequila-qulacs)", marker="o", color="forestgreen")

time={}
time[2]=6.4
time[4]=17.9
time[6]=57.03
time[8]=456

plt.plot(list(time.keys()),list(time.values()), label="UpCCGSD/MRA-PNO (tequila-qulacs)", marker="o", color="tab:red")

time={}
time[2]=0.47736144065856934
time[4]=2.937643051147461
time[6]=54.78564476966858
time[8]=865.6871042251587
plt.plot(list(time.keys()),list(time.values()), label="UpCCGSD/STO-3G (tequila-qulacs)", marker="o", color="navy")


# pennylane with qulacs (12 threads)
time={}
time[2]=62.33531093597412

plt.plot(list(time.keys()),list(time.values()), label="UpCCGSD/STO-3G (Pennylane-qulacs.simulator)", marker="x", color="tab:orange", linestyle="dashed")

# pennylane with lightning (12 threads?)
time={}
time[2]=1.49
time[4]=241.3956272602081

plt.plot(list(time.keys()),list(time.values()), label="UpCCGSD/STO-3G (Pennylane-lightning.qubit)", marker="x", color="purple", linestyle="dashed")

# pennylane with default.qubit
time={}
time[2]=0.9652109146118164
time[4]=12.165194749832153
time[6]=111.2861869335174
time[8]=3036.0 # aborted since it looks converged

plt.plot(list(time.keys()),list(time.values()), label="UpCCGSD/STO-3G (Pennylane-default.qubit)", marker="x", linestyle="dashed", color="tab:blue")

plt.xticks([2,4,6,8,10,12,14,16,18,20,22])
plt.yscale("log")
plt.ylabel("walltime/s")
plt.xlabel("number of electrons")
plt.legend(loc="lower right")
plt.savefig("benchmark.png")
plt.show()

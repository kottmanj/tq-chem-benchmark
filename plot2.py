import matplotlib.pyplot as plt

time={}
time[2]= 0.38211846351623535
time[4]= 1.8320884704589844
time[6]= 31.665756702423096
time[8]= 555.1905162334442
plt.plot(list(time.keys()),list(time.values()), label="UpCCGSD/STO-3G (tequila-qulacs) nojax", marker="o", color="tab:red")

time={}
time[2]=0.47736144065856934
time[4]=2.937643051147461
time[6]=54.78564476966858
time[8]=865.6871042251587
plt.plot(list(time.keys()),list(time.values()), label="UpCCGSD/STO-3G (tequila-qulacs)", marker="o", color="navy")

plt.yscale("log")
plt.ylabel("walltime/s")
plt.xlabel("number of electrons")
plt.legend(loc="lower right")
plt.savefig("benchmark2.png")
plt.show()

import numpy as np
import matplotlib.pyplot as plt
data = np.loadtxt("frenkel_ladd_squares_dense_sampling_vlarge.out",skiprows=1)
data2 = np.loadtxt("frenkel_ladd_triangles_dense_sampling_vlarge.out",skiprows=1)
lattice_E = data[500::100,3]
sk =data[500::100,2]
x = sk
y= lattice_E/sk
integral=np.trapz(y = y,x = x)
print("Squares free energy:",integral)
plt.plot(x,y,'*')
plt.plot(x,y,'--')
plt.show()

lattice_E = data2[500::100,3]
sk = data2[500::100,2]
x = sk
y= lattice_E/sk
integral=np.trapz(y = y,x = x)
print("Triangles free energy:",integral)
plt.plot(x,y,'*')
plt.plot(x,y,'--')
plt.show()

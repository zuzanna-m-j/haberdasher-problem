import numpy as np
import matplotlib.pyplot as plt
datat = np.loadtxt("frenkel_ladd_squares_dense_sampling_vlarge.out",skiprows=1)
datas = np.loadtxt("frenkel_ladd_triangles_dense_sampling_vlarge.out",skiprows=1)
datap = np.loadtxt("frenkel_ladd_triangles_dense_sampling_vlarge.out",skiprows=1)

lattice_E = datat[500::100,3]
sk =datat[500::100,2]
x = sk
y= lattice_E/sk
integral=np.trapz(y = y,x = x)
print("Triangles free energy:",integral)
plt.plot(x,y,'*')
plt.plot(x,y,'--')
plt.show()

lattice_E = datap[500::100,3]
sk =datap[500::100,2]
x = sk
y= lattice_E/sk
integral=np.trapz(y = y,x = x)
print("Pentagon free energy:",integral)
plt.plot(x,y,'*')
plt.plot(x,y,'--')
plt.show()

lattice_E = datas[500::100,3]
sk = datas[500::100,2]
x = sk
y= lattice_E/sk
integral=np.trapz(y = y,x = x)
print("Squares free energy:",integral)
plt.plot(x,y,'*')
plt.plot(x,y,'--')
plt.show()

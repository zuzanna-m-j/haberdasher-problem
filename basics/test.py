import numpy as np

with open('pos.npy', 'rb') as f:
    a = np.load(f)
print(a)
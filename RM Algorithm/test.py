import numpy as np


# pattern periodicity
p = 10
a = np.array([1]+[0]*(p-1))
b = np.tile(a,3)

print(b)
import numpy as np

Ny = 10; Nx = 10

y,x = np.meshgrid(range(Ny),range(Nx))
arr = np.multiply(y,x)

choices = np.array([arr]*5)

newvals = np.array(range(5))

choices[:,0,0] = newvals[:]

print(choices)
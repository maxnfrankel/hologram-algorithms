import cmath
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from PtArrayModule import PtArrayCoords
from analyzeSimModule import perf

# SLM array dimensions in pixels
Nx = 768
Ny = 768

# create array for indexing
x,y = np.meshgrid(range(Nx),range(Ny))

# create trap plane with same dimensions as SLM
trap_plane = np.zeros((Ny,Nx),dtype = float)

# get trap indices
npx = 10 # number of pts in x direction
npy = 10 # number of pts in y direction
px = 70 # x periodicity
py = 70 # y periodicity
xm,ym = PtArrayCoords(npx,npy,px,py)

# send light at trap locations
trap_plane[ym.astype(int),xm.astype(int)] = 1.0

plt.imshow(trap_plane)
plt.title('Target')
plt.show()

# create the SLM plane
slm_phase = np.empty((Ny,Nx), dtype=float)

# choose random number from 0 to n_traps-1 for each slm pixel
n_traps = npx*npy
random_num = np.random.randint(n_traps,size=(Ny,Nx))

plt.imshow(random_num)
plt.title('SLM plane, trap # which each pixel corresponds to')
plt.show()

# set phi_j in each slm pixel
xjxm = np.multiply(x,xm[random_num])/Nx
yjym = np.multiply(y,ym[random_num])/Ny

slm_phase = 2*cmath.pi*(np.add(xjxm,yjym))

slm = np.exp(1j*slm_phase)

ft = fft.fft2((slm))

plt.imshow(abs(ft))
plt.title('Result')
plt.colorbar()
plt.show()

print(perf(xm,ym,abs(ft)))
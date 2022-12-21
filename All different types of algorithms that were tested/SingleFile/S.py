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
trap_plane = np.zeros((Ny,Nx), dtype=complex)

# get trap indices
npx = 10 # number of pts in x direction
npy = 10 # number of pts in y direction
px = 70 # x periodicity
py = 70 # y periodicity
xm,ym = PtArrayCoords(npx,npy,px,py)

# send light at trap locations
trap_plane[ym,xm] = 1.0

plt.imshow(fft.fftshift(abs(trap_plane)))
plt.title('Target')
plt.show()

# initialize slm phase
slm_phase = np.angle(fft.ifft2(trap_plane))

# create slm field
slm = np.exp(1j*slm_phase)

ft = fft.fft2((slm))

plt.imshow(fft.fftshift(abs(ft)))
plt.title('Result')
plt.colorbar()
plt.show()

print(perf(xm,ym,abs(ft)))
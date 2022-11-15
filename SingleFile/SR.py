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

# get trap indices
npx = 10 # number of pts in x direction
npy = 10 # number of pts in y direction
px = 70 # x periodicity
py = 70 # y periodicity
xm,ym = PtArrayCoords(npx,npy,px,py)

# create a random phase for each trap
theta_m = np.random.uniform(-cmath.pi,cmath.pi,size=xm.size)

# create trap plane with same dimensions as SLM
trap_plane = np.zeros((Ny,Nx), dtype=complex)

# send light at trap locations with phase from theta_m
trap_plane[ym,xm] = np.exp(1j*theta_m)

plt.imshow(fft.fftshift(abs(trap_plane)))
plt.title('Target')
plt.show()

# calculate slm phase
slm_phase = np.angle(fft.ifft2(trap_plane))

# create slm field
slm = np.exp(1j*slm_phase)

ft = fft.fft2((slm))

plt.imshow(fft.fftshift(abs(ft)))
plt.title('Result')
plt.colorbar()
plt.show()

print(perf(xm,ym,abs(ft)))
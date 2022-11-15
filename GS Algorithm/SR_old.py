import cmath
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from PtArrayModule import PtArrayCoords
from analyzeSimModule import perf

# SLM array dimensions in pixels
Nx = 768
Ny = 768

# create trap plane with same dimensions as SLM
trap_plane = np.zeros((Ny,Nx),dtype = float)

# get trap indices
npx = 10 # number of pts in x direction
npy = 10 # number of pts in y direction
px = 70 # x periodicity
py = 70 # y periodicity
xm,ym = PtArrayCoords(npx,npy,px,py)

# for each trap, there is a random theta_m corresponding to the trap's phase
theta_m = np.random.uniform(-cmath.pi,cmath.pi,size=xm.size)

# send light at trap locations
trap_plane[ym.astype(int),xm.astype(int)] = 1.0

plt.imshow(fft.fftshift(trap_plane))
plt.title('Target')
plt.show()

# initialize slm phase
slm_phase = np.zeros((Ny,Nx),dtype=float) 

# calculate sum of all e^(i*delta_j^m+theta_m))
for xj in range(Nx):
    for yj in range(Ny):
        
        # calculate delta_j^m, the phase accumulated traveling to each trap
        xjxm = np.multiply(xj,xm)/Nx
        yjym = np.multiply(yj,ym)/Ny
        
        delta_j_m = 2*cmath.pi*np.add(xjxm,yjym) # delta_j_m is a 1D array with length equal to number of traps, M. Indexed by m

        # e^i(delta_j^m+theta_m), to be summed over m
        # this is like the contribution from a single trap propagated back to the SLM pixel
        trap_contribution = np.exp(1j*np.add(delta_j_m,theta_m))

        # calculate phi_j and set slm[yj,xj] equal to it
        slm_phase[yj,xj] = np.angle(np.sum(trap_contribution))

    print(xj)


# create slm field
slm = np.exp(1j*slm_phase)

ft = fft.fft2((slm))

plt.imshow(fft.fftshift(abs(ft)))
plt.title('Result')
plt.colorbar()
plt.show()

print(perf(xm,ym,abs(ft)))
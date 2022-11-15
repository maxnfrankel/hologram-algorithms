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

# raise an error if npx*px or npy*py is odd, as this would make npx*px/2 fall on a non-integer coordinate
lenx = npx*px; leny = npy*py
if (lenx%2 == 1) | (leny%2 == 1):
    raise ValueError("Make sure that px*npx and py*npy are both even.")

# for each trap, there is a random theta_m corresponding to the trap's phase
theta_m = np.random.uniform(-cmath.pi,cmath.pi,size=xm.size)

# send light at trap locations
trap_plane[ym.astype(int),xm.astype(int)] = 1.0

plt.imshow(fft.fftshift(trap_plane))
plt.title('Target')
plt.show()

# initialize slm phase
slm_phase = np.zeros((Ny,Nx),dtype=float) 

# create 3D matrix for indexing delta_j^m, where j has two coords xj,yj, and m is 1D
yj,m,xj = np.meshgrid(range(Ny),range(xm.size),range(Nx))

# calculate delta_j^m
# xj,yj are 3D arrays where only the x,y coord is indexed, respectively
# m is a 3D array where each 2D slice in z corresponds to a different trap number
# thus, xm[m] is a 3D array where each slice in z is all the same value, x[m]. ym[m] is similar
# this is just used to speed up calculation so we don't need to do a for loop over every xj and yj to repeat calculation
# for loop method took 23 seconds to calculate, this method took 8s
xjxm = np.multiply(xj,xm[m])/Nx
yjym = np.multiply(yj,ym[m])/Ny

delta_j_m_addtheta = np.add(2.0*cmath.pi*np.add( xjxm, yjym ) , theta_m[m])

# calculate exp(i(delta_j_m + theta_m)), to be summed over
trap_contribution = np.exp(1j*delta_j_m_addtheta)

# calculate phi_j. We need to do a sum of trap contributions over m, so sum trap_contributions over the m axis
slm_phase = np.angle(np.sum(trap_contribution,axis=0))

# create slm field
slm = np.exp(1j*slm_phase)

ft = fft.fft2((slm))

plt.imshow(fft.fftshift(abs(ft)))
plt.title('Result')
plt.colorbar()
plt.show()

print(perf(xm,ym,abs(ft)))
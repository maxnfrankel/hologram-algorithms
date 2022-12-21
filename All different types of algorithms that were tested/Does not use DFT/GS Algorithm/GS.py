import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from PtArrayModule import PtArrayCoords
from analyzeSimModule import perf
from SRModule import SR
import cmath

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

# send light at trap locations
trap_plane[ym.astype(int),xm.astype(int)] = 1.0

plt.imshow(fft.fftshift(trap_plane))
plt.title('Target')
plt.show()

# find initial guess for SLM phase through SR algorithm
slm_phase = SR(Nx,Ny,xm,ym)

# now it's time to do the GS algorithm

# create 3D matrix for indexing delta_j^m, where j has two coords xj,yj, and m is 1D
# the ordering of yj,m,xj is important so that np.multiply(xj,xm[m]) and np.multiply(yj,ym) are multiplying the correct temrs
yj,m,xj = np.meshgrid(range(Ny),range(xm.size),range(Nx))

# calculate delta_j^m
# xj,yj are 3D arrays where only the x,y coord is indexed, respectively
# m is a 3D array where each 2D slice in z corresponds to a different trap number
# thus, xm[m] is a 3D array where each slice in z is all the same value, x[m]. ym[m] is similar
# this is just used to speed up calculation so we don't need to do a for loop over every xj and yj to repeat calculation
xjxm = np.multiply(xj,xm[m])/Nx # xm is actually supposed to be a frequency coordinate xm/Nx that we get out in the fourier transform
yjym = np.multiply(yj,ym[m])/Ny

print("Beginning Gershberg-Saxton algorithm")

delta_j_m = 2.0*cmath.pi*np.add( xjxm, yjym )

# calculate Vm/|Vm|
# Vm = sum over j of 1/N*exp(1j*(phi_j-delta_j_m)), should be a 1d array of length M
# What we really want is the phase of Vm. We don't need its length since we're dividing by |Vm|
Vm_phase = np.angle(np.sum(np.sum(np.exp(1j*np.add(slm_phase,-1*delta_j_m)),axis=-1),axis=-1))

# this is now exp(1j*delta_j_m)*Vm/|Vm|, to be summed over m
phaseToSum = np.add(np.array([slm_phase]*npx*npy),Vm_phase[m])

# now we sum exp(1j*delta_j_m)*Vm/|Vm| over m and find the argument
slm_phase = np.angle(np.sum(np.exp(1j*phaseToSum),axis=0))

# create slm field
slm = np.exp(1j*slm_phase)

ft = fft.fft2((slm))

print(perf(xm,ym,abs(ft)))

plt.imshow(fft.fftshift(abs(ft)))
plt.title('Result')
plt.colorbar()
plt.show()

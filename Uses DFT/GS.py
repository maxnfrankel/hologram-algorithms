import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from PtArrayModule import PtArrayCoords
from analyzeSimModule import perf
from SRModule import SR

def GS(slm_phase):
    # get field at SLM
    slm = np.exp(1j*slm_phase)

    # get signal field and extract phase
    signal = fft.fft2(slm)
    signal_phase = np.angle(signal)

    # set trap phase equal to that found in signal_phase
    Vm_phase = np.multiply(trap_plane,np.exp(1j*signal_phase))

    # create slm field and extract phase
    slm = fft.ifft2(Vm_phase)
    slm_phase = np.angle(slm)

    # only return phase
    return slm_phase

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
print('Beginning GS Algorithm')
niter = 30 # define a number of iterations to apply the GS algorithm

for i in range(niter):
    slm_phase = GS(slm_phase)
    print(i)

# create final SLM field
slm = np.exp(1j*slm_phase)

# take the Fourier Transform to get the signal
ft = fft.fft2((slm))

print("GS result after ",i," iterations: e , u, sigma = ",perf(xm,ym,abs(ft)))

plt.imshow(fft.fftshift(abs(ft)))
plt.title('Result')
plt.colorbar()
plt.show()

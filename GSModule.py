import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from PtArrayModule import PtArrayCoords
from analyzeSimModule import perf
from SRModule import SR

def GS_iteration(slm_phase,trap_plane):
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

def GS(Nx,Ny,xm,ym,niter,showGraph=False):

    # inputs:
        # Nx, Ny: the SLM's dimensions in pixels
        # xm, ym: both 1D arrays with the x and y coords of each trap, in order

    # output:
        # 2D array of values between -pi and pi. Values come from the optimization of the slm phase using the SR method

    # create trap plane with same dimensions as SLM
    trap_plane = np.zeros((Ny,Nx),dtype = float)

    # send light at trap locations
    trap_plane[ym.astype(int),xm.astype(int)] = 1.0

    if showGraph == True:
        plt.imshow(fft.fftshift(trap_plane))
        plt.title('Target signal')
        plt.show()

    # find initial guess for SLM phase through SR algorithm
    print('Performing SR Algorithm initial guess for SLM phase')
    slm_phase = SR(Nx,Ny,xm,ym)

    # now it's time to do the GS algorithm
    print('Beginning GS Algorithm')

    for i in range(niter):
        slm_phase = GS_iteration(slm_phase,trap_plane)

    # create final SLM field
    slm = np.exp(1j*slm_phase)

    # take the Fourier Transform to get the signal
    ft = fft.fft2((slm))

    print("GS result after ",i+1," iterations: e , u, sigma = ",perf(xm,ym,abs(ft)))

    if showGraph == True:
        plt.imshow(fft.fftshift(abs(ft)))
        plt.title('Resulting signal')
        plt.colorbar()
        plt.show()

    return fft.fftshift(slm_phase)

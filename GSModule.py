import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from analyzeSimModule import perf

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

def GS(slm_phase,n,xm,ym,niter,showGraph=False):

    # inputs:
        # slm_phase: nxn array with initial guess for the slm phase, with values btween -pi and pi
        # n: the hologram's dimensions in pixels is nxn
        # xm, ym: both 1D arrays with the x and y coords of each trap, in order
        # niter: number of iterations in the algorithm
        # showGraph: when true, graphs of the target and resulting signal plane are shown

    # output: slm_phase, performance
        # slm_phase: 2D array of values between -pi and pi. Values come from the optimization of the slm phase using the GS method
        # performance: [e, u, sigma] where e is efficiency, u is unifority, and sigma is fractional standard deviation, as defined in Leonardo et. al.

    # create trap plane with same dimensions as SLM
    trap_plane = np.zeros((n,n),dtype = float)

    # send light at trap locations
    trap_plane[ym.astype(int),xm.astype(int)] = 1.0

    if showGraph == True:
        plt.imshow(fft.fftshift(trap_plane))
        plt.title('Target signal')
        plt.show()

    # now it's time to do the GS algorithm
    print('Beginning GS Algorithm')

    for i in range(niter):
        slm_phase = GS_iteration(slm_phase,trap_plane)

    # create final SLM field
    slm = np.exp(1j*slm_phase)

    # take the Fourier Transform to get the signal
    ft = fft.fft2((slm))

    performance = perf(xm,ym,abs(ft))

    if showGraph == True:
        plt.imshow(fft.fftshift(abs(ft)))
        plt.title('Resulting signal')
        plt.colorbar()
        plt.show()

    return fft.fftshift(slm_phase), performance

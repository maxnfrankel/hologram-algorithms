import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from PtArrayModule import PtArrayCoords
from analyzeSimModule import perf
from SRModule import SR

def GAA_iteration(slm_phase,trap_plane,xm,ym,xi):
    # get field at SLM
    slm = np.exp(1j*slm_phase)

    # get signal field, extract phase and normalized trap amplitudes
    signal = fft.fft2(slm)
    signal_phase = np.angle(signal)
    signal_trap_amplitudes = abs(signal[ym,xm])
    signal_trap_amplitudes = signal_trap_amplitudes/np.amax(signal_trap_amplitudes)

    # amplitude coefficient used in GAA. a is a 1D array of length M where each value corresponds to a different trap m
    a = 1.0 - xi + xi/signal_trap_amplitudes

    # trap plane with trap amplitudes modified by a
    trap_plane[ym,xm] = a

    # set trap phase equal to that found in signal_phase
    Vm_phase = np.multiply(trap_plane , np.exp(1j*signal_phase))

    # create slm field and extract phase
    slm = fft.ifft2(Vm_phase)
    slm_phase = np.angle(slm)

    # only return phase
    return slm_phase

def GAA(slm_phase,Nx,Ny,xm,ym,niter,xi,showGraph=False):

    # inputs: 
        # slm_phase: Nx*Ny array with initial guess for the slm phase, with values btween -pi and pi
        # Nx, Ny: the SLM's dimensions in pixels
        # xm, ym: both 1D arrays with the x and y coords of each trap, in order
        # niter: number of iterations in the algorithm
        # xi: a float between 0 and 1 that determines how much the maximization of Sum(log|V_m|) is prioritized over Sum(|Vm|)
        # showGraph: when true, graphs of the target and resulting signal plane are shown

    # output: slm_phase, performance
        # slm_phase: 2D array of values between -pi and pi. Values come from the optimization of the slm phase using the GAA method
        # performance: [e, u, sigma] where e is efficiency, u is unifority, and sigma is fractional standard deviation, as defined in Leonardo et. al.


    # create trap plane with same dimensions as SLM
    trap_plane = np.zeros((Ny,Nx),dtype = float)

    # send light at trap locations
    trap_plane[ym.astype(int),xm.astype(int)] = 1.0

    if showGraph == True:
        plt.imshow(fft.fftshift(trap_plane))
        plt.title('Target signal')
        plt.show()

    # now it's time to do the GS algorithm
    print('Beginning GAA Algorithm')

    for i in range(niter):
        slm_phase = GAA_iteration(slm_phase,trap_plane,xm,ym,xi)

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


import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from PtArrayModule import PtArrayCoords
from analyzeSimModule import perf
from SRModule import SR

def GSW_iteration(slm_phase,ym,xm,trap_plane,w):
    # inputs:

    # outputs:
        # slm_phase: array of slm pixel phases, improved by one iteration
        # w: incremented weight

    # get field at SLM
    slm = np.exp(1j*slm_phase)

    # get signal field and extract phase and amplitude
    signal = fft.fft2(slm)
    trap_phase = np.angle(signal)[ym,xm]
    trap_amplitudes = np.abs(signal)[ym,xm]

    # find average trap amplitude
    avg_trap_amp = np.mean(trap_amplitudes)

    # divide avg trap amplitude by trap amplitude to get 1d array, length M, of <|V_m|>/|V_m|
    weight_frac = np.divide(avg_trap_amp,trap_amplitudes)

    # increment w
    w = np.multiply(w,weight_frac)

    # in trap plane, set amplitude equal to w_m and phase equal to the phase of trap resulting from previous guess of slm phase
    Vm = np.multiply(w,np.exp(1j*trap_phase))
    trap_plane[ym,xm] = Vm

    # create slm field and extract phase
    slm = fft.ifft2(trap_plane)
    slm_phase = np.angle(slm)

    # only return phase
    return slm_phase, w

def GSW(slm_phase,n,xm,ym,niter,showGraph=False):

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
    trap_plane = np.zeros((n,n),dtype = complex)

    # send light at trap locations
    trap_plane[ym.astype(int),xm.astype(int)] = 1.0

    if showGraph == True:
        plt.imshow(fft.fftshift(abs(trap_plane)))
        plt.title('Target signal')
        plt.show()

    # now it's time to do the GS algorithm
    print('Beginning GSW Algorithm')

    # weights for each trap
    w = np.ones(xm.size,dtype=float)

    for i in range(niter):
        slm_phase, w = GSW_iteration(slm_phase,ym,xm,trap_plane,w)

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

import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from analyzeSimModule import perf

def S(n,xm,ym,showGraph=False):

    # inputs:
        # n: the holograms's dimensions in pixels is nxn
        # xm, ym: both 1D arrays with the x and y coords of each trap, in order
        # showGraph: when true, graphs of the target and resulting signal plane are shown

    # output: slm_phase, performance
        # slm_phase: 2D array of values between -pi and pi. Values come from the optimization of the slm phase using the S method
        # performance: [e, u, sigma] where e is efficiency, u is unifority, and sigma is fractional standard deviation, as defined in Leonardo et. al.

    # create trap plane with same dimensions as SLM
    trap_plane = np.zeros((n,n), dtype=complex)

    # send light at trap locations
    trap_plane[ym,xm] = 1.0

    if showGraph == True:
        plt.imshow(fft.fftshift(abs(trap_plane)))
        plt.title('Target signal')
        plt.show()

    # calculate slm phase
    slm_phase = np.angle(fft.ifft2(trap_plane))

    # create slm field
    slm = np.exp(1j*slm_phase)

    # take the fourier transform to evaluate performance
    ft = fft.fft2((slm))

    performance = perf(xm,ym,abs(ft))

    if showGraph == True:
        plt.imshow(fft.fftshift(abs(ft)))
        plt.title('Resulting signal')
        plt.colorbar()
        plt.show()

    return fft.fftshift(slm_phase), performance
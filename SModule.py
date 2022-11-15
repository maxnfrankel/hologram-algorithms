import cmath
import numpy as np
import scipy.fft as fft
from analyzeSimModule import perf

def S(Nx,Ny,xm,ym):

    # inputs:
        # Nx, Ny: the SLM's dimensions in pixels
        # xm, ym: both 1D arrays with the x and y coords of each trap, in order

    # output:
        # 2D array of values between -pi and pi. Values come from the optimization of the slm phase using the SR method

    # create trap plane with same dimensions as SLM
    trap_plane = np.zeros((Ny,Nx), dtype=complex)

    # send light at trap locations
    trap_plane[ym,xm] = 1.0

    # calculate slm phase
    slm_phase = np.angle(fft.ifft2(trap_plane))

    # create slm field
    slm = np.exp(1j*slm_phase)

    # take the fourier transform to evaluate performance
    ft = fft.fft2((slm))
    print("S result: e , u, sigma = ", perf(xm,ym,abs(ft)))

    return slm_phase
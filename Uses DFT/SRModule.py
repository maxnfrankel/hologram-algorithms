import cmath
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from PtArrayModule import PtArrayCoords
from analyzeSimModule import perf

def SR(Nx,Ny,xm,ym):

    # inputs:
        # Nx, Ny: the SLM's dimensions in pixels
        # xm, ym: both 1D arrays with the x and y coords of each trap, in order

    # output:
        # 2D array of values between -pi and pi. Values come from the optimization of the slm phase using the SR method

    # for each trap, there is a random theta_m corresponding to the trap's phase
    theta_m = np.random.uniform(-cmath.pi,cmath.pi,size=xm.size)

    # create trap plane with same dimensions as SLM
    trap_plane = np.zeros((Ny,Nx), dtype=complex)

    # send light at trap locations
    trap_plane[ym,xm] = np.exp(1j*theta_m)

    # calculate slm phase
    slm_phase = np.angle(fft.ifft2(trap_plane))

    # create slm field
    slm = np.exp(1j*slm_phase)

    # take the fourier transform to evaluate performance
    ft = fft.fft2((slm))
    print("SR initial guess: e , u, sigma = ", perf(xm,ym,abs(ft)))

    return slm_phase
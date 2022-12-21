import cmath
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from PtArrayModule import PtArrayCoords
from analyzeSimModule import perf

def RM(n,xm,ym,showGraph=False):

    # inputs:
        # n: the holograms's dimensions in pixels is nxn
        # xm, ym: both 1D arrays with the x and y coords of each trap, in order
        # showGraph: when true, graphs of the target and resulting signal plane are shown

    # output: slm_phase, performance
        # slm_phase: 2D array of values between -pi and pi. Values come from the optimization of the slm phase using the RM method
        # performance: [e, u, sigma] where e is efficiency, u is unifority, and sigma is fractional standard deviation, as defined in Leonardo et. al.


    # for each trap, there is a random theta_m corresponding to the trap's phase
    # create array for indexing
    x,y = np.meshgrid(np.arange(-round(n/2),round(n/2)),np.arange(-round(n/2),round(n/2)))

    # create trap plane with same dimensions as SLM
    trap_plane = np.zeros((n,n),dtype = complex)

    # send light at trap locations
    trap_plane[ym,xm] = 1.0

    if showGraph == True:
        plt.imshow(fft.fftshift(abs(trap_plane)))
        plt.title('Target signal')
        plt.show()

    # create the SLM plane
    slm_phase = np.empty((n,n), dtype=float)

    # choose random number from 0 to n_traps-1 for each slm pixel
    n_traps = xm.size
    random_num = np.random.randint(n_traps,size=(n,n))

    if showGraph == True:
        plt.imshow(random_num)
        plt.title('SLM plane, trap # which each pixel corresponds to')
        plt.show()

    # set phi_j in each slm pixel
    xjxm = np.multiply(x,xm[random_num])/n
    yjym = np.multiply(y,ym[random_num])/n

    slm_phase = 2*cmath.pi*(np.add(xjxm,yjym))

    slm = np.exp(1j*slm_phase)

    ft = fft.fft2((slm))

    performance = perf(xm,ym,abs(ft))

    if showGraph == True:
        plt.imshow(fft.fftshift(abs(ft)))
        plt.title('Resulting signal')
        plt.colorbar()
        plt.show()

    return fft.fftshift(slm_phase), performance
import cmath
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
from analyzeSimModule import perf
from random import randrange

def evaluate_gainfunc(slm_phase,xm,ym,f):
    # inputs:
        # slm_phase: some slm phase
        # xm,ym: coordinates of traps in the point array
        # f:  float between 0 and 1 that increases the priority of lowering standard deviation over increasing the average intensity
    
    # output:
        # evaluated gain function <I> - f*sigma


    # create slm field
    slm = np.exp(1j*slm_phase)

    # take the fourier transform to evaluate the gain function
    ft = fft.fft2((slm))

    # find the average trap intensity
    trap_intensities = abs(ft[ym,xm])
    I_avg = np.mean(trap_intensities)

    # calculate the % stdev sigma
    inBrackets = np.square(np.add(trap_intensities,-I_avg)) #(I - <I>)^2
    sigma = cmath.sqrt(np.mean(inBrackets))/I_avg

    # return value of evaluated gain function
    return I_avg - f*sigma

def DS(slm_phase,n,xm,ym,niter,f,showGraph=False):

    # inputs:
        # slm_phase: initial guess for SLM phase
        # n: the hologram's dimensions in pixels is nxn
        # xm, ym: both 1D arrays with the x and y coords of each trap, in order
        # niter: number of iterations algorithm
        # f:  float between 0 and 1 that increases the priority of lowering standard deviation over increasing the average intensity
        # showGraph: when true, graphs of the target and resulting signal plane are shown

    # output: slm_phase, performance
        # slm_phase: 2D array of values between -pi and pi. Values come from the optimization of the slm phase using the DS method
        # performance: [e, u, sigma] where e is efficiency, u is unifority, and sigma is fractional standard deviation, as defined in Leonardo et. al.


    # create trap plane with same dimensions as SLM
    trap_plane = np.zeros((n,n), dtype=complex)

    # send light at trap locations
    trap_plane[ym,xm] = 1.0

    if showGraph == True:
        plt.imshow(fft.fftshift(abs(trap_plane)))
        plt.title('Target signal')
        plt.show()

    gain_func = evaluate_gainfunc(slm_phase,xm,ym,f)
    
    print('Beginning DS algorithm')

    # loop over the chosen number of iterations
    for i in range(niter):
        print('Iteration: ',i,end='\r')

        # select a random pixel to adjust pixel
        xj = randrange(n); yj = randrange(n)

        # create layers of slm_phase, each layer having a different gray value of phi_j
        gray_lvls = 256
        diff_phij_choices = np.array([slm_phase]*gray_lvls)
        diff_phij_choices[:,yj,xj] = np.array(range(gray_lvls))/(gray_lvls-1)*cmath.pi*2 - cmath.pi # insert the 256 possible phase values at coordinates (xj,yj) in each layer

        # evaluate gain function
        gain_func_choices = np.empty(gray_lvls,dtype=float)

        for j in range(gray_lvls):
            gain_func_choices[j] = evaluate_gainfunc(diff_phij_choices[j],xm,ym,f)

        # get the index of the best phij choice and set slm_phase equal to it
        slm_phase = diff_phij_choices[np.argmax(gain_func_choices)]

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

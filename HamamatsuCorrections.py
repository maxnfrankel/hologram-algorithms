# this module is for applying the necessary corrections for displaying on the Hamamatsu SLM

import numpy as np
from PIL import Image

def correct(slm_phase,Nx,Ny):
    
    # first, we want to apply the correction needed for 532nm light due to SLM surface irregularity
    im = Image.open("532nmCorrection.bmp")
    correction = np.array(np.asarray(im))
    slm_phase = np.add(slm_phase,correction) % 256 # wrap phases around if they exceed the max value

    # now apply LUT
    LUT = np.genfromtxt('LUT_532nm.csv', delimiter=',') # creates list of values where LUT[input value] = converted value
    slm_phase = LUT[slm_phase.astype(int)]

    return slm_phase
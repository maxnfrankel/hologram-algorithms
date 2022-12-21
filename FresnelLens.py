import numpy as np
import cmath

def FresnelLens(Nx,Ny,f,pp,wavelength):
    
    x,y = np.meshgrid(range(Nx),range(Ny))

    x = x*pp; y = y*pp # convert to spatial dimensions

    r = np.sqrt((np.add(np.square(x-Nx//2),np.square(y-Ny//2))) + f**2)
    
    phase = (r/wavelength) % 1

    # convert to value between 0-255 and return
    return phase*255

    


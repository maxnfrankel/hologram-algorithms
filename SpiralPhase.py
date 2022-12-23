import numpy as np
import matplotlib.pyplot as plt
import cmath


def spiral(Nx,Ny,l):
    # inputs:
        # Nx,Ny: SLM dimensions
        # l: charge of the spiral phase (how many cycles in phase over the full 360 degrees

    x,y = np.meshgrid(range(Nx),range(Ny))
    x = x-Nx/2; y = y-Ny/2 # move origin to center

    # create complex array of (x+1j*y) and then use np.angle to extract angle
    angle = np.angle(l*np.add(x,1j*y)) + cmath.pi # add pi to get values between 0 and 2pi

    plt.imshow(angle)
    plt.title("Spiral phase")
    plt.show()

    # convert to value between 0-255 and return
    return angle/(2*cmath.pi)*255

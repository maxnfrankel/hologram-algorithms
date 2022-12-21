# this is the script from which a phase hologram is created using the weighted Gershberg-Saxton algorithm

# import two important functions for calculating the hologram
from SRModule import SR
from GSWModule import GSW


from PtArrayModule import PtArrayCoords # function that calculates coordinates for your desired point array
from HamamatsuCorrections import correct # function that applies corrections necessary for 532nm on the Hamamatsu SLM
from FresnelLens import FresnelLens # function that adds fresnel lens to your hologram

import numpy as np
import cmath
import matplotlib.pyplot as plt
from PIL import Image

# In this first part, we are going to set our point array specifications

# set the SLM dimensions
Nx = 1272
Ny = 1024
pp = 12.5e-6 # pixel pitch (side length)

# set the point array dimensions
npx = 60 # number of pts in x direction
npy = 60 # number of pts in y direction
# the hologram is calculated on a square array to ensure that the x and y directions are scaled the same way
# choose the larger dimension as your side length, so we get nxn array
n = max([Nx,Ny])
px = 15 # x periodicity
py = 15 # y periodicity

# done setting point array specifications
# form pt array
xm,ym = PtArrayCoords(npx,npy,px,py)

# to do perform the GSW algorithm, we find an initial guess for the SLM phase through the SR algorithm

print('Performing SR Algorithm initial guess for SLM phase')
initial_slm_phase, perf_SR = SR(n,xm,ym,showGraph=False)
print(perf_SR) # this tells us how well hologram created by the SR algorithm performed

# now we do GSW
slm_phase, perf_GSW = GSW(initial_slm_phase,n,xm,ym,niter=50,showGraph=False)
print(perf_GSW) # this tells us how well hologram created by the GSW algorithm performed

"""# show the SLM phase
plt.imshow(slm_phase)
plt.title('SLM phase')
plt.colorbar()
plt.show()
"""
# show the FT, which is what will be observed in the focal plane of a lens
ft = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(np.exp(1j*slm_phase))))

"""plt.imshow(abs(ft))
plt.title('Resulting signal')
plt.colorbar()
plt.show()"""

# rescale to values from 0 to 255 to save phasemap as bmp, to be displayed on our SLM
slm_phase = np.round((slm_phase + cmath.pi)/(2*cmath.pi)*255)

# Crop array so that it fits on the SLM
slm_phase_cropped = slm_phase[0:Ny,0:Nx]

"""# add Fresnel lens phase with focal length f for wavelength
f = 500-3
wavelength = 532e-9
slm_phase_cropped = np.add(slm_phase_cropped,FresnelLens(Nx,Ny,f,pp,wavelength))%256
"""
slm_phase_final = correct(slm_phase_cropped,Nx,Ny)

# save hologram
im = Image.fromarray(np.fft.fftshift(slm_phase_final))
im = im.convert('L') # convert to 8-bit depth

im.save("npx60_px10_PointArrayHolo_CorrectedAndLUT.bmp")
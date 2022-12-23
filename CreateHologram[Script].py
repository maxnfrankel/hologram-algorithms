# this is the script from which a phase hologram is created using the weighted Gershberg-Saxton algorithm

# import two important functions for calculating the hologram
from SRModule import SR
from GSWModule import GSW


from PtArrayModule import PtArrayCoords # function that calculates coordinates for your desired point array
from HamamatsuCorrections import correct # function that applies corrections necessary for 532nm on the Hamamatsu SLM
from FresnelLens import FresnelLens # function that adds fresnel lens to your hologram
from SpiralPhase import spiral # function that adds spiral phase

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
slm_phase_large, perf_SR = SR(n,xm,ym,showGraph=False) # outputs slm_phase_large, "large" because it's on a square array with sidelength max([Nx,Ny]), larger than the actual SLM
print(perf_SR) # this tells us how well hologram created by the SR algorithm performed

# now we do GSW
slm_phase_large, perf_GSW = GSW(slm_phase_large,n,xm,ym,niter=100,showGraph=False)
print(perf_GSW) # this tells us how well hologram created by the GSW algorithm performed

"""# show the SLM phase
plt.imshow(slm_phase)
plt.title('SLM phase')
plt.colorbar()
plt.show()
"""
# show the FT, which is what will be observed in the focal plane of a lens
ft = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(np.exp(1j*slm_phase_large))))

plt.imshow(abs(ft))
plt.title('Resulting signal')
plt.colorbar()
plt.show()

# rescale to values from 0 to 255 to save phasemap as bmp, to be displayed on our SLM
slm_phase_large = (slm_phase_large + cmath.pi)/(2*cmath.pi)*255

# Crop array so that it fits on the SLM
slm_phase = slm_phase_large[0:Ny,0:Nx]

# add Fresnel lens phase with focal length f for wavelength
f = 0.5
wavelength = 532e-9
slm_phase = np.add(slm_phase,-1*FresnelLens(Nx,Ny,f,pp,wavelength))%256 # multiply FresnelLens output with factor of -1 is for converging lens, +1 for diverging

# add spiral phase
slm_phase = np.add(slm_phase,spiral(Nx,Ny,1))

# apply corrections for SLM surface irregularities and wavelength-dependent phase modulation
slm_phase = correct(slm_phase,Nx,Ny)

# convert to integer
slm_phase_final = slm_phase.astype(np.uint8)

plt.imshow(slm_phase_final)
plt.title('Final hologram')
plt.show()

# save hologram
im = Image.fromarray(slm_phase_final)
im = im.convert('L') # convert to 8-bit depth

im.save("npx60_px10_PointArrayHolo_CorrectedAndLUT_wFresnelLens_wSpiral.bmp")
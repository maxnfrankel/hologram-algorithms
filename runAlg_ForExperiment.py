# this is the script from which the different algorithms can be run

from RMModule import RM
from SModule import S
from SRModule import SR
from GSModule import GS
from GAAModule import GAA
#from DSModule import DS
from GSWModule import GSW

from PtArrayModule import PtArrayCoords

import numpy as np
import cmath
import matplotlib.pyplot as plt
from PIL import Image

# In this first part, we are going to set our point array specifications

# set the SLM dimensions
Nx = 1280
Ny = 1024

# set the point array dimensions
npx = 60 # number of pts in x direction
npy = 60 # number of pts in y direction
# the hologram is calculated on a square array to ensure that the x and y directions are scaled the same way
# choose the smaller dimension as your side length, so we get nxn array
#n = min(Nx,Ny)
n = min([Nx,Ny])
px = 10 # x periodicity
py = 10 # y periodicity

# done setting point array specifications
# form pt array
xm,ym = PtArrayCoords(npx,npy,px,py)

# all the functions (RM, S, SR, GS, GAA, GSW) that perform the different algorithms take inputs in the form (Nx,Ny,xm,ym)
# we now have all of the inputs. Just comment out all but the algorithm you want to use

#slm_phase, perf_RM = RM(n,xm,ym,showGraph=True)
#slm_phase, perf_S = S(n,xm,ym,showGraph=True)
#slm_phase, perf_SR = SR(n,xm,ym,showGraph=True)

# to do the GS, GAA, DS, GSW,find initial guess for SLM phase through SR algorithm
print('Performing SR Algorithm initial guess for SLM phase')
initial_slm_phase, perf_SR = SR(n,xm,ym,showGraph=False)

print(perf_SR)

#slm_phase, perf_GS = GS(initial_slm_phase,n,xm,ym,niter=30,showGraph=False) # niter is the number of iterations for the GS algorithm
#slm_phase, perf_GAA = GAA(initial_slm_phase,n,xm,ym,niter=30,xi=0.74,showGraph=False) # xi is a number between 0 and 1 that determines how much the maximization of Sum(log|V_m|) is prioritized over Sum(|Vm|)
#slm_phase, perf_DS = DS(sinitial_slm_phase,n,xm,ym,niter=int(round(Nx*Ny*1.3)),f=0.5,showGraph=True)
slm_phase, perf_GSW = GSW(initial_slm_phase,n,xm,ym,niter=50,showGraph=True)

print(perf_GSW)

slm_phase = np.add(slm_phase,1)%(2*cmath.pi) - cmath.pi

# show the SLM phase
plt.imshow(slm_phase)
plt.title('SLM phase')
plt.colorbar()
plt.show()

# show the FT
ft = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(np.exp(1j*slm_phase))))

plt.imshow(abs(ft))
plt.title('Resulting signal')
plt.colorbar()
plt.show()

# rescale to values from 0 to 255
slm_phase = np.round((slm_phase + cmath.pi)/(2*cmath.pi)*255)

# add to fullsize SLM
slm_phase_fullsize = np.zeros((Ny,Nx),dtype=float)
slm_phase_fullsize[round(Ny/2 - n/2):round(Ny/2+n/2),round(Nx/2 - n/2):round(Nx/2+n/2)] = slm_phase # if slm larger than calculated hologram
#slm_phase_fullsize = slm_phase[0:Ny,0:Nx]

# save hologram
im = Image.fromarray(slm_phase_fullsize)
im = im.convert('L')

im.save("npx60_px10_PointArrayHolo.bmp")

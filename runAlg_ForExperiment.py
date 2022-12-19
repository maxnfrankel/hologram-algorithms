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

# set the filename you want to save to. Will end in "Holo.bmp"
name = 'PointArray'

# set the SLM dimensions
Nx = 1280
Ny = 1024

# set the point array dimensions
npx = 60 # number of pts in x direction
npy = 60 # number of pts in y direction

px = 5 # x periodicity
py = 5 # y periodicity

# done setting point array specifications

# the hologram is calculated on a square array to ensure that the x and y directions are scaled the same way
# choose the smaller dimension as your side length, so we get nxn array
n = min(Nx,Ny)

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
#slm_phase, perf_DS = DS(initial_slm_phase,n,xm,ym,niter=int(round(Nx*Ny*1.3)),f=0.5,showGraph=True)
slm_phase, perf_GSW = GSW(initial_slm_phase,n,xm,ym,niter=500,showGraph=True)

print(perf_GSW)

# uncomment the code below to save the hologram
plt.imshow(slm_phase)
plt.colorbar()
plt.show()

# rescale to values from 0 to 255
slm_phase = np.round((slm_phase + cmath.pi)/(2*cmath.pi)*255)

# add to fullsize SLM
slm_phase_fullsize = np.zeros((Ny,Nx),dtype=float)
slm_phase_fullsize[round(Ny/2 - n/2):round(Ny/2+n/2),round(Nx/2 - n/2):round(Nx/2+n/2)] = slm_phase

# save hologram
im = Image.fromarray(slm_phase_fullsize)
im = im.convert('RGB')

im.save(name+"GSW_5p_Holo.bmp")

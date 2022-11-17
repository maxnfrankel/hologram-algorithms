# this is the script from which the GSW algorithm can be run

from SRModule import SR
from GSModule import GS
from GSWModule import GSW

from PtArrayModule import PtArrayCoords

import numpy as np
import cmath
import matplotlib.pyplot as plt
from PIL import Image

# set the filename you want to save to. Will end in "Holo.bmp"
name = 'PointArrayDS'

# set the SLM dimensions
Nx = 768
Ny = 768

# set the point array dimensions
npx = 10 # number of pts in x direction
npy = 10 # number of pts in y direction
px = 70 # x periodicity
py = 70 # y periodicity

# form pt array
xm,ym = PtArrayCoords(npx,npy,px,py)

# to do the GSW, find initial guess for SLM phase through SR algorithm

# create array that holds performance of SR, GS, and GSW for the 10 trials
# [0   ,  1 ,  2     ,  3 , 4  ,    5   ,  6  ,  7  ,    8    ]
# [SR_e,SR_u,SR_sigma,GS_e,GS_u,GS_sigma,GSW_e,GSW_u,GSW_sigma]
performances = np.empty((10,6),dtype=float)

for i in range(10):
    initial_slm_phase, performances[i,0:3] = SR(Nx,Ny,xm,ym,showGraph=False)
    #slm_phase, performances[i,3:6] = GS(initial_slm_phase,Nx,Ny,xm,ym,niter=30,showGraph=False)
    slm_phase, performances[i,3:6] = GSW(initial_slm_phase,Nx,Ny,xm,ym,niter=100,showGraph=False)

# calculate performances
performances_avgs = np.mean(performances,axis=0)
perforamnces_stdevs = np.std(performances,axis=0)

print(performances_avgs)
print(perforamnces_stdevs)

# uncomment the code below to save the hologram
# extract slm_phase
plt.imshow(slm_phase)
plt.colorbar()
plt.show()

# rescale to values from 0 to 255
slm_phase = np.round((slm_phase + cmath.pi)/(2*cmath.pi)*7)

# save hologram
im = Image.fromarray(slm_phase)
im = im.convert('RGB')
im.save(name+"Holo.bmp")
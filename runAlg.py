# this is the script from which the different algorithms can be run

from RMModule import RM
from SModule import S
from SRModule import SR
from GSModule import GS

from PtArrayModule import PtArrayCoords

import numpy as np
import cmath
import matplotlib.pyplot as plt
from PIL import Image

# set the filename you want to save to. Will end in "Holo.bmp"
name = 'PointArray'

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

# all the functions (RM, S, SR, GS) that perform the different algorithms take inputs in the form (Nx,Ny,xm,ym)
# we now have all of the inputs. Just comment out all but the algorithm you want to use

#slm_phase = RM(Nx,Ny,xm,ym,showGraph=True)
#slm_phase = S(Nx,Ny,xm,ym,showGraph=True)
#slm_phase = SR(Nx,Ny,xm,ym,showGraph=True)
slm_phase = GS(Nx,Ny,xm,ym,niter=30,showGraph=False) # niter is the number of iterations for the GS algorithm

# extract slm_phase
plt.imshow(slm_phase)
plt.colorbar()
plt.show()

# rescale to values from 0 to 255
slm_phase = np.round((slm_phase + cmath.pi)/(2*cmath.pi)*255)

# save hologram
im = Image.fromarray(slm_phase)
im = im.convert('RGB')
im.save(name+"Holo.bmp")
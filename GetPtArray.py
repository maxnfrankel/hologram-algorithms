from PtArrayModule import PtArrayCoords

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# set the SLM dimensions
Nx = 1280
Ny = 1024

# set the point array dimensions
npx = 60 # number of pts in x direction
npy = 60 # number of pts in y direction
# the hologram is calculated on a square array to ensure that the x and y directions are scaled the same way
# choose the smaller dimension as your side length, so we get nxn array
#n = min(Nx,Ny)
n = 1280
px = 10 # x periodicity
py = 10 # y periodicity

xm,ym = PtArrayCoords(npx,npy,px,py)

# create trap plane with same dimensions as SLM
trap_plane = np.zeros((n,n),dtype = float)

# send light at trap locations
trap_plane[ym.astype(int),xm.astype(int)] = 255

plt.imshow(np.fft.fftshift(trap_plane))
plt.show()

# save pt array
im = Image.fromarray(np.fft.fftshift(trap_plane))
im = im.convert('RGB')

im.save("PtArray.bmp")
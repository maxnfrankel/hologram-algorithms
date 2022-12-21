import numpy as np
import matplotlib.pyplot as plt
import cmath
from PIL import Image
import os
from analyzeSimModule import perf

# directory
dir_path = os.path.dirname(os.path.realpath(__file__))

#npx60_px10_PointArrayHolo
#testPattern

# import image (phase map)
img = Image.open("FT/npx60_px10_PointArrayHolo.bmp")
slm_phase = np.array(np.asarray(img))

# get size of phase map
dim = slm_phase.shape

slm = np.exp(1j*slm_phase/255*2*cmath.pi)

ft = np.fft.fft2(np.fft.fftshift(slm))

ftshift = np.fft.fftshift(ft)

plt.imshow(abs(ftshift))
plt.show()

# check performance

# get trap coords
npx = 60; npy = 60; px = 10; py = 8; offs_x = 0; offs_y = 0
grid_xm = np.arange(-npx*px/2,npx*px/2,px)+offs_x
grid_ym = np.arange(-npy*py/2,npy*py/2,py)+offs_y

xm,ym = np.meshgrid(grid_xm,grid_ym)
xm = xm.flatten().astype(int); ym = ym.flatten().astype(int)

"""#check overlap
ft[ym,xm] = 1.7e4

plt.imshow(np.fft.fftshift(abs(ft)))
plt.show()"""

print(perf(xm,ym,abs(ft)))
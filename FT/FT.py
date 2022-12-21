import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import math
from skimage.io import imread
import matplotlib.image as mpimg
from scipy.fft import fft2, fftshift

name = 'PtArray'

dir_path = os.path.dirname(os.path.realpath(__file__))
im = imread(os.path.join(dir_path,name+"Holo.bmp"))
ch1 =(im[:,:,1]/255-0.5)*2*math.pi

dim = ch1.shape

unifAmp = np.ones(dim,dtype=float)

y,x = np.meshgrid(np.arange(-round(dim[1]/2),round(dim[1]/2)),np.arange(-round(dim[0]/2),round(dim[0]/2)))
w = 300
gaussianAmp = np.exp(-1*np.add(np.square(x),np.square(y))/(w**2))

plt.figure()
plt.imshow(gaussianAmp)
plt.show()

slm = np.multiply(gaussianAmp,np.exp(1j*ch1))

plt.imshow(np.angle(slm))
plt.show()

ft = fftshift(fft2(slm))
ft[round(dim[0]/2),round(dim[1]/2)] = 0

plt.imshow(np.square(abs(ft)))
plt.show()
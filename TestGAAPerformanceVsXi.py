from RMModule import RM
from SModule import S
from SRModule import SR
from GSModule import GS
from GAAModule import GAA

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
npx = 11 # number of pts in x direction
npy = 11 # number of pts in y direction
px = 70 # x periodicity
py = 70 # y periodicity

# form pt array
xm,ym = PtArrayCoords(npx,npy,px,py)

# all the functions (RM, S, SR, GS) that perform the different algorithms take inputs in the form (Nx,Ny,xm,ym)
# we now have all of the inputs. Just comment out all but the algorithm you want to use

#slm_phase = RM(Nx,Ny,xm,ym,showGraph=True)
#slm_phase = S(Nx,Ny,xm,ym,showGraph=True)
#slm_phase = SR(Nx,Ny,xm,ym,showGraph=True)

# find initial guess for SLM phase through SR algorithm
print('Performing SR Algorithm initial guess for SLM phase')
initial_slm_phase, perf_SR = SR(Nx,Ny,xm,ym,showGraph=False)

slm_phase, perf_GAA = GAA(initial_slm_phase,Nx,Ny,xm,ym,niter=30,xi=0.5,showGraph=False) # xi is a number between 0 and 1 that determines how much the maximization of Sum(log|V_m|) is prioritized over Sum(|Vm|)

# take steps in xi
n_steps = 100
xi_var = np.linspace(0,1,num=n_steps,endpoint=True)

perf = np.empty((n_steps,3), dtype=float) # array containing [e,u,sigma] for each step in xi

for i in range(n_steps):
    perf[i] = GAA(initial_slm_phase,Nx,Ny,xm,ym,niter=30,xi=xi_var[i],showGraph=False)[1]

e = perf[:,0]
u = perf[:,1]
sigma = perf[:,2]

fig = plt.figure(figsize=(12,6))
ax1 = fig.add_subplot(1,3,1); ax2 = fig.add_subplot(1,3,2); ax3 = fig.add_subplot(1,3,3)
ax1.scatter(xi_var,e); ax2.scatter(xi_var,u); ax3.scatter(xi_var,sigma)
ax1.set_xlabel('\u03BE'); ax2.set_xlabel('\u03BE'); ax3.set_xlabel('\u03BE')
ax1.set_ylabel('e'); ax2.set_ylabel('u'); ax3.set_ylabel('\u03C3')
fig.suptitle('GAA performance after 30 iterations for various choices of \u03BE')
plt.savefig('GAAPerformanceVsXi.png')
plt.show()

# save data from plots in textfile
GAAperf = np.transpose(np.array([xi_var,e,u,sigma]))
np.savetxt("GAAPerformanceVsXi.csv", GAAperf, delimiter=",")

# uncomment the code below to save the hologram
"""
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
"""
# this is the script from which the different algorithms can be run

from SRModule import SR
from GSWPerformanceVsIteration import GSW

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

# all the functions (RM, S, SR, GS, GAA, GSW) that perform the different algorithms take inputs in the form (Nx,Ny,xm,ym)
# we now have all of the inputs. Just comment out all but the algorithm you want to use

#slm_phase, perf_RM = RM(Nx,Ny,xm,ym,showGraph=True)
#slm_phase, perf_S = S(Nx,Ny,xm,ym,showGraph=True)
#slm_phase, perf_SR = SR(Nx,Ny,xm,ym,showGraph=True)

# to do the GS, GAA, DS, GSW,find initial guess for SLM phase through SR algorithm
print('Performing SR Algorithm initial guess for SLM phase')
initial_slm_phase, perf_SR = SR(Nx,Ny,xm,ym,showGraph=False)

print(perf_SR)

#slm_phase, perf_GS = GS(initial_slm_phase,Nx,Ny,xm,ym,niter=30,showGraph=False) # niter is the number of iterations for the GS algorithm
#slm_phase, perf_GAA = GAA(initial_slm_phase,Nx,Ny,xm,ym,niter=30,xi=0.8,showGraph=False) # xi is a number between 0 and 1 that determines how much the maximization of Sum(log|V_m|) is prioritized over Sum(|Vm|)
#slm_phase, perf_DS = DS(initial_slm_phase,Nx,Ny,xm,ym,niter=int(round(Nx*Ny*1.3)),f=0.5,showGraph=True)

niter = 500

slm_phase, perf_GSW = GSW(initial_slm_phase,Nx,Ny,xm,ym,niter,showGraph=False)

e = perf_GSW[:,0]
u = perf_GSW[:,1]
sigma = perf_GSW[:,2]

loge = np.log10(1-1*perf_GSW[:,0])
logu = np.log10(1-1*perf_GSW[:,1])
logsigma = np.log10(perf_GSW[:,2])
x = range(niter)

print(perf_GSW[-1])

fig = plt.figure(figsize=(16,6))
ax1 = fig.add_subplot(1,3,1); ax2 = fig.add_subplot(1,3,2); ax3 = fig.add_subplot(1,3,3)
ax1.scatter(x,e); ax2.scatter(x,u); ax3.scatter(x,sigma)
ax1.set_xlabel('\u03BE'); ax2.set_xlabel('\u03BE'); ax3.set_xlabel('\u03BE')
ax1.set_ylabel('e'); ax2.set_ylabel('u'); ax3.set_ylabel('\u03C3')
fig.suptitle('GSW performance vs iteration step number')
plt.savefig('GSWPerformanceVsIteration.png')
plt.show()

fig = plt.figure(figsize=(16,6))
ax1 = fig.add_subplot(1,3,1); ax2 = fig.add_subplot(1,3,2); ax3 = fig.add_subplot(1,3,3)
ax1.scatter(x,loge); ax2.scatter(x,logu); ax3.scatter(x,logsigma)
ax1.set_xlabel('\u03BE'); ax2.set_xlabel('\u03BE'); ax3.set_xlabel('\u03BE')
ax1.set_ylabel('log10(1-e)'); ax2.set_ylabel('log10(1-u)'); ax3.set_ylabel('log10(\u03C3)')
fig.suptitle('GSW performance vs iteration step number')
plt.savefig('GSWPerformanceVsIterationLogScale.png')
plt.show()

# rescale to values from 0 to 255
slm_phase = np.round((slm_phase + cmath.pi)/(2*cmath.pi)*255)

# save hologram
im = Image.fromarray(slm_phase)
im = im.convert('RGB')
im.save(name+"Holo.bmp")
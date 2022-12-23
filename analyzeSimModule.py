import cmath
import numpy as np

def perf(xm,ym,sim):
    # inputs:
        # xm, ym are the target trap coordinates
    
    # output: 
        # e = efficiency
        # u = uniformity
        # sigma = stdev in %

    # get amplitude of sim at the trap coordinates
    sim_trap_vals = abs(sim[ym.astype(int),xm.astype(int)])

    # get simulated trap intensities
    ITraps = np.square(sim_trap_vals)

    # calculate the efficiency
    Iwhole = np.sum(np.square(abs(sim))) # calculate the total intensity in the simulated plane. Will divide trap intensity sum by this amt
    Isum = np.sum(ITraps) # calculate the sum of the simulated trap intensities
    e = Isum/Iwhole

    # calculate the uniformity
    trapMax = np.amax(ITraps); trapMin = np.amin(ITraps) # get max and min trap intensity vals
    u = 1 - (trapMax - trapMin)/(trapMax + trapMin)

    # calculate the % stdev
    IAvg = np.mean(ITraps)
    inBrackets = np.square(np.add(ITraps,-IAvg))#(I - <I>)^2
    sigma = cmath.sqrt(np.mean(inBrackets))/IAvg

    return [e,u,sigma]
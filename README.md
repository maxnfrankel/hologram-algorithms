# hologram-algorithms

## Running an algorithm

Each algorithm is contained in a function in the module corresponding to its name (ex: Gershberg-Saxton algorithm is contained in the module GSModule.py). To run an algorithm, its corresponding function can be called in a script, together with the parameters for the point array you want to create. For an example, see the file "runAlg.py"

## About this project

This repository contains different algorithms used for creating holograms of optical focus arrays, meant to be displayed on a phase-only spatial light modulator. An optical focus array is a 2-D intensity distribution where light is concentrated in a grid of points with a set periodicity. Exploring the advantages provided by creating a focus array with a spatial light modulator instead of a microlens array is the goal of my Fulbright research in Sweden.

The algorithms in this repository are based off of a paper by Leonardo et al [^1].

## Analysis of the algorithms

In the paper of Leonardo et al, to evaluate the performance of each algorithm introduced, each was used to create holgram of a 10x10 grid of traps for a 768x768 pixel SLM. The performance of an algorithm was quantified by efficiency $e$, uniformity $u$, and percent standard deviation $\sigma$

$e = \sum_{m}{I_m}$

$u = 1 - \frac{max(I_m)-min(I_m)}{max(I_m)+min(I_m)}$

$\sigma = 100\sqrt{\langle (I - \langle I \rangle)^2 \rangle} / \langle I \rangle $

where $I_m$ is the intensity at the $m^{th}$ trap coordinate $(x_m,y_m)$, and $\langle I \rangle$ denotes the average over $m$.

Each algorithm boils to a maximization problem. To maximize the fraction of the total light sent to traps, or $e$, we simply seek to maximize the sum of the magnitudes of the electric field at each trap with respect to the 768x768 SLM pixels, each of which is treated as a single variable. The maximization is done with increasing accuracy for RM, S, SR, and GS. 

For GAA, we seek to maximize a combination of both the sum of electric field amplitudes at traps and their product. Maximizing the product of the electric field amplitudes creates a bias towards maximizing the uniformity, as the greatest possible "volume" is created when the "surface area" is as small as possible. In other words, for a certain total amount of light, the product of the magnitude of the electric field at each trap is maximized when the energy is uniformly distributed between the different traps.

The numerically simulated performance of my algorithms compared to the performance recorded by Leonardo et al. is shown in the tables below. The algorithms were used to create holgram of a 10x10 grid of traps for a 768x768 pixel SLM.

algorithm | e (theirs) | u (theirs) | $\sigma$ (theirs) 
---|---|---|---
RM | $0.01$ | $0.58$ | $16$ 
S | $0.29$ | $0.01$ | $257$ 
SR | $0.69$ | $0.01$ | $89$ 
GS | $0.94$ | $0.60$ | $17$
GAA | $0.93$ | $0.79$ | $9$
DS | $0.68$ | $1.00$ | $0$
GSW | $0.93$ | $0.99$ | $1$

algorithm | e (mine) | u (mine) | $\sigma$ (mine)
---|---|---|---
RM | $0.0102 \pm 0.0001$ | $0.59 \pm 0.03$ | $17.5 \pm 0.9$
S | $0.29$ | $0.01$ | $266$
SR | $0.85 \pm 0.01$ | $0.27 \pm 0.03$ | $36 \pm 3$
GS | $0.938 \pm 0.003$ | $0.56 \pm 0.05$ | $18 \pm 2$
GAA| $0.933 \pm 0.004$ | $0.74 \pm 0.03$ | $11 \pm 1$
GSW| $0.923 \pm 0.005$ | $0.97 \pm 0.01$ | $1.0 \pm 0.5$

I calculated e, u, and $\sigma$ in 10 runs and found the average and standard deviation, which are the values displayed in my table. S is an analytic solution, and thus had no standard deviation. The discrepancy between my values and theirs is likely due to our slightly different choice of trap geometry. It is notable that my SR algorithm performed significantly better than theirs in $e$, $u$, and $\sigma$.

The GS, GAA, and GSW algorithms all use SR as a starting guess for slm phase and then iteratively converge to a solution. My calculation of the performance of GS and GSW was done using the same set of converged holograms that were used to calculate the performance of SR. GAA was calculated separately, with a different set of SR solutions.

In the Leonardo et. al. paper, they use $\xi = 0.5$. I found that the optimal choice of $\xi$ seems to vary depending initial phase guess around an average value of $0.74 \pm 0.10$, where $\pm 0.10$ is the standard deviation in the optimal $\xi$ values over 10 runs. Here are graphs of performance vs 100 evenly spaced values of $\xi$ between 0 and 1:

[graphs of performance vs xi](https://github.com/maxnfrankel/hologram-algorithms/blob/main/GAAPerformanceVsXi.pdf)

The values I found for $u$ at $\xi = 0.5$ are all lower than that found by Leonardo et. al., and I'm not sure why. Perhaps it has to do with our differring trap geometries, or because we are already getting different results from the SR algorithm, which is used as an initial guess for GAA. However, my SR algorithm outperforms theirs, so I don't see why my GAA algorithm shouldn't as well. My GS algorithm had performance consistent with theirs, though, and that also used my SR algorithm as an intial guess. At least the GAA algorithm does show an improvement in $e$ from the GS algorithm, although $u$ is sacrificed.

My GSW also underperformed, not quite reaching $u=0.99$. However, after 100 iterations instead of 30, the algorithm achieved

$e = 0.932 \pm 0.001$,   $u = 0.991 \pm 0.001$,   $\sigma = 0.4 \pm 0.2$

over 10 runs. After 500 iterations, the algorithm achieved 

$e = 0.938$,   $u = 0.999997$,   $\sigma = 0.0001$

[^1]: R. Di Leonardo, F. Ianni, and G. Ruocco, "Computer generation of optimal holograms for optical trap arrays," Opt. Express 15, 1913-1922 (2007).

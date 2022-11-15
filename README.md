# hologram-algorithms

## Running an algorithm

Each algorithm is contained in a function in the module corresponding to its name (ex: Gershberg-Saxton algorithm is contained in the module GS.py). To run an algorithm, its corresponding function can be called in a script, together with the parameters for the point array you want to create. For an example, see the file "runAlg.py"

## About this project

This repository contains different algorithms used for creating holograms of optical focus arrays, meant to be displayed on a phase-only spatial light modulator. An optical focus array is a 2-D intensity distribution where light is concentrated in a grid of points with a set periodicity. Exploring the advantages provided by creating a focus array with a spatial light modulator instead of a microlens array is the goal of my Fulbright research in Sweden.

The algorithms in this repository are based off of a paper by Leonardo et al [^1].

In the paper of Leonardo et al, the performance of each algorithm was quantified by efficiency $e$, uniformity $u$, and percent standard deviation $\sigma$

$e = \sum_{m}{I_m}$

$u = 1 - \frac{max(I_m)-min(I_m)}{max(I_m)+min(I_m)}$

$\sigma = 100\sqrt{\langle (I - \langle I \rangle)^2 \rangle} / \langle I \rangle $

where $I_m$ is the intensity at the $m^{th}$ trap coordinate $(x_m,y_m)$, and $\langle I \rangle$ denotes the average over $m$.

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
SR | $0.85 \pm 0.01$ | $0.22 \pm 0.06$ | $38 \pm 2$
GS | $0.937 \pm 0.003$ | $0.63 \pm 0.05$ | $17 \pm 1$

I calculated e, u, and $\sigma$ in 10 runs and found the average and standard deviation, which are the values displayed in my table. S is an analytic solution, and thus the discrepancy between my values and theirs is likely due to our slightly different choice of trap geometry. It is notable that my SR algorithm performed significantly better than theirs in $e$, $u$, and $\sigma$.

[^1]: R. Di Leonardo, F. Ianni, and G. Ruocco, "Computer generation of optimal holograms for optical trap arrays," Opt. Express 15, 1913-1922 (2007).

# hologram-algorithms

This repository contains different algorithms used for creating holograms of optical focus arrays, meant to be displayed on a phase-only spatial light modulator. An optical focus array is a 2-D intensity distribution where light is concentrated in a grid of points with a set periodicity. Exploring the advantages provided by creating a focus array with a spatial light modulator instead of a microlens array is the goal of my Fulbright research in Sweden.

The algorithms in this repository are based off of a paper by Leonardo, Ianni, and Ruocco [^1]. In this paper, the performance of each algorithm was quantified by efficiency *e*, uniformity *u*, and percent standard deviation *


$e = \sum_{m}{I_m}$
$u = 1 - \frac{max(I_m)-min(I_m)}{max(I_m)+min(I_m)}$
$σ = 100\sqrt{\langle (I - \langle I \rangle)^2 \rangle} / \langle I \rangle $

[^1]: R. Di Leonardo, F. Ianni, and G. Ruocco, "Computer generation of optimal holograms for optical trap arrays," Opt. Express 15, 1913-1922 (2007).

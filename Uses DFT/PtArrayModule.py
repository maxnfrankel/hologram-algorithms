import numpy as np

def PtArrayCoords(npx,npy,px,py):
    # inputs:
        # npx, npy are the number of points in the point array in x and y
        # px, py are the periodicities in x and y of the point array pattern in pixels
        
    # output:
        # trap indicies in form [[x0,x1,x2,...,x_M-1],[y0,y1,...,y_M-1]]

    # we always want a square grid so we should be able to control both the number of pts and the periodicity
    # a square grid should be formed in the center

    # set up indices in x and y direction
    grid_x = np.arange(-npx*px/2,npx*px/2)
    grid_y = np.arange(-npy*py/2,npy*py/2)

    x,y = np.meshgrid(grid_x,grid_y)

    return x,y # trap coordinates in form [x1,x2,x3,...],[y1,y2,y3,...]

import numpy as np

def PtArrayCoords(npx,npy,px,py):
    # inputs:
        # npx, npy are the number of points in the point array in x and y
        # px, py are the periodicities in x and y of the point array pattern in pixels
        
    # output:
        # trap indicies in form [[x0,x1,x2,...,x_M-1],[y0,y1,...,y_M-1]]

    # check if pt array dimensions are even or odd
    lenx = npx*px; leny = npy*py
    is_xOdd = 0
    is_yOdd = 0
    if (lenx%2 == 1):
        is_xOdd = 1
    if (leny%2 == 1):
        is_yOdd = 1
    
    # set up indices in x and y direction
    # indices are set up around the origin, with a point at the origin
    grid_x = np.arange(-npx*px/2,npx*px/2+is_xOdd,px)
    grid_y = np.arange(-npy*py/2,npy*py/2+is_yOdd,py)

    x,y = np.meshgrid(grid_x,grid_y)
    x = x.flatten(); y = y.flatten()

    return x.astype(int),y.astype(int) # trap coordinates in form [x1,x2,x3,...],[y1,y2,y3,...]

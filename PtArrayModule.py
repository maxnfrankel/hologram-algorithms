import numpy as np

def PtArrayCoords(npx,npy,px,py,offs_x=0,offs_y=0):
    # inputs:
        # npx, npy are the number of points in the point array in x and y
        # px, py are the periodicities in x and y of the point array pattern in pixels
        # offs_x, offs_y are the x and y offsets of the patterns
        
    # output:
        # xm,ym which are trap coordinates in form [x0,x1,x2,...,x_M-1],[y0,y1,...,y_M-1], indexed from m=0 to M-1

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
    grid_xm = np.arange(-npx*px/2,npx*px/2+is_xOdd,px)+offs_x
    grid_ym = np.arange(-npy*py/2,npy*py/2+is_yOdd,py)+offs_y

    xm,ym = np.meshgrid(grid_xm,grid_ym)
    xm = xm.flatten(); ym = ym.flatten()

    return xm.astype(int),ym.astype(int) # trap coordinates in form [x1,x2,x3,...],[y1,y2,y3,...]

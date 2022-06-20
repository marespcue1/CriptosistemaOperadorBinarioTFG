from math import sin, cos
import numpy as np
from itertools import product

class ICM2D:

    def __init__(self, a0, b0, x, y, T, C1, C2):

        # Original
        #self.a = (a0 + T * C1) % 5 + 16
        #self.b = (b0 + T * C2) % 5 + 16
        # Modificado
        self.a = (a0 + T * C1)
        self.b = (b0 + T * C2)
        # Original
        #self.x0 = (x + T * C1) % 2 - 1
        #self.y0 = (y + T * C2) % 2 - 1
        # Modificado
        # Comprobar si es 0??
        self.x0 = x + 1
        self.y0 = y + 1

    def iterate(self, times = 1, xPrev = None, yPrev = None):

        if xPrev == None: xPrev = self.x0
        if yPrev == None: yPrev = self.y0

        for _ in range(times):
            xNew = sin(self.a/yPrev) * cos(self.b/xPrev)
            yNew = sin(self.a/xPrev) * cos(self.b/yPrev)
            xPrev = xNew
            yPrev = yNew
        
        self.x0 = xPrev
        self.y0 = yPrev
        return (xPrev,yPrev)

    def expand(self, size, xPrev = None, yPrev = None):
        
        if len(size) == 1:
            res = self.expand1D(size[0], xPrev=xPrev, yPrev=yPrev)

        elif len(size) == 2:
            res = self.expand2D(size[0], size[1], xPrev=xPrev, yPrev=yPrev)

        return res
    
    def expand1D(self, m, xPrev, yPrev):

        vectorX = np.empty(m)
        vectorY = np.empty(m)
        for i in range(m):
            xPrev, yPrev = self.iterate(xPrev=xPrev, yPrev=yPrev)
            vectorX[i] = abs(xPrev)
            vectorY[i] = abs(yPrev)
        
        return (vectorX,vectorY)

    def expand2D(self, m, n, xPrev, yPrev):

        matrixX = np.empty((m,n))
        matrixY = np.empty((m,n))
        for x,y in product(range(m),range(n)):
            xPrev, yPrev = self.iterate(xPrev=xPrev, yPrev=yPrev)
            matrixX[x,y] = abs(xPrev)
            matrixY[x,y] = abs(yPrev)

        return (matrixX,matrixY)


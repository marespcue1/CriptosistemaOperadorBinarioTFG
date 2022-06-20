import numpy as np
import cv2
from math import log10
from collections import Counter

def varianza(img):
    m,n = list(img.shape)[:2]
    flat = img.flatten()
    mu = np.ulonglong(0)
    for elem in flat:
        mu+=elem/len(flat)
    res = np.ulonglong(0)
    for pixel in flat:
        res += (pixel-mu)**2/(m*n)
    #return sum([(pixel-mu)**2 for pixel in flat])/(m*n)
    return res

def entropia(img):
    flat = img.flatten()
    prob = Counter(flat)
    suma =  np.ulonglong(0)
    for i in prob:
        suma +=  (prob[i]/len(flat))*(log10(1/(prob[i]/len(flat))))
    return suma
     
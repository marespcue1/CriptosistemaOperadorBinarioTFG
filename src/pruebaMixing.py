from math import floor, ceil
import numpy as np
from funcionesCripto import *
import Criptosistema
from random import random
import hashlib
import ICM



# 4 iter
#img = np.array([[1,2,3],[4,5,6],[7,8,9]])
# 3 iter
#img = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
# 5 iter
#img = np.array([[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]])

#img = np.array([[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]])

#img = np.array([[1,2,3,4,5,6],[7,8,9,10,11,12],[13,14,15,16,17,18],[19,20,21,22,23,24]])

img = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],[16,17,18],[17,18,19],[20,21,22],[23,24,25],[26,27,28],[29,30,31],[32,33,34],[35,36,37],[38,39,40]])
img = np.transpose(img)
p = 8

import cv2
img_path = 'Imagenes/Asus.PNG'
print('Lectura')
if img_path[-4:] == '.dcm':
    pass
else:
    img = cv2.imread(img_path)
    if True:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if len(img.shape) == 2:
        first_pixel = (0,0)
        m, n = img.shape
        c = 1
    elif len(img.shape) == 3:
        first_pixel = (0,0,0)
        m, n, c = img.shape
    else:
        raise 'Formato de imagen desconocido.'

print(img)
antes_acm = modified_ACM(img, p)

#antes_mix = mixing(antes_acm, p)

# --------------------------------

#despues_mix = demixing(antes_mix, p)

despues_acm = decript_modified_ACM(antes_acm, p)

print(img)
print(despues_acm)
print(str(despues_acm) == str(img))
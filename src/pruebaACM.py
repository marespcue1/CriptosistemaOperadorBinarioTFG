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
key = '1234'

print(img)
# Gestión de clave
if key == None:
    #imprime('Generación de clave')

    randomKey = format(random.getrandbits(240),'b')
    #imprime(randomKey)
    #imprime(hex(int(randomKey, 2)))
else:
    #imprime('Tratamiento de clave')
    randomKey = hashlib.sha256(key.encode()).hexdigest()
    #imprime(randomKey)
    randomKey = bin(int(randomKey, 16))[2:].zfill(len(randomKey)*4)[0:240]
    #imprime(randomKey)

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
        raise "Formato de imagen desconocido."

# Inicio de mapa caótico
a0, b0, x, y, T, C1, C2 = int(randomKey[0:40],2), int(randomKey[40:80],2), int(randomKey[80:120],2), int(randomKey[120:160],2),int(randomKey[160:200],2),int(randomKey[200:220],2), int(randomKey[220:240],2)

print('Generación de mapa')

m, n = img.shape
p=8
mapa = ICM.ICM2D(a0, b0, x, y, T, C1, C2)
cipher_image = np.empty((img.shape), dtype='uint8')



print('Generación de vector inicial')
cIV = get_initial_vector(mapa, m, p)
print('Generación de Rule Map 1')
cRM1 = get_ruleMap(mapa, m, n, p)
print('Generación de Rule Map 2')
cRM2 = get_ruleMap(mapa, m, n, p)
#imprime(str(globales.GLOBRM2) == str(RM2))
#imprime('a0, b0 = ' + str((mapa.x0, mapa.y0)))

print('Obtención del mapa de sustitución de ADN')
cDSM = get_DNA_substitution_map(mapa, cRM2, m, n, p)
#imprime(str(globales.GLOBDSM) == str(DSM))
#imprime('a0, b0 = ' + str((mapa.x0, mapa.y0)))

print('Obtención de Rule Map 3')
cRM3 = get_ruleMap(mapa, m, n, p)
#imprime(str(globales.GLOBRM3) == str(RM3))
#imprime('a0, b0 = ' + str((mapa.x0, mapa.y0)))

print('Obtención de Rule Map 4')
cRM4 = get_ruleMap(mapa, m, n, p)

print('Mezclado de filas')
cimg_mixedRows = mix_rows(img, cIV, p)

print('ACM modificado')
cimg_ACM = modified_ACM(cimg_mixedRows, p)

print('Mezclado de la imagen')
cimg_mixed = mixing(cimg_ACM, p)

print('Codificado de ADN')
cimg_encoded = dna_encoding(cimg_mixed, p, cRM1)

print('Sustitución de ADN')
cimg_substitution = substitution(cimg_encoded, cDSM, cRM3)

print('Decodificación de ADN')
cdna_decoded = dna_decoding(cimg_substitution, m, n, p, cRM4)  

print('Fin codific')
print(cdna_decoded)


 # -----------------------------------------------------------

print('Generación de mapa')

m, n = img.shape
p=8
mapa = ICM.ICM2D(a0, b0, x, y, T, C1, C2)

print('Generación de vector inicial')
dIV = get_initial_vector(mapa, m, p)
print(str(cIV) == str(dIV))

print('Generación de Rule Map 1')
dRM1 = get_ruleMap(mapa, m, n, p)
print(str(cRM1) == str(dRM1))

print('Generación de Rule Map 2')
dRM2 = get_ruleMap(mapa, m, n, p)
print(str(cRM2) == str(dRM2))

#imprime(str(globales.GLOBRM2) == str(RM2))
#imprime('a0, b0 = ' + str((mapa.x0, mapa.y0)))

print('Obtención del mapa de sustitución de ADN')
dDSM = get_DNA_substitution_map(mapa, dRM2, m, n, p)
print(str(cDSM) == str(dDSM))

print('Obtención de Rule Map 3')
dRM3 = get_ruleMap(mapa, m, n, p)
print(str(dRM3) == str(cRM3))

print('Obtención de Rule Map 3')
dRM4 = get_ruleMap(mapa, m, n, p)
print(str(cRM4) == str(dRM4))

print('Codificado de ADN')
dimg_encoded = dna_encoding(cdna_decoded, p, dRM4)
print(str(dimg_encoded) == str(cimg_substitution))

print('Sustitución de ADN')
dimg_substitution = desubstitution(dimg_encoded, dDSM, dRM3)
print(str(dimg_substitution) == str(cimg_encoded))

print('Decodificación de ADN')
ddna_decoded = dna_decoding(dimg_substitution, m, n, p, dRM1) 
print(str(ddna_decoded) == str(cimg_mixed))

print('Mezclado de la imagen')
dimg_mixed = demixing(ddna_decoded, p)  
print(str(dimg_mixed) == str(cimg_ACM))  

print('ACM modificado')
dimg_ACM = decript_modified_ACM(dimg_mixed, p)
print(str(dimg_ACM) == str(cimg_mixedRows)) 

print('Mezclado de filas')
dimg_mixedRows = demix_rows(dimg_ACM, dIV, p)
print(str(dimg_mixedRows) == str(img)) 

print('final')
print(dimg_mixedRows)
print(str(dimg_mixedRows) == str(img))



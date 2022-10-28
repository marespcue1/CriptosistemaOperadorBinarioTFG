import random
import numpy as np
import cv2
import hashlib
from matplotlib import pyplot as plt
from copy import deepcopy
import pydicom as dicom
from funcionesCripto import *
from collections import Counter
from funcionesEstadisticas import *
import sys

import ICM

def imprime(cont):
    print(cont)
    sys.stdout.flush()

colorHist = {0:'blue',1:'green',2:'red'}

def cifrado(img_path, key = None, savePath = 'cipherImage.png', grey_scale = True, path_intermedios = ''):

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

    # Inicio de mapa caótico
    a0, b0, x, y, T, C1, C2 = int(randomKey[0:40],2), int(randomKey[40:80],2), int(randomKey[80:120],2), int(randomKey[120:160],2),int(randomKey[160:200],2),int(randomKey[200:220],2), int(randomKey[220:240],2)

    imprime('Generación de mapa')
    
    mapa = ICM.ICM2D(a0, b0, x, y, T, C1, C2)

    histogramas = list()
    ochoBit = True
    
    #Lectura
    imprime('Lectura')
    if img_path[-4:] == '.dcm':
        ochoBit = False
        ds = dicom.dcmread(img_path)
        img = ds.pixel_array
        if len(img.shape) == 2:
            first_pixel = (0,0)
            m, n = img.shape
            c = 1
        elif len(img.shape) == 3:
            first_pixel = (0,0,0)
            m, n, c = img.shape
        else:
            raise "Formato de imagen desconocido."
    else:
        img = cv2.imread(img_path)
        if grey_scale:
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
    
    #imprime('ORIGINAL')
    #imprime(img)
    varorig = varianza(img)
    entorig = entropia(img)
    imprime('Varianza original: ' + str(varorig))
    imprime('Entropía original: ' + str(entorig))

    if str(type(img[first_pixel])) == '<class \'numpy.uint8\'>':
        p = 8
        img_type = 'uint8'
    elif str(type(img[first_pixel])) == '<class \'numpy.uint16\'>':
        p = 16
        img_type = 'uint16'
    else:
        raise "Los pixeles no son de 8 o 16 bits."

    
    cipher_image = np.empty((img.shape), dtype=img_type)

    if grey_scale or (not grey_scale and not ochoBit):
        contador = Counter(img.flatten())
        plt.bar(contador.keys(), contador.values(), 1.0, color='b')
        plt.savefig('salidas/' + str(path_intermedios) + '/HistCifrado.png')
        plt.clf()

    else:
        plt.clf()
        for i in range(c):
            canal = img[:,:,i]
            contador = Counter(canal.flatten())
            plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/HistCifrado.png')
        plt.clf()
    
    if img_path[-4:] == '.dcm':
        plt.imshow(ds.pixel_array, cmap=plt.cm.bone)  
        plt.savefig('salidas/' + str(path_intermedios) + '/original.png')  
        plt.clf()
    else:
        cv2.imwrite('salidas/' + str(path_intermedios) + '/original.png', img)
        plt.clf()       

    # Por cada capa de la imagen se ejecuta el algoritmo
    for i in range(c):
        imprime('Canal ' + str(i+1) + ' de ' + str(c))
        if c == 1:
            channel = img[:,:]
        else:
            channel = img[:,:,i]

        imprime('Generación de vector inicial')
        IV = get_initial_vector(mapa, m, p)

        imprime('Generación de Rule Map 1')
        RM1 = get_ruleMap(mapa, m, n, p)

        imprime('Generación de Rule Map 2')
        RM2 = get_ruleMap(mapa, m, n, p)

        imprime('Obtención del mapa de sustitución de ADN')
        DSM = get_DNA_substitution_map(mapa, RM2, m, n, p)

        imprime('Mezclado de filas')
        img_mixedRows = mix_rows(channel, IV, p)
        contador = Counter(img_mixedRows.flatten())
        plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/CifHistPaso1Canal' + str(i+1) + 'MezcladoFilas.png')
        plt.clf()
        if img_path[-4:] == '.dcm':
            ds2 = deepcopy(ds)
            ds2.PixelData = img_mixedRows.tobytes()
            ds2.save_as('salidas/' + str(path_intermedios) + '/CifPaso1Canal' + str(i+1) + 'MezcladoFilas.dcm')
            plt.imshow(ds2.pixel_array, cmap=plt.cm.bone)  
            plt.savefig('salidas/' + str(path_intermedios) + '/CifPaso1Canal' + str(i+1) + 'MezcladoFilas.png')  
            plt.clf()

        else:
            cv2.imwrite('salidas/' + str(path_intermedios) + '/CifPaso1Canal' + str(i+1) + 'MezcladoFilas.png', img_mixedRows)

        imprime('ACM modificado')
        img_ACM = modified_ACM(img_mixedRows, p)
        contador = Counter(img_ACM.flatten())
        plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/CifHistPaso2Canal' + str(i+1) + 'ACM.png')
        plt.clf()
        if img_path[-4:] == '.dcm':
            ds2 = deepcopy(ds)
            ds2.PixelData = img_ACM.tobytes()
            ds2.save_as('salidas/' + str(path_intermedios) + '/CifPaso2Canal' + str(i+1) + 'ACM.dcm')
            plt.imshow(ds2.pixel_array, cmap=plt.cm.bone)  
            plt.savefig('salidas/' + str(path_intermedios) + '/CifPaso2Canal' + str(i+1) + 'ACM.png')  
            plt.clf()
        else:
            cv2.imwrite('salidas/' + str(path_intermedios) + '/CifPaso2Canal' + str(i+1) + 'ACM.png', img_ACM)
            plt.clf()

        imprime('Mezclado de la imagen')
        img_mixed = mixing(img_ACM, p)
        contador = Counter(img_mixed.flatten())
        plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/CifHistPaso3Canal' + str(i+1) + 'Mezclado.png')
        plt.clf()
        if img_path[-4:] == '.dcm':
            ds2 = deepcopy(ds)
            ds2.PixelData = img_mixed.tobytes()
            ds2.save_as('salidas/' + str(path_intermedios) + '/CifPaso3Canal' + str(i+1) + 'Mezclado.dcm')
            plt.imshow(ds2.pixel_array, cmap=plt.cm.bone)  
            plt.savefig('salidas/' + str(path_intermedios) + '/CifPaso3Canal' + str(i+1) + 'Mezclado.png')  
            plt.clf()
        else:
            cv2.imwrite('salidas/' + str(path_intermedios) + '/CifPaso3Canal' + str(i+1) + 'Mezclado.png', img_mixed)
            plt.clf()

        imprime('Codificado de ADN')
        img_encoded = dna_encoding(img_mixed, p, RM1)

        imprime('Obtención de Rule Map 3')
        RM3 = get_ruleMap(mapa, m, n, p)
        
        imprime('Sustitución de ADN')
        img_substitution = substitution(img_encoded, DSM, RM3)

        imprime('Obtención de Rule Map 4')
        RM4 = get_ruleMap(mapa, m, n, p)
        
        imprime('Decodificación de ADN')
        dna_decoded = dna_decoding(img_substitution, m, n, p, RM4)  
        contador = Counter(dna_decoded.flatten())
        histogramas.append(contador)
        plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/CifHistPaso4Canal' + str(i+1) + 'ADN.png')
        plt.clf()  
        if img_path[-4:] == '.dcm':
            ds2 = deepcopy(ds)
            ds2.PixelData = dna_decoded.tobytes()
            ds2.save_as('salidas/' + str(path_intermedios) + '/CifPaso4Canal' + str(i+1) + 'ADN.dcm')
            plt.imshow(ds2.pixel_array, cmap=plt.cm.bone)  
            plt.savefig('salidas/' + str(path_intermedios) + '/CifPaso4Canal' + str(i+1) + 'ADN.png')    
            plt.clf()
        else:
            cv2.imwrite('salidas/' + str(path_intermedios) + '/CifPaso4Canal' + str(i+1) + 'ADN.png', dna_decoded)
            plt.clf()
        
        
        if c > 1:
            cipher_image[:,:,i] = dna_decoded
        else:
            cipher_image = dna_decoded
        
    if not grey_scale:
        i = 0
        plt.clf()
        for hist in histogramas:
            plt.bar(hist.keys(), hist.values(), 1.0, color=colorHist[i])
            i+=1
        plt.savefig('salidas/' + str(path_intermedios) + '/CifHistFinal.png')  

    if img_path[-4:] == '.dcm':
        ds2 = deepcopy(ds)
        ds2.PixelData = cipher_image.tobytes()
        ds2.save_as(savePath)
        
    else:
        cv2.imwrite(savePath, cipher_image)

    return cipher_image

# DESCIFRADO -----------------------------------------------------------------------


def descifrado(img_path, key, savePath = 'planeImage.png', grey_scale = True, path_intermedios = ''):
    
    histogramas = list()

    imprime('Procesado de clave')
    randomKey = hashlib.sha256(key.encode()).hexdigest()
    randomKey = bin(int(randomKey, 16))[2:].zfill(len(randomKey)*4)[0:240]

    a0, b0, x, y, T, C1, C2 = int(randomKey[0:40],2), int(randomKey[40:80],2), int(randomKey[80:120],2), int(randomKey[120:160],2),int(randomKey[160:200],2),int(randomKey[200:220],2), int(randomKey[220:240],2)
    
    
    imprime('Generación de mapa')
    
    mapa = ICM.ICM2D(a0, b0, x, y, T, C1, C2)
    
    ochoBit = False
    imprime('Lectura')
    if img_path[-4:] == '.dcm':
        ds = dicom.dcmread(img_path)
        img = ds.pixel_array
        if len(img.shape) == 2:
            first_pixel = (0,0)
            m, n = img.shape
            c = 1
        elif len(img.shape) == 3:
            first_pixel = (0,0,0)
            m, n, c = img.shape
        else:
            raise "Formato de imagen desconocido."
    else:
        ochoBit = True
        img = cv2.imread(img_path)
        if grey_scale:
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
    
    varorig = varianza(img)
    entorig = entropia(img)
    imprime('Varianza cifrado: ' + str(varorig))
    imprime('Entropía cifrado: ' + str(entorig))

    if str(type(img[first_pixel])) == '<class \'numpy.uint8\'>':
        p = 8
    elif str(type(img[first_pixel])) == '<class \'numpy.uint16\'>':
        p = 16
    else:
        raise "Los pixeles no son de 8 o 16 bits."

    planeImage = np.empty((img.shape), dtype='uint'+str(p))

    if grey_scale or (not grey_scale and not ochoBit):
        contador = Counter(img.flatten())
        plt.bar(contador.keys(), contador.values(), 1.0, color='b')
        plt.savefig('salidas/' + str(path_intermedios) + '/HistCifrado.png')
        plt.clf()

    else:
        plt.clf()
        for i in range(c):
            canal = img[:,:,i]
            contador = Counter(canal.flatten())
            plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/HistCifrado.png')
        plt.clf()

    if ochoBit:
        cv2.imwrite('salidas/' + str(path_intermedios) + '/Original.png', img)
        plt.clf()
    else:
        plt.imshow(ds.pixel_array, cmap=plt.cm.bone)  
        plt.savefig('salidas/' + str(path_intermedios) + '/Original.png') 

    for i in range(c):
        imprime('Canal ' + str(i+1) + ' de ' + str(c))
        if c == 1:
            channel = img[:,:]
        else:
            channel = img[:,:,i]

        imprime('Generación de vector inicial')
        IV = get_initial_vector(mapa, m, p)

        imprime('Generación de Rule Map 1')
        RM1 = get_ruleMap(mapa, m, n, p)

        imprime('Generación de Rule Map 2')
        RM2 = get_ruleMap(mapa, m, n, p)

        imprime('Obtención del mapa de sustitución de ADN')
        DSM = get_DNA_substitution_map(mapa, RM2, m, n, p)

        imprime('Obtención de Rule Map 3')
        RM3 = get_ruleMap(mapa, m, n, p)

        imprime('Obtención de Rule Map 4')
        RM4 = get_ruleMap(mapa, m, n, p)


        # Para deshacer los pasos de codificar y descodificar en ADN, vale con usar el mismo RM
        imprime('Codificado de ADN')
        img_encoded = dna_encoding(channel, p, RM4)
        
        # Para deshacer hacer la desubstitución se ha tenido que crear otra función especifica que usa
        # el mismo RM y DSM
        imprime('Sustitución de ADN')
        img_substitution = desubstitution(img_encoded, DSM, RM3)

        imprime('Decodificación de ADN')
        dna_decoded = dna_decoding(img_substitution, m, n, p, RM1) 
        contador = Counter(dna_decoded.flatten())
        plt.clf()
        plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/DescifHistPaso1Canal' + str(i+1) + 'ADN.png') 
        plt.clf()  
        if ochoBit:
            cv2.imwrite('salidas/' + str(path_intermedios) + '/DescifPaso1Canal' + str(i+1) + 'ADN.png', dna_decoded)
        else:
            ds2 = deepcopy(ds)
            ds2.PixelData = dna_decoded.tobytes()
            ds2.save_as('salidas/' + str(path_intermedios) + '/DescifPaso1Canal' + str(i+1) + 'ADN.dcm')
            plt.imshow(ds2.pixel_array, cmap=plt.cm.bone)  
            plt.savefig('salidas/' + str(path_intermedios) + '/DescifPaso1Canal' + str(i+1) + 'ADN.png') 
        plt.clf()

        
        imprime('Mezclado de la imagen')
        img_mixed = demixing(dna_decoded, p)
        contador = Counter(img_mixed.flatten())
        plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/DescifHistPaso2Canal' + str(i+1) + 'Mezclado.png')
        plt.clf() 
        if ochoBit:
            cv2.imwrite('salidas/' + str(path_intermedios) + '/DescifPaso2Canal' + str(i+1) + 'Mezclado.png', img_mixed)
            plt.clf() 
        else:
            ds2 = deepcopy(ds)
            ds2.PixelData = img_mixed.tobytes()
            ds2.save_as('salidas/' + str(path_intermedios) + '/DescifPaso2Canal' + str(i+1) + 'Mezclado.dcm')
            plt.imshow(ds2.pixel_array, cmap=plt.cm.bone)  
            plt.savefig('salidas/' + str(path_intermedios) + '/DescifPaso2Canal' + str(i+1) + 'Mezclado.png')
            plt.clf() 
        
        imprime('ACM modificado')
        img_ACM = decript_modified_ACM(img_mixed, p)
        contador = Counter(img_ACM.flatten())
        plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/DescifHistPaso3Canal' + str(i+1) + 'ACM.png') 
        if ochoBit:
            cv2.imwrite('salidas/' + str(path_intermedios) + '/DescifPaso3Canal' + str(i+1) + 'ACM.png', img_ACM)
        else:
            ds2 = deepcopy(ds)
            ds2.PixelData = img_ACM.tobytes()
            ds2.save_as('salidas/' + str(path_intermedios) + '/DescifPaso3Canal' + str(i+1) + 'ACM.dcm')
            plt.imshow(ds2.pixel_array, cmap=plt.cm.bone)  
            plt.savefig('salidas/' + str(path_intermedios) + '/DescifPaso3Canal' + str(i+1) + 'ACM.png') 
            plt.clf()

        imprime('Mezclado de filas')
        img_mixedRows = demix_rows(img_ACM, IV, p)
        contador = Counter(img_mixedRows.flatten())
        histogramas.append(contador)
        plt.clf()
        plt.bar(contador.keys(), contador.values(), 1.0, color=colorHist[i])
        plt.savefig('salidas/' + str(path_intermedios) + '/DescifHistPaso4Canal' + str(i+1) + 'MecladoFilas.png') 
        plt.clf()    
        if ochoBit:
            cv2.imwrite('salidas/' + str(path_intermedios) + '/DescifPaso4Canal' + str(i+1) + 'MecladoFilas.png', img_mixedRows)
        else:
            ds2 = deepcopy(ds)
            ds2.PixelData = img_mixedRows.tobytes()
            ds2.save_as('salidas/' + str(path_intermedios) + '/DescifPaso4Canal' + str(i+1) + 'MecladoFilas.dcm')
            plt.imshow(ds2.pixel_array, cmap=plt.cm.bone)  
            plt.savefig('salidas/' + str(path_intermedios) + '/DescifPaso4Canal' + str(i+1) + 'MecladoFilas.png') 
            plt.clf()

        if c > 1:
            planeImage[:,:,i] = img_mixedRows
        else:
            planeImage = img_mixedRows

    if not grey_scale:
        i = 0
        plt.clf()
        for hist in histogramas:
            plt.bar(hist.keys(), hist.values(), 1.0, color=colorHist[i])
            i+=1
        plt.savefig('salidas/' + str(path_intermedios) + '/DescifHistFinal.png')  
            

    if ochoBit:
        cv2.imwrite(savePath, planeImage)
    else:
        ds2 = deepcopy(ds)
        ds2.PixelData = planeImage.tobytes()
        ds2.save_as(savePath)

    return planeImage

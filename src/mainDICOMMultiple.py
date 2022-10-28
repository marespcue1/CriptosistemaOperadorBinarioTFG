#pip install pydicom

from collections import defaultdict
import pydicom as dicom
import Criptosistema
from datetime import datetime
from funcionesEstadisticas import *
import os
import csv
from pynput import keyboard
from copy import deepcopy
import time

break_program = False
def on_press(key):
    global break_program
    if key == keyboard.Key.alt_l:
        print ('end pressed')
        break_program = True
        return False

dictTam = defaultdict(int)

with keyboard.Listener(on_press=on_press) as listener:
    files = list()
    folders = list()
    for (path, dirnames, filenames) in os.walk('ImagenesCOVID'):
        #folders.extend(os.path.join(path, name) for name in dirnames)
        files.extend(os.path.join(path, name) for name in filenames)

    #print(files)
    #print(folders)
    with open('tablaVarianza3.csv','w') as fileV, open('tablaEntropia3.csv','w') as fileE, open('tablaTiempo2.csv','r') as fileT:
        #fileE.flush(); fileV.flush(); 
        fileE.flush()
        fileV.flush()
        csvwriterE = csv.writer(fileE)
        csvwriterV = csv.writer(fileV)
        csvreaderT = csv.reader(fileT)
        csvwriterE.writerow(['Path','forma','entropia original','entropia cifrado'])
        csvwriterV.writerow(['Path','forma','varianza original','varianza cifrado'])
        primero = True
        paths = list()
        for line in csvreaderT:
            if primero:
                primero = False
                continue
            paths.append(line[0])
        #csvwriterT.writerow(['Path','forma','Tiempo para encriptar'])
        i = 1
        for image_path in files:
            print(str(i) + ' de ' + str(len(files)))
            #image_path = 'ImagenesCOVID/manifest-1594658036421/COVID-19-AR/COVID-19-AR-16406498/02-22-2012-NA-CT CHEST W CONTRAST-94020/80328.000000-MPR CORONALS Coronal-36788/1-001.dcm'
            print(image_path)
            image_path_splited = '\/'.join(str(image_path).split('\\')[-3:])
            print( str(image_path_splited))
            if not image_path_splited in paths:
                continue

            ds = dicom.dcmread(image_path)

            img = ds.pixel_array

            varorig = varianza(img)
            print(varorig)
            entorig = entropia(img)
            print(entorig)

            if str(type(img[0,0])) == '<class \'numpy.uint8\'>':
                print('8 BITS')
                p = 8
                img_type = 'uint8'
            elif str(type(img[0,0])) == '<class \'numpy.uint16\'>':
                print('16 BITS')
                p = 16
                img_type = 'uint16'
            
            print('Forma: ' + str(img.shape))
            m,n = img.shape
            if dictTam[str(img.shape)] > 3:
                i+=1
                continue
            else:
                i+=1
                dictTam[str(img.shape)]+=3
            print(dictTam)
            #if m>2096 or n>2096:
                #    i+=1
                #    continue

            #startC = datetime.now()
            #startC =  time.time()
            startC = time.process_time()
            #cifrado = Criptosistema.cifrado('Imagenes/00008058_001.png', key='1234', grey_scale = True)
            cifrado = Criptosistema.cifrado(image_path, key='1234', savePath='cipher.dcm', grey_scale = False)
            #endC = datetime.now()
            #endC = time.time()
            endC = time.process_time()

            print('Forma: ' + str(cifrado.shape))
            #print(cifrado)
            print(cifrado.shape)
            print(type(cifrado[0,0]))

            
            print("The time of execution of above program is :",
                str(endC-startC)[5:])
            #startD = datetime.now()

            varcif = varianza(cifrado)
            print(varcif)
            entcif = entropia(cifrado)
            print(entcif)

            descifrado = Criptosistema.descifrado('cipher.dcm', '1234', grey_scale = True)

            print('Forma: ' + str(descifrado.shape))
            print(descifrado)
            if str(descifrado)!=str(img):
                break

            #endD = datetime.now()
            #print("The time of execution of above program is :",
            #    str(endD-startD)[5:])
            #csvwriterV.writerow([str(image_path_splited),str(cifrado.shape),str(varorig), str(varcif)])
            #csvwriterE.writerow([str(image_path_splited),str(cifrado.shape),str(entorig), str(entcif)])
            #csvwriterT.writerow([str(image_path_splited),str(cifrado.shape),str(endC-startC)[5:]])
            ds2 = deepcopy(cifrado)
            ds2.PixelData = cifrado.tobytes()
            ds2.save_as('image' + str(i) + '.dcm')

            if break_program:
                break

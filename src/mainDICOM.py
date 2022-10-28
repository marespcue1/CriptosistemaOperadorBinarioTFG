#pip install pydicom

import pydicom as dicom
import Criptosistema
from datetime import datetime
from funcionesEstadisticas import *
from matplotlib import pyplot as plt
from collections import Counter

#print(files)
#print(folders)

#image_path = 'C:/Users/M/Desktop/US/Cuarto/tfg/Proyecto/ImagenesCOVID/manifest-1594658036421/COVID-19-AR/COVID-19-AR-16406488/01-15-2012-NA-XR CHEST AP ONLY-24124/1001.000000-NA-00046/1-1.dcm'
image_path = 'C:/Users/M/Desktop/US/Cuarto/tfg/Proyecto/ImagenesCOVID/manifest-1594658036421/COVID-19-AR/COVID-19-AR-16406488/02-14-2012-NA-CT PE CHEST-63916/2.000000-locator-16446/1-1.dcm'
#image_path = 'C:/Users/M/Desktop/US/Cuarto/tfg/Proyecto/ImagenesCOVID/manifest-1594658036421/COVID-19-AR/COVID-19-AR-16445168/03-03-2012-NA-XR CHEST AP PORTABLE-10344/1.000000-AP-57553/1-1.dcm'
startC = datetime.now()
ds = dicom.dcmread(image_path)

img = ds.pixel_array
print(img.shape)

varorig = varianza(img)
entorig = entropia(img)

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

print(img)
plt.imshow( img, cmap=plt.cm.bone)
plt.show()
#plt.hist(img.ravel(),2**p,[0,2**p]); plt.show()

c = Counter(img.flatten())
menos = 0
mas = 0
for elem in c:
    if elem >255: mas+=c[elem]
    else: menos +=c[elem]
print(menos)
print(mas)

plt.bar(c.keys(), c.values(), 1.0, color='g')
plt.savefig('salidas/Horiginal.png')
plt.show()

#cifrado = Criptosistema.cifrado('Imagenes/00008058_001.png', key='1234', grey_scale = True)
cifrado = Criptosistema.cifrado(image_path, key='1234', savePath='cipher.dcm', grey_scale = False)

print('Forma: ' + str(cifrado.shape))
#print(cifrado)
print(cifrado.shape)
print(type(cifrado[0,0]))
plt.imshow( cifrado, cmap=plt.cm.bone)
plt.show()
c = Counter(cifrado.flatten())
plt.bar(c.keys(), c.values(), 1.0, color='g')
plt.savefig('salidas/Hcifrado.png')
plt.show()


endC = datetime.now()
print("The time of execution of above program is :",
    str(endC-startC)[5:])
startD = datetime.now()

varcif = varianza(cifrado)
entcif = entropia(cifrado)

descifrado = Criptosistema.descifrado('cipher.dcm', '1234', grey_scale = True)

print('Forma: ' + str(descifrado.shape))
#print(descifrado)
print('Es correcto?: ' + str(str(descifrado)==str(img)))
plt.imshow(descifrado, cmap=plt.cm.bone)
plt.show()
c = Counter(descifrado.flatten())
plt.bar(c.keys(), c.values(), 1.0, color='g')
plt.savefig('salidas/Hdescifrado.png')
plt.show()

endD = datetime.now()
print("The time of execution of above program is :",
    str(endD-startD)[5:])

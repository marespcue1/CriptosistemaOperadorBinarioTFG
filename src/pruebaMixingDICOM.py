from ctypes.wintypes import LONG
import Criptosistema
import pydicom as dicom
import numpy as np
import sys

a = np.ulonglong(40319)
b = np.ulonglong(59682)
c = np.ulonglong(1)
#print(a+c)
#print(b+c)
#print(np.multiply((a+c),(b+c)))
p = np.ulonglong(65537)
#print(type(a))
#print(type(1<<31))
#print(sys.maxsize)

print( (np.multiply((a+1) , (b+1)) % p) - 1 )
image_path = 'ImagenesCOVID/manifest-1594658036421/COVID-19-AR/COVID-19-AR-16406498/02-22-2012-NA-CT CHEST W CONTRAST-94020/80328.000000-MPR CORONALS Coronal-36788/1-001.dcm'


ds = dicom.dcmread(image_path)

img = ds.pixel_array
print(img)

mixed = Criptosistema.mixing(img, 16)

print(mixed)

demixed = Criptosistema.demixing(mixed, 16)

print(demixed)
print(str(mixed) == str(demixed))

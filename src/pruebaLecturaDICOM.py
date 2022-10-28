import pydicom as dicom
import matplotlib.pylab as plt
import numpy as np
import os
from copy import deepcopy
from collections import Counter

image_path = 'ImagenesCOVID/manifest-1594658036421/COVID-19-AR/COVID-19-AR-16406488/02-14-2012-NA-CT PE CHEST-63916/1.000000-SCOUT-04116/1-1.dcm'


ds = dicom.dcmread(image_path)

print(ds.PixelData)
print(ds.pixel_array)
print(ds)

arr = ds.pixel_array
ds2 = deepcopy(ds)
ds2.PixelData = arr.tobytes()
ds2.save_as("temp.dcm")

print(ds2.PixelData)
print(ds2.pixel_array)
print(ds2)

print()
plt.imshow(ds.pixel_array, cmap=plt.cm.bone)  # set the color map to bone
plt.show()

folders = list()
files = list()
for (path, dirnames, filenames) in os.walk('ImagenesCOVID'):
    folders.extend(os.path.join(path, name) for name in dirnames)
    files.extend(os.path.join(path, name) for name in filenames)
    
for file in files:
    ds = dicom.dcmread(file)
    tam = (ds.pixel_array.shape)
    if tam==(1760, 1760):
        print(path)
        plt.imshow(ds.pixel_array, cmap=plt.cm.bone)  # set the color map to bone
        plt.show()
        c = Counter(ds.pixel_array.flatten())
        plt.bar(c.keys(), c.values(), 1.0, color='g');plt.show()
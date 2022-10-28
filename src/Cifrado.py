import CriptosistemaInterfaz
from funcionesEstadisticas import *
import sys

#imprime(files)
#imprime(folders)
def imprime(cont):
    print(cont)
    sys.stdout.flush()

#image_path = 'C:/Users/M/Desktop/US/Cuarto/tfg/Proyecto/ImagenesCOVID/manifest-1594658036421/COVID-19-AR/COVID-19-AR-16406488/01-15-2012-NA-XR CHEST AP ONLY-24124/1001.000000-NA-00046/1-1.dcm'
#image_path = 'C:/Users/M/Desktop/US/Cuarto/tfg/Proyecto/ImagenesCOVID/manifest-1594658036421/COVID-19-AR/COVID-19-AR-16406488/02-14-2012-NA-CT PE CHEST-63916/2.000000-locator-16446/1-1.dcm'
#image_path = 'C:/Users/M/Desktop/US/Cuarto/tfg/Proyecto/ImagenesCOVID/manifest-1594658036421/COVID-19-AR/COVID-19-AR-16445168/03-03-2012-NA-XR CHEST AP PORTABLE-10344/1.000000-AP-57553/1-1.dcm'
image_path = 'C:/Users/M/Desktop/Carpeta/proyectoTFG/1-1.dcm'
grey_scale = True
contrasenya = 'abWccFOf'
savePath = 'cipher.png'
path_intermedios = 'abcdef'

"""image_path = sys.argv[1]
contrasenya = sys.argv[2]
savePath = sys.argv[3]
grey_scale = int(sys.argv[4])
path_intermedios = sys.argv[5]"""


#cifrado = Criptosistema.cifrado('Imagenes/00008058_001.png', key='1234', grey_scale = True)
cifrado = CriptosistemaInterfaz.cifrado(image_path, key=contrasenya, savePath=savePath, grey_scale = grey_scale, path_intermedios = path_intermedios)

varcif = varianza(cifrado)
entcif = entropia(cifrado)
imprime('Varianza cifrado: ' + str(varcif))
imprime('Entropía cifrado: ' + str(entcif))


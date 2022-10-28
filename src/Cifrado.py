import CriptosistemaInterfaz
from funcionesEstadisticas import *
import sys

#imprime(files)
#imprime(folders)
def imprime(cont):
    print(cont)
    sys.stdout.flush()

image_path = sys.argv[1]
contrasenya = sys.argv[2]
savePath = sys.argv[3]
grey_scale = int(sys.argv[4])
path_intermedios = sys.argv[5]


#cifrado = Criptosistema.cifrado('Imagenes/00008058_001.png', key='1234', grey_scale = True)
cifrado = CriptosistemaInterfaz.cifrado(image_path, key=contrasenya, savePath=savePath, grey_scale = grey_scale, path_intermedios = path_intermedios)

varcif = varianza(cifrado)
entcif = entropia(cifrado)
imprime('Varianza cifrado: ' + str(varcif))
imprime('Entropía cifrado: ' + str(entcif))


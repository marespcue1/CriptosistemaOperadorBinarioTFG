import Criptosistema
import sys

"""#path = 'Imagenes/blanco.jpg'
path = 'Imagenes/Lena.jpg'
grey_scale = True"""

desencript = int(sys.argv[1]) # Booleano, modo encriptar (0) o desencriptar (1)
path = sys.argv[2] # Ruta de la imagen objetivo
contrasenya = sys.argv[3] # Contraseña que se usa como clave
savePath = sys.argv[4] # Ruta de guardado de la imagen final
grey_scale = int(sys.argv[5]) # Booleano, escala de grises (1) o color (0)

# Ejecución del algoritmo
if not desencript: cifrado = Criptosistema.cifrado(path, contrasenya, savePath=savePath, grey_scale = grey_scale)

else: descifrado = Criptosistema.descifrado(path, contrasenya, savePath=savePath, grey_scale = grey_scale)
# CriptosistemaOperadorBinarioTFG
Código generado para crear el criptosistema para el proyecto del Trabajo de Fin de Grado.
Se incluye también la documentación en Version-Final-TFG.pdf

## Resumen

Con la necesidad de transmitir información por la red, se dan casos donde los datos que se van
a transmitir no deben ser comprendidos por alguien que, accidental o intencionadamente pueda
interceptarlos. 

En este caso, la información a transmitir son imágenes, ya sean imágenes normales
que vemos a diario, o imágenes médicas que deben ser transmitidas entre personal sanitario. Estas imágenes médicas no solo pueden contener radiografías de pacientes, lo cual ya proporciona
mucha información delicada, también existen datos extra relativos al paciente directamente «incrustados» en la propia imagen, por ejemplo nombre, estatura y otros datos de interés médico. 

El objetivo es implementar un algoritmo de cifrado capaz de tratar imágenes naturales y estas imágenes médicas llamadas DICOM (Digital Imaging and Digital Communication In Medicine) que se
codifican en 16-bits. 

El criptosistema propuesto hace uso de distintas herramientas matemáticas
como son las secuencias caóticas, computación basada en ADN y un nuevo operador binario propuesto por un artículo científico reciente (2021) el cual será el punto de partida para implementar
dicho criptosistema. Además, se comprueban empíricamente los resultados de dicho artículo.

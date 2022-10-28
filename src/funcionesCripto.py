from distutils.log import error
from pickletools import uint8
from math import floor, ceil
from cv2 import transform
import numpy as np
import sympy
from matplotlib import pyplot as plt
from copy import deepcopy
import warnings


warnings.filterwarnings("error")

def acm(pixels, n):
    nuevo = np.empty(pixels.shape)
    for j in range(n):
        for i in range(n):
            nuevo[i,j] = pixels[(2*i+j)%n,(i+j)%n]
    return np.array(nuevo)

def des_acm(pixels, n):
    nuevo = np.empty(pixels.shape)
    for j in range(n):
        for i in range(n):
            nuevo[i,j] = pixels[(i-j)%n,(-i+2*j)%n]
    return np.array(nuevo)


def decript_modified_ACM(imgParam, p):
    # Para deshacer el cambio buscamos la inversa de [[2,1],[1,1]] que es [[1,-1],[-1,2]]
    img = deepcopy(imgParam)
    transformed_img = np.empty((img.shape), dtype='uint' + str(p))
    m,n = img.shape
    N = min(img.shape)
    alpha = ceil(max(img.shape)/N)
    print('Cuadrados sobre los que se aplica ACM: ' + str(alpha))
    L = N - (max(img.shape) % N)
    # O es el tamaño de cada superposicion excepto la ultima.
    # No viene en articulo la posibilidad de que la imagen ya sea cuadrada, y aqui se podria dividir por 0
    # Se arregla con un if
    O = floor(L/(alpha - 1)) if alpha != 1 else 0
    k = largest_prime_less_than(int(N/2))
    x0, y0 = (0,0)
    
    def next(i):
        return  (i-1) * (N - O)

    if m > n:
        x0 = m - N
    else:
        y0 = n - N
    
    for i in range(alpha-1,-1,-1):
        print('Alpha nº ' + str(i+1))
        # No se si hay que añadir el -1 del articulo, mirar despues
        Sq = img[x0 : x0 + N, y0 : y0 + N]
        acm_Sq = Sq
        for _ in range(k):
            acm_Sq = des_acm(acm_Sq,N)
        img[x0 : x0 + N, y0 : y0 + N] = np.array(acm_Sq)
        transformed_img[x0 : x0 + N, y0 : y0 + N] = np.array(acm_Sq)
        if m > n:
            #x0 = x0 + N - O
            x0 = next(i)
        else:
            #y0 = x0 + N - O
            y0 = next(i)

    return transformed_img

def get_initial_vector(icm, m, p):
    expandedMapX, expandedMapY = icm.expand([m])

    IV = np.empty(m, dtype='uint'+str(p))

    for i in range(m):
        # Para hacer el modulo hago funcion suelo???? trabaja en 32 bits?
        IV[i] = floor(abs(expandedMapX[i]) * abs(expandedMapY[i]) * ((2**31)-1)) % (2**p)

    return IV


def get_ruleMap(icm, m, n, p):

    expandedMapX, expandedMapY = icm.expand([m,n])
    #RM = np.empty((m*(int(n*(p/2)))))
    RM = list()
    #print(expandedMapX.shape)

    vX = np.empty(m*n)
    vY = np.empty(m*n)

    for i in range(m):
        #count = 1
        for j in range(n):
            #pos = i*n+j
            vX = floor(expandedMapX[i,j] * ((2**31)-1)) % (2**p)
            vY = floor(expandedMapY[i,j] * ((2**31)-1)) % (2**p)
            # La x que es en el articulo????
            for k in range(int(p/4)):
                RM.append((vX % 8) + 1)
                RM.append((vY % 8) + 1)
                vX = floor(vX/8)
                vY = floor(vY/8)
    
    #print(len(RM))
    return np.array(RM, dtype='uint'+str(p))


def get_DNA_substitution_map(icm, RM, m, n, p):

    expandedMapX, expandedMapY = icm.expand([m,n])
    DSM = list()

    for i in range(m):
        count = 0
        for j in range(n):
            #pos = i*n + j
            v = floor(abs(expandedMapX[i,j]) * abs(expandedMapY[i,j]) * ((2**31) - 1)) % (2**p)
            b = format(v, '0'+str(p)+'b')
            #if len(b) % 2 == 1:
            #    b = '0' + b

            k = 0
            while k <= len(b)-2:
                pos = i*(n*(int(p/2))) + count
                d = DNA_TABLE[RM[pos]][b[k:k+2]]
                DSM.append(d)
                count += 1
                k+=2

    return DSM

DNA_TABLE = {1:{'00':'A', '01':'C', '10':'G', '11':'T'},
            2:{'00':'A', '01':'G', '10':'C', '11':'T'},
            3:{'00':'C', '01':'A', '10':'T', '11':'G'},
            4:{'00':'G', '01':'A', '10':'T', '11':'C'},
            5:{'00':'C', '01':'T', '10':'A', '11':'G'},
            6:{'00':'G', '01':'T', '10':'A', '11':'C'},
            7:{'00':'T', '01':'C', '10':'G', '11':'A'},
            8:{'00':'T', '01':'G', '10':'C', '11':'A'}}

DNA_TABLE_DECODE = {1:{'A':'00', 'C':'01', 'G':'10', 'T':'11'},
            2:{'A':'00', 'G':'01', 'C':'10', 'T':'11'},
            3:{'C':'00', 'A':'01', 'T':'10', 'G':'11'},
            4:{'G':'00', 'A':'01', 'T':'10', 'C':'11'},
            5:{'C':'00', 'T':'01', 'A':'10', 'G':'11'},
            6:{'G':'00', 'T':'01', 'A':'10', 'C':'11'},
            7:{'T':'00', 'C':'01', 'G':'10', 'A':'11'},
            8:{'T':'00', 'G':'01', 'C':'10', 'A':'11'}}

# p esta añadido, no includio en articulo
def mix_rows(img, IV, p):
    m,n = img.shape
    if p == 8:
        prime = 257
        imgType = 'uint8'
    elif p == 16:
        prime = 65537
        imgType = 'uint16'
    else:
        error
    mixed_img = np.empty((m,n), dtype=imgType)
    for i in range(m):
        mixed_img[i,0] = image_operator(img[i,0], IV[i], prime)
        for j in range(1,n):
            mixed_img[i,j] = image_operator(img[i,j], mixed_img[i,j-1], prime)
    return mixed_img

def demix_rows(img, IV, p):
    # El inverso del anterior por el pixel cifrado obtiene el pixel original
    m,n = img.shape
    if p == 8:
        prime = 257
        imgType = 'uint8'
    elif p == 16:
        prime = 65537
        imgType = 'uint16'
    else:
        error
    demixed_img = np.empty((m,n), dtype=imgType)
    for i in range(m):
        demixed_img[i,0] = image_operator(img[i,0], inverso(IV[i],prime), prime)
        for j in range(1,n):
            demixed_img[i,j] = image_operator(img[i,j], inverso(img[i,j-1],prime), prime)
    return demixed_img

def image_operator(a, b, p):
    primero = np.ulonglong(a+1)
    segundo = np.longlong(b+1)
    p = np.ulonglong(p)
    multi = np.multiply(primero, segundo)
    modulo = int(multi) % p
    return int(modulo-1)

# No lo estaba haciendo con pow y por eso he perdido tanto tiempo
def inverso(a,p):
    return (pow(int(a+1),int(p-2), int(p))) - 1

def inverse_image_operator(a,c,p):
    #print('a = ' + str(a) + '; c = ' + str(c) + '; p = ' + str(p))
    # (a*c^-1)^-1=b
    cInversa = inverso(c,p)
    #print('c^-1 = ' + str(cInversa))
    aPorC = image_operator(a,cInversa,p)
    #print('a*c^-1 = ' + str(aPorC))
    return inverso(aPorC,p)

def modified_ACM(imgParam, p):
    # Para deshacer el cambio buscamos la inversa de [[2,1],[1,1]] que es [[1,-1],[-1,2]]
    img = deepcopy(imgParam)
    transformed_img = np.empty((img.shape), dtype='uint' + str(p))
    m,n = img.shape
    N = min(img.shape)
    alpha = ceil(max(img.shape)/N)
    print('Cuadrados sobre los que se aplica ACM: ' + str(alpha))
    L = N - (max(img.shape) % N)
    # No viene en articulo la posibilidad de que la imagen ya sea cuadrada, y aqui se podria dividir por 0
    # Se arregla con un if
    O = floor(L/(alpha - 1)) if alpha != 1 else 0
    k = largest_prime_less_than(int(N/2))
    #print("k es: " + str(k))
    x0, y0 = (0,0)
    # La funcion de arnodls cat map definida en una lambda
    #acm = lambda M,n:[[M[(2*i+j)%n][(i+j)%n]for i in range(n)]for j in range(n)]

    for i in range(alpha):
        print('Alpha nº ' + str(i+1))
        #print(str((x0,y0)))
        # No se si hay que añadir el -1 del articulo, mirar despues
        Sq = img[x0 : x0 + N, y0 : y0 + N]
        acm_Sq = Sq
        for _ in range(k):
            acm_Sq = acm(acm_Sq,N)
        img[x0 : x0 + N, y0 : y0 + N] = np.array(acm_Sq)
        transformed_img[x0 : x0 + N, y0 : y0 + N] = np.array(acm_Sq)

        if i == alpha-2:
            #print('if i == alpha-1:')
            if m > n:
                #print('if m > n:')
                x0 = m - N
            else:
                #print('else:')
                y0 = n - N
        else:
            #print(' NO if i == alpha-1:')
            if m > n:
                #print('m > n')
                x0 = x0 + N - O
            else:
                #print('else:')
                # ESTO VIENE MAL EN EL ARTICULO?????, se contradice
                y0 = y0 + N - O

    return transformed_img

def largest_prime_less_than(n):
    while n >= 1:
        if sympy.isprime(n) or n == 1:
            return n
        n-=1


def forward_row_mixing(img, p):
    m,n = img.shape
    copia = deepcopy(img)
    # -------forward row mixing------
    for x in range(m):
        for y in range(1,n):
            img[x,y] = image_operator(copia[x,y], img[x,y-1],p)
    return img
def forward_column_mixing(img, p):
    m,n = img.shape
    copia = deepcopy(img)
    # -------forward row mixing------
    for y in range(n):
        for x in range(1,m):
            img[x,y] = image_operator(copia[x,y], img[x-1,y],p)
    return img
def reverse_row_mixing(img, p):
    m,n = img.shape
    copia = deepcopy(img)
    # -------reverse_row_mixing------
    for x in range(m):
        for y in range(n-2,-1,-1):
            img[x,y] = image_operator(copia[x,y], img[x,y+1],p)
    return img
def reverse_column_mixing(img,p):
    m,n = img.shape
    copia = deepcopy(img)
    # -------reverse_row_mixing------
    for y in range(n):
        for x in range(m-2,-1,-1):
            img[x,y] = image_operator(copia[x,y], img[x+1,y],p)
    return img

def mixing(img, p):
    # -------forward row mixing------
    img = forward_row_mixing(img,2**p+1)
    # -------forward column mixing------
    img = forward_column_mixing(img,2**p+1)
    # -------reverse row mixing------
    img = reverse_row_mixing(img,2**p+1)
    # -------reverse column mixing------
    img = reverse_column_mixing(img,2**p+1)
    return img

def forward_row_demixing(img,p):
    m,n = img.shape
    # IMPORTANTE FIJARSE EN ESTO
    copia = deepcopy(img)
    # -------forward row mixing------
    for x in range(m):
        for y in range(1,n):
            img[x,y] = inverse_image_operator(copia[x,y-1],img[x,y],p)
    return img

def forward_column_demixing(img,p):
    m,n = img.shape
    # IMPORTANTE FIJARSE EN ESTO
    copia = deepcopy(img)
    # -------forward row mixing------
    for y in range(n):
        for x in range(1,m):
            img[x,y] = inverse_image_operator(copia[x-1,y],img[x,y], p)
    return img

def reverse_row_demixing(img,p):
    m,n = img.shape
    # IMPORTANTE FIJARSE EN ESTO
    copia = deepcopy(img)
    # -------forward row mixing------
    for x in range(m):
        for y in range(n-2,-1,-1):
            img[x,y] = inverse_image_operator(copia[x,y+1],img[x,y], p)
    return img

def reverse_column_demixing(img,p):
    m,n = img.shape
    # IMPORTANTE FIJARSE EN ESTO
    copia = deepcopy(img)
    # -------forward row mixing------
    for y in range(n):
        for x in range(m-2,-1,-1):
            img[x,y] = inverse_image_operator(copia[x+1,y],img[x,y],p)
    return img

def demixing(img, p):
    # -------reverse column mixing------
    img_res = reverse_column_demixing(img,2**p+1)
    # -------reverse row mixing------
    img_res = reverse_row_demixing(img_res,2**p+1)
    # -------forward column mixing------
    img_res = forward_column_demixing(img_res,2**p+1)
    # -------forward row mixing------
    img_res = forward_row_demixing(img_res,2**p+1)
    return img_res

def dna_encoding(img, p, RM):

    D = list()
    m,n = img.shape
    for x in range(m):
        count = 0
        for y in range(n):
            b = format(img[x,y], '0'+str(p)+'b')
            #if len(b) % 2 == 1:
            #    b = '0' + b

            k = 0
            while k <= len(b)-2:
                # La x es la i??? No esta calro esta parte
                pos = x*(n*(int(p/2))) + count
                d = DNA_TABLE[RM[pos]][b[k:k+2]]
                D.append(d)
                count += 1
                k+=2

    return np.array(D)


def substitution(img_encoded, DSM, RM):
    img_substitution = list()

    for i in range(len(img_encoded)):
        rule = RM[i]
        dm = int(DNA_TABLE_DECODE[rule][DSM[i]],2)
        di = int(DNA_TABLE_DECODE[rule][img_encoded[i]],2)
        d = DNA_TABLE[rule][format(image_operator(dm,di,5),'02b')]
        img_substitution.append(d)

    return np.array(img_substitution)

def desubstitution(img_encoded, DSM, RM):
    img_substitution = list()

    for i in range(len(img_encoded)):
        rule = RM[i]
        dm = int(DNA_TABLE_DECODE[rule][DSM[i]],2)
        di = int(DNA_TABLE_DECODE[rule][img_encoded[i]],2)
        d = DNA_TABLE[rule][format(inverse_image_operator(dm,di,5),'02b')]
        img_substitution.append(d)

    return np.array(img_substitution)


def dna_decoding(img_substitution, m, n , p, RM):

    index = int(p/2)
    I = np.empty((m,n),dtype='uint'+str(p))
    count = 0
    pixel = 0
    while index <= len(img_substitution):
        de = 0
        nucleotids = img_substitution[index-int(p/2):index]
        for i in range(int(p/2)):
            v = int(DNA_TABLE_DECODE[RM[count]][nucleotids[i]], 2)
            de = 4 * de + v
            # No hace falta el floor probablemente
            count+=1
        I[floor(int(pixel/n)),pixel%n] = de
        index+=int(p/2)
        pixel+=1
        
    return I


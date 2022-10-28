import pandas as pd
import numpy as np
import Criptosistema
from copy import deepcopy
from matplotlib import pyplot as plt

iteraciones = list()
for n in range(3,300):
    img = np.random.rand(n,n)
    distinto = True
    transformado = deepcopy(img)
    i = 0
    while distinto:
        transformado = Criptosistema.acm_test(transformado,n)
        i = i + 1
        if(str(img) == str(transformado)):
            iteraciones.append(i)
            break

print(iteraciones)

df = pd.DataFrame(zip(list(range(3,300)),iteraciones),columns = ['Tamaño de imagen', 'Iteraciones'])
print(df)

df.plot(x = 'Tamaño de imagen', y='Iteraciones',kind='bar')
plt.show()
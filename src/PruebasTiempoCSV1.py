from matplotlib import pyplot as plt
import csv
import pandas as pd

tams=list()
times=list()
with open('tablaTiempo2.csv', 'r') as file:
    csvReader = csv.reader(file)
    i = 0
    for line in csvReader:
        if i == 0:
            i+=1
            continue
        if line == []:
            continue
        tam = line[1]
        tam = tam.replace('(','').replace(')','').replace(' ','').split(',')
        x = tam[0]
        y = tam[1]
        tams.append((int(x),int(y)))

        time = float(line[3])
        times.append(time)

#print(list(zip(tams, times))[0])
l = sorted(list(zip(tams, times)),key=lambda x : x[0][0]*x[0][1])
d = dict()
for tam, tim in l:
    if tam in d:
        d[tam] = (d[tam][0]+tim,d[tam][1]+1)
    else:
        d[tam] = (tim,1)
dfinal = dict()
for k in d:
    dfinal[k] = d[k][0]/d[k][1]

tams = list(dfinal.keys())
times = list(dfinal.values())
l = sorted(list(zip(tams, times)),key=lambda x : x[0][0]*x[0][1])
print(l)
df = pd.DataFrame(l,columns =['Tamanyos', 'Tiempo en horas'])
#plt.rcParams.update({'font.size': 7})
plt.rcParams.update({'xtick.labelsize': 6})
ax = df.plot(kind='line', use_index=True)
ax.set_xticks(range(len(df['Tamanyos'])))
ax.set_xticklabels(df['Tamanyos'])
ax.set
plt.show()
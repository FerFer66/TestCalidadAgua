import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Definicion de Funciones

#Funcion que separa un archivo csv por Region y crea sus archivos respectivos.
#Entrada: Un Dataframe de un csv entregado
#Salida: La creacion de N archivos dependiendo de las n Regiones del csv entregado.
def crearArchivosSeparados(Dataframe):
    #Con las herramientas de la libreria pandas se crea una lista de regiones sin repetir
    regiones = df["Region"].unique()
    i = 0
    while(i< len(regiones)):
        regioni = df[df["Region"] == regiones[i]][["pozo", "biologico", "turbiedad", "desinfeccion"]]
        regioni.to_csv(regiones[i]+".csv",";", index=False)
        i= i+1

#Funciones que se encargan de verificar si la calidad es aceptable en cada test
#Entrada: Numero, la suma de los test del pozo (para ese test).
#Salida : 1 o 0, pasa o no el test respectivamente.
def analizarTurbiedad(sumadeturbiedad):
    cincoporciento = sumadeturbiedad*0.05
    if(cincoporciento> 4):
        return 1
    else:
        return 0

def analizarDesinfeccion(sumadedesinfeccion, mayorvalor):
    diezporciento = sumadedesinfeccion * 0.1
    if (diezporciento > 0.2 and mayorvalor < 2):
        return 1
    else:
        return 0


def analizarMicrobiologico(sumademicrobiologico):
    diezporciento = sumademicrobiologico * 0.1
    cincoporciento = sumademicrobiologico * 0.05
    if (cincoporciento > 5 and diezporciento > 1):
        return 1
    else:
        return 0
#Funcion que convierte un arreglo de areglos de varios test de pozos, en un arreglo de arreglo de dos posiciones con:
#Pimera posicion : Cantidad de pozos potables de la region, Segunda posicion : Cantidad de pozos no Potables de la region
#Entrada: Lista de Listas.
#Salida : Lista de Listas de dos posiciones.
def convertirResultados_a_ArregloGrafico(Lista):
    ArregloGrafico = [[],[]]
    i=0
    while(i<len(Lista)):
        j=0
        contadorTestPositivo = 0
        contadorTestNegativo = 0
        while(j<len(Lista[i])):
            if(Lista[i][j] ==  1 ):
                contadorTestPositivo = contadorTestPositivo + 1
            else:
                contadorTestNegativo = contadorTestNegativo + 1
            j=j+1
        ArregloGrafico[0].append(contadorTestPositivo)
        ArregloGrafico[1].append(contadorTestNegativo)
        i=i+1


    return ArregloGrafico

#Bloque Principal

#Bienvenida.
print('                      _ _     _           _         _____      _ _     _           _       _      _')
print('    /\               | (_)   (_)         | |       / ____|    | (_)   | |         | |     | |    | |     /\ ')
print('   /  \   _ __   __ _| |_ ___ _ ___    __| | ___  | |     __ _| |_  __| | __ _  __| |   __| | ___| |    /  \   __ _ _   _  __ _')

print('  / /\ \ | \'_ \ / _` | | / __| / __|  / _` |/ _ \ | |    / _` | | |/ _` |/ _` |/ _` |  / _` |/ _ \ |   / /\ \ / _` | | | |/ _` |')

print(' / ____ \| | | | (_| | | \__ \ \__ \ | (_| |  __/ | |___| (_| | | | (_| | (_| | (_| | | (_| |  __/ |  / ____ \ (_| | |_| | (_| |')
print('/_/    \_\_| |_|\__,_|_|_|___/_|___/  \__,_|\___|  \_____\__,_|_|_|\__,_|\__,_|\__,_|  \__,_|\___|_| /_/    \_\__, |\__,_|\__,_|')
print('                                                                                                               __/ |')
print('                                                                                                              |___/             ')


#Se obtiene la informacion del fichero

nombre_archivo = raw_input("Ingrese el nombre del archivo (sin extension): ")
fichero = pd.read_csv(nombre_archivo+".csv",";")
df = pd.DataFrame(fichero)

#Obtenemos Las regiones que existen en el texto
regiones =df["Region"].unique()

#Llamamos a la funcion que crea los archivos separados
crearArchivosSeparados(df)

#Lista que almacena los dataframe de pozos
ListaDataFrameRegiones = []
ListaResultados = []
#Ya que estan creados los archivos procedemos a leerlos y a crear los arreglos de los analisis
j=0
while(j<len(regiones)):
    pozosregionj = []
    regionj = pd.read_csv(regiones[j] + ".csv", ";")
    dfj = pd.DataFrame(regionj)
    nombrepozos = dfj["pozo"].unique()
    regionj.set_index("pozo", inplace=True)
    print ("Region " + regiones[j]+":")
    print(regionj)
    ListaDataFrameRegiones.append(dfj)
    print("--------------------------------")
    k=0
    while(k<len(nombrepozos)):
        pozo = nombrepozos[k]
        #tablapozo = dfj[dfj["pozo"] == pozo][["biologico", "turbiedad", "desinfeccion"]]

        sumaBiologico = (regionj.loc[pozo,"biologico"]).sum()
        sumaTurbiedad = (regionj.loc[pozo,"turbiedad"]).sum()
        sumaDesinfeccion = (regionj.loc[pozo,"desinfeccion"]).sum()
        maxDesinfeccion = (regionj.loc[pozo,"desinfeccion"]).max()


        turbiedad = analizarTurbiedad(sumaTurbiedad)
        biologico = analizarMicrobiologico(sumaBiologico)
        desinfeccion = analizarDesinfeccion(sumaDesinfeccion,maxDesinfeccion)

        if (turbiedad == 1 and biologico == 1 and desinfeccion == 1 ):
            pozosregionj.append(1)
        else:
            pozosregionj.append(0)
        k = k+1
    ListaResultados.append(pozosregionj)
    j = j+1

arregloGrafico = convertirResultados_a_ArregloGrafico(ListaResultados)

#Ya se tiene un arreglo de cada region y sus pozos con uno o cero respectivamente procedemos a graficar

ind = np.arange(len(arregloGrafico[0]))

#print arregloGrafico

p1 = plt.bar(ind, arregloGrafico[0], 1, color='#1f77b4',label = "Pozo Potable")
p2 = plt.bar(ind, arregloGrafico[1], 1, color='#ff7f0e',label = "Pozo No Potable",bottom=arregloGrafico[0])

plt.xticks(np.arange(len(regiones)),regiones)
plt.title('Cantidad de Pozos potables y no potables por region')
plt.xlabel('Regiones')
plt.ylabel('Cantidad de Pozos')
plt.legend(loc='upper right')

plt.show()

print ("Ha terminado el programa.")

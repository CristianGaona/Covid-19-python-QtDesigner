# Impotación de liberiaas
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt

#Agregando path
data_path = '../data/covid_data.csv'
data_fr = pd.read_csv(data_path)
data_fr.head()

#Utilizar función melt para pasar dejar a country y sate como columnas y las fechas y los datos pasar de filas a columnas
data_fr = pd.melt(data_fr, id_vars=['Country', 'State'], var_name='Date', value_name='cases_deaths')
print(data_fr)

#Separar casos y muertes en columnas diferentes
separated_df = data_fr["cases_deaths"].str.split(expand=True)
separated_df.columns = ['Casos', 'Muertes']
data_fr['Casos']=separated_df['Casos']
data_fr['Muertes']=separated_df['Muertes']



#Eliminar columna cases_deaths
dataReady=data_fr.drop(['cases_deaths'], axis=1)
print(dataReady)

#Conversión de Object a diferentes tipos
dataReady['Casos']= dataReady['Casos'].astype('int')
dataReady['Muertes']= dataReady['Muertes'].astype('int')
dataReady['Date']=pd.to_datetime(dataReady['Date'])

#Graficar
fig = plt.figure(figsize = (20,5))

lista1 = dataReady.iloc[1:,3]   # Declara lista1 los casos de covid
plt.plot(lista1, label="Casos")   # Dibuja el gráfico
plt.xlabel("Fecha")   # Inserta el título del eje X
plt.ylabel("Cantidad")   # Inserta el título del eje Y
plt.ioff()   # Desactiva modo interactivo de dibujo
lista2 = dataReady.iloc[1:,4]    # Declara lista2 declara muertes por covid
plt.plot(lista2, label="Muertes")   # No dibuja datos de lista2
plt.ion()   # Activa modo interactivo de dibujo
plt.plot(lista2)   # Dibuja datos de lista2 sin borrar datos de lista1
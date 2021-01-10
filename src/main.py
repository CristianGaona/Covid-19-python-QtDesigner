# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import uic, QtWidgets

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
import sys
import pandas as pd
import matplotlib.pyplot as plt
#Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MatplotlibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("appMain.ui", self)

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")

        self.bntGraficar.clicked.connect(self.plotPaisCasos)
        self.bntMuertes.clicked.connect(self.plotPaisMuertes)

        self.bntCargarCSV.clicked.connect(self.getCSV)

        #self.pushButton_generate_random_signal.clicked.connect(self.update_graph)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def update_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.axes.cla()
        self.MplWidget.canvas.draw()

    def plot(self):
        lista1 = self.dataReady.iloc[1:, 3]  # Declara lista1 los casos de covid
        self.MplWidget.canvas.axes.plot(lista1)  # Dibuja el gráfico
        #plt.xlabel("Fecha")  # Inserta el título del eje X
        #plt.ylabel("Cantidad")  # Inserta el título del eje Y
        # plt.ioff()   # Desactiva modo interactivo de dibujo
        lista2 = self.dataReady.iloc[1:, 4]  # Declara lista2 declara muertes por covid
        self.MplWidget.canvas.axes.plot( lista2)  # No dibuja datos de lista2
        self.MplWidget.canvas.axes.legend(('Casos', 'Muertes'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('Casos y Muertes')
        # plt.ion()   # Activa modo interactivo de dibujo
        self.MplWidget.canvas.axes.plot(lista2)  # Dibuja datos de lista2 sin borrar datos de lista1
        self.MplWidget.canvas.draw()

    def plotPaisCasos(self):
        pais = self.comboBoxCountry.currentText()
        r = self.dataReady.loc[[pais], ['Date', 'Casos']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        #self.axes.cla()
        self.MplWidget.canvas.axes.plot(x, y)  # Dibuja el gráfico
        self.MplWidget.canvas.axes.set_title('Casos Covid por Pais')
        #self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        #self.MplWidget.canvas.axes.set_ylabel("Casos " + pais)  # Inserta el título del eje Y
        self.MplWidget.canvas.draw()

    def plotPaisMuertes(self):

        pais = self.comboBoxCountry.currentText()
        r = self.dataReady.loc[[pais], ['Date', 'Muertes']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        #self.axes.cla()
        self.MplWidget.canvas.axes.plot(x, y)  # Dibuja el gráfico
        self.MplWidget.canvas.axes.set_title('Muertes Covid por Pais')
        # self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        # self.MplWidget.canvas.axes.set_ylabel("Casos " + pais)  # Inserta el título del eje Y
        self.MplWidget.canvas.draw()

    # Esta función abre el archivo CSV
    def getCSV(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/Users/crgao')
        if filePath != "":
            print("Dirección", filePath)  # Opcional imprimir la dirección del archivo
            self.data_fr = pd.read_csv(str(filePath), sep=';')
            self.data_fr = pd.melt(self.data_fr, id_vars=['Country', 'State'], var_name='Date',
                                   value_name='cases_deaths')

            # Separar casos y muertes en columnas diferentes
            separated_df = self.data_fr["cases_deaths"].str.split(expand=True)
            separated_df.columns = ['Casos', 'Muertes']
            self.data_fr['Casos'] = separated_df['Casos']
            self.data_fr['Muertes'] = separated_df['Muertes']

            # Eliminar columna cases_deaths
            self.dataReady = self.data_fr.drop(['cases_deaths'], axis=1)

            # Conversión de Object a diferentes tipos
            self.dataReady['Casos'] = self.dataReady['Casos'].astype('int')
            self.dataReady['Muertes'] = self.dataReady['Muertes'].astype('int')
            self.dataReady['Date'] = pd.to_datetime(self.dataReady['Date'])

            # Agregar indice
            self.dataReady.set_index("Country", inplace=True)


            # Reemplazar los nan por All
            data_r = self.dataReady.replace("nan", "All")

            #Agrupar Paises
            grouped = data_r.groupby(['Country'])
            df2 = grouped.sum()

            self.comboBoxCountry.addItems(list(df2.index))



app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
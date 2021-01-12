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

       # self.bntCasos.clicked.connect(self.plotPaisCasos)
       # self.bntMuertes.clicked.connect(self.plotPaisMuertes)
        self.bntBoth.clicked.connect(self.plotAmbos)

        self.bntCargarCSV.clicked.connect(self.getCSV)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        if self.radioButtonCasos.isCheckable():
            self.radioButtonCasos.clicked.connect(self.plotPaisCasos)
        if self.radioButtonMuertes.isCheckable():
            self.radioButtonMuertes.clicked.connect(self.plotPaisMuertes)
        if self.radioButtonAmbos.isCheckable():
            self.radioButtonAmbos.clicked.connect(self.plotAmbos)



    def plotPaisCasos(self):
        self.MplWidget.canvas.axes.cla()
        pais = self.comboBoxCountry.currentText()
        r = self.dataReady.loc[[pais], ['Date', 'Casos']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        self.MplWidget.canvas.axes.plot(x, y)  # Dibuja el gráfico
        self.MplWidget.canvas.axes.set_title("Casos Covid pais de "+ pais)
        self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y
        self.MplWidget.canvas.draw()

    def plotPaisMuertes(self):

        self.MplWidget.canvas.axes.cla()
        pais = self.comboBoxCountry.currentText()
        r = self.dataReady.loc[[pais], ['Date', 'Muertes']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]

        self.MplWidget.canvas.axes.bar(x, y)  # Dibuja el gráfico
        self.MplWidget.canvas.axes.set_title("Muertes Covid pais de " + pais)
        self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

        self.MplWidget.canvas.draw()


    def plotAmbos(self):
        pais_data = self.comboBoxCountry.currentText()
        print(pais_data)
        estate = self.data_r[self.data_r['Country'] == pais_data].groupby('State')
        self.comboBoxEstado.addItems(list(estate.groups.keys()))
        print(estate.groups.keys())

        #self.comboBoxEstado.clear() #Borrar variable de combo

        # Esta función abre el archivo CSV
    def getCSV(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/Users/crgao')
        if filePath != "":
            print("Dirección", filePath)  # Opcional imprimir la dirección del archivo
            self.data_fr = pd.read_csv(str(filePath), sep=';', na_values="All")
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
            self.dataReady['State'] = self.dataReady['State'].astype('str')

            # Reemplazar los nan por All
            self.data_r = self.dataReady.replace("nan", "All")

            #Agrupar Paises
            self.grouped = self.data_r.groupby(['Country'])
            #df2 = grouped.sum()

            #Agregar Items a ComboBox Paises
            self.comboBoxCountry.addItems(list(self.grouped.groups.keys()))

            # Agregar indice
            self.dataReady.set_index("Country", inplace=True)





app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
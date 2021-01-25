# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import uic, QtWidgets

from matplotlib.backends.backend_qt5agg import ( NavigationToolbar2QT as NavigationToolbar)

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
        self.getCSV()
        self.indexState()
        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        self.comboBoxCountry.activated.connect(self.clearStates)
        self.comboBoxCountry.activated.connect(self.loadEstados)

        self.radioButtonCasos.clicked.connect(self.btnstate)
        self.radioButtonMuertes.clicked.connect(self.btnstate)
        self.radioButtonAmbos.clicked.connect(self.btnstate)

    # =============== Métodos ======================
    # Definir estos de los radioButton
    def btnstate(self):
        #self.plotPaisCasos()

        if self.radioButtonCasos.isChecked():
            self.comboBoxCountry.activated.connect(self.plotPaisCasos)
            self.comboBoxEstado.activated.connect(self.plotEstadosCasos)

        elif self.radioButtonMuertes.isChecked():
            self.comboBoxCountry.activated.connect(self.plotPaisMuertes)
            self.comboBoxEstado.activated.connect(self.plotEstadoMuertes)

        elif self.radioButtonAmbos.isChecked():
            self.comboBoxCountry.activated.connect(self.plotAmbosPaises)
            self.comboBoxEstado.activated.connect(self.plotAmbosEstados)


    # Casos pais
    def plotPaisCasos(self):
        self.MplWidget.canvas.axes.cla()
        pais = self.comboBoxCountry.currentText()
        r = self.dataReady.loc[[pais], ['Date', 'Casos']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        self.MplWidget.canvas.axes.plot(x, y, label = "Casos")  # Dibuja el gráfico
        self.MplWidget.canvas.axes.legend()
        self.MplWidget.canvas.axes.set_title("Casos Covid pais de "+ pais)
        self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y
        self.MplWidget.canvas.draw()

    # Casos estado
    def plotEstadosCasos(self):
        self.MplWidget.canvas.axes.cla()
        estado = self.comboBoxEstado.currentText()
        r = self.indState.loc[[estado], ['Date', 'Casos']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        self.MplWidget.canvas.axes.plot(x, y, label="Casos")  # Dibuja el gráfico
        self.MplWidget.canvas.axes.legend()
        self.MplWidget.canvas.axes.set_title("Casos Covid de " + estado)
        self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y
        self.MplWidget.canvas.draw()

    # Muertes estado
    def plotEstadoMuertes(self):
        self.aux = 4
        print(self.aux)
        self.MplWidget.canvas.axes.cla()
        estado = self.comboBoxEstado.currentText()
        r = self.indState.loc[[estado], ['Date', 'Muertes']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        self.MplWidget.canvas.axes.plot(x, y, label="Muertes")  # Dibuja el gráfico
        self.MplWidget.canvas.axes.legend()
        self.MplWidget.canvas.axes.set_title("Muertes Covid de " + estado)
        self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
        self.MplWidget.canvas.draw()

    # Muertes pais
    def plotPaisMuertes(self):
        self.aux = 2
        print(self.aux)
        #self.activateGrpah = 2
        self.MplWidget.canvas.axes.cla()
        pais = self.comboBoxCountry.currentText()
        r = self.dataReady.loc[[pais], ['Date', 'Muertes']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]

        self.MplWidget.canvas.axes.plot(x, y, label="Muertes")  # Dibuja el gráfico
        self.MplWidget.canvas.axes.legend()
        self.MplWidget.canvas.axes.set_title("Muertes Covid pais de " + pais)
        self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

        self.MplWidget.canvas.draw()

    def plotAmbosPaises(self):
        # Borrar Axes
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()
        # Obtener datos de Muertes
        pais = self.comboBoxCountry.currentText()
        r1 = self.dataReady.loc[[pais], ['Date', 'Muertes']]
        x1 = r1.iloc[:, 0]
        y1 = r1.iloc[:, 1]

        # Obtener datos de Casos
        r = self.dataReady.loc[[pais], ['Date', 'Casos']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]

        self.MplWidget.canvas.axes.plot(x, y, 'r', label = "Casos")
        self.MplWidget.canvas.axes1.plot(x1, y1, label = "Muertes")

        self.MplWidget.canvas.axes.set_title("Muertes y Casos Covid pais de " + pais)
        self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
        self.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
        self.MplWidget.canvas.axes.legend()
        self.MplWidget.canvas.axes1.legend()

        self.MplWidget.canvas.draw()

    def plotAmbosEstados(self):
        # Borrar Axes
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()
        # Obtener datos de Muertes
        estado = self.comboBoxEstado.currentText()
        r1 = self.indState.loc[[estado], ['Date', 'Muertes']]
        x1 = r1.iloc[:, 0]
        y1 = r1.iloc[:, 1]

        # Obtener datos de Casos
        r = self.indState.loc[[estado], ['Date', 'Casos']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]

        self.MplWidget.canvas.axes.plot(x, y, 'r', label = "Casos")
        self.MplWidget.canvas.axes1.plot(x1, y1, label = "Muertes")

        self.MplWidget.canvas.axes.set_title("Muertes y Casos Covid de " + estado)
        self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
        self.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
        self.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
        self.MplWidget.canvas.axes.legend()
        self.MplWidget.canvas.axes1.legend()

        self.MplWidget.canvas.draw()

    # Método para limpiar el combo box de estados
    def clearStates(self):
        self.comboBoxEstado.clear()

    # Método para cargar los estados en combo box
    def loadEstados(self):
        listEstado = []
        listEstado.append('All')
        pais_data = self.comboBoxCountry.currentText()
        estate = self.data_r[self.data_r['Country'] == pais_data].groupby('State')

        # Colocal la palabra ALL al inicio del combo box
        for i in estate.groups.keys():
            if i != 'All':
                listEstado.append(i)


        self.comboBoxEstado.addItems(list(listEstado))

    # Esta función abre el archivo CSV
    def getCSV(self):
        data_path = '../data/covid_data.csv'

        self.data_fr = pd.read_csv(data_path, sep=';')
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

        # Agrupar Paises
        self.grouped = self.data_r.groupby(['Country'])

        # Agregar Items a ComboBox Paises
        self.comboBoxCountry.addItems(list(self.grouped.groups.keys()))

        # Agregar indice
        self.dataReady.set_index("Country", inplace=True)

        self.loadEstados()

    # Asignar indice para graficas de estado
    def indexState(self):
        self.indState = self.data_r
        self.indState.set_index("State", inplace=True)

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
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


# Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MatplotlibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("appMain.ui", self)
        self.getCSV() # Cargar datos CSV
        self.indexState() # Indice para estados
        self.indexDate() # Indice de fechas
        self.setWindowTitle("Dashboard Covid 19 QT Designer ") # Título de MainWindows
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self)) # Agregar Axes
        self.comboBoxCountry.activated.connect(self.clearStates) # Limpiar listBox de estados, para una carga nueva
        self.comboBoxCountry.activated.connect(self.loadEstados) # Cargar estados al listBox

        self.plotAmbosPaises() # Graficar de inicio Muertes y casos acumulativos

        # llamar métodos según el radio Button seleccionado para graficar
        self.radioButtonCasos.clicked.connect(self.selectPlotCasos)
        self.radioButtonMuertes.clicked.connect(self.selectPlotMuertes)
        self.radioButtonAmbos.clicked.connect(self.selectPlotAmbos)

        # llamar métodos según el radio Button seleccionado para graficar datos diarios y acumulados
        self.radioButtonDiarios.clicked.connect(self.DatosDiarios)
        self.radioButton_2.clicked.connect(self.DatosAcumulativos)

        # Al hacer clic en un pais se grafica de forma automática segun los radio Buttos y listBox activados
        self.comboBoxCountry.activated.connect(self.btnstate)

        # Al hacer clic en un estado se grafica de forma automática segun los radio Buttos y listBox activados
        self.comboBoxEstado.activated.connect(self.btnstate2)

    # =============== Métodos ======================
    # Diarios Datos
    def DatosDiarios(self):
        if self.radioButtonCasos.isChecked() and self.radioButtonDiarios.isChecked():
            self.selectPlotCasos()
        elif self.radioButtonMuertes.isChecked() and self.radioButtonDiarios.isChecked():
            self.selectPlotMuertes()
        elif self.radioButtonAmbos.isChecked() and self.radioButtonDiarios.isChecked():
            self.selectPlotAmbos()

    # Datos Acumulativos
    def DatosAcumulativos(self):
        print("ento aqui")
        if self.radioButtonCasos.isChecked() :
            print("1")
            self.selectPlotCasos()
        elif self.radioButtonMuertes.isChecked():
            print("2")
            self.selectPlotMuertes()
        elif self.radioButtonAmbos.isChecked() :
            print("3")
            self.selectPlotAmbos()

    # Definir estos de los radioButton
    def btnstate(self):
        print("ENTRO 1")
        if self.comboBoxCountry.activated and self.radioButtonAmbos.isChecked():
            print("1.1")

            print(self.radioButtonAmbos.text())
            self.plotAmbosPaises()
        elif self.comboBoxCountry.activated and self.radioButtonCasos.isChecked():
            print("1.2")
            self.plotPaisCasos()
        elif self.comboBoxCountry.activated and self.radioButtonMuertes.isChecked():
            print("1.3")
            self.plotPaisMuertes()

    def btnstate2(self):
        print("ENTRO 2")
        if self.comboBoxEstado.activated and self.radioButtonMuertes.isChecked():
            self.plotEstadoMuertes()
        elif self.comboBoxEstado.activated and self.radioButtonCasos.isChecked():
            self.plotEstadosCasos()
        elif self.comboBoxEstado.activated and self.radioButtonAmbos.isChecked():
            self.plotAmbosEstados()

    # Método para escoger si grafica Datos paises o estados de acuerdo a los radio buttons (Casos, Muertes, Ambos)
    def selectPlotCasos(self):
        if self.comboBoxCountry.activated and self.radioButtonCasos.isChecked() and self.comboBoxEstado.currentText() == 'All':
            self.plotPaisCasos()
        elif self.comboBoxEstado.activated and self.radioButtonCasos.isChecked() and self.comboBoxEstado.currentText() != 'All':
            self.plotEstadosCasos()

    def selectPlotMuertes(self):
        if self.comboBoxCountry.activated and self.radioButtonMuertes.isChecked() and self.comboBoxEstado.currentText() == 'All':
            self.plotPaisMuertes()
        elif self.comboBoxEstado.activated and self.radioButtonMuertes.isChecked() and self.comboBoxEstado.currentText() != 'All':
            self.plotEstadoMuertes()

    def selectPlotAmbos(self):
        if self.comboBoxCountry.activated and self.radioButtonAmbos.isChecked() and self.comboBoxEstado.currentText() == 'All':
            self.plotAmbosPaises()
        elif self.comboBoxEstado.activated and self.radioButtonAmbos.isChecked() and self.comboBoxEstado.currentText() != 'All':
            self.plotAmbosEstados()

    # Casos pais
    def plotPaisCasos(self):
        print("Casos paises")
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()
        pais = self.comboBoxCountry.currentText()
        r = self.dataReady.loc[[pais], ['Date', 'Casos']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]

        if self.radioButtonCasos.isChecked() and self.radioButton_2.isChecked():
            print("Entro acumulados paises")
            self.MplWidget.canvas.axes.plot(x, y, 'r', label="Casos")
            self.MplWidget.canvas.axes.legend()
            self.MplWidget.canvas.axes.set_title("Casos Acumulados Covid pais de " + pais)
            self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y

        elif self.radioButtonCasos.isChecked() and self.radioButtonDiarios.isChecked():
            print("Entro diarios paises")

            casosArray = np.zeros([len(y), 1], dtype=int)

            casosAux = np.zeros([len(y), 1], dtype=int)

            for i in range(len(y)):

                if i == 0:
                    casosArray[0] = 0
                else:
                    casosAux[i] = (y[i].sum() - y[i - 1].sum())

                    if casosAux[i] < 0:
                        casosArray[i] = 0
                    else:
                        casosArray[i] = casosAux[i]

            self.MplWidget.canvas.axes.plot(x, casosArray, 'r', label="Casos")
            self.MplWidget.canvas.axes.legend()
            self.MplWidget.canvas.axes.set_title("Casos Diarios Covid pais de " + pais)
            self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y
        self.MplWidget.canvas.draw()

    # Casos estado
    def plotEstadosCasos(self):

        print("Casos estados")
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()
        estado = self.comboBoxEstado.currentText()
        if estado == 'All':
            self.plotPaisCasos()
        else:
            r = self.indState.loc[[estado], ['Date', 'Casos']]
            x = r.iloc[:, 0]
            y = r.iloc[:, 1]

            if self.radioButtonCasos.isChecked() and self.radioButton_2.isChecked():
                print("Entro acumulados estado")
                self.MplWidget.canvas.axes.plot(x, y, 'r', label="Casos")
                self.MplWidget.canvas.axes.legend()
                self.MplWidget.canvas.axes.set_title("Casos Acumulados Covid " + estado)
                self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y
            elif self.radioButtonCasos.isChecked() and self.radioButtonDiarios.isChecked():
                print("Entro diarios estado")

                casosArray = np.zeros([len(y), 1], dtype=int)

                casosAux = np.zeros([len(y), 1], dtype=int)

                for i in range(len(y)):

                    if i == 0:
                        casosArray[0] = 0
                    else:
                        casosAux[i] = (y[i].sum() - y[i - 1].sum())

                        if casosAux[i] < 0:
                            casosArray[i] = 0
                        else:
                            casosArray[i] = casosAux[i]

                self.MplWidget.canvas.axes.plot(x, casosArray, 'r', label="Casos")
                self.MplWidget.canvas.axes.legend()
                self.MplWidget.canvas.axes.set_title("Casos Diarios Covid pais de " + estado)
                self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y
            self.MplWidget.canvas.draw()

    # Muertes estado
    def plotEstadoMuertes(self):
        print("Muertes estados")
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()
        estado = self.comboBoxEstado.currentText()
        if estado == 'All':
            self.plotPaisMuertes()
        else:
            r = self.indState.loc[[estado], ['Date', 'Muertes']]
            x = r.iloc[:, 0]
            y = r.iloc[:, 1]
            if self.radioButtonMuertes.isChecked() and self.radioButton_2.isChecked():
                print("Entro acumulados estados")
                self.MplWidget.canvas.axes.plot(x, y, label="Muertes")
                self.MplWidget.canvas.axes.legend()
                self.MplWidget.canvas.axes.set_title("Muertes Acumuladas Covid de " + estado)
                self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
            elif self.radioButtonMuertes.isChecked() and self.radioButtonDiarios.isChecked():
                print("Entro diarios estados")

                muertesArray = np.zeros([len(y), 1], dtype=int)

                muertesAux = np.zeros([len(y), 1], dtype=int)

                for i in range(len(y)):

                    if i == 0:
                        muertesArray[0] = 0
                    else:
                        muertesAux[i] = (y[i].sum() - y[i - 1].sum())

                        if muertesAux[i] < 0:
                            muertesArray[i] = 0
                        else:
                            muertesArray[i] = muertesAux[i]

                self.MplWidget.canvas.axes.plot(x, muertesArray, label="Muertes")

                self.MplWidget.canvas.axes.legend()
                self.MplWidget.canvas.axes.set_title("Muertes Diarias Covid de " + estado)
                self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

            self.MplWidget.canvas.draw()

    # Muertes pais
    def plotPaisMuertes(self):
        print("Muertes paises")
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()
        pais = self.comboBoxCountry.currentText()
        r = self.dataReady.loc[[pais], ['Date', 'Muertes']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]

        if self.radioButtonMuertes.isChecked() and self.radioButton_2.isChecked():
            print("Entro acumulados paises")
            self.MplWidget.canvas.axes.plot(x, y, label="Muertes")
            self.MplWidget.canvas.axes.legend()
            self.MplWidget.canvas.axes.set_title("Muertes Acumuladas Covid pais de " + pais)
            self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

        elif self.radioButtonMuertes.isChecked() and self.radioButtonDiarios.isChecked():
            print("Entro diarios paises")

            muertesArray = np.zeros([len(y), 1], dtype=int)

            muertesAux = np.zeros([len(y), 1], dtype=int)

            for i in range(len(y)):

                if i == 0:
                    muertesArray[0] = 0
                else:
                    muertesAux[i] = (y[i].sum() - y[i - 1].sum())

                    if muertesAux[i] < 0:
                        muertesArray[i] = 0
                    else:
                        muertesArray[i] = muertesAux[i]

            self.MplWidget.canvas.axes.plot(x, muertesArray, label="Muertes")

            self.MplWidget.canvas.axes.legend()
            self.MplWidget.canvas.axes.set_title("Muertes Diarias Covid pais de " + pais)
            self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

        self.MplWidget.canvas.draw()

    def plotAmbosPaises(self):
        self.rollingMean()
        print("Casos y Muertes paises")
        # Borrar Axes
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()
        pais = self.comboBoxCountry.currentText()
        r1 = self.dataReady.loc[[pais], ['Date', 'Muertes']]
        x1 = r1.iloc[:, 0]
        y1 = r1.iloc[:, 1]
        # Obtener datos de Casos
        r = self.dataReady.loc[[pais], ['Date', 'Casos']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        # Obtener datos de Muertes
        if self.radioButtonAmbos.isChecked() and self.radioButton_2.isChecked():
            print("Entro acumulados paises")
            self.MplWidget.canvas.axes.plot(x, y, 'r', label="Casos")
            self.MplWidget.canvas.axes1.plot(x1, y1, label="Muertes")
            self.MplWidget.canvas.axes.set_title("Muertes y Casos Acumulados Covid pais de " + pais)
            self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
            self.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
        elif self.radioButtonAmbos.isChecked() and self.radioButtonDiarios.isChecked():
            print("Entro diarios paises")

            muertesArray = np.zeros([len(y1), 1], dtype=int)
            casosArray = np.zeros([len(y1), 1], dtype=int)

            muertesAux = np.zeros([len(y1), 1], dtype=int)
            casosAux = np.zeros([len(y1), 1], dtype=int)

            for i in range(len(y1)):

                if i == 0:
                    muertesArray[0] = 0
                    casosArray[0] = 0
                else:
                    muertesAux[i] = (y1[i].sum() - y1[i - 1].sum())
                    casosAux[i] = (y[i].sum() - y[i - 1].sum())
                    if muertesAux[i] < 0:
                        muertesArray[i] = 0
                    else:
                        muertesArray[i] = muertesAux[i]
                    if casosAux[i] < 0:
                        casosArray[i] = 0
                    else:
                        casosArray[i] = casosAux[i]
            self.MplWidget.canvas.axes.plot(x, casosArray, 'r', label="Casos")
            self.MplWidget.canvas.axes1.plot(x1, muertesArray, label="Muertes")

            self.MplWidget.canvas.axes.set_title("Muertes y Casos Diarios pais de " + pais)
            self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
            self.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
        # self.MplWidget.canvas.axes.legend()
        # self.MplWidget.canvas.axes1.legend()

        self.MplWidget.canvas.draw()

    def plotAmbosEstados(self):
        print("Casos y Muertes estados")
        # Borrar Axes
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()
        # Obtener datos de Muertes
        estado = self.comboBoxEstado.currentText()

        if estado == 'All':
            self.plotAmbosPaises()
        else:
            r1 = self.indState.loc[[estado], ['Date', 'Muertes']]
            x1 = r1.iloc[:, 0]
            y1 = r1.iloc[:, 1]

            # Obtener datos de Casos
            r = self.indState.loc[[estado], ['Date', 'Casos']]
            x = r.iloc[:, 0]
            y = r.iloc[:, 1]
            if self.radioButtonAmbos.isChecked() and self.radioButton_2.isChecked():
                print("Entro acumulados estados")

                self.MplWidget.canvas.axes.plot(x, y, 'r', label="Casos")
                self.MplWidget.canvas.axes1.plot(x1, y1, label="Muertes")

                self.MplWidget.canvas.axes.set_title("Muertes y Casos Covid de " + estado)
                self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
                self.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
            elif self.radioButtonAmbos.isChecked() and self.radioButtonDiarios.isChecked():
                print("Entro diarios diarios")
                muertesArray = np.zeros([len(y1), 1], dtype=int)
                casosArray = np.zeros([len(y1), 1], dtype=int)

                muertesAux = np.zeros([len(y1), 1], dtype=int)
                casosAux = np.zeros([len(y1), 1], dtype=int)

                for i in range(len(y1)):

                    if i == 0:
                        muertesArray[0] = 0
                        casosArray[0] = 0
                    else:
                        muertesAux[i] = (y1[i].sum() - y1[i - 1].sum())
                        casosAux[i] = (y[i].sum() - y[i - 1].sum())
                        if muertesAux[i] < 0:
                            muertesArray[i] = 0
                        else:
                            muertesArray[i] = muertesAux[i]
                        if casosAux[i] < 0:
                            casosArray[i] = 0
                        else:
                            casosArray[i] = casosAux[i]
                self.MplWidget.canvas.axes.plot(x, casosArray, 'r', label="Casos")
                self.MplWidget.canvas.axes1.plot(x1, muertesArray, label="Muertes")

                self.MplWidget.canvas.axes.set_title("Muertes y Casos Diarios  de " + estado)
                self.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
                self.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

            self.MplWidget.canvas.draw()

    # Método para limpiar el combo box de estados
    def clearStates(self):
        self.comboBoxEstado.clear()

    # Método para cargar los estados en combo box
    def loadEstados(self):
        # Borrar Axes
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes1.cla()
        listEstado = []
        listEstado.append('All')
        pais_data = self.comboBoxCountry.currentText()
        estate = self.data_r[self.data_r['Country'] == pais_data].groupby('State')

        # Coloca la palabra ALL al inicio del combo box
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
        self.data_d = self.dataReady.replace("nan", "All")

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

    def indexDate(self):
        self.indDate = self.data_d
        self.indDate.set_index("Date", inplace= True)

    def rollingMean(self):
        print(self.indDate.rolling(2).mean())

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()

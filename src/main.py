import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from appMain import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)


import pandas as pd
import numpy as np

class MatplotlibWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.getCSV()  # Cargar datos CSV
        self.indexState()  # Indice para estados
        self.indexDate()  # Indice de fechas
        self.setWindowTitle("Dashboard Covid 19 QT Designer ")  # Título de MainWindows
        self.addToolBar(NavigationToolbar(self.ui.MplWidget.canvas, self))  # Agregar Axes
        self.ui.comboBoxCountry.activated.connect(self.clearStates)  # Limpiar listBox de estados, para una carga nueva
        self.ui.comboBoxCountry.activated.connect(self.loadEstados)  # Cargar estados al listBox
        self.plotAmbosPaises()  # Graficar de inicio Muertes y casos acumulativos

        # llamar métodos según el radio Button seleccionado para graficar
        self.ui.radioButtonCasos.clicked.connect(self.selectPlotCasos)
        self.ui.radioButtonMuertes.clicked.connect(self.selectPlotMuertes)
        self.ui.radioButtonAmbos.clicked.connect(self.selectPlotAmbos)

        # llamar métodos según el radio Button seleccionado para graficar datos diarios y acumulados
        self.ui.radioButtonDiarios.clicked.connect(self.DatosDiarios)
        self.ui.radioButton_2.clicked.connect(self.DatosAcumulativos)

        # Al hacer clic en un pais se grafica de forma automática segun los radio Buttos y listBox activados
        self.ui.comboBoxCountry.activated.connect(self.btnstate)

        # Al hacer clic en un estado se grafica de forma automática segun los radio Buttos y listBox activados
        self.ui.comboBoxEstado.activated.connect(self.btnstate2)

        # Según se mueva el slider y de acurdo a los radio buttons selccionados se presentará la media móvil
        self.ui.sliderPromedio.valueChanged.connect(self.sliderSelect)

    # =============== Funciones ======================

    """
    Con esta función se lee el CSV con los datos del COVID-19, para la lectura de datos se utiliza la función de pandas
    read_csv(), se coloca en una sola columna todas las columnas de las fechas que contiene los caso y muertes según 
    el pais y estado, luego separamos los casos y muertes en columnas diferentes y se le asigna una cabecera representativa, 
    borramos la columna original de casos y muertes, se cambia el tipo de datos de las columnas de object a int, datetime y
    str, todas las celdas de los estados que no tengan un valor se rellenara con la palabra ALL, finalmente se llena 
    el comboBxox con la lista de paises.
    """

    def getCSV(self):
        data_path = '../data/covid_data_download.csv'
        # Transponer todas las filas de las fechas a una sola columna
        self.data_fr = pd.read_csv(data_path)
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
        self.dataReady = self.dataReady.replace("nan", "All")

        # Agrupar Paises
        self.groupedCountries = self.data_r.groupby(['Country'])

        listCountries = []
        # Coloca la palabra ALL al inicio del combo box
        for i in self.groupedCountries.groups.keys():
            if i != 'Global':
                listCountries.append(i)

        # Agregar Items a ComboBox Paises
        self.ui.comboBoxCountry.addItems(list(listCountries))

        # Agregar indice
        self.dataReady.set_index("Country", inplace=True)

        # Cargar estados
        self.loadEstados()

        # Método para cargar los estados en combo box y agregar la palabra All al inicio de la lista
    def loadEstados(self):
        # Borrar Axes
        self.ui.MplWidget.canvas.axes.cla()
        self.ui.MplWidget.canvas.axes1.cla()
        listEstado = []
        listEstado.append('All')
        pais_data = self.ui.comboBoxCountry.currentText()
        estate = self.data_r[self.data_r['Country'] == pais_data].groupby('State')

        # Coloca la palabra ALL al inicio del combo box
        for i in estate.groups.keys():
            if i != 'All':
                listEstado.append(i)

        self.ui.comboBoxEstado.addItems(list(listEstado))

    """
        Esta función permite escoger los datos diarios en relación a la sentencia de control que cumpla las condiciones
        Se compara si el radio button de casos, muertes y ambos con el radio button de datos diarios y se llama al método
        según la codición que se cumpla.
    """
    def DatosDiarios(self):
        if self.ui.radioButtonCasos.isChecked() and self.ui.radioButtonDiarios.isChecked():
            self.selectPlotCasos()
        elif self.ui.radioButtonMuertes.isChecked() and self.ui.radioButtonDiarios.isChecked():
            self.selectPlotMuertes()
        elif self.ui.radioButtonAmbos.isChecked() and self.ui.radioButtonDiarios.isChecked():
            self.selectPlotAmbos()

    """
        Esta función permite escoger los datos acumulados en relación a la sentencia de control que cumpla las condiciones
        Se compara si el radio button de casos, muertes y ambos con el radio button de datos acumulados y se llama al método
        según la codición que se cumpla.
    """
    def DatosAcumulativos(self):
        if self.ui.radioButtonCasos.isChecked():
            self.selectPlotCasos()
        elif self.ui.radioButtonMuertes.isChecked():
            self.selectPlotMuertes()
        elif self.ui.radioButtonAmbos.isChecked():
            self.selectPlotAmbos()
    """
        En esta función si el comboBox que contiene la lista de paises, detecta la selcción de un nuevo pais y lo compara
        con el radio button seleccionado para realizarlas respectiva gráfica
    """
    # Cambio de estado comboList de paises
    def btnstate(self):
        if self.ui.comboBoxCountry.activated and self.ui.radioButtonAmbos.isChecked():
            self.plotAmbosPaises()
        elif self.ui.comboBoxCountry.activated and self.ui.radioButtonCasos.isChecked():
            self.plotPaisCasos()
        elif self.ui.comboBoxCountry.activated and self.ui.radioButtonMuertes.isChecked():
            self.plotPaisMuertes()

    """
        Esta función encambio detecta la selección de un nuevo estado para compararlo con los radio buttons que esten 
        seleccionados para realizar la gráfica correspondiente
    """
    def btnstate2(self):
        if self.ui.comboBoxEstado.activated and self.ui.radioButtonMuertes.isChecked():
            self.plotEstadoMuertes()
        elif self.ui.comboBoxEstado.activated and self.ui.radioButtonCasos.isChecked():
            self.plotEstadosCasos()
        elif self.ui.comboBoxEstado.activated and self.ui.radioButtonAmbos.isChecked():
            self.plotAmbosEstados()

    """
        Esta función verifica el radio button selccionado y en relación a eso invocar a los métodos que cumplan con la 
        condición correcta
    """
    def sliderSelect(self):
        if self.ui.radioButtonCasos.isChecked():
            self.selectPlotCasos()
        elif self.ui.radioButtonMuertes.isChecked():
            self.selectPlotMuertes()
        elif self.ui.radioButtonAmbos.isChecked():
            self.selectPlotAmbos()

    """
        Esta función permite invocar a otras funciones que realizan la gráfica de casos covid por paises y estados, según las condiciones que se cumplan
        de los combo Box seleccionados y los radio buttons.
    """

    def selectPlotCasos(self):
        if self.ui.comboBoxCountry.activated and self.ui.radioButtonCasos.isChecked() and self.ui.comboBoxEstado.currentText() == 'All':
            self.plotPaisCasos()
        elif self.ui.comboBoxEstado.activated and self.ui.radioButtonCasos.isChecked() and self.ui.comboBoxEstado.currentText() != 'All':
            self.plotEstadosCasos()

    """
        Esta función permite invocar a otras funciones que realizan la gráfica de muertes  covid por 
        paises y estados, según las condiciones que se cumplan de los combo Box seleccionados y los radio buttons.
    """

    def selectPlotMuertes(self):
        if self.ui.comboBoxCountry.activated and self.ui.radioButtonMuertes.isChecked() and self.ui.comboBoxEstado.currentText() == 'All':
            self.plotPaisMuertes()
        elif self.ui.comboBoxEstado.activated and self.ui.radioButtonMuertes.isChecked() and self.ui.comboBoxEstado.currentText() != 'All':
            self.plotEstadoMuertes()

    """
        Esta función permite invocar a otras funciones que realizan la gráfica de los casos y muertes covid 
        por paises y estados, según las condiciones que se cumplan de los combo Box seleccionados y los radio buttons.
    """
    def selectPlotAmbos(self):
        if self.ui.comboBoxCountry.activated and self.ui.radioButtonAmbos.isChecked() and self.ui.comboBoxEstado.currentText() == 'All':
            self.plotAmbosPaises()
        elif self.ui.comboBoxEstado.activated and self.ui.radioButtonAmbos.isChecked() and self.ui.comboBoxEstado.currentText() != 'All':
            self.plotAmbosEstados()

    """
        Esta función permite realizar la gráfica de casos covid según el pais selccionado, se incia limpiando el widget
        de la gráfica anterior para presentar la nueva, se obtiene el nombre del paise selcciona para luego realizar una
        consulta al dataFrame por pais y que recupere los datos como fecha, casos, muertes y estados del pais en caso
        de tener estados, luego se realiza una descomposición con la función iloc para obtener las columnas que 
        corresponden a la fecha, casos y estados, implenmeta un for con la finalidad implementa para 
        obtener valores generales de paises que tienen estados y no acumular adicionalmnete los valores de sus estados
         y con eso evitar errores en las graficas, luego según las codiciones que se cumplan prestnará la grafica con 
         los datos acumulados o datos diarios, además una nueva gráfica de acurdo al slider que gráfica la media móvil
    """
    def plotPaisCasos(self):
        self.clearRows()
        self.ui.MplWidget.canvas.axes.cla()
        self.ui.MplWidget.canvas.axes1.cla()
        pais = self.ui.comboBoxCountry.currentText() # Obtiene el nombre del paise selciionado
        r = self.dataReady.loc[[pais], ['Date', 'Casos', 'State']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        estadoCasos = r.iloc[:, 2]

        # Variables auxiliares para almacenar y posterior enviarlos a la fucnión que llena la tabla
        casosList = []
        fechaListCasos = []
        datosMuertes = []

        for i in range(len(estadoCasos)):
            if (estadoCasos[i] == 'All'):
                casosList.append(y[i]) # Se agregan los casos extaridos del dataFrame a la lista
                fechaListCasos.append(x[i]) # Se agrega la columna de fechas
                datosMuertes.append(' ') # se agregan valores vacios para que los datos se coloque en su respectiva columna

        slider = self.rollingMean() # Se obtiene el valor del slider según el deslizamiento
        self.ui.lcdNumberSlider.display(slider) # el valor recuperado del slider pasarlo al led

        # Se convierte las listas a dataFrames para utilizar la función rolling para la media móvil
        df_CasosAcumulativos = pd.DataFrame(casosList, columns=['Casos'])
        rolling_mean = df_CasosAcumulativos.rolling(window=slider).mean()

        # Si esta sunción se cumple se presentará la gráfica de casos covid con datos acumulativos
        if self.ui.radioButtonCasos.isChecked() and self.ui.radioButton_2.isChecked():
            self.tableWidget(casosList, datosMuertes, fechaListCasos)  # Enviar datos a la tabla
            self.ui.MplWidget.canvas.axes.plot(fechaListCasos, casosList, 'r', label="Casos") # Graficas casos covid
            self.ui.MplWidget.canvas.axes.legend() # Agregar etiquetas
            self.ui.MplWidget.canvas.axes.set_title("Casos Acumulados Covid pais de " + pais) # Titulo de la gráfica
            self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y

            # Si el slider cambia su valor presentará una nueva grádica en relación a la media móvil
            if self.ui.sliderPromedio.value() > 1:
                self.ui.MplWidget.canvas.axes.cla()
                self.ui.MplWidget.canvas.axes.plot(fechaListCasos, rolling_mean, 'r', label="Casos")
                self.ui.MplWidget.canvas.axes.legend() # Agregar etiquetas
                self.ui.MplWidget.canvas.axes.set_title("Casos Acumuladas Promedio Covid pais de " + pais)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y

        # Si se cumple la condición se presenta la gráfica con datos diarios
        elif self.ui.radioButtonCasos.isChecked() and self.ui.radioButtonDiarios.isChecked():

            # Arreglos de ceros numpy con logitud de acuerdo a la cantidad de datos
            casosArray = np.zeros([len(casosList), 1], dtype=int)
            casosAux = np.zeros([len(casosList), 1], dtype=int)

            # For para calcular los datos diarios y almacenarlos en los arreglos correspondientes
            for i in range(len(casosList)):

                if i == 0:
                    casosArray[0] = 0
                else:
                    casosAux[i] = (casosList[i].sum() - casosList[i - 1].sum())

                    if casosAux[i] < 0:
                        casosArray[i] = 0
                    else:
                        casosArray[i] = casosAux[i]

            # Llenar datos vacios a la lista, esto se hace porque en esta función no se optinen las muertes, y asi
            # conseguir que los datos se vayyan a las columnas correctas
            for i in range(len(y)):
                datosMuertes.append(' ')
            self.tableWidget(casosArray, datosMuertes, fechaListCasos)  # Enviar los datos de casos,
            self.ui.MplWidget.canvas.axes.plot(fechaListCasos, casosArray, 'r', label="Casos")
            self.ui.MplWidget.canvas.axes.legend() # agregar etiquetas
            self.ui.MplWidget.canvas.axes.set_title("Casos Diarios Covid pais de " + pais)
            self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y

            # Convertir de array a dataFrame
            df_MuertesDiarias = pd.DataFrame(casosArray, columns=['Casos'])
            rolling_mean2 = df_MuertesDiarias.rolling(window=slider).mean()

            # Graficar la media móvil con datos diarios
            if self.ui.sliderPromedio.value() > 1:
                self.ui.MplWidget.canvas.axes.cla()
                self.ui.MplWidget.canvas.axes.plot(fechaListCasos, rolling_mean2, 'r', label="Casos")
                self.ui.MplWidget.canvas.axes.legend() # Agregar etiquetas
                self.ui.MplWidget.canvas.axes.set_title("Casos Diarias Promedio Covid pais de " + pais)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y

        self.ui.MplWidget.canvas.draw() # dibuja la gráfica

    """
    Esta función permite graficar los datos de los estados selccionados, en el caso que dentro de la lista de los 
    estados se selccione All llame a la función de graficar casos del pais, en el caso contario extrae del dataFrame 
    la fecha y los casos del estado correspondiente, de forma acumulativa y diaria, al igual que la media móvil
    """
    def plotEstadosCasos(self):
        self.clearRows() # Borrar datos de la tabla, para llenar con los nuevos datos

        # Borrar las gráficas del Widget
        self.ui.MplWidget.canvas.axes.cla()
        self.ui.MplWidget.canvas.axes1.cla()
        estado = self.ui.comboBoxEstado.currentText() # Alamacenar el estado sleccionado del comboBox

        # Si selecciona la palabra All presenta la gráfica de casos del pais
        if estado == 'All':
            self.plotPaisCasos()

         # Caso contrario realiza un filtro de datos de acuerdo al estado selccionado, obteniendo Fecha y casos de estados
        else:
            r = self.indState.loc[[estado], ['Date', 'Casos']]
            x = r.iloc[:, 0]
            y = r.iloc[:, 1]

            # Variables Auxiliares para enviar datos a la tabla
            datosMuertes = []
            fecha = x
            datosCasos = y

            # Valores vacios a la columna Muertes
            for i in range(len(y)):
                datosMuertes.append(' ')

            slider = self.rollingMean() # Alamacena el valor del slider
            self.ui.lcdNumberSlider.display(slider)
            rolling_mean = r.iloc[:, 1].rolling(window=slider).mean() # Obitiene la media móvil segun los dias seleccionados

            # Presenta grafica de estados de forma acumulativa
            if self.ui.radioButtonCasos.isChecked() and self.ui.radioButton_2.isChecked():
                self.tableWidget(datosCasos, datosMuertes, fecha)  # Datos tabla
                self.ui.MplWidget.canvas.axes.plot(x, y, 'r', label="Casos")
                self.ui.MplWidget.canvas.axes.legend() # Agrega etiquetas
                self.ui.MplWidget.canvas.axes.set_title("Casos Acumulados Covid " + estado)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y

                # Realiza grafica de acuerdo al numero de dias seleccionado en el slider de forma acumulativa
                if self.ui.sliderPromedio.value() > 1:
                    self.ui.MplWidget.canvas.axes.cla()
                    self.ui.MplWidget.canvas.axes1.cla()
                    self.ui.MplWidget.canvas.axes.plot(x, rolling_mean, 'r', label="Casos")
                    self.ui.MplWidget.canvas.axes.legend()
                    self.ui.MplWidget.canvas.axes.set_title("Casos Promedio Acumulados Covid " + estado)
                    self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                    self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y

            # Presenta gráficas de muertes de forma diaria
            elif self.ui.radioButtonCasos.isChecked() and self.ui.radioButtonDiarios.isChecked():

                # Arreglos con ceros de numpy con logitud de la columna casos
                casosArray = np.zeros([len(y), 1], dtype=int)
                casosAux = np.zeros([len(y), 1], dtype=int)

                # For para clacular datos de forma diaria
                for i in range(len(y)):
                    if i == 0:
                        casosArray[0] = 0
                    else:
                        casosAux[i] = (y[i].sum() - y[i - 1].sum())
                        if casosAux[i] < 0:
                            casosArray[i] = 0
                        else:
                            casosArray[i] = casosAux[i]

                # listas para lamacenar datos y enviarlos a las columnas de la tabla
                datosMuertes = []
                fecha = x
                datosCasos = casosArray
                for i in range(len(y)):
                    datosMuertes.append(' ')
                self.tableWidget(datosCasos, datosMuertes, fecha)  # Enviar datos a la tabla
                self.ui.MplWidget.canvas.axes.plot(x, casosArray, 'r', label="Casos")
                self.ui.MplWidget.canvas.axes.legend()
                self.ui.MplWidget.canvas.axes.set_title("Casos Diarios Covid pais de " + estado)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y

                # Convertir de lista a Dataframe para obntener la media móvil con la función rolling
                df_MuertesDiarias = pd.DataFrame(casosArray, columns=['Casos'])
                rolling_mean2 = df_MuertesDiarias.rolling(window=slider).mean()

                # Graficar media móvil con datos diarios
                if self.ui.sliderPromedio.value() > 1:
                    self.ui.MplWidget.canvas.axes.cla()
                    self.ui.MplWidget.canvas.axes1.cla()
                    self.ui.MplWidget.canvas.axes.plot(x, rolling_mean2, 'r', label="Casos")
                    self.ui.MplWidget.canvas.axes.legend()
                    self.ui.MplWidget.canvas.axes.set_title("Casos Promedio Diarios Covid de " + estado)
                    self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                    self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de Casos ")  # Inserta el título del eje Y
            self.ui.MplWidget.canvas.draw()

    """
       Esta función permite graficar los datos de los estados seleccionados, en el caso que dentro de la lista de los 
       estados se seleccione All, llama a la función de graficar muertes del pais, en el caso contario extrae del dataFrame 
       la fecha y los casos del estado correspondiente, de forma acumulativa y diaria, al igual que la media móvil
    """
    def plotEstadoMuertes(self):
        self.clearRows()
        print("Muertes estados")
        self.ui.MplWidget.canvas.axes.cla()
        self.ui.MplWidget.canvas.axes1.cla()
        estado = self.ui.comboBoxEstado.currentText()
        if estado == 'All':
            self.plotPaisMuertes()
        else:
            r = self.indState.loc[[estado], ['Date', 'Muertes']]
            x = r.iloc[:, 0]
            y = r.iloc[:, 1]

            datosMuertes = y
            fecha = x
            datosCasos = []
            # Valores vacios a la columna
            for i in range(len(y)):
                datosCasos.append(' ')
            slider = self.rollingMean()
            self.ui.lcdNumberSlider.display(slider)
            rolling_mean = r.iloc[:, 1].rolling(window=slider).mean()
            if self.ui.radioButtonMuertes.isChecked() and self.ui.radioButton_2.isChecked():
                self.tableWidget(datosCasos, datosMuertes, fecha)  # Datos tabla
                print("Entro acumulados estados")
                self.ui.MplWidget.canvas.axes.plot(x, y, label="Muertes")
                self.ui.MplWidget.canvas.axes.legend()
                self.ui.MplWidget.canvas.axes.set_title("Muertes Acumuladas Covid de " + estado)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
                if self.ui.sliderPromedio.value() > 1:
                    self.ui.MplWidget.canvas.axes.cla()
                    self.ui.MplWidget.canvas.axes.plot(x, rolling_mean, label="Muertes")
                    self.ui.MplWidget.canvas.axes.legend()
                    self.ui.MplWidget.canvas.axes.set_title("Muertes Promedio Acumuladas Covid de " + estado)
                    self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                    self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
            elif self.ui.radioButtonMuertes.isChecked() and self.ui.radioButtonDiarios.isChecked():

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
                datosMuertes = muertesArray
                fecha = x
                datosCasos = []
                for i in range(len(y)):
                    datosCasos.append(' ')
                self.tableWidget(datosCasos, datosMuertes, fecha)  # Datos tabla
                self.ui.MplWidget.canvas.axes.plot(x, muertesArray, label="Muertes")

                self.ui.MplWidget.canvas.axes.legend()
                self.ui.MplWidget.canvas.axes.set_title("Muertes Diarias Covid de " + estado)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
                df_MuertesDiarias = pd.DataFrame(muertesArray, columns=['Muertes'])
                rolling_mean2 = df_MuertesDiarias.rolling(window=slider).mean()
                if self.ui.sliderPromedio.value() > 1:
                    self.ui.MplWidget.canvas.axes.cla()
                    self.ui.MplWidget.canvas.axes.plot(x, rolling_mean2, label="Muertes")
                    self.ui.MplWidget.canvas.axes.legend()
                    self.ui.MplWidget.canvas.axes.set_title("Muertes Promedio Diarias Covid de " + estado)
                    self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                    self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

            self.ui.MplWidget.canvas.draw()

    """
            Esta función permite realizar la gráfica de muertes covid según el pais selccionado, se incia limpiando el widget
            de la gráfica anterior para presentar la nueva, se obtiene el nombre del pais selccionado para luego realizar una
            consulta al dataFrame por pais y que recupere los datos como fecha, muertes y estados del pais en caso
            de tener estados, luego se realiza una descomposición con la función iloc para obtener las columnas que 
            corresponden a la fecha, casos y estados, implemeneta un for con la finalidad de 
            obtener valores generales de paises que tienen estados y no acumular adicionalmnete los valores de sus estados
             y con eso evitar errores en las graficas, luego según las condiciones que se cumplan presentará la grafica con 
             los datos acumulados o datos diarios, además una nueva gráfica de acurdo al slider que gráfica la media móvil
    """
    def plotPaisMuertes(self):
        self.clearRows()
        print("Muertes paises")
        self.ui.MplWidget.canvas.axes.cla()
        self.ui.MplWidget.canvas.axes1.cla()
        pais = self.ui.comboBoxCountry.currentText()
        r = self.dataReady.loc[[pais], ['Date', 'Muertes', 'State']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        estadoMuertes = r.iloc[:, 2]

        # Variables auxiliares
        muertesList = []
        fechaListMuertes = []
        datosCasos = []
        for i in range(len(estadoMuertes)):
            if (estadoMuertes[i] == 'All'):
                muertesList.append(y[i])
                fechaListMuertes.append(x[i])
                datosCasos.append(' ')

        slider = self.rollingMean()
        self.ui.lcdNumberSlider.display(slider)
        df_MuertesAcumulativas = pd.DataFrame(muertesList, columns=['Muertes'])
        rolling_mean = df_MuertesAcumulativas.rolling(window=slider).mean()

        if self.ui.radioButtonMuertes.isChecked() and self.ui.radioButton_2.isChecked():
            self.tableWidget(datosCasos, muertesList, fechaListMuertes)  # Datos tabla
            print("Entro acumulados paises")
            self.ui.MplWidget.canvas.axes.plot(fechaListMuertes, muertesList, label="Muertes")
            self.ui.MplWidget.canvas.axes.legend()
            self.ui.MplWidget.canvas.axes.set_title("Muertes Acumuladas Covid pais de " + pais)
            self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

            if self.ui.sliderPromedio.value() > 1:
                self.ui.MplWidget.canvas.axes.cla()
                self.ui.MplWidget.canvas.axes.plot(fechaListMuertes, rolling_mean, label="Muertes")
                self.ui.MplWidget.canvas.axes.legend()
                self.ui.MplWidget.canvas.axes.set_title("Muertes Acumuladas Promedio Covid pais de " + pais)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

        elif self.ui.radioButtonMuertes.isChecked() and self.ui.radioButtonDiarios.isChecked():

            print("Entro diarios paises")

            muertesArray = np.zeros([len(muertesList), 1], dtype=int)
            muertesAux = np.zeros([len(muertesList), 1], dtype=int)

            for i in range(len(muertesList)):
                if i == 0:
                    muertesArray[0] = 0
                else:
                    muertesAux[i] = (muertesList[i].sum() - muertesList[i - 1].sum())

                    if muertesAux[i] < 0:
                        muertesArray[i] = 0
                    else:
                        muertesArray[i] = muertesAux[i]

            self.tableWidget(datosCasos, muertesArray, fechaListMuertes)  # Datos tabla

            self.ui.MplWidget.canvas.axes.plot(fechaListMuertes, muertesArray, label="Muertes")

            self.ui.MplWidget.canvas.axes.legend()
            self.ui.MplWidget.canvas.axes.set_title("Muertes Diarias Covid pais de " + pais)
            self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
            df_MuertesDiarias = pd.DataFrame(muertesArray, columns=['Muertes'])
            rolling_mean2 = df_MuertesDiarias.rolling(window=slider).mean()
            if self.ui.sliderPromedio.value() > 1:
                self.ui.MplWidget.canvas.axes.cla()
                self.ui.MplWidget.canvas.axes.plot(fechaListMuertes, rolling_mean2, label="Muertes")
                self.ui.MplWidget.canvas.axes.legend()
                self.ui.MplWidget.canvas.axes.set_title("Muertes Diarias Promedio Covid pais de " + pais)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
        self.ui.MplWidget.canvas.draw()

    """
         Esta función permite realizar gráficas de muertes y casos por pais, se obtiene un filtro de fecha casos, 
         muertes y estados, segun el pais selccionado en el comboBox, las gráfica seran con datos acumulados o diarios
        según el pais selccionado, además si cambia el valor del slider presenta una nueva gráfica de la media móvil
    """
    def plotAmbosPaises(self):
        self.clearRows()

        print("Casos y Muertes paises")
        # Borrar Axes
        self.ui.MplWidget.canvas.axes.cla()
        self.ui.MplWidget.canvas.axes1.cla()

        pais = self.ui.comboBoxCountry.currentText()

        # Obtener Muertes de paises
        r1 = self.dataReady.loc[[pais], ['Date', 'Muertes', 'State']]
        x1 = r1.iloc[:, 0]
        y1 = r1.iloc[:, 1]
        estadoMuertes = r1.iloc[:, 2]

        # Variables auxiliares
        muertesList = []
        fechaListCasos = []
        fechaListMuertes = []

        for i in range(len(estadoMuertes)):
            if (estadoMuertes[i] == 'All'):
                muertesList.append(y1[i])
                fechaListMuertes.append(x1[i])

        # Obtener datos de Casos
        r = self.dataReady.loc[[pais], ['Date', 'Casos', 'State']]
        x = r.iloc[:, 0]
        y = r.iloc[:, 1]
        estadoCasos = r1.iloc[:, 2]

        casosList = []
        for i in range(len(estadoCasos)):
            if (estadoCasos[i] == 'All'):
                casosList.append(y[i])
                fechaListCasos.append(x[i])

        slider = self.rollingMean()
        self.ui.lcdNumberSlider.display(slider)

        df_MuertesAcumulativas = pd.DataFrame(muertesList, columns=['Muertes'])
        df_CasosAcumulativos = pd.DataFrame(casosList, columns=['Casos'])
        rolling_mean_CA = df_CasosAcumulativos.rolling(window=slider).mean()
        rolling_mean_MA = df_MuertesAcumulativas.rolling(window=slider).mean()

        # Obtener datos de Muertes
        if self.ui.radioButtonAmbos.isChecked() and self.ui.radioButton_2.isChecked():
            self.tableWidget(casosList, muertesList, fechaListCasos)  # Datos tabla
            print("Entro acumulados paises")
            self.ui.MplWidget.canvas.axes.plot(fechaListCasos, casosList, 'r-', label="Casos")
            self.ui.MplWidget.canvas.axes1.bar(fechaListMuertes, muertesList)
            self.ui.MplWidget.canvas.axes.set_title("Muertes y Casos Acumulados Covid pais de " + pais)
            self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
            self.ui.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
            if self.ui.sliderPromedio.value() > 1:
                self.ui.MplWidget.canvas.axes.cla()
                self.ui.MplWidget.canvas.axes1.cla()
                self.ui.MplWidget.canvas.axes.plot(fechaListCasos, rolling_mean_CA, 'r', label="Casos")
                self.ui.MplWidget.canvas.axes1.plot(fechaListMuertes, rolling_mean_MA, label="Muertes")
                self.ui.MplWidget.canvas.axes.set_title("Muertes y Casos Promedio Acumulados Covid pais de " + pais)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
                self.ui.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
        elif self.ui.radioButtonAmbos.isChecked() and self.ui.radioButtonDiarios.isChecked():
            print("Entro diarios paises")

            muertesArray = np.zeros([len(muertesList), 1], dtype=int)
            casosArray = np.zeros([len(casosList), 1], dtype=int)

            muertesAux = np.zeros([len(muertesList), 1], dtype=int)
            casosAux = np.zeros([len(casosList), 1], dtype=int)

            for i in range(len(casosList)):

                if i == 0:
                    muertesArray[0] = 0
                    casosArray[0] = 0
                else:
                    muertesAux[i] = (muertesList[i].sum() - muertesList[i - 1].sum())
                    casosAux[i] = (casosList[i].sum() - casosList[i - 1].sum())
                    if muertesAux[i] < 0:
                        muertesArray[i] = 0
                    else:
                        muertesArray[i] = muertesAux[i]
                    if casosAux[i] < 0:
                        casosArray[i] = 0
                    else:
                        casosArray[i] = casosAux[i]

            self.tableWidget(casosArray, muertesArray, fechaListCasos)  # Datos tabla
            self.ui.MplWidget.canvas.axes.plot(fechaListCasos, casosArray, 'r', label="Casos")
            self.ui.MplWidget.canvas.axes1.plot(fechaListMuertes, muertesArray, label="Muertes")
            self.ui.MplWidget.canvas.axes.set_title("Muertes y Casos Diarios pais de " + pais)
            self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
            self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
            self.ui.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
            df_MuertesDiarias = pd.DataFrame(casosArray, columns=['Muertes'])
            df_CasosDiarios = pd.DataFrame(muertesArray, columns=['Casos'])
            rolling_mean_MD = df_MuertesDiarias.rolling(window=slider).mean()
            rolling_mean_CD = df_CasosDiarios.rolling(window=slider).mean()
            if self.ui.sliderPromedio.value() > 1:
                self.ui.MplWidget.canvas.axes.cla()
                self.ui.MplWidget.canvas.axes1.cla()
                self.ui.MplWidget.canvas.axes.plot(fechaListCasos, rolling_mean_CD, 'r', label="Casos")
                self.ui.MplWidget.canvas.axes1.plot(fechaListMuertes, rolling_mean_MD, label="Muertes")
                self.ui.MplWidget.canvas.axes.set_title("Muertes y Casos Promedio Diarios pais de " + pais)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
                self.ui.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

        self.ui.MplWidget.canvas.draw()

    def plotAmbosEstados(self):
        self.clearRows()
        print("Casos y Muertes estados")
        # Borrar Axes
        self.ui.MplWidget.canvas.axes.cla()
        self.ui.MplWidget.canvas.axes1.cla()
        # Obtener datos de Muertes
        estado = self.ui.comboBoxEstado.currentText()

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

            datosMuertes = y1
            fecha = x
            datosCasos = y

            slider = self.rollingMean()
            self.ui.lcdNumberSlider.display(slider)
            rolling_mean_CA = r.iloc[:, 1].rolling(window=slider).mean()
            rolling_mean_MA = r1.iloc[:, 1].rolling(window=slider).mean()
            if self.ui.radioButtonAmbos.isChecked() and self.ui.radioButton_2.isChecked():
                print("Entro acumulados estados")
                self.tableWidget(datosCasos, datosMuertes, fecha)  # Datos tabla

                self.ui.MplWidget.canvas.axes.plot(x, y, 'r', label="Casos")
                self.ui.MplWidget.canvas.axes1.plot(x1, y1, label="Muertes")

                self.ui.MplWidget.canvas.axes.set_title("Muertes y Casos Covid de " + estado)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
                self.ui.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
                if self.ui.sliderPromedio.value() > 1:
                    self.ui.MplWidget.canvas.axes.cla()
                    self.ui.MplWidget.canvas.axes1.cla()
                    self.ui.MplWidget.canvas.axes.plot(x, rolling_mean_CA, 'r', label="Casos")
                    self.ui.MplWidget.canvas.axes1.plot(x1, rolling_mean_MA, label="Muertes")
                    self.ui.MplWidget.canvas.axes.set_title("Muertes y Casos Promedio Covid de " + estado)
                    self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                    self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
                    self.ui.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
            elif self.ui.radioButtonAmbos.isChecked() and self.ui.radioButtonDiarios.isChecked():
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

                datosMuertes = muertesArray
                fecha = x
                datosCasos = casosArray
                self.tableWidget(datosCasos, datosMuertes, fecha)  # Datos tabla
                self.ui.MplWidget.canvas.axes.plot(x, casosArray, 'r', label="Casos")
                self.ui.MplWidget.canvas.axes1.plot(x1, muertesArray, label="Muertes")

                self.ui.MplWidget.canvas.axes.set_title("Muertes y Casos Diarios  de " + estado)
                self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
                self.ui.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y
                df_MuertesDiarias = pd.DataFrame(casosArray, columns=['Muertes'])
                df_CasosDiarios = pd.DataFrame(muertesArray, columns=['Casos'])
                rolling_mean_MD = df_MuertesDiarias.rolling(window=slider).mean()
                rolling_mean_CD = df_CasosDiarios.rolling(window=slider).mean()
                if self.ui.sliderPromedio.value() > 1:
                    self.ui.MplWidget.canvas.axes.cla()
                    self.ui.MplWidget.canvas.axes1.cla()
                    self.ui.MplWidget.canvas.axes.plot(x, rolling_mean_CD, 'r', label="Casos")
                    self.ui.MplWidget.canvas.axes1.plot(x1, rolling_mean_MD, label="Muertes")
                    self.ui.MplWidget.canvas.axes.set_title("Muertes y Casos Promedio Diarios  de " + estado)
                    self.ui.MplWidget.canvas.axes.set_xlabel("Fecha")  # Inserta el título del eje X
                    self.ui.MplWidget.canvas.axes.set_ylabel("Cantidad de casos")  # Inserta el título del eje Y
                    self.ui.MplWidget.canvas.axes1.set_ylabel("Cantidad de muertes")  # Inserta el título del eje Y

            self.ui.MplWidget.canvas.draw()

    # Método para limpiar el combo box de estados
    def clearStates(self):
        self.ui.comboBoxEstado.clear()

    # Asignar indice para graficas de estado
    def indexState(self):
        self.indState = self.data_r
        self.indState.set_index("State", inplace=True)

    def indexDate(self):
        self.indDate = self.data_d
        self.indDate.set_index("Date", inplace=True)

    def rollingMean(self):

        value = self.ui.sliderPromedio.value()
        return value

    def tableWidget(self, casos, muertes, fecha):
        fila = 0
        lista2 = []
        for i in range(len(casos)):
            casos[i]
            fecha[i]
            muertes[i]
            lista2.append((str(fecha[i]), str(casos[i]), str(muertes[i])))
        for registro in lista2:
            columna = 0
            # print(registro)
            self.ui.tableWidgetCovid.insertRow(fila)
            for elemento in registro:
                celda = QTableWidgetItem(str(elemento))
                self.ui.tableWidgetCovid.setItem(fila, columna, celda)
                columna += 1
        fila += 1

    # Limpiar contenido de la tabla
    def clearRows(self):
        while self.ui.tableWidgetCovid.rowCount() > 0:
            self.ui.tableWidgetCovid.removeRow(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatplotlibWidget()
    window.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 17:44:36 2019

@author: Quique
"""

from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWidgets import *

import lungcancer.Aplicacion.main as main
import lungcancer.Funciones.funciones as fun
from lungcancer.Aplicacion.mplwidget import *
from lungcancer.Aplicacion.principal1_ui import *


class MainWindow(QMainWindow, mplWidget, Ui_LCDetection):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.texto = "Utilice los espacios habilitados debajo de la representación gráfica para introducir \nlos puntos pertenecientes a los pulmones para así poder realizar la segmentación"
        self.label_instrucciones.setText(
            "Escoja el paciente con el desplegable de arriba ")
        self.buttons_acepta_segmentacion.setVisible(False)
        #ocultando lo correspondiente a introducir las coordenadas
        self.label_pulmon_derecho.setVisible(False)
        self.label_pulmon_izquierdo.setVisible(False)
        self.line_x_der.setVisible(False)
        self.line_x_izq.setVisible(False)
        self.line_y_izq.setVisible(False)
        self.line_y_der.setVisible(False)
        self.button_enviar_coordenadas.setVisible(False)
        #inhabilitando el botón para introducir el slice a ver
        self.button_slice.setEnabled(False)

        self.slider_slices.valueChanged.connect(self.valor_slider)
        self.comboBox.addItems(["Paciente 1", "Paciente 2", "Paciente 3",
                                "Paciente 4", "Paciente 5", "Paciente 6", "Paciente 7", "Paciente 8"])
        self.comboBox.activated.connect(self.inicio)

        self.button_slice.clicked.connect(self.dibujar_slice)
        self.button_enviar_coordenadas.clicked.connect(self.segmentar_pulmon)
        self.buttons_acepta_segmentacion.accepted.connect(self.aceptado)
        self.buttons_acepta_segmentacion.rejected.connect(self.rechazado)
        self.button_3d.clicked.connect(self.representacion_3d_pulmones)

    def inicio(self):
        self.label_instrucciones.setText(
            "Espere mientras se leen los datos del paciente...")
        self.label_instrucciones.repaint()
        dir = main.escoge_paciente(self.comboBox.currentIndex())
        main.leer_directorio_usuario(dir)
        num_sliders = main.paciente_sitk.GetDepth()
        self.slider_slices.setMaximum(num_sliders-1)
        self.label_max_slice.setText(str(num_sliders))
        self.button_slice.setEnabled(True)
        main.representado = main.paciente_array
        self.label_instrucciones.setText(
            "Use el slider para seleccionar el slice que quiere visualizar del paciente y \n presione botón ok para visualizarlo")

    def valor_slider(self):
        self.label_val_slider.setText(str(self.slider_slices.value()))

    def dibujar_slice(self):
        slice = self.slider_slices.value()
        slice_paciente = main.devuelve_array(slice)
        self.widget.canvas.axes.clear()
        if self.map == 0:
            self.widget.canvas.axes.imshow(slice_paciente, cmap='gray')
            self.widget.canvas.draw()
            self.label_pulmon_derecho.setVisible(True)
            self.label_pulmon_izquierdo.setVisible(True)
            self.line_x_der.setVisible(True)
            self.line_x_izq.setVisible(True)
            self.line_y_izq.setVisible(True)
            self.line_y_der.setVisible(True)
            self.button_enviar_coordenadas.setVisible(True)
            self.label_instrucciones.setText(self.texto)
        else:
            self.widget.canvas.axes.imshow(slice_paciente)
            self.widget.canvas.draw()

    def segmentar_pulmon(self):
        self.label_3d.setText(
            "El proceso para realizar la segmentación consiste en:\n1) Suavizado gaussiano\n2) Binarización mediante crecimiento de regiones\n3) Cierre morfológico\n4) Multiplicar la máscara con la imagen original")
        self.label_3d.setAlignment(QtCore.Qt.AlignLeft)
        self.label_3d.repaint()
        self.label_instrucciones.setText(
            "Espere mientras se realiza la segmentación...")
        self.label_instrucciones.repaint()
        slice = self.slider_slices.value()
        semillas = [(int(self.line_x_izq.text()), int(self.line_y_izq.text()), slice),
                    (int(self.line_x_der.text()), int(self.line_y_der.text()), slice)]
        main.segmentacion_pulmones(main.paciente_sitk, semillas)
        main.representado = main.pulmones_array
        self.buttons_acepta_segmentacion.setVisible(True)
        self.button_3d.setEnabled(True)
        self.texto = "Elige un slice para comprobar que esté bien hecha la segmentación\n de ser así responda a la pregunta abajo a la derecha"
        self.dibujar_slice()

    def representacion_3d_pulmones(self):
        if self.map == 1:
            main.representado = main.nodulo_segmentado_array
            level = None
        else:
            level = -650
        self.label_3d.setText(
            "La representación en 3D tardará unos minutos\n al cabo de un tiempo se le abrirá una ventana\n en el navegador con la representación 3d\n mientras tanto sea paciente...")
        self.label_3d.repaint()
        verts, faces = fun.make_mesh(main.representado, level=level)
        fun.plotly_3d(verts, faces)

    def aceptado(self):
        self.label_instrucciones.setText(
            "Espere mientras se realiza todo el proceso para la obtención del nódulo\n y la extracción de sus características. Sea paciente, puede demorarse unos minutos...")
        self.label_instrucciones.repaint()
        self.label_3d.setText(
            "El proceso de la segmentación 3D del interior de los\n pulmones es el siguiente:\n1) Gradiente 3D de la imagen\n2) Calcular módulo del gradiente\n3) Algoritmo de watershed en 3D")
        self.label_3d.repaint()
        self.map = 1
        main.realizar_watershed(main.pulmones_sitk)
        main.extraer_etiqueta()
        (elongation, energy, sphericity) = main.extraer_caracteristicas_nodulo(
            main.region_cancer)
        #Hacer invisible lo correspondiente al paso anterior
        self.comboBox.setVisible(False)
        self.labelpaciente.setVisible(False)
        self.label_instrucciones.setVisible(False)
        #Invisibles los botones de debajo de la representación gráfica
        self.label_pulmon_derecho.setVisible(False)
        self.label_pulmon_derecho.repaint()
        self.label_pulmon_izquierdo.setVisible(False)
        self.label_pulmon_izquierdo.repaint()
        self.line_x_der.setVisible(False)
        self.line_x_der.repaint()
        self.line_x_izq.setVisible(False)
        self.line_x_izq.repaint()
        self.line_y_izq.setVisible(False)
        self.line_y_izq.repaint()
        self.line_y_der.setVisible(False)
        self.line_y_der.repaint()
        self.button_enviar_coordenadas.setVisible(False)
        self.button_enviar_coordenadas.repaint()
        self.buttons_acepta_segmentacion.setVisible(False)
        self.label_resultado.setVisible(True)
        self.label_resultado.setText("Las características del nódulo (elongacion, energía, esfericidad) son: "
                                     + str((round(elongation, 3), round(float(energy), 3), round(float(sphericity), 3))) +
                                     "\nEl nódulo cancerígeno se encuentra en la slice: " + str(fun.obtener_slice_nodulo(main.nodulo_segmentado)))
        self.label_3d.setText(
            "Para obtener los nódulos filtramos las regiones de watershed\n y comprobamos cuales de estas tienen las características de\n los nódulos cancerígenos basándonos en los descriptores de\n elongación, energía y esfericidad.")
        main.nodulo_overlay = fun.obterner_array_overlay(
            main.pulmones_sitk, main.nodulo_segmentado)
        main.representado = main.nodulo_overlay
        self.texto = ""
        
        self.dibujar_slice()

    def rechazado(self):
        self.buttons_acepta_segmentacion.setVisible(False)
        main.representado = main.paciente_array
        self.texto = "Introduzca unas nuevas coordenadas y vuelva a pulsar el botón enviar\n para volver a realizar la segmentación"
        self.dibujar_slice()

    def escribe_texto(self, texto):
        self.label_instrucciones.setText(texto)

    def visualizacion(self):
        main.representado = main.nodulo_overlay
        self.dibujar_slice()
        self.texto_boton[0] = 0


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

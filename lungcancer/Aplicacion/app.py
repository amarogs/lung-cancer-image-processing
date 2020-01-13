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


class MainWindow(QMainWindow,mplWidget,Ui_LCDetection):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.label_instrucciones.setText("Escoja el paciente con el desplegable de arriba " )
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
        self.comboBox.addItems(["Paciente 1","Paciente 2","Paciente 3","Paciente 4","Paciente 5","Paciente 6","Paciente 7","Paciente 8"])
        self.comboBox.activated.connect(self.inicio)
        self.button_slice.clicked.connect(self.dibujar_slice)
        self.button_enviar_coordenadas.clicked.connect(self.segmentar_pulmon)
        self.buttons_acepta_segmentacion.accepted.connect(self.aceptado)
        self.buttons_acepta_segmentacion.rejected.connect(self.rechazado)
        self.button_3d.clicked.connect(self.representacion_3d_pulmones)


        #self.slider_slices.setValue()
        #self.label.setText("Haz clic en el botón")
        #self.pushButton.setText("Presióname")
        #self.pushButton.clicked.connect(self.imagen)
        
    def inicio(self):
        dir = main.escoge_paciente(self.comboBox.currentIndex())
        main.leer_directorio_usuario(dir)
        num_sliders= main.paciente_sitk.GetDepth()
        self.slider_slices.setMaximum(num_sliders)
        self.label_max_slice.setText(str(num_sliders))
        self.button_slice.setEnabled(True)
        main.representado= main.paciente_array
        self.label_instrucciones.setText("Use el slider para seleccionar el slice que quiere visualizar del paciente y \n presione botón ok para visualizarlo")


    def valor_slider(self):
        self.label_val_slider.setText(str(self.slider_slices.value()))

    def dibujar_slice(self):
        slice = self.slider_slices.value()
        slice_paciente = main.devuelve_array(slice)
        self.widget.canvas.axes.clear()
        self.widget.canvas.axes.imshow(slice_paciente, cmap='gray')
        self.widget.canvas.draw()
        self.label_pulmon_derecho.setVisible(True)
        self.label_pulmon_izquierdo.setVisible(True)
        self.line_x_der.setVisible(True)
        self.line_x_izq.setVisible(True)
        self.line_y_izq.setVisible(True)
        self.line_y_der.setVisible(True)
        self.button_enviar_coordenadas.setVisible(True)
        self.label_instrucciones.setText("Utilice los espacios habilitados debajo de la representación gráfica para introducir \n los puntos pertenecientes a los pulmones para así poder realizar la segmentación ")

    def segmentar_pulmon(self):
        slice= self.slider_slices.value()
        semillas=[(int(self.line_x_izq.text()),int(self.line_y_izq.text()),slice),(int(self.line_x_der.text()),int(self.line_y_der.text()),slice)]
        main.segmentacion_pulmones(main.paciente_sitk,semillas)
        main.representado= main.pulmones_array
        self.label_instrucciones.setText("Elige un slice para comprobar que esté bien hecha la segmentación\n de ser así responda a la pregunta abajo a la derecha")
        self.buttons_acepta_segmentacion.setVisible(True)

    def representacion_3d_pulmones(self):
        verts,faces = fun.make_mesh(main.paciente_sitk)
        fun.plotly_3d(verts,faces)

    def aceptado(self):
        pass

    def rechazado(self):
        pass





    #Esto no va a hacer falta pero lo tengo aqui para acordarme de como se llamaba cada cosa
    def getPixel(self, event):
        x = event.pos().x()
        y = event.pos().y()
        c = self.img.pixel(x,y)
        c_rgb = QColor(c).getRgb()
        self.label.setText("Pixel: (" + str(x) +","+ str(y) + ")    Color: " + str(c_rgb))
    
    def imagen(self):
        self.img = QImage("./image.png")
        self.im = QPixmap(QPixmap.fromImage(self.img))
        #self.im = QPixmap("./image.png")
        self.label.setPixmap(self.im)
        self.label.mousePressEvent = self.getPixel
    
        

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

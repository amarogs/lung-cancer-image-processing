# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 17:44:36 2019

@author: Quique
"""

from principal_ui import *
from PyQt5.QtGui import QPixmap,QImage,QColor
import main as main
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget 

class MainWindow(QtWidgets.QMainWindow, Ui_LCDetection):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.buttons_acepta_segmentacion.setVisible(False)
        self.slider_slices.valueChanged.connect(self.valor_slider)
        self.comboBox.addItems(["Paciente 1","Paciente 2","Paciente 3","Paciente 4","Paciente 5","Paciente 6","Paciente 7","Paciente 8"])
        self.comboBox.activated.connect(self.inicio)
        self.button_slice.clicked.connect(self.dibujar_slice)


        #self.slider_slices.setValue()
        #self.label.setText("Haz clic en el botón")
        #self.pushButton.setText("Presióname")
        #self.pushButton.clicked.connect(self.imagen)
        
    def inicio(self):
        #self.label_instrucciones.setText("El paciente es: " + str(self.comboBox.currentIndex()))
        dir = main.escoge_paciente(self.comboBox.currentIndex())
        main.leer_directorio_usuario(dir)

    def valor_slider(self):
        self.label_val_slider.setText(str(self.slider_slices.value()))

    def dibujar_slice(self):
        slice = self.slider_slices.value()
        slice_paciente = main.devuelve_array(slice)
        self.mplwidget.canvas.axes.clear()
        self.mplwidget.canvas.axes.imshow(slice_paciente)
        self.mplwidget.canvas.draw()
    
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
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
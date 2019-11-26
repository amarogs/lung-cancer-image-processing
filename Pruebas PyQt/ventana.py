# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 17:44:36 2019

@author: Quique
"""

from ventana_ui import *
from PyQt5.QtGui import QPixmap,QImage,QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget 

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.label.setText("Haz clic en el botón")
        self.pushButton.setText("Presióname")
        self.pushButton.clicked.connect(self.imagen)
        
        
    def actualizar(self):
        self.label.setText("¡Acabas de hacer clic en el botón!")
    
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
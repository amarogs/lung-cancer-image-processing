# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventana_pricipal.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from lungcancer.Aplicacion.mplwidget import mplWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LCDetection(object):
    def setupUi(self, LCDetection):
        LCDetection.setObjectName("LCDetection")
        LCDetection.resize(922, 590)
        self.slider_slices = QtWidgets.QSlider(LCDetection)
        self.slider_slices.setGeometry(QtCore.QRect(530, 130, 21, 351))
        self.slider_slices.setOrientation(QtCore.Qt.Vertical)
        self.slider_slices.setObjectName("slider_slices")
        self.comboBox = QtWidgets.QComboBox(LCDetection)
        self.comboBox.setGeometry(QtCore.QRect(170, 40, 191, 22))
        self.comboBox.setObjectName("comboBox")
        self.labelpaciente = QtWidgets.QLabel(LCDetection)
        self.labelpaciente.setGeometry(QtCore.QRect(50, 40, 121, 16))
        self.labelpaciente.setObjectName("labelpaciente")
        self.widget = mplWidget(LCDetection)
        self.widget.setGeometry(QtCore.QRect(39, 129, 461, 351))
        self.widget.setObjectName("widget")
        self.label_instrucciones = QtWidgets.QLabel(LCDetection)
        self.label_instrucciones.setGeometry(QtCore.QRect(40, 75, 431, 41))
        self.label_instrucciones.setText("")
        self.label_instrucciones.setObjectName("label_instrucciones")
        self.button_slice = QtWidgets.QPushButton(LCDetection)
        self.button_slice.setGeometry(QtCore.QRect(530, 100, 21, 23))
        self.button_slice.setObjectName("button_slice")
        self.button_3d = QtWidgets.QPushButton(LCDetection)
        self.button_3d.setEnabled(False)
        self.button_3d.setGeometry(QtCore.QRect(640, 180, 191, 31))
        self.button_3d.setObjectName("button_3d")
        self.label_3d = QtWidgets.QLabel(LCDetection)
        self.label_3d.setGeometry(QtCore.QRect(600, 250, 291, 191))
        self.label_3d.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3d.setText("")
        self.label_3d.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_3d.setObjectName("label_3d")
        self.buttons_acepta_segmentacion = QtWidgets.QDialogButtonBox(
            LCDetection)
        self.buttons_acepta_segmentacion.setGeometry(
            QtCore.QRect(670, 480, 161, 31))
        self.buttons_acepta_segmentacion.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttons_acepta_segmentacion.setObjectName(
            "buttons_acepta_segmentacion")
        self.label_segmentacion = QtWidgets.QLabel(LCDetection)
        self.label_segmentacion.setGeometry(QtCore.QRect(630, 460, 251, 16))
        self.label_segmentacion.setText("")
        self.label_segmentacion.setObjectName("label_segmentacion")
        self.label_slice_seleccionado = QtWidgets.QLabel(LCDetection)
        self.label_slice_seleccionado.setGeometry(
            QtCore.QRect(200, 495, 111, 21))
        self.label_slice_seleccionado.setText("")
        self.label_slice_seleccionado.setObjectName("label_slice_seleccionado")
        self.label_max_slice = QtWidgets.QLabel(LCDetection)
        self.label_max_slice.setGeometry(QtCore.QRect(560, 130, 46, 13))
        self.label_max_slice.setText("")
        self.label_max_slice.setObjectName("label_max_slice")
        self.label_min_slice = QtWidgets.QLabel(LCDetection)
        self.label_min_slice.setGeometry(QtCore.QRect(560, 470, 46, 13))
        self.label_min_slice.setObjectName("label_min_slice")
        self.label_val_slider = QtWidgets.QLabel(LCDetection)
        self.label_val_slider.setGeometry(QtCore.QRect(510, 280, 20, 31))
        self.label_val_slider.setText("")
        self.label_val_slider.setObjectName("label_val_slider")
        self.line_x_izq = QtWidgets.QLineEdit(LCDetection)
        self.line_x_izq.setGeometry(QtCore.QRect(170, 500, 41, 20))
        self.line_x_izq.setObjectName("line_x_izq")
        self.line_y_izq = QtWidgets.QLineEdit(LCDetection)
        self.line_y_izq.setGeometry(QtCore.QRect(170, 530, 41, 20))
        self.line_y_izq.setObjectName("line_y_izq")
        self.line_y_der = QtWidgets.QLineEdit(LCDetection)
        self.line_y_der.setGeometry(QtCore.QRect(410, 530, 41, 20))
        self.line_y_der.setObjectName("line_y_der")
        self.line_x_der = QtWidgets.QLineEdit(LCDetection)
        self.line_x_der.setGeometry(QtCore.QRect(410, 500, 41, 20))
        self.line_x_der.setObjectName("line_x_der")
        self.label_pulmon_izquierdo = QtWidgets.QLabel(LCDetection)
        self.label_pulmon_izquierdo.setGeometry(QtCore.QRect(40, 490, 111, 61))
        self.label_pulmon_izquierdo.setObjectName("label_pulmon_izquierdo")
        self.label_pulmon_derecho = QtWidgets.QLabel(LCDetection)
        self.label_pulmon_derecho.setGeometry(QtCore.QRect(260, 490, 111, 61))
        self.label_pulmon_derecho.setObjectName("label_pulmon_derecho")
        self.button_enviar_coordenadas = QtWidgets.QPushButton(LCDetection)
        self.button_enviar_coordenadas.setGeometry(
            QtCore.QRect(470, 510, 75, 23))
        self.button_enviar_coordenadas.setObjectName(
            "button_enviar_coordenadas")
        self.label_resultado = QtWidgets.QLabel(LCDetection)
        self.label_resultado.setGeometry(QtCore.QRect(40, 30, 721, 71))
        self.label_resultado.setText("")
        self.label_resultado.setObjectName("label_resultado")
        self.label_resultado.setVisible(False)
        #self.button_visualizacion = QtWidgets.QPushButton(LCDetection)
        #self.button_visualizacion.setGeometry(QtCore.QRect(170, 110, 141, 23))
        #self.button_visualizacion.setObjectName("button_visualizacion")
        #self.button_visualizacion.setVisible(False)
        self.map = 0

        self.retranslateUi(LCDetection)
        QtCore.QMetaObject.connectSlotsByName(LCDetection)

    def retranslateUi(self, LCDetection):
        _translate = QtCore.QCoreApplication.translate
        LCDetection.setWindowTitle(_translate("LCDetection", "LCDetection"))
        self.labelpaciente.setText(_translate(
            "LCDetection", "Seleccione paciente"))
        self.button_slice.setText(_translate("LCDetection", "Ok"))
        self.button_3d.setText(_translate("LCDetection", "Ver en 3d"))
        self.label_min_slice.setText(_translate("LCDetection", "1"))
        self.label_pulmon_izquierdo.setText(_translate("LCDetection", "Coordenadas\n"
                                                       " X (arriba) e Y (abajo) \n"
                                                       " del pulmón izquierdo"))
        self.label_pulmon_derecho.setText(_translate("LCDetection", "Coordenadas\n"
                                                     " X (arriba) e Y (abajo) \n"
                                                     " del pulmón derecho"))
        self.button_enviar_coordenadas.setText(
            _translate("LCDetection", "Segmentar"))
        self.texto_boton = [
            0, ["Ver solo el nódulo", "ver el nódulo en su entorno"]]
        #self.button_visualizacion.setText(self.texto_boton[1][self.texto_boton[0]])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LCDetection = QtWidgets.QWidget()
    ui = Ui_LCDetection()
    ui.setupUi(LCDetection)
    LCDetection.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resultado.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(923, 590)
        self.label_resultado = QtWidgets.QLabel(Form)
        self.label_resultado.setGeometry(QtCore.QRect(40, 30, 721, 71))
        self.label_resultado.setObjectName("label_resultado")
        self.widget_mostrar_cancer = QtWidgets.QWidget(Form)
        self.widget_mostrar_cancer.setGeometry(QtCore.QRect(30, 150, 431, 351))
        self.widget_mostrar_cancer.setObjectName("widget_mostrar_cancer")
        self.button_3d_2 = QtWidgets.QPushButton(Form)
        self.button_3d_2.setEnabled(False)
        self.button_3d_2.setGeometry(QtCore.QRect(620, 160, 191, 31))
        self.button_3d_2.setObjectName("button_3d_2")
        self.label_3d_2 = QtWidgets.QLabel(Form)
        self.label_3d_2.setGeometry(QtCore.QRect(550, 210, 321, 251))
        self.label_3d_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3d_2.setText("")
        self.label_3d_2.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_3d_2.setObjectName("label_3d_2")
        self.label_min_slice_2 = QtWidgets.QLabel(Form)
        self.label_min_slice_2.setGeometry(QtCore.QRect(520, 160, 46, 13))
        self.label_min_slice_2.setObjectName("label_min_slice_2")
        self.label_max_slice_2 = QtWidgets.QLabel(Form)
        self.label_max_slice_2.setGeometry(QtCore.QRect(520, 500, 46, 13))
        self.label_max_slice_2.setText("")
        self.label_max_slice_2.setObjectName("label_max_slice_2")
        self.slider_slices = QtWidgets.QSlider(Form)
        self.slider_slices.setGeometry(QtCore.QRect(490, 160, 21, 351))
        self.slider_slices.setOrientation(QtCore.Qt.Vertical)
        self.slider_slices.setObjectName("slider_slices")
        self.button_slice_2 = QtWidgets.QPushButton(Form)
        self.button_slice_2.setGeometry(QtCore.QRect(490, 130, 21, 23))
        self.button_slice_2.setObjectName("button_slice_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(180, 525, 111, 21))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_val_slider = QtWidgets.QLabel(Form)
        self.label_val_slider.setGeometry(QtCore.QRect(470, 310, 20, 31))
        self.label_val_slider.setText("")
        self.label_val_slider.setObjectName("label_val_slider")
        self.button_visualizacion = QtWidgets.QPushButton(Form)
        self.button_visualizacion.setGeometry(QtCore.QRect(170, 110, 141, 23))
        self.button_visualizacion.setObjectName("button_visualizacion")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "LCDetection"))
        self.label_resultado.setText(_translate(
            "Form", "El paciente tiene un cáncer con las siguientes características :"))
        self.button_3d_2.setText(_translate("Form", "Ver en 3d"))
        self.label_min_slice_2.setText(_translate("Form", "1"))
        self.button_slice_2.setText(_translate("Form", "Ok"))
        self.button_visualizacion.setText(
            _translate("Form", "Ver Sólo el nódulo"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

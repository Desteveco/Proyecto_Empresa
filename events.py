import sys
import time

from PyQt6 import QtWidgets, QtCore, QtGui

import conexion
import globals
import dlgCalendar

class Events:
    @staticmethod
    def messageExit():
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setWindowIcon(QtGui.QIcon('./img/logo.jpg'))
            mbox.setWindowTitle('Exit')
            mbox.setText('Are you sure you want to exit?')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Yes')
            mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
            mbox.resize(600, 800)
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                sys.exit()
            else:
                mbox.hide()
        except Exception as e:
            print("error en la salida",e)

    @staticmethod
    def openCalendar():
        try:
            globals.vencal.show()
        except Exception as e:
            print("error en la salida",e)

    def loadProv(self):
        try:
            globals.ui.cmbProvcli_2.clear()
            list = conexion.Conexion.listProv(self)
            globals.ui.cmbProvcli_2.addItems(list)
        except Exception as e:
            print("error en la conexion",e)

    def loadData(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if globals.ui.panMain_2.currentIndex() == 0:
                globals.ui.txtAltacli_2.setText(data)
            time.sleep(0.15)
            globals.vencal.hide()

        except Exception as e:
            print("error en cargar Data", e)

    def loadMunicli(self):
        try:
            province = globals.ui.cmbProvcli_2.currentText()
            list = conexion.Conexion.listMuniProv(province)
            globals.ui.cmbMunicli_2.clear()
            globals.ui.cmbMunicli_2.addItems(list)
        except Exception as e:
            print("error en cargar Municli", e)

import sys
import time

from PyQt6 import QtWidgets, QtCore, QtGui, QtSql

from connection import *
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


    def loadProv(self=None):
        try:
            globals.ui.cb_province.clear()
            list = Connection.listProv(self)
            globals.ui.cb_province.addItems(list)
        except Exception as e:
            print("error en la conexion",e)

    def loadData(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if globals.ui.pan_main.currentIndex() == 0:
                globals.ui.le_date.setText(data)
            time.sleep(0.15)
            globals.vencal.hide()

        except Exception as e:
            print("error en cargar Data", e)

    @staticmethod
    def loadMunicli():
        try:
            province = globals.ui.cb_province.currentText()
            list = Connection.listMuniProv(province)
            globals.ui.cb_city.clear()
            globals.ui.cb_city.addItems(list)
        except Exception as e:
            print("error en cargar Municli", e)

    @staticmethod
    def resizeTabCustomers(self):
        try:
            header = globals.ui.table_customer.horizontalHeader()
            for i in range(header.count()):
                if i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.table_customer.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en cargar Customers", e)

    @staticmethod
    def messageAbout():
        try:
            globals.about.show()
        except Exception as e:
            print("error en cargar About", e)
    @staticmethod
    def closeAbout():
        try:
            globals.about.hide()
        except Exception as e:
            print("error en cargar About", e)

    def clearEntries(self=None):
        try:
            for text in [globals.ui.le_dni,
                            globals.ui.le_date,
                            globals.ui.le_surname,
                            globals.ui.le_name,
                            globals.ui.le_email,
                            globals.ui.le_phone,
                            globals.ui.le_address,
                            ]:
                text.clear()

            for combo in [globals.ui.cb_province,
                            globals.ui.cb_city]:
                combo.setCurrentIndex(-1)

            globals.ui.rbt_digitalbill.setChecked(True)
            globals.ui.chk_inactive.setChecked(False)

        except Exception as error:
            print("!!! (Events.clearEntries) Error clearing entries", error)
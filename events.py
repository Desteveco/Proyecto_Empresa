import csv
import datetime
import os
import shutil
import sys
import time
import zipfile

from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
from conexion import Conexion
import globals
import dlgCalendar
import customers


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
            print("error en la salida", e)

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

    def openCalendar(self=None):
        try:
            globals.vencal.show()
        except Exception as e:
            print("error calendar", e)

    def loadData(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if globals.ui.pan_main.currentIndex() == 0:
                globals.ui.le_date.setText(data)
            time.sleep(0.15)
            globals.vencal.hide()

        except Exception as e:
            print("error en cargar Data", e)

    def loadProv(self):
        try:
            globals.ui.cb_province.clear()
            list = Conexion.listProv(self)
            globals.ui.cb_province.addItems(list)
        except Exception as e:
            print("error en la conexion", e)

    def loadMunicli(self):
        try:
            province = globals.ui.cb_province.currentText()
            list = Conexion.listMuniProv(province)
            globals.ui.cb_city.clear()
            globals.ui.cb_city.addItems(list)
        except Exception as e:
            print("error en cargar Municli", e)

    def resizeTabProducts(self):
        try:
            header = globals.ui.table_productos.horizontalHeader()
            for i in range(header.count()):
                if i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.table_productos.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en cargar Customers", e)

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

    def resizeTabAllFact(self):

        try:
            globals.ui.table_all_fact.horizontalHeader().setVisible(True)
            header = globals.ui.table_all_fact.horizontalHeader()

            for i in range(header.count()):
                if i < 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.table_all_fact.horizontalHeaderItem(i)

                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en cargar Customers", e)

    def resizeTabSales(self):

        try:
            globals.ui.table_sales.horizontalHeader().setVisible(True)
            header = globals.ui.table_sales.horizontalHeader()

            for i in range(header.count()):
                if i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = globals.ui.table_sales.horizontalHeaderItem(i)

                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en cargar Customers", e)

    def saveBackup(self):
        try:
            data = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            fileName = data + "_backup.zip"
            directory, file = globals.dlgopen.getSaveFileName(None, "Save Backup File", fileName, "zip")

            if globals.dlgopen.accept and file:
                print("directory")
                filezip = zipfile.ZipFile(file, 'w')
                filezip.write('./data/bbdd.sqlite', os.path.basename('data/bbdd.sqlite'))
                filezip.close()
                shutil.move(file, directory)
                print("directory")
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/logo.png"))
                mbox.setWindowTitle("Save Backup")
                mbox.setText("Save Backup Done")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
        except Exception as e:
            print("error en save backup", e)

    def restoreBackup(self):
        try:
            filename = globals.dlgopen.getOpenFileName(None, "Restore Backup File", '', "*.zip;;All Files (*)")
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(path='./data', pwd=None)
                    # shutil.move('bbdd.sqlite', './data')
                bbdd.close()
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("./img/logo.jpg"))
                mbox.setWindowTitle("Restore Backup")
                mbox.setText("Restore Backup Done")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                Conexion.db_conexion(self)
                Events.loadProv(self)
                customers.Customers.loadTablecli(True)
        except Exception as e:
            print("error en restore backup", e)

    @staticmethod
    def exportXlsCustomers():
        try:
            data = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            copy = str(data) + '_customers.csv'
            directory, file = globals.dlgopen.getSaveFileName(None, "Save Backup file", copy, '.csv')
            # globals.dlgOpen.centrar()
            var = False
            if file:
                records = Conexion.listCustomers(var)
                with open(file, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['DNI_NIE', 'AddData', 'Surname', 'Name', 'eMail', 'Mobile', 'Address',
                                     'Province', 'City', 'InvoiceType', 'Active'])
                    for record in records:
                        writer.writerow(record)
                shutil.move(file, directory)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Export Customers')
                mbox.setText('Export Customers Done')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                mbox.setWindowTitle('Export Customers')
                mbox.setText('Export Customers Error')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
        except Exception as e:
            print("Error en exportar customers", e)

    def loadStatusBar(self):
        try:
            data = datetime.datetime.now().strftime('%d/%m/%y')
            self.labelstatus = QtWidgets.QLabel(self)
            self.labelstatus.setText(data)
            self.labelstatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            globals.ui.statusbar.addPermanentWidget(self.labelstatus)
            self.labelversion = QtWidgets.QLabel(self)
            self.labelversion.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.labelversion.setText("Version 0.0.1")
            self.labelversion.setObjectName("labelversion")
            globals.ui.statusbar.addPermanentWidget(self.labelversion)
        except Exception as e:
            print("error en loadStatusBar", e)

import re

from PyQt6 import QtCore
from PyQt6.QtWidgets import QTableWidget, QWidget
from PyQt6.uic.Compiler.qtproxies import QtWidgets

import globals
from connection import *

class Customers:
    @staticmethod
    def checkDni(self=None):
        try:
            dni = globals.ui.le_dni.text()
            dni = str(dni).upper()
            globals.ui.le_dni.setText(dni)
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    globals.ui.le_dni.setStyleSheet('background-color:#9EFF8C;')
                else:
                    globals.ui.le_dni.setStyleSheet('background-color:#FFC0CB;')
                    globals.ui.le_dni.setText("")
                    globals.ui.le_dni.setFocus()
            else:
                globals.ui.le_dni.setStyleSheet('background-color:#FF8C8C;')
                globals.ui.le_dni.setText("")
                globals.ui.le_dni.setFocus()
        except Exception as error:
            print("error en validar dni ", error)

    def capitalize(text, widget):
        try:
            capitalizedText = str(text).title()
            widget.setText(capitalizedText)
        except Exception as error:
            print("error en poner mayusculas ", error)


    @staticmethod
    def checkMail(self=None):
        email = globals.ui.le_email.text()
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            globals.ui.le_email.setStyleSheet('background-color: rgb(255, 255, 220); color: black')
        else:
            globals.ui.le_email.setStyleSheet('background-color:#FFC0CB; color: black')
            globals.ui.le_email.setText("")
            globals.ui.le_email.setPlaceholderText("Invalid email")
            globals.ui.le_email.setFocus()


    @staticmethod
    def checkMobile(self=None):
        number = globals.ui.le_phone.text()
        pattern = r'^[67]\d{8}$'
        if re.match(pattern, number):
            globals.ui.le_phone.setStyleSheet('background-color: rgb(255, 255, 220); color: black')
        else:
            globals.ui.le_phone.setStyleSheet('background-color:#FFC0CB; color: black')
            globals.ui.le_phone.setText("")
            globals.ui.le_phone.setPlaceholderText("Invalid phone")
            globals.ui.le_phone.setFocus()

    @staticmethod
    def loadTable(self):
        try:
            listTabCustomers = Connection.getCustomers()
            print("\n(Customers.loadTable): CUSTOMER LIST LOADED")
            index = 0
            for customer in listTabCustomers:
                globals.ui.table_customer.setRowCount(index + 1)
                globals.ui.table_customer.setItem(index, 0, QtWidgets.QTableWidgetItem(str(customer[2])))
                globals.ui.table_customer.setItem(index, 1, QtWidgets.QTableWidgetItem(str(customer[3])))
                globals.ui.table_customer.setItem(index, 2, QtWidgets.QTableWidgetItem(str(customer[5])))
                globals.ui.table_customer.setItem(index, 3, QtWidgets.QTableWidgetItem(str(customer[7])))
                globals.ui.table_customer.setItem(index, 4, QtWidgets.QTableWidgetItem(str(customer[8])))
                globals.ui.table_customer.setItem(index, 5, QtWidgets.QTableWidgetItem(str(customer[9])))
                state = "Alta" if str(customer[6]).lower() in ["true", "1"] else "Baja"
                globals.ui.table_customer.setItem(index, 6, QtWidgets.QTableWidgetItem(state))

                for col in range(7):  # columnas 0–6
                    align = QtCore.Qt.AlignmentFlag.AlignCenter
                    if col in [0, 1]:  # por ejemplo, alinear izq. las columnas de texto
                        align = QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
                    globals.ui.table_customer.item(index, col).setTextAlignment(align)
                index += 1
        except Exception as error:
            print("error en loadTablecli ", error)

    @staticmethod
    def selectCustomer():
        try:
            row_selected = globals.ui.table_customer.selectedItems()
            mobile_customer_selected = row_selected[2].text()
            customer_data = Connection.dataOneCustomer(str(mobile_customer_selected), "mobile")

            Customers.loadData(customer_data)

        except Exception as error:
            print("(Customers.selectCustomer) Error while selecting a customer ", error)


    @staticmethod
    def deleteCustomer(self=None):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("WARNING!")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete customer?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if mbox.exec():
                dnicif = globals.ui.le_dni.text()
                Connection.deleteCustomer(dnicif)
                print("dnicif: ", dnicif)
                Customers.loadTable(self)
                mboxaux = QtWidgets.QMessageBox()
                mboxaux.setWindowTitle("Información")
                mboxaux.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mboxaux.setText("Deleting customer" + str(dnicif))
                mboxaux.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText(
                    "An error has ocurred during the delete execution. Contact the administrator or try again.")
                mbox.exec()
        except Exception as error:
            print("!!(Customers.deleteCustomer) Error while deleting customer", error)


    def saveCustomer(self):
        try:
            if Connection.addCustomer(Customers.parseData()):
                Customers.loadTable(self)

        except Exception as error:
            print("!!(Customers.saveCustomer) Error saving customers", error)

    @staticmethod
    def modifyCustomer(self=None):
        try:
            if Connection.alterCustomer(Customers.parseData()):
                Customers.loadTable(self)

        except Exception as error:
            print("!!(Customers.modifyCustomer) Error while modifying customer", error)

    @staticmethod
    def searchCustomer():
        try:
            search_id = globals.ui.le_dni.text()
            customerData = Connection.dataOneCustomer(str(search_id), "ID")

            if len(customerData) > 0:
                Customers.loadData(customerData)
                print("(Customers.searchCustomer) FOUND CUSTOMER: ", customerData)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("No customer by that ID has been found.")
                mbox.exec()

        except Exception as error:
            print("!!(Customer.searchCustomer) Error while searching a customer ", error)


    @staticmethod
    def loadData(all_customer_data):
        all_data_boxes = [globals.ui.le_dni,
                            globals.ui.le_date,
                            globals.ui.le_surname,
                            globals.ui.le_name,
                            globals.ui.le_email,
                            globals.ui.le_phone,
                            globals.ui.le_address]
        for i in range(len(all_data_boxes)):
            all_data_boxes[i].setText(str(all_customer_data[i]))

        globals.ui.cb_province.setCurrentText(str(all_customer_data[7]))
        globals.ui.cb_city.setCurrentText(str(all_customer_data[8]))

        if str(all_customer_data[9]) == "paper":
            globals.ui.rb_paper.setChecked(True)
        else:
            globals.ui.rb_electronic.setChecked(True)

    @staticmethod
    def parseData():
        try:
            customerInfo = [globals.ui.le_dni.text(),
                            globals.ui.le_date.text(),
                            globals.ui.le_surname.text(),
                            globals.ui.le_name.text(),
                            globals.ui.le_email.text(),
                            globals.ui.le_phone.text(),
                            globals.ui.le_address.text(),
                            globals.ui.cb_province.currentText(),
                            globals.ui.cb_city.currentText()]

            if globals.ui.rb_paper.isChecked():
                customerInfo.append("paper")
            else:
                customerInfo.append("electronic")

            if globals.ui.chk_inactive.isChecked():
                customerInfo.append(str(True))
            else:
                customerInfo.append(str(False))

            return customerInfo
        except Exception as error:
            print("!!(Customers.parseData) Error while parsing data", error)

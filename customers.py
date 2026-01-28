import re

from PyQt6.QtSql import *

from events import *


class Customers:
    @staticmethod
    def checkDni(self=None):
        """
        Modulo para calcular la letra del dni correcta
        :param self: None
        :type self: None
        """
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
                    globals.ui.le_dni.setText(None)
                    globals.ui.le_dni.setFocus()
            else:
                globals.ui.le_dni.setStyleSheet('background-color:#FF8C8C;')
                globals.ui.le_dni.setText(None)
                globals.ui.le_dni.setFocus()
        except Exception as error:
            print("error en validar dni ", error)

    def capitalizar(texto,widget):
        """
        Modulo para capitalizar la letra de los inputs
        :param widget: texto y widget
        :type widget: basestring y widget input
        """
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("error en poner mayusculas ", error)


    @staticmethod
    def checkMail(self=None):
        """
               Módulo para validar el correo electrónico usando una expresión regular.
               Cambia el color del campo según sea válido o no.
               :param self: No usado
               :type self: None
               """
        email = globals.ui.le_email.text()
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            globals.ui.le_email.setStyleSheet('background-color: rgb(255, 255, 220); color: black')
        else:
            globals.ui.le_email.setStyleSheet('background-color:#FFC0CB; color: black')
            globals.ui.le_email.setText(None)
            globals.ui.le_email.setPlaceholderText("Invalid email")
            globals.ui.le_email.setFocus()


    @staticmethod
    def checkMobile(self=None):
        """
               Módulo para validar un número de teléfono móvil español.
               Solo acepta números que empiecen por 6 o 7 y tengan 9 cifras.
               :param self: No usado
               :type self: None
               """
        number = globals.ui.le_phone.text()
        pattern = r'^[67]\d{8}$'
        if re.match(pattern, number):
            globals.ui.le_phone.setStyleSheet('background-color: rgb(255, 255, 220); color: black')
        else:
            globals.ui.le_phone.setStyleSheet('background-color:#FFC0CB; color: black')
            globals.ui.le_phone.setText(None)
            globals.ui.le_phone.setPlaceholderText("Invalid phone")
            globals.ui.le_phone.setFocus()

    def cleanCli(self):
        """
                Limpia todos los campos del formulario de cliente,
                restablece estilos, recarga provincias y deja el estado por defecto.
                :param self: Instancia del objeto
                :type self: Customers
                """
        try:
            formcli = [globals.ui.le_dni,
                     globals.ui.le_date,
                     globals.ui.le_surname,
                     globals.ui.le_name,
                     globals.ui.le_email,
                     globals.ui.le_phone,
                     globals.ui.le_address]

            for i,dato in enumerate(formcli):
                formcli[i] = dato.setText("")
            Events.loadProv(self)
            globals.ui.cb_province.clear()
            globals.ui.rb_electronic.setChecked(True)
            globals.ui.le_dni.setEnabled(True)
            globals.ui.le_dni.setStyleSheet('background-color: rgb(255, 255, 255);')
            globals.ui.le_email.setStyleSheet('background-color: rgb(255, 255, 255);')
            globals.ui.le_phone.setStyleSheet('background-color: rgb(255, 255, 255);')
            globals.ui.le_email.setPlaceholderText("")
            globals.ui.le_phone.setPlaceholderText("")
            globals.ui.lblWarning.setStyleSheet('background-color: rgb(220, 245, 229);')

        except Exception as error:
            print("error in clean ", error)



    @staticmethod
    def loadTablecli(varCli):
        globals.ui.table_customer.setSortingEnabled(False)
        try:
            listTabCustomers = Conexion.listCustomers(varCli)

            index = 0
            for record in listTabCustomers:
                globals.ui.table_customer.setRowCount(index + 1)
                globals.ui.table_customer.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.table_customer.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.table_customer.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[5])))
                globals.ui.table_customer.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[7])))
                globals.ui.table_customer.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[8])))
                globals.ui.table_customer.setItem(index, 5, QtWidgets.QTableWidgetItem(str(record[9])))
                if str(record[10])== "True":
                    globals.ui.table_customer.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Alta")))
                else:
                    globals.ui.table_customer.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Baja")))
                globals.ui.table_customer.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.table_customer.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.table_customer.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.table_customer.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.table_customer.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.table_customer.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)

                index += 1
            globals.ui.table_customer.setSortingEnabled(True)
        except Exception as error:
            print("error en loadTablecli ", error)

    @staticmethod
    def Historicocli(self):
        try:
            if globals.ui.chkb_hystorical.isChecked():
                varcli = False
            else:
                varcli = True
            Customers.loadTablecli(varcli)
        except Exception as error:
            print("error en historicocli ", error)

    @staticmethod
    def selectCustomer():

        try:
            row = globals.ui.table_customer.selectedItems()
            data = [dato.text() for dato in row]
            record = Conexion.dataOneCustomer(data[2])
            boxes = [globals.ui.le_dni,
                     globals.ui.le_date,
                     globals.ui.le_surname,
                     globals.ui.le_name,
                     globals.ui.le_email,
                     globals.ui.le_phone,
                     globals.ui.le_address]

            for i in range(len(boxes)):
                boxes[i].setText(str(record[i]))
            globals.ui.cb_province.setCurrentText(str(record[7]))
            globals.ui.cb_city.setCurrentText(str(record[8]))
            if str(record[9]) == "paper":
                globals.ui.rb_paper.setChecked(True)
            else:
                globals.ui.rb_electronic.setChecked(True)
                globals.estado = str(record[10])
        except Exception as error:
            print("error en selectCustomer ", error)

    def delCliente(self):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("WARNING")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Client?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:

                dni = globals.ui.le_dni.text()
                if Conexion.deleteCli(dni):

                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Delete Client?")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No )
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

                else:
                    print("Something went wrong")
                Customers.loadTablecli(self)
                globals.ui.chkb_hystorical.setChecked(True)
            else:
                pass

        except Exception as error:
            print("error en deleting customer ", error)


    @staticmethod
    def Historicocli():
        try:
            if globals.ui.chkb_hystorical.isChecked():
                varCli = False
                Customers.loadTablecli(varCli)
            else:
                varCli = True
            Customers.loadTablecli(varCli)

        except Exception as error:
            print("error historicocli ", error)


    def saveCli(self):
        try:
            newcli = [globals.ui.le_dni.text(),
              globals.ui.le_date.text(),
              globals.ui.le_surname.text(),
              globals.ui.le_name.text(),
              globals.ui.le_email.text(),
              globals.ui.le_phone.text(),
              globals.ui.le_address.text(),
              globals.ui.cb_province.currentText(),
              globals.ui.cb_city.currentText(),]

            if globals.ui.rb_paper.isChecked():
                fact = "paper"
            elif globals.ui.rb_electronic.isChecked():
                fact = "electronic"
            newcli.append(fact)
            if Conexion.addCli(newcli) and len(newcli) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                if mbox.exec():
                    mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Warning, no Client added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                if mbox.exec():
                    mbox.hide()
                varcli = True
                Customers.loadTablecli(varcli)
        except Exception as error:
            print("Error  saving customer ", error)

    def modifCli(self):
        try:
            varcli = "True"

            if globals.estado == str("False"):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client non activated. DO you want activated?")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                reply = mbox.exec()
                if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                    globals.estado = str("True")

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Modify")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setText("Modify Client?")
            mbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                dni = globals.ui.le_dni.text()
                modifcli = [globals.ui.le_date.text(), globals.ui.le_surname.text(),
                            globals.ui.le_name.text(), globals.ui.le_email.text(), globals.ui.le_phone.text(),
                            globals.ui.le_address.text(), globals.ui.cb_province.currentText(),
                            globals.ui.cb_city.currentText(), globals.estado]
                if globals.ui.rb_paper.isChecked():
                    fact = "paper"
                elif globals.ui.rb_electronic.isChecked():
                    fact = "electronic"
                modifcli.append(fact)
                if Conexion.modifCli(dni, modifcli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Client modified")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec():
                        mbox.hide()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Warning")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("Warning, no Client modified")
                    if mbox.exec():
                        mbox.hide()




            else:
                mbox.hide()

            Customers.loadTablecli(varcli)
            globals.ui.chkb_hystorical.setChecked(False)
        except Exception as error:
            print("error en modifing customer ", error)

    @staticmethod
    def buscaCli():
        try:
            record=[]
            dni = globals.ui.le_dni.text()
            if record == Conexion.dataOneCustomer(str(dni)):
                if not record:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Client not found")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec():
                        mbox.hide()
                else:
                    box = [globals.ui.le_dni,
                     globals.ui.le_date,
                     globals.ui.le_surname,
                     globals.ui.le_name,
                     globals.ui.le_email,
                     globals.ui.le_phone,
                     globals.ui.le_address]

            for i in range(len(box)):
                box[i].setText(str(record[i]))
            globals.ui.cb_province.setCurrentText(str(record[7]))
            globals.ui.cb_city.setCurrentText(str(record[8]))
            if str(record[9]) == "paper":
                globals.ui.rb_paper.setChecked(True)
            else:
                globals.ui.rb_electronic.setChecked(True)
        except Exception as error:
            print("error en selectCustomer ", error)



    @staticmethod
    def searchCli():
        try:
            record = []
            dni = globals.ui.le_dni.text()
            record = Conexion.dataOneCustomer(str(dni))
            if not record:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client does not exists")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide()
            else:
                box = [globals.ui.le_dni, globals.ui.le_date, globals.ui.le_surname, globals.ui.le_name,
                       globals.ui.le_email, globals.ui.le_phone, globals.ui.le_address]
                for i in range(len(box)):
                    box[i].setText(record[i])

                globals.ui.cb_province.setCurrentText(str(record[7]))
                globals.ui.cb_city.setCurrentText(str(record[8]))
                if str(record[9]) == 'paper':
                    globals.ui.rb_paper.setChecked(True)
                else:
                    globals.ui.rb_electronic.setChecked(True)
                if str(record[10]) == 'False':

                    globals.ui.lblWarning.setText("Hystorical Client")
                    globals.ui.lblWarning.setStyleSheet("background-color:rgb(255,255,200); color:red;")


        except Exception as e:

            print(f"Error in searching customer: {e}")

    @staticmethod
    def cleanCli():
        try:
            formcli=[globals.ui.le_dni,
                     globals.ui.le_date,
                     globals.ui.le_surname,
                     globals.ui.le_name,
                     globals.ui.le_email,
                     globals.ui.le_phone,
                     globals.ui.le_address]

            for i, dato in enumerate(formcli):
                formcli[i] = dato.setText("")
            Events.loadProv(self)
            globals.ui.le_dni.setEnabled(True)
            globals.ui.cb_province.clear()
            globals.ui.rb_paper.setChecked(True)
        except Exception as error:
            print("error en buscaCli ", error)


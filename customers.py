
import re
from conexion import *
import globals

class Customers:
    @staticmethod
    def checkDni(self=None):
        try:
            dni = globals.ui.txtDnicli_2.text()
            dni = str(dni).upper()
            globals.ui.txtDnicli_2.setText(dni)
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
                    globals.ui.txtDnicli_2.setStyleSheet('background-color:#9EFF8C;')
                else:
                    globals.ui.txtDnicli_2.setStyleSheet('background-color:#FFC0CB;')
                    globals.ui.txtDnicli_2.setText(None)
                    globals.ui.txtDnicli_2.setFocus()
            else:
                globals.ui.txtDnicli_2.setStyleSheet('background-color:#FF8C8C;')
                globals.ui.txtDnicli_2.setText(None)
                globals.ui.txtDnicli_2.setFocus()
        except Exception as error:
            print("error en validar dni ", error)

    def capitalizar(texto,widget):
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("error en poner mayusculas ", error)


    @staticmethod
    def checkMail(self=None):
        email = globals.ui.txtEmailcli_2.text()
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            globals.ui.txtEmailcli_2.setStyleSheet('background-color: rgb(255, 255, 220); color: black')
        else:
            globals.ui.txtEmailcli_2.setStyleSheet('background-color:#FFC0CB; color: black')
            globals.ui.txtEmailcli_2.setText(None)
            globals.ui.txtEmailcli_2.setPlaceholderText("Invalid email")
            globals.ui.txtEmailcli_2.setFocus()


    @staticmethod
    def checkMobile(self=None):
        number = globals.ui.lblNomecli_6.text()
        pattern = r'^[67]\d{8}$'
        if re.match(pattern, number):
            globals.ui.lblNomecli_6.setStyleSheet('background-color: rgb(255, 255, 220); color: black')
        else:
            globals.ui.lblNomecli_6.setStyleSheet('background-color:#FFC0CB; color: black')
            globals.ui.lblNomecli_6.setText(None)
            globals.ui.lblNomecli_6.setPlaceholderText("Invalid phone")
            globals.ui.lblNomecli_6.setFocus()

    @staticmethod
    def loadTablecli(self=None):
        try:
            listTabCustomers = Conexion.listCustomers()
            print(listTabCustomers)
        except Exception as error:
            print("error en loadTablecli ", error)

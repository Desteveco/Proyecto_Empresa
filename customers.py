import globals

class Customers:
    @staticmethod
    def checkDni(self=None):
        try:
            dni = globals.ui.txtDnicli_2.text()
            dni = str(dni).upper()
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
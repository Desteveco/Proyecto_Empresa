from PyQt6.QtWidgets import QTableWidget, QWidget

import events
import globals
import styles
from venAux import *
from customers import *
from events import *
from window import *
from connection import *
from styles import *
import sys

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)
        self.setStyleSheet(styles.load_stylesheet())

        #Instancias
        globals.vencal = Calendar()
        globals.about = About()

        #Conexión base de datos
        Connection.db_conexion()
        Customers.loadTable(self)
        Events.resizeTabCustomers(self)

        # Menú
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.dlg_about.triggered.connect(Events.messageAbout)

        # Funciones de cuestionario
        globals.ui.le_dni.editingFinished.connect(Customers.checkDni)
        globals.ui.le_surname.editingFinished.connect(
            lambda: Customers.capitalize(globals.ui.le_surname.text(), globals.ui.le_surname))
        globals.ui.le_name.editingFinished.connect(
            lambda: Customers.capitalize(globals.ui.le_name.text(), globals.ui.le_name))
        globals.ui.le_email.editingFinished.connect(Customers.checkMail)
        globals.ui.le_phone.editingFinished.connect(Customers.checkMobile)

        # Funciones de tabla
        globals.ui.table_customer.clicked.connect(Customers.selectCustomer)

        # Botones
        globals.ui.btn_calendar.clicked.connect(Events.openCalendar)
        globals.ui.btn_clean.clicked.connect(Events.clearEntries)
        globals.ui.btn_save_cust.clicked.connect(Customers.saveCustomer)
        globals.ui.btn_del_cust.clicked.connect(Customers.deleteCustomer)
        globals.ui.btn_modify_cust.clicked.connect(Customers.modifyCustomer)

        # Funciones de combobox
        globals.ui.cb_province.currentIndexChanged.connect(Events.loadMunicli)
        Events.loadProv(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.setWindowIcon(QtGui.QIcon("./img/logo.jpg"))
    window.showMaximized()
    sys.exit(app.exec())

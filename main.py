import sys

import customers
import globals
import events
from dlgCalendar import Ui_dlgCalendar
from window import *
from events import *
from customers import *
from venAux import *
from conexion import *




class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)
        globals.vencal = Calendar()

        Conexion.db_conexion(self)
        Customers.loadTablecli()
#tableCustomerlist_2
        Events.loadProv(self)
        globals.ui.cmbProvcli_2.currentIndexChanged.connect(events.Events.loadMunicli)
        #FUNCIONES EN EL MENU BAR
        globals.ui.actionExit.triggered.connect(Events.messageExit)

        #FUNCIONES EN LINEEDIT
        globals.ui.txtDnicli_2.editingFinished.connect(Customers.checkDni)

        #FUNCIONES OF BUTTONS
        globals.ui.btnFechaltacli_2.clicked.connect(Events.openCalendar)
        globals.ui.txtApelcli_2.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtApelcli_2.text(), globals.ui.txtApelcli_2))
        globals.ui.lblNomecli_5.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.lblNomecli_5.text(), globals.ui.lblNomecli_5))
        globals.ui.txtEmailcli_2.editingFinished.connect(lambda: Customers.checkMail(globals.ui.txtEmailcli_2.text()))
        globals.ui.lblNomecli_6.editingFinished.connect(lambda: Customers.checkMobile(globals.ui.lblNomecli_6.text()))



if __name__ == '__main__':
     app = QtWidgets.QApplication(sys.argv)
     window = Main()
     window.showMaximized()
     sys.exit(app.exec())

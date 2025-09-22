import sys

import events
from window import *
from events import *
import globals
from customers import *
from venCalendar import Ui_venCalendar




class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        #FUNCIONES EN EL MENU BAR
        globals.ui.actionExit.triggered.connect(Events.messageExit)

        #FUNCIONES EN LINEEDIT
        globals.ui.txtDnicli_2.editingFinished.connect(Customers.checkDni)

        #FUNCIONES OF BUTTONS
        globals.ui.btnFechaltacli_2.clicked.connect(events.Events.openCalendar)

        #prueba
        globals.venCalendar = QtWidgets.QMainWindow()
        self.uiCalendar = Ui_venCalendar()
        self.uiCalendar.setupUi(globals.venCalendar)


if __name__ == '__main__':
     app = QtWidgets.QApplication(sys.argv)
     window = Main()
     window.showMaximized()
     sys.exit(app.exec())

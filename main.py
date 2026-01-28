
from customers import *
from invoice import Invoice
from products import Products
from report import Report
from venAux import *
from window import *
from events import *
import styles

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        #Instances
        globals.vencal = Calendar()
        globals.about = About()
        globals.dlgopen = FileDialogOpen()
        self.report = Report()
        self.invoice = Invoice()

        #Estilos
        self.setStyleSheet(styles.load_stylesheet())

        # Conexión base de datos

        varcli = True
        Conexion.db_conexion(self)
        Customers.loadTablecli(varcli)
        Products.loadTableProduct()
        Invoice.loadTablefact()

        Events.resizeTabProducts(self)
        Events.resizeTabCustomers(self)
        Events.resizeTabSales(self)
        Products.cargaFamilypro(self)
        Events.resizeTabAllFact(self)




        # Menú
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.dlg_about.triggered.connect(Events.messageAbout)
        ##globals.ui.actionSave_Data.triggered.connect(Events.saveBackup)
        globals.ui.actionImport_Data.triggered.connect(Events.restoreBackup)
        globals.ui.actionExport_Data.triggered.connect(Events.exportXlsCustomers)
        globals.ui.actionCustomerReport.triggered.connect(self.report.reportCustomers)



        # Validaciones
        globals.ui.le_dni.editingFinished.connect(Customers.checkDni)
        globals.ui.le_surname.editingFinished.connect(
            lambda: Customers.capitalizar(globals.ui.le_surname.text(), globals.ui.le_surname))
        globals.ui.le_name.editingFinished.connect(
            lambda: Customers.capitalizar(globals.ui.le_name.text(), globals.ui.le_name))
        globals.ui.le_email.editingFinished.connect(Customers.checkMail)
        globals.ui.le_phone.editingFinished.connect(Customers.checkMobile)

        # Carga municipios al cambiar provincia
        Events.loadProv(self)
        globals.ui.cb_province.currentIndexChanged.connect(Events.loadMunicli)

        globals.ui.chkb_hystorical.stateChanged.connect(Customers.Historicocli)

        # Botones
        globals.ui.table_productos.clicked.connect(Products.selectProduct)
        globals.ui.btn_save_product.clicked.connect(Products.newProduct)
        globals.ui.btn_modify_product.clicked.connect(Products.modifyPro)
        globals.ui.btn_del_product.clicked.connect(Products.delProducto)
        globals.ui.btn_clear_product.clicked.connect(Products.cleanProd)
        globals.ui.table_customer.clicked.connect(Customers.selectCustomer)
        globals.ui.btn_calendar.clicked.connect(Events.openCalendar)
        globals.ui.btn_save_cust.clicked.connect(Customers.saveCli)
        globals.ui.btn_del_cust.clicked.connect(Customers.delCliente)
        globals.ui.btn_modify_cust.clicked.connect(Customers.modifCli)
        globals.ui.btn_clear.clicked.connect(Customers.cleanCli)
        globals.ui.btn_search.clicked.connect(Customers.searchCli)
        globals.ui.lb_dni_cliente.editingFinished.connect(Invoice.setInvoice)
        globals.ui.btn_clean_fact.clicked.connect(Invoice.cleanInvoice)
        globals.ui.btn_save_fact.clicked.connect(Invoice.saveInvoice)
        globals.ui.table_all_fact.clicked.connect(Invoice.selectInvoice)
        globals.ui.lb_dni_cliente.editingFinished.connect(lambda : Invoice.setInvoice(globals.ui.lb_dni_cliente))
        globals.ui.table_sales.itemChanged.connect(self.invoice.cellChangedSales)
        globals.ui.lb_dni_cliente.setText("00000000T")
        Events.loadStatusBar(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
